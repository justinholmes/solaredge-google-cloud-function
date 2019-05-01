import os

import arrow
import solaredge as solaredge
import gcs_upload
import json

api_key = os.environ.get("solaredge_api_key")
solaredge_api = solaredge.Solaredge(api_key)
site_id = os.environ.get("solaredge_id")
site_energy_date = arrow.now().format('YYYY-MM-DD')
date_and_hour = 'YYYY-MM-DD hh:mm:ss'
site_power_start_date = arrow.now().replace(days=-1).format(date_and_hour)
site_power_end_date = arrow.now().replace().format(date_and_hour)


def get_energy():
    power_details = solaredge_api.get_power_details(site_id, site_power_start_date, site_power_end_date)
    energy = solaredge_api.get_energy(site_id, start_date=site_energy_date, end_date=site_energy_date)
    day_production = {'total_produced': energy['energy']['values'][0]['value']}
    combined_dicts = ({**day_production, **power_details})
    gcs_upload.upload(site_energy_date, json.dumps(combined_dicts))


if __name__ == '__main__':
    get_energy()
