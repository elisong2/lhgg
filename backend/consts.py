
"""API Key"""
API_KEY = "RGAPI-c2777492-e73d-4386-a14d-2dc7c2db3bf2"

"""S15 Start: January 9th 2025 midnight, LA time"""
jan9_start = 1736409600
s15_start = 1736452800
curr_season = 15

"""Account PUUIDs"""
OPMAGE_PUUID    = "MghYJizn45WaJRnByqkNLzNdHBs_E3dpwS2NqC0-T77vpuDZj2Adz5VqXG8Q3JIK718qeY5r5mMvZw"
GOOSE_PUUID     = "oL8GDrbXU1FdtSPP3eQeHvvabBdT3KKQGu6M_3T9WFtPHg16-aTb2pweUIEf9_z_tW90fG5bwMVMvw"
HWANG_PUUID     = "CNiaK1yD4UTRPbOvsgnEagsOknfqXKbLIO7ZrVJAUuPdDe-6eSyey-un2WnD75K7J-yfXFc0OCev-Q"
PHILgc_PUUID    = ""
PHILpk_PUUID    = "XLM6TrOTTA-mCpF7il1Zo2Fv5xEwBT5EkEFjYMcYCuTeeNqVe-14N9aPL5zCtcsiUsG6Fr3XjNiYPw"
SEB_PUUID       = "e_JF1BQNx5qgaGsmH8E6uA3yEdDO7-LhKsZsZS-eBzU4--62xeuCLkd2RiEuyQTwjM0_kPH8mGizPA"
KENNEDY_PUUID   = "DWRpFa8lubNXGM3w9UOlIddeqx-I5b3HQvtIE3042BMR5yRbVOL6fEoSO6ARDFaRb_oLQbTRP0PxgA"
JACK_PUUID      = "zomlM7WEk9SCcvRZJOcLT5Xckh2Ykrr_za3HerlI1YyZZnTeqLfsuVRp14WkJ8VvjQR8IPez8XKNgw"

"""Queue Codes"""         
# https://static.developer.riotgames.com/docs/lol/queues.json
NORMS               = 400 # 5v5 draft only
ARAMHA              = 450 # Howling Abyss
ARAMBB              = 100 # Butchers Bridge
RANKED              = 420
DYNAMICQUEUE        = 410 # positional ranks dogwater
FLEX                = 440

URF                 = 1900
ARURF               = 900
SNOWARURF           = 1010
ARENA               = 1700 # or 1710 idk will have to test
SPELLBOOK           = 1400
ONEFORALL           = 1020
NEXUSBLITZ          = 1300

"""Summoner Spell Codes"""
# https://ddragon.leagueoflegends.com/cdn/15.9.1/data/en_US/summoner.json
HEAL                = 7        
GHOST               = 6
BARRIER             = 21
EXHAUST             = 3
CLARITY             = 13
FLASH               = 4
TELEPORT            = 12
SMITE               = 11
CLEANSE             = 1
IGNITE              = 14

MARK                = 32
URFMARK             = 39
FLEE                = 2201
CHERRYFLASH         = 2202 # I think this is arena

def ss_picker(code):   
    if int(code) == 7:
        return "Heal"
    elif int(code) == 6:
        return "Ghost"
    elif int(code) == 21:
        return "Barrier"
    elif int(code) == 3:
        return "Exhaust"
    elif int(code) == 13:
        return "Clarity"
    elif int(code) == 4 or int(code) == 2202:
        return "Flash"
    elif int(code) == 12:
        return "Teleport"
    elif int(code) == 11:
        return "Smite"
    elif int(code) == 1:
        return "Cleanse"
    elif int(code) == 14:
        return "Ignite"
    elif int(code) == 32 or int(code) == 39:
        return "Mark"
    elif int(code) == 2201:
        return "Flee"
    
    return "ERROR"

# matchmymods