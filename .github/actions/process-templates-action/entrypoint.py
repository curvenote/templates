from os import path, mkdir, environ
import pathlib
import json
import typer
import tempfile
from analyse import analyse
from shutil import make_archive
from TemplateStorage import TemplateStorage
from TemplateAssets import TemplateAssets
import yaml
import subprocess
from google.cloud import storage as gcp_storage
from typing import Dict


import logging
logging.getLogger().setLevel(logging.INFO)


def main(repo_path: str):
  logging.info(f"repo_path set to {repo_path}")
  if not path.exists(repo_path):
    raise IOError(f"Repo not found at {repo_path}")

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
    all_templates, to_process, to_remove_from_bucket = analyse(repo_path, prev_listing)

    # process assets ready for update
    logging.info("Start processing...")
    processed_assets: List[TemplateAssets] = []
    for tmpl in to_process:
    # run procesing steps on each template; zip
      logging.info(f"processing: {tmpl}")
      mkdir(path.join(tmp_folder, tmpl))

      zip_filepath = make_archive(
        path.join(tmp_folder, tmpl, 'latex.template'), 'zip', path.join(repo_path, tmpl))
      logging.info(f"created zipfile {zip_filepath}")

      options_json_filepath = path.join(tmp_folder, tmpl, 'options.json')
      with open(path.join(repo_path, tmpl, 'options.yml')) as oyml:
        with open(options_json_filepath, 'w') as ojson:
          options = yaml.load(oyml, Loader=yaml.FullLoader)
          json.dump(options, ojson, indent=4)
      logging.info(f"created options.json {zip_filepath}")

      processed_assets.append(TemplateAssets(tmpl, zip_filepath, options_json_filepath))
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
      for tmpl in to_remove_from_bucket:
        storage.delete_template_asset(processed_assets[tmpl])
      logging.info("Removal complete")

    # TODO: commit to git - if needed

    # update listings and lastrun commit hash
    gitsha = subprocess.check_output('git rev-parse --short HEAD', shell=True, encoding="utf-8")
    logging.info(f"Logging this run with current git sha {gitsha}")
    storage.push_listing({
      "all": all_templates,
      "lastrun": { "commit": gitsha.strip() }
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
