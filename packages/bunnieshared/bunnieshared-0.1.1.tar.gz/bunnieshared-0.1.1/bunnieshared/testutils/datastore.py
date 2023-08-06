class FakeKey():
  """Fake of google.cloud.datastore.Key."""

  def _flat_path(self):
    return "FakeFlatPath"


class FakeDataStoreClient():
  """Fake of google.cloud.datastore.Client."""

  def __init__(self):
    self._start_failing = False

  def key(self, *path_args, **kwargs):
    return FakeKey()

  def put(self, entity):
    if self._start_failing:
      raise ValueError('Value error')

    self.entity = entity

  def start_failing(self):
    self._start_failing = True
