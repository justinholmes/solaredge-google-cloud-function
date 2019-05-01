import zlib

from google.cloud import storage
import os

client = storage.Client(project=os.environ.get('GCP_PROJECT'))
bucket = client.get_bucket(os.environ.get('gcs_bucket'))
compressobj = zlib.compressobj(9, zlib.DEFLATED, 31)

def upload(date, blob_data):
    blob = bucket.blob("ingestion/solaredge/{}/data.json".format(date))
    blob.content_encoding = 'gzip'
    blob.upload_from_string(compressobj.compress(blob_data) + compressobj.flush())
