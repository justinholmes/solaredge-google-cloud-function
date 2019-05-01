from google.cloud import storage
import os

client = storage.Client(project=os.environ('GCP_PROJECT'))
bucket = client.get_bucket(os.environ('gcs_bucket'))


def upload(date, blob_data):
    blob = bucket.blob("ingestion/solaredge/{}/data.json".format(date))
    blob.upload_from_string(blob_data)
