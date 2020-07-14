import asyncio
import get_data_from_api as gt_api
import get_data_from_historic as gt_hst
import player_scoring as ps
import optimisation_problem as opt
import output

CONSTANTS = {"salary_cap": 1008,
             "num_teams": 20,
             "positions": ["GK", "DF", "MF", "FW"],
             "num_same_position": [2, 5, 5, 3],
             "max_same_team": 3}

scoring_coeffs = {"select": 1/24,
                  "form": 1/5,
                  "points": 1/155,
                  "ict": 1/196,
                  "fdr": 10}


if __name__ == '__main__':
    players = asyncio.run(gt_api.get_all_players())
    for player in players:
        my_score = ps.get_player_score(player, scoring_coeffs)
        setattr(player, "my_score", my_score)

    player_df = gt_api.create_df_from_api(players, CONSTANTS)

    solved_prob = opt.lp_create_and_solve(player_df, CONSTANTS)

    output.total_team_value(solved_prob, players)




