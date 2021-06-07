import pytest
from Differ import Differ, FileStatus


@pytest.mark.parametrize("status,name,rm,proc", [
  ["D", "deleted.py", True, False],
  ["A", "added.py", False, True],
  ["C", "changed.py", False, True],
  ["", "", False, False],
])
def test_file_status(status, name, rm, proc):
  fs = FileStatus(status, name);
  assert fs.to_remove == rm
  assert fs.to_process == proc


@pytest.mark.parametrize("output, num_changes", [
  ("", 0),
  ("D deleted.py", 1),
  ("D deleted.py\nA added.py", 2),
  ("D deleted.py\nA added.py\nA added.py", 3),
])
def test_parse_diff_output(output, num_changes):
  differ = Differ()
  differ.parse_output(output)
  assert len(differ.files) == num_changes

@pytest.mark.parametrize("files,folders", [
  ([], {}),
  ([FileStatus("","")], {}),
  ([FileStatus("A","tmpl1/main.sty")], {"tmpl1": "A"}),
  ([FileStatus("A","tmpl1/main.sty"), FileStatus("A","tmpl1/extra.sty")], {"tmpl1": "A"}),
  ([FileStatus("A","tmpl1/main.sty"), FileStatus("D","tmpl1/extra.sty")], {"tmpl1": "A"}),
  ([FileStatus("D","tmpl1/main.sty"), FileStatus("D","tmpl1/extra.sty")], {"tmpl1": "D"}),
  (
    [FileStatus("A","tmpl1/main.sty"), FileStatus("C","tmpl2/main.sty"), FileStatus("A","tmpl1/extra.sty")],
    {"tmpl1": "A", "tmpl2": "C"}
  ),
])
def test_reduce_to_folders(files, folders):
  differ = Differ()
  differ.files = files

  differ.reduce_to_folders()

  assert len(differ.folders.keys()) == len(list(folders.keys()))
  assert differ.folders == folders

