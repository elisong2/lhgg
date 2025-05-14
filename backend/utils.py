import requests
import math
import numpy as np
import time
import datetime
import csv

from consts import *


class utils: 
    def get_puuid(ign, tag, api_key, region="americas"):
        my_url = ("https://" + region + ".api.riotgames.com/riot/account/v1/accounts/"
            + "by-riot-id/"  + ign + "/" + tag
            + "?api_key="    + api_key)
        
        while True:
            api_resp = requests.get(my_url)
            if api_resp.status_code == 429:
                time.sleep(15)
                continue
            elif api_resp.status_code == 200:
                my_info = api_resp.json()
                return my_info['puuid']
            else:
                # print("ERROR", api_resp.status_code)
                return ["ERROR", str(api_resp.status_code)]

    def get_match_ids_all_q_types(puuid, api_key, start_idx=0, count=20, region="americas"):
        my_url = ("https://" + region + ".api.riotgames.com/lol/match/v5/matches/"
            + "by-puuid/"    + puuid
            + "/ids"
            + "?start="      + str(start_idx)
            + "&count="      + str(count)
            + "&api_key="    + api_key)

        while True:
            api_resp = requests.get(my_url)
            if api_resp.status_code == 429:
                time.sleep(15)
                continue
            elif api_resp.status_code == 200:
                return api_resp.json()
            else:
                # print("ERROR", api_resp.status_code)
                return ["ERROR", str(api_resp.status_code)]

    def get_match_ids_by_q_type(puuid, api_key, q_code, start_idx=0, count=20):
        my_url = ("https://americas.api.riotgames.com/lol/match/v5/matches/"
            + "by-puuid/" + puuid
            + "/ids"
            + "?queue="   + str(q_code)
            + "&start="   + str(start_idx)
            + "&count="   + str(count)
            + "&api_key=" + api_key)

        while True:
            api_resp = requests.get(my_url)
            if api_resp.status_code == 429:
                time.sleep(15)
                continue
            elif api_resp.status_code == 200:
                return api_resp.json()
            else:
                # print("ERROR", api_resp.status_code)
                return ["ERROR", str(api_resp.status_code)]
        

    def get_match_data(match_id, api_key):
        my_url = ("https://americas.api.riotgames.com/lol/match/v5/matches/"
            + match_id
            + "?api_key=" + api_key)

        while True:
            api_resp = requests.get(my_url)
            if api_resp.status_code == 429:
                time.sleep(15)
                continue
            elif api_resp.status_code == 200:
                return api_resp.json()
            else:
                # print("ERROR", api_resp.status_code)
                return ["ERROR", str(api_resp.status_code)]


    def get_player_data(match_data, puuid):
        players = match_data['metadata']['participants']
        idx = players.index(puuid)
        player_data = match_data['info']['participants'][idx]
        return player_data
    

    def unix_converter(epoch):
        # timestamp = epoch//1000
        timestamp = epoch
        dt_obj = datetime.datetime.fromtimestamp(timestamp)
        return dt_obj

        # # Unix epoch timestamp (e.g., 1696857600)
        # timestamp = 1729322547223
        # # Convert the Unix timestamp to a datetime object
        # dt_object = datetime.datetime.fromtimestamp(timestamp//1000)
        # print(timestamp//1000)
        # # Print the result
        # print(dt_object)

    def write_csv(matchIDs, filename):
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            
            for ID in matchIDs:
                writer.writerow([ID])

    def reformat_csv(file):
        return 0
# should I use package file system
# how to run individual functions in a file and give it inputs

