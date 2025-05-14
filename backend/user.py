import os
from utils import utils 
from consts import *
from datetime import datetime, timezone
import pandas as pd
import csv

class user:
    def __init__(self, ign, tag):
        self.ign = ign
        self.tag = tag

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.join(script_dir, "user_data")

        self.user_dir = os.path.join(self.base_dir, ign + tag)  
        if not os.path.exists(self.user_dir):
            os.makedirs(self.user_dir)
            self.create_dataframe()
            print("Welcome " + ign + "!")
        else: print("Welcome back " + ign + "!")
        
            
    def create_dataframe(self):
        temp = utils.get_puuid(self.ign, self.tag[1:], API_KEY, region="americas")
        if temp[0] == "ERROR":
                print(temp)
                print("Try again later!")
                return
        #
        prof_data = {
            "Summoner": [self.ign + self.tag],     # To store event or action timestamps
            "PUUID": [temp],
            "Last updated": [s15_start]            
        }
        self.prof_df = pd.DataFrame(prof_data)
        
        #
        gen_stats = {
            "S15 KDA": [],
            "S15 W/L": [],

            "Norms KDA": [],
            "Norms W/L": [],

            "ARAM KDA": [],
            "ARAM W/L": [],

            "Arena KDA": [],
            "Arena W/L": []
        }
        self.gen_df = pd.DataFrame(gen_stats)
        
        #
        self.ss_df = pd.DataFrame(columns=["Spell", "Uses"])
       
        #
        self.champ_df = pd.DataFrame(columns=["Champion", "Q_casts", "W_casts", "E_casts", "R_casts", "Kills", "Deaths", "Assists"])

        # Save the newly created DataFrame
        self.prof_df.to_csv(os.path.join(self.user_dir, self.ign + self.tag + '_prof.csv'), index=False)
        self.gen_df.to_csv(os.path.join(self.user_dir, self.ign + self.tag + 'genStats.csv'))
        self.ss_df.to_csv(os.path.join(self.user_dir, self.ign + self.tag + 'ssCasts.csv'))
        self.champ_df.to_csv(os.path.join(self.user_dir, self.ign + self.tag + 'champStats.csv'))

        with open(os.path.join(self.user_dir, self.ign + self.tag + ".csv"), mode="w") as file:
            pass 

        print(f"New dataframes created and saved")
        

    def update(self):
        start_idx = 0
        count = 20 

        # fetching a copy of the profile
        prof_filepath = os.path.join(self.user_dir, self.ign + self.tag + '_prof.csv')  
        profile = pd.read_csv(prof_filepath)
        puuid = profile["PUUID"].iloc[0]
        last_updated = int(profile["Last updated"].iloc[0])
        last_updated_temp = last_updated
        
        match_list = []
        recent_flag = False
        counter = 0
        total_counter = 0
        gen_stats_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'genStats.csv') 
        champ_df_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'champStats.csv') 
        ss_df_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'ssCasts.csv')

        gen_stats_df = pd.read_csv(gen_stats_filepath)
        champ_df = pd.read_csv(champ_df_filepath)
        ss_df = pd.read_csv(ss_df_filepath)

        while 1:
            # get all the matches
            matches = utils.get_match_ids_all_q_types(puuid, API_KEY, start_idx=start_idx, count=count)
            if matches[0] == "ERROR":
                print(matches)
                print("Try again later!")
                return
            # go through the matches we have just pulled
            for i in range(len(matches)):
                # if the time of the match is greater than what was last recorded then you append + adding second clause to ensure only season 15 games for now
                curr_match = utils.get_match_data(matches[i], API_KEY)
                if "ERROR" in curr_match:
                    print(curr_match)
                    print("Try again later!")
                    return
                time = int(curr_match["info"]["gameStartTimestamp"]) // 1000 #gameCreation is loading screen
                version = int(curr_match["info"]["gameVersion"][:2])
                # if time > last_updated: print("this is a recent game")
                # print(version)
                if time <= last_updated:
                    break
                elif time > last_updated and version == curr_season:
                    counter += 1
                    total_counter += 1
                    if recent_flag == False:
                        last_updated_temp = time
                        recent_flag = True
                    # create sublist starting from oldest match that meets this requirement ^^^ and onward
                    match_list.append(matches[i])
                    
                    my_game_data = utils.get_player_data(curr_match, puuid)
                    gen_stats_df = self.update_gen_stats_df(gen_stats_df, my_game_data)
                    champ_df = self.update_champ_df(champ_df, my_game_data)  
                    ss_df = self.update_ss_df(ss_df, my_game_data) 
                
            # append the correct set of matches
           

            # if all games from request were appended then you run another iteration
            if len(matches) == counter:
                start_idx += count
                counter = 0
            else: 
                print("\nUpdate completed for " + profile["Summoner"].iloc[0])
                profile.at[0, "Last updated"] = last_updated_temp 
                profile.to_csv(prof_filepath, index=False)

                gen_stats_df.to_csv(gen_stats_filepath, index=False)
                champ_df.to_csv(champ_df_filepath, index=False)
                ss_df.to_csv(ss_df_filepath, index=False)

                match_id_filepath = os.path.join(self.user_dir, self.ign + self.tag + '.csv')
                utils.write_csv(match_list, match_id_filepath)


                print(total_counter, "new games recorded :D")
                return
            
        
    def update_champ_df(self, df, my_game_data):
        champ_name = my_game_data["championName"]
        q = int(my_game_data["spell1Casts"])
        w = int(my_game_data["spell2Casts"])
        e = int(my_game_data["spell3Casts"])
        r = int(my_game_data["spell4Casts"])
        k = int(my_game_data["kills"])
        d = int(my_game_data["deaths"])
        a = int(my_game_data["assists"])

        if champ_name in df["Champion"].values:
            df.loc[df["Champion"] == champ_name, "Q"] += q
            df.loc[df["Champion"] == champ_name, "W"] += w
            df.loc[df["Champion"] == champ_name, "E"] += e
            df.loc[df["Champion"] == champ_name, "R"] += r
            df.loc[df["Champion"] == champ_name, "Kills"] += k
            df.loc[df["Champion"] == champ_name, "Deaths"] += d
            df.loc[df["Champion"] == champ_name, "Assists"] += a
        else:
            new_row = pd.DataFrame([{
                "Champion": champ_name,
                "Q": q,
                "W": w,
                "E": e,
                "R": r,
                "Kills": k,
                "Deaths": d,
                "Assists": a
            }])
            df = pd.concat([df, new_row], ignore_index=True)
        
        return df
        # pass

    def update_gen_stats_df(self, df, my_game_data):
        pass

    def update_ss_df(self, df, my_game_data):
        ss1_name = ss_picker(my_game_data["summoner1Id"])
        ss1_casts = int(my_game_data["summoner1Casts"])
        ss2_name = ss_picker(my_game_data["summoner2Id"])
        ss2_casts = int(my_game_data["summoner2Casts"])
        
        
        if ss1_name in df["Spell"].values:
            df.loc[df["Spell"] == ss1_name, "Uses"] += ss1_casts
        else:
            new_row = pd.DataFrame([{"Spell": ss1_name, "Uses": ss1_casts}])
            df = pd.concat([df, new_row], ignore_index=True)
        
        if ss2_name in df["Spell"].values:
            df.loc[df["Spell"] == ss2_name, "Uses"] += ss2_casts
        else:
            new_row = pd.DataFrame([{"Spell": ss2_name, "Uses": ss2_casts}])
            df = pd.concat([df, new_row], ignore_index=True)
        print(df)
        return df
        # pass
            
  
    def reshape(self):
        return
        # fetching a copy of the profile
        prof_filepath = os.path.join(self.user_dir, self.ign + self.tag + '_prof.csv')  
        profile = pd.read_csv(prof_filepath)
        puuid = profile["PUUID"].iloc[0]
        
        total_counter = 0
        gen_stats_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'genStats.csv') 
        champ_df_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'champStats.csv') 
        ss_df_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'ssCasts.csv')

        gen_stats_df = pd.read_csv(gen_stats_filepath)
        champ_df = pd.read_csv(champ_df_filepath)
        ss_df = pd.read_csv(ss_df_filepath)

   
        # get all the matches
        with open(self.user_dir, self.ign + self.tag + '.csv', mode ='r')as file:
            csvFile = csv.reader(file)
            for lines in csvFile:
                print(lines)
                curr_match = utils.get_match_data(str(lines), API_KEY)
                if "ERROR" in curr_match:
                    print(curr_match)
                    print("Try again later!")
                    return
                total_counter += 1
                my_game_data = utils.get_player_data(curr_match, puuid)
                gen_stats_df = self.update_gen_stats_df(gen_stats_df, my_game_data)
                champ_df = self.update_champ_df(champ_df, my_game_data)  
                ss_df = self.update_ss_df(ss_df, my_game_data) 

        
            print("\nReshape completed for " + profile["Summoner"].iloc[0])
            gen_stats_df.to_csv(gen_stats_filepath, index=False)
            champ_df.to_csv(champ_df_filepath, index=False)
            ss_df.to_csv(ss_df_filepath, index=False)

            


            print(total_counter, "new games recorded :D")
            return