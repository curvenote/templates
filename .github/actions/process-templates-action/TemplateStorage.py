from google.cloud.storage import Client
from os import path
from typing import Dict
import json
import logging
from TemplateAssets import TemplateAssets

class TemplateStorage():
  """
    Provides a simple interface around the Google Storage Client tailored
    to managing LaTeX template assets
  """
  def __init__(self, client: Client, bucket_name: str, tmp_folder: str):
    self.storage_path_base = "public"
    self.listing_storage_path = f"{self.storage_path_base}/listing.json"

    logging.info(f"Initialising Template Storage Class")
    self.client = client
    logging.info(f"Got client 🚀")
    logging.info(f"Try accessing bucket {bucket_name}")
    self.bucket = self.client.get_bucket(bucket_name)
    logging.info("Got bucket")
    self.tmp_folder = tmp_folder

  def get_listing(self):
    logging.info(f"Fetching last listing from {self.listing_storage_path}")
    blob = self.bucket.get_blob(self.listing_storage_path)

    if not blob:
      logging.info(f"No listing found")
      return None

    prev_listing_path = path.join(self.tmp_folder, "prev_listing.json")
    blob.download_to_filename(prev_listing_path)
    logging.info("Found and downloaded existing listing")
    with open(prev_listing_path) as fp:
      logging.info(f"Opened local file {prev_listing_path}")
      return json.load(fp)

  def push_template_asset(self, template: TemplateAssets):
    """
      Given the name of and paths to template template, this will create a 'folder'
      on storage and upload the template
    """
    for asset in template.contents:
      tmpl_base = f"{self.storage_path_base}/{template.name}"
      blob = self.bucket.blob(f"{tmpl_base}/{asset.storage_name}")
      blob.upload_from_filename(asset.path, asset.content_type)

  def delete_template_asset(self, template_name: str):
    """
      Given the template name will remove all blobs with the prefix
        self.storage_path_base/template_name
    """
    prefix = f"{self.storage_path_base}/{template_name}"
    blobs = self.bucket.list_blobs(prefix=prefix)
    for blob in blobs:
      blob.delete()

  def push_listing(self, listing: Dict):
    """
      Given any dict this will be uploaded to storage as the main listing.json file
    """
    local_path = path.join(self.tmp_folder, "new_listing.json")
    try:
      with open(local_path, 'w') as fp:
        json.dump(listing, fp)
    except Exception as err:
      logging.info(f"Could not create local listing file at {local_path}")
      raise err
    new_blob = self.bucket.blob(self.listing_storage_path)
    logging.info(f"Created blob {self.listing_storage_path}")
    new_blob.upload_from_filename(local_path, 'application/json')
    logging.info(f"Uploaded listing")
