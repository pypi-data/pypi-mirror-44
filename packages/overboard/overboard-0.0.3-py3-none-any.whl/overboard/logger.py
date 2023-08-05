
import os, math, datetime, json, inspect, shutil

try:
  from torch import save
except ImportError:
  # fallback to regular pickle if pytorch not installed
  import pickle
  def save(obj, path):
    with open(path, 'wb') as file:
      pickle.dump(obj, file, pickle.HIGHEST_PROTOCOL)


class Logger:
  def __init__(self, directory, stat_names, meta=None, index_name="iteration", save_timestamp=True):
    """Initialize log writer on a new directory, with the given list of statistics names.
       The main file that is written is "stats.csv", containing one column for each stat."""
    assert(all(isinstance(name, str) and not ',' in name for name in stat_names))
    self.file = None
    self.directory = directory
    self.stat_names = stat_names
    self.index_name = index_name
    self.count = 0

    # for averaging stats before appending to the log
    self.avg_accum = {}
    self.avg_count = {}

    # meta should be a dict or a Namespace object from argparse
    if meta is None:
      meta = {}  # ensure it's a new instance (default arguments all refer to the same instance)
    elif meta.__class__.__name__ == 'Namespace':  # check type without importing argparse
      meta = vars(meta)
    elif not isinstance(meta, dict):
      raise AssertionError("Meta should be a dictionary or argparse.Namespace.")
    meta['_done'] = False
    meta['vis'] = []
    self.meta = meta
    self.save_timestamp = save_timestamp
    self.vis_functions = {}

  def __enter__(self):
    # create directory if it doesn't exist
    os.makedirs(self.directory, exist_ok=True)

    # get current timestamp as string, including timezone offset
    if self.save_timestamp:
      self.meta['timestamp'] = str(datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0))
    
    # write arguments to JSON file
    self.save_meta()

    # open CSV file and write header
    self.file = open(self.directory + '/stats.csv', 'w')
    self.file.write(self.index_name + ',' + ','.join(self.stat_names) + '\n')  # header
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    # close CSV file
    self.file.close()
    self.file = None

    # mark experiment as done, and write to JSON file
    self.meta['_done'] = True
    self.save_meta()
  
  def save_meta(self):
    # write metadata to JSON file
    with open(self.directory + '/meta.json', 'w') as file:
      json.dump(self.meta, file)
  
  def append(self, points=None):
    """Write the given stats dict to CSV file. If none is given, the average values computed so far are used (see update_average)."""
    if self.file is None:
      raise AssertionError('Can only call logger.append() from within a "with Logger(...) as logger:" enclosure.')

    if points is None:
      # use computed average, and reset accumulator
      points = self.average()
      self.avg_accum = {}
      self.avg_count = {}

    for name in points.keys():
      assert name in self.stat_names, 'Unknown stat name: ' + name

    # first element is always the iteration
    self.count += 1
    self.file.write(str(self.count))

    # write remaining stat values
    for name in self.stat_names:
      self.file.write(',')
      if name in points:
        self.file.write(str(points[name]))
      else:
        self.file.write('NaN')
    self.file.write('\n')
    self.file.flush()
  
  def update_average(self, points):
    """Keep track of average value for each stat, adding a new data point."""
    for (name, value) in points.items():
      if name not in self.avg_accum:  # initialize
        self.avg_accum[name] = value
        self.avg_count[name] = 1
      else:
        self.avg_accum[name] += value
        self.avg_count[name] += 1
  
  def average(self):
    """Return the average value of each stat so far (see update_average)."""
    return {name: self.avg_accum[name] / self.avg_count[name] for name in self.avg_accum.keys()}

  def print(self, points=None, prefix=None, as_string=False, line_prefix='', line_suffix=''):
    """Print the current stats averages to the console, or the given values, nicely formatted.
    If prefix is given, only stat names beginning with it will be printed (e.g. "train" or "val")."""
    if points is None:
      points = self.average()
    if prefix:  # remove the prefix from the stat names
      points = {key[len(prefix):].strip('.'): val for (key, val) in points.items() if key.startswith(prefix)}
      line_prefix = line_prefix + prefix + ' '

    # this trick prints floats with 3 significant digits and no sci notation (e.g. 1e-4)
    text = ' '.join(["%s: %s" % (key, float('%.3g' % val)) for (key, val) in points.items()])
    text = line_prefix + text + line_suffix

    if as_string:
      return text
    else:
      print(text)
  
  def vis(self, name, func, *args, **kwargs):
    """Store a visualization function call, with a unique name.
    OverBoard will call the given function with the name as argument, plus the given arguments and keyword arguments.
    It should return a list of matplotlib.Figure objects, which will be shown as extra plots."""

    if name in self.vis_functions:
      # reuse previously registered visualization function
      info = self.vis_functions[name]
      if info['func'] != func:
        raise ValueError("Attempting to register a different visualization function under a previously used name.")
      source_file = info['source']
    else:
      # new function. copy function source file to freeze changes in visualization code
      source_file = inspect.getsourcefile(func)  # python source for function
      if not source_file or func.__name__ == '<lambda>':
        raise ValueError("Only visualization functions defined at the top-level of a script are supported.")
      shutil.copy(source_file, self.directory + '/' + name + '.py')

      # register visualization function for quick look-up
      self.vis_functions[name] = {'func': func, 'source': source_file}

      # register also in the metadata (JSON file)
      self.meta['vis'].append(name)
      self.save_meta()

    # pickle the function and arguments
    data = {'func': func.__name__, 'source': source_file, 'args': args, 'kwargs': kwargs}
    save(data, self.directory + '/' + name + '.pth')
