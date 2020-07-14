import aiohttp
from fpl import FPL
import pandas as pd


USER_ID = 2900521


def create_df_from_api(players, consts):
    player_df = pd.DataFrame([{"name": p.first_name + " " + p.second_name, "salary": p.now_cost,
                               "points": p.my_score, "team": p.team,
                               "position": consts["positions"][int(p.element_type) - 1]} for p in players])

    for team in range(1, consts["num_teams"] + 1):
        team_name = "team_" + str(team)
        player_df[team_name] = [1 if plr == team else 0 for plr in player_df.team]

    return player_df


async def get_player(i):
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        player = await fpl.get_player(i)
        return player


async def get_all_players():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        players = await fpl.get_players()
        return players


async def get_picks():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        user = await fpl.get_user(USER_ID)
        picks = await user.get_picks()
        return picks


async def get_fdr():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        fdr = await fpl.FDR()
        return fdr
