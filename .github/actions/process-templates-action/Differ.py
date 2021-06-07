import subprocess
import logging
import io
import pathlib


class FileStatus():
  def __init__(self, status: str, name: str):
    self.status = status
    self.name = name

  @property
  def to_remove(self):
    return self.status == "D"

  @property
  def to_process(self):
    return self.status != "" and self.status != "D"

class Differ():

  def __init__(self):
    self.files: FileStatus = []
    self.folders = {}

  def run(self, from_commit:str = "HEAD~1"):
    """
      Run `git diff` between the current HEAD and the from_commit specified
      Will then parse the output from the command to build a list of file changes
      and a dict of changed root template folder names

      `subprocess.check_output` will raise a `CalledProcessError` on error and the
      caller should handle
    """
    CMD=rf"git diff {from_commit} HEAD --name-status"
    output = subprocess.check_output(CMD, shell=True, encoding="utf-8")
    self.parse_output(output)
    self.reduce_to_folders()


  def parse_output(self, output):
    """
      Parse the raw output returned by
    """
    self.files = []
    for item in output.split('\n'):
      if len(item) > 0:
        status, name = item.split()
        self.files.append(FileStatus(status, name))

  def reduce_to_folders(self):
    """
      Scan the file status list and convert this to a list of new FileStatus objects
      that point only to the first level directory of the original FileStatus objects
      without duplication. So that mulitple file chjanges in a single folder get reduced
      to a single entry.

      Also carry accross the appropraite status code for the folder.
    """
    self.folders = {}
    for file in self.files:
      p = pathlib.Path(file.name)
      if len(p.parts) == 0:
        continue
      folder = p.parts[0]

      # if we have already seen a change in this folder skip
      if folder in self.folders:
        # but first log any non delete status we see
        # doesn't matter which one
        if file.status != "D":
          self.folders[folder] = file.status
        continue

      # first time we've seen this path, add the folder and add to seen
      self.folders[folder] = file.status

