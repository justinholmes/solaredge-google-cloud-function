import json
import os
from datetime import datetime

from arrow import arrow
from solaredge import solaredge

import gcs_upload
import solaredge_api

start = datetime(2019, 4, 23)
api_key = os.environ.get("solaredge_api_key")
end = arrow.Arrow.now().replace(days=-1)
solaredge_api = solaredge.Solaredge(api_key)
site_id = os.environ.get("solaredge_id")

for r in arrow.Arrow.range('day', start, end):
    date = r.format("YYYY-MM-DD")
    print(date)
    energy = solaredge_api.get_energy(site_id, start_date=date, end_date=date)
    print(energy)
    power_details = solaredge_api.get_power_details(site_id, r.format("YYYY-MM-DD 00:00:00"),
                                                    r.format("YYYY-MM-DD 21:00:00"))
    day_production = {'date': date, 'total_produced': energy['energy']['values'][0]['value']}
    combined_dicts = ({**day_production, **power_details})
    gcs_upload.upload(date, json.dumps(combined_dicts))
