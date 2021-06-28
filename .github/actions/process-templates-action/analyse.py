from os import path
from typing import Dict, Union
import pathlib
import json
import logging
from Differ import Differ


def analyse(latex_path: str, prev_listing: Union[Dict, None]):
  process_all = False

  # 1 - load previous listing
  existing_templates = {}
  if prev_listing and 'all' in prev_listing:
    existing_templates = prev_listing['all']
  else:
    logging.warning("Could not read/parse previous listing file, processing all templates")
    prev_listing = {}
    existing_templates = {}
    process_all = True


  # 2 - find folders that have been removed and need to be removed from the bucket
  p = pathlib.Path(latex_path)
  current_templates = [f.parts[-1] for f in p.iterdir() if f.is_dir()]
  current_templates = [c for c in current_templates if not c.startswith(".") and not c.startswith("__")]
  to_remove_from_bucket = [existing for existing in existing_templates if existing not in current_templates]


  # 3 - find folders with changes
  from_commit = "HEAD~1"
  to_process = []
  if 'lastrun' in prev_listing and 'commit' in prev_listing['lastrun'] and prev_listing['lastrun']['commit'] is not None:
      from_commit = prev_listing['lastrun']['commit']
  else:
    logging.warning("No lastrun commit in listing.json, processing all templates")
    existing_templates = {}
    to_process = current_templates
    process_all = True

  if not process_all:
    # use a diff from last commit to inform which templates to [re]process
    differ = Differ()
    try:
      differ.run(from_commit)
      to_process = [folder for folder in current_templates if folder in differ.folders]
    except:
      logging.warning("Could not get a diff, process all templates")
      to_process = current_templates
      process_all = True

    # NOTE could also scan bucket and look for missing


  # SETUP ANALYSIS COMPLETE
  logging.info("Run Setup Complete")
  logging.info(f"{len(to_remove_from_bucket)} templates will be removed from the bucket")
  for d in to_remove_from_bucket:
    logging.info(f" -{d}")
  if process_all:
    logging.info(f"All templates will be processed and pushed to the bucket")
  else:
    logging.info(f"{len(to_process)} templates will be processed and pushed to the bucket")
  for p in to_process:
    logging.info(f" +{p}")

  return current_templates, to_process, to_remove_from_bucket
