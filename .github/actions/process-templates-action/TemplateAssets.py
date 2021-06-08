from os import path
from typing import List

class Asset():
  path: str
  storage_name: str
  content_type: str

  def __init__(self, path: str, storage_name: str, content_type: str) -> None:
    self.path = path
    self.storage_name = storage_name
    self.content_type = content_type

class TemplateAssets():
  name: str
  contents: List[Asset]

  def __init__(self, name: str, zip_path: str, options_path: str) -> None:
    self.name = name
    self.contents = []
    self.contents.append(
      Asset(path=zip_path, storage_name='template.latex.zip', content_type='application/zip')
      )
    self.contents.append(
      Asset(path=options_path, storage_name='options.json', content_type='application/json')
      )
