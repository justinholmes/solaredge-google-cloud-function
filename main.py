import json

import base64
import solaredge_api


def message(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    json_payload = json.loads(pubsub_message)
    if 'ingest' in json_payload:
        if json_payload['ingest'] == 'solaredge':
            solaredge_api.get_energy()
