from os import path
from typing import List

class Asset():
  def __init__(self, path: str, storage_name: str, content_type: str) -> None:
    self.path: str = path
    self.storage_name: str = storage_name
    self.content_type: str = content_type

class TemplateAssets(list):

  def __init__(self, name: str) -> None:
    self.name: str = name

  #   self.contents.append(
  #     Asset(path=zip_path, storage_name='template.latex.zip', content_type='application/zip')
  #     )
  #   self.contents.append(
  #     Asset(path=options_path, storage_name='options.json', content_type='application/json')
  #     )

  # def append(path: str, storage_name: str,  content_type:str):
  #   self.
