class FakeQuery():
  """Fake of google.cloud.datastore.Query."""

  def __init__(self, kind):
    self.kind = kind
    self.results = []

  def add_filter(self, property_name, operator, value):
    self.property_name = property_name
    self.operator = operator
    self.value = value

  def fetch(self,
            limit=None,
            offset=0,
            start_cursor=None,
            end_cursor=None,
            client=None,
            eventual=False):
    self.limit = limit
    return self.results


class FakeKey():
  """Fake of google.cloud.datastore.Key."""

  def __init__(self, entity_name):
    self.id = 1
    self.entity_name = entity_name

  def _flat_path(self):
    return "FakeFlatPath"


class FakeTransaction():
  """Fake of google.cloud.datastore.Transaction."""

  def __enter__(self):
    pass

  def __exit__(self, type, value, traceback):
    pass


class FakeDataStoreClient():
  """Fake of google.cloud.datastore.Client."""

  def __init__(self):
    self._start_failing = False
    self.query_results = []
    self.get_result = None

  def key(self, *path_args, **kwargs):
    return FakeKey(path_args)

  def put(self, entity):
    if self._start_failing:
      raise ValueError('Value error')

    self.entity = entity

  def transaction(self):
    return FakeTransaction()

  def query(self, kind):
    self.query = FakeQuery(kind)
    self.query.results = self.query_results
    return self.query

  def get(self, key):
    return self.get_result

  def start_failing(self):
    self._start_failing = True
