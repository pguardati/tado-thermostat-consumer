import json
import os
import re
from datetime import datetime

import pandas as pd
import requests


def get_token(client_secret):
    url = "https://auth.tado.com/oauth/token"
    payload = {
        "client_id": "tado-web-app",
        "grant_type": "password",
        "scope": "home.user",
        "username": os.environ["TADO_EMAIL"],
        "password": os.environ["TADO_PASSWORD"],
        "client_secret": client_secret,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.request("POST", url, headers=headers, data=payload)
    token = json.loads(response.text)["access_token"]
    return token


def get_home_id(token):
    url = "https://my.tado.com/api/v1/me"
    response = requests.request(
        "GET", url, headers={"Authorization": f"Bearer {token}"}
    )
    home_id = json.loads(response.text)["homeId"]
    return home_id


def get_zones(token, home_id):
    # curl -s "https://my.tado.com/api/v2/homes/123456/zones" -H "Authorization: Bearer abc"
    url = f"https://my.tado.com/api/v2/homes/{home_id}/zones"
    response = requests.request(
        "GET", url, headers={"Authorization": f"Bearer {token}"}
    )
    zones = json.loads(response.text)
    zone_id = zones[0]["id"]
    return zone_id


def get_daily_data(token, home_id, zone_id, date):
    # curl -s 'https://my.tado.com/api/v2/homes/123456/zones/1/dayReport?date=2018-02-14' -H 'Authorization: Bearer abc'  # noqa
    url = f"https://my.tado.com/api/v2/homes/{home_id}/zones/{zone_id}/dayReport?date={date}"
    response = requests.request(
        "GET", url, headers={"Authorization": f"Bearer {token}"}
    )
    historic_data = json.loads(response.text)
    return historic_data


def _get_historic_data(
    token,
    home_id,
    zone_id,
    start_date,
    download_dir,
    reload_today,
    reload_all,
):
    def _delete_today_data(date):
        if date.strftime("%Y-%m-%d") == datetime.now().strftime("%Y-%m-%d"):
            file = os.path.join(download_dir, f"historic_data_{date}.json")
            if os.path.isfile(file):
                os.remove(file)
                print("delete today data")

    def _get_missing_daily_data(date):
        file = os.path.join(download_dir, f"historic_data_{date}.json")
        if os.path.isfile(file) and not reload_all:
            print(f"historic_data_{date}.json already exists")
        else:
            print(f"Getting data for {date}")
            date = date.strftime("%Y-%m-%d")
            historic_data = get_daily_data(token, home_id, zone_id, date)
            with open(file, "w") as f:
                json.dump(historic_data, f)

    end_date = datetime.now().strftime("%Y-%m-%d")
    print(f"Getting data from {start_date} to {end_date}")
    for date in pd.date_range(start_date, end_date):
        if reload_today:
            _delete_today_data(date)
        _get_missing_daily_data(date)


def get_client_secret():
    response = requests.request("GET", "https://app.tado.com/env.js")
    if response.status_code != 200:
        raise Exception("Failed to get client secret")
    data_string = response.text
    client_secret_match = re.search(r"clientSecret: '([^']+)'", data_string)
    client_secret = client_secret_match.group(1) if client_secret_match else None
    return client_secret


def get_historic_data(start_date, download_dir, reload_today, reload_all):
    client_secret = get_client_secret()
    token = get_token(client_secret)
    home_id = get_home_id(token)
    zone_id = get_zones(token, home_id)
    _get_historic_data(
        token,
        home_id,
        zone_id,
        start_date,
        download_dir,
        reload_today,
        reload_all,
    )
