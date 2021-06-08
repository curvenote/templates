import json
import builtins
from unittest.mock import Mock, MagicMock, patch, mock_open, call
from google.cloud.storage import Client, Bucket
from TemplateStorage import TemplateStorage
from TemplateAssets import TemplateAssets


@patch.object(Client, "get_bucket")
def test_init(mock_client):
  mock_bucket = MagicMock()
  mock_client.return_value = mock_bucket
  client = Client('curvenote-dev-1')
  storage = TemplateStorage(client, 'some_bucket', '/tmp')
  assert storage.bucket == mock_bucket

def test_get_listing_when_none():
  storage = TemplateStorage(MagicMock(), 'some_bucket', '/tmp')
  storage.bucket = MagicMock()
  storage.bucket.get_blob = Mock(return_value=None)

  assert storage.get_listing() is None

def test_push_template_asset():
  storage = TemplateStorage(MagicMock(), 'some_bucket', '/tmp')
  storage.bucket = MagicMock()

  storage.push_template_asset(TemplateAssets('tmpl1', 'p/t.zip', 'p/o.json'))

  storage.bucket.blob.assert_has_calls([
    call('public/tmpl1/template.latex.zip'),
    call().upload_from_filename('p/t.zip', 'application/zip'),
    call('public/tmpl1/options.json'),
    call().upload_from_filename('p/o.json', 'application/json')
    ])
