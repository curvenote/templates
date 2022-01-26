from os import path, mkdir, environ
import pathlib
import json
import typer
import yaml
import tempfile
from analyse import analyse
from shutil import make_archive, move
from TemplateStorage import TemplateStorage
from TemplateAssets import TemplateAssets, Asset
import subprocess
from google.cloud import storage as gcp_storage
from typing import Dict, List, Any


import logging
logging.getLogger().setLevel(logging.INFO)

def get_local_options(latex_path: str, tmpl: str):
  with open(path.join(latex_path, tmpl, 'template.yml')) as oyml:
    return yaml.load(oyml, Loader=yaml.FullLoader)

def scope_options_metadata(options: Dict[str, Any], template_id: str) -> Dict[str, Any]:
  metadata = options["metadata"]
  return dict(**metadata, id=f"public/{template_id}", owner='public', kind='tex', is_private=False)

def move_folders(folders: List[str], src: str, dest: str):
  for folder in folders:
    if path.exists(path.join(src, folder)):
      logging.info(f"Found folder, moving from {src} to {dest}")
      move(path.join(src, folder), path.join(dest, folder))

def main(repo_path: str):
  logging.info(f"repo_path set to {repo_path}")
  if not path.exists(repo_path):
    raise IOError(f"Repo not found at {repo_path}")

  latex_path = path.join(repo_path, 'latex')
  logging.info(f"Looking for latex template in {latex_path}")

  with tempfile.TemporaryDirectory() as tmp_folder:
    logging.info("Created Temporary Folder")

    # EARLY CHECK for bucket permissions
    try:
      storage  = TemplateStorage(
        gcp_storage.Client(environ["GCP_PROJECT_ID"]),
        environ['BUCKET_NAME'],
        tmp_folder
        )
    except Exception as err:
      logging.error("Failed to get bucket, maybe an auth issue")
      raise err

    # pull the previous listing down
    prev_listing = storage.get_listing()
    # Analyse the repo contents, listing and diff since last processing pass
    all_templates, to_process, to_remove_from_bucket = analyse(latex_path, prev_listing)

    # check for rebuild all flag
    with open(path.join(repo_path, 'config.yml'), 'r') as file:
      base_config = yaml.load(file, Loader=yaml.FullLoader)

    if base_config["action"]["rebuild"]:
      to_process = all_templates

    # process assets ready for update
    logging.info("Start processing...")
    processed_assets: List[TemplateAssets] = []
    for template_id in to_process:
    # run procesing steps on each template; zip
      logging.info(f"processing: {template_id}")
      mkdir(path.join(tmp_folder, template_id))

      move_folders(['original','example'], path.join(latex_path, template_id), tmp_folder)

      zip_filepath = make_archive(
        path.join(tmp_folder, template_id, 'latex.template'), 'zip', path.join(latex_path, template_id))
      logging.info(f"created zipfile {zip_filepath}")

      move_folders(['original','example'], tmp_folder, path.join(latex_path, template_id))

      options_json_filepath = path.join(tmp_folder, template_id, 'template.json')
      options = get_local_options(latex_path, template_id)
      options = scope_options_metadata(options, template_id)
      with open(options_json_filepath, 'w') as ojson:
        json.dump(options, ojson, indent=4)
      logging.info(f"created template.json {zip_filepath}")

      template_assets = TemplateAssets(template_id)
      template_assets.append(Asset(zip_filepath, 'template.latex.zip', 'application/zip'))
      template_assets.append(Asset(options_json_filepath, 'template.json', 'application/json'))
      thumbnail_filepath = path.join(latex_path, template_id, 'thumbnail.png')
      if path.exists(thumbnail_filepath):
        template_assets.append(Asset(thumbnail_filepath, 'thumbnail.png', 'image/png'))

      processed_assets.append(template_assets)
    logging.info("Processing complete")

    # push new templates
    if len(processed_assets):
      logging.info("Start uploading processed assets...")
      for assets in processed_assets:
        storage.push_template_asset(assets)
        logging.info(f"{assets.name} uploaded")
      logging.info("Upload complete")

    if len(to_remove_from_bucket):
      logging.info("Removing deleted templates...")
      # delete removed templates
      for template_id in to_remove_from_bucket:
        logging.info(f"Removing {template_id}")
        storage.delete_template_asset(template_id)
      logging.info("Removal complete")

    # TODO: commit to git - if needed

    # get current git sha for tagging
    gitsha = subprocess.check_output(
      'git rev-parse --short HEAD', shell=True, encoding="utf-8").strip()

    # update listings and refresh metadata
    all = []
    for template_id in all_templates:
      options = get_local_options(latex_path, template_id)
      options = scope_options_metadata(options, template_id)
      all.append(dict(commit=gitsha, **options['metadata']))

    # update listings and lastrun commit hash
    logging.info(f"Logging this run with current git sha {gitsha}")
    storage.push_listing({
      "items": all,
      "lastrun": { "commit": gitsha }
    })

    # TODO: git push - id needed

if __name__ == "__main__":
  logging.info("Started Python Processing Script")

  missing_env = []
  if 'GOOGLE_APPLICATION_CREDENTIALS' not in environ:
    typer.echo('GOOGLE_APPLICATION_CREDENTIALS missing, run gcloud-setup action prior to this')
    typer.Exit(1)
  if 'GCP_PROJECT_ID' not in environ:
    missing_env.append("GCP_PROJECT_ID")
  if 'GCP_SA_KEY' not in environ:
    missing_env.append("GCP_SA_KEY")
  if 'BUCKET_NAME' not in environ:
    missing_env.append("BUCKET_NAME")
  if len(missing_env) > 1:
    typer.echo(f"{','.join(missing_env)} not set")
    raise typer.Exit(1)

  typer.run(main)
