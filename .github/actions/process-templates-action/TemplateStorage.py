from google.cloud import storage
from os import path
from typing import Dict
import json
import logging

class TemplateStorage():

  def __init__(self, project_id: str, bucket_name: str, tmp_folder: str):
    logging.info(f"Initialising Template Storage Class for project {project_id}")
    self.client = storage.Client(project_id)
    logging.info(f"Got client 🚀")
    logging.info(f"Try accessing bucket {bucket_name}")
    self.bucket = self.client.get_bucket(bucket_name)
    logging.info("Got bucket")
    self.tmp_folder = tmp_folder

  def get_listing(self):
    blob = self.bucket.get_blob('public/listing.json')

    if not blob:
      return None

    prev_listing_path = path.join(self.tmp_folder, "prev_listing.json")
    blob.download_to_filename(prev_listing_path)
    logging.info("Found and downloaded existing listing")
    with open(prev_listing_path) as fp:
      return json.load(fp)

  def push_template_assets(self, assets: Dict):
    pass

  def delete_template_assets(self, template: str):
    pass

  def push_listing(self, listing: Dict):
    pass
