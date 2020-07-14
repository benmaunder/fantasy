from pulp import *


def lp_set_up_prob(df, CONSTANTS):
    salaries = {}
    points = {}
    teams = {}
    for pos in df.position.unique():
        available_pos = df[df.position == pos]
        salary = list(available_pos[["name", "salary"]].set_index("name").to_dict().values())[0]
        point = list(available_pos[["name", "points"]].set_index("name").to_dict().values())[0]
        team_array = {}
        for team in range(1, CONSTANTS["num_teams"] + 1):
            teamname = "team_" + str(team)
            team_array[teamname] = list(available_pos[["name", teamname]].set_index("name").to_dict().values())[0]
        salaries[pos] = salary
        points[pos] = point
        teams[pos] = team_array

    return salaries, points, teams


def lp_create_and_solve(df, CONSTANTS):

    salaries, points, teams = lp_set_up_prob(df, CONSTANTS)

    pos_num_available = dict(zip(CONSTANTS["positions"], CONSTANTS["num_same_position"]))

    _vars = {k: LpVariable.dict(k, v, cat="Binary") for k, v in points.items()}


    prob = LpProblem("Fantasy", LpMaximize)
    rewards = []
    costs = []
    team_constraints = [[] for i in range(20)]

    for k, v in _vars.items():
        costs += lpSum([salaries[k][i] * _vars[k][i] for i in v])
        rewards += lpSum([points[k][i] * _vars[k][i] for i in v])
        prob += lpSum([_vars[k][i] for i in v]) == pos_num_available[k]
        for team in range(CONSTANTS["num_teams"]):
            teamname = "team_" + str(team+1)
            team_constraints[team] += lpSum([teams[k][teamname][i] * _vars[k][i] for i in v])

    for team in range(CONSTANTS["num_teams"]):
        prob += lpSum(team_constraints[team]) <= CONSTANTS["max_same_team"]

    prob += lpSum(rewards)
    prob += lpSum(costs) <= CONSTANTS["salary_cap"]

    prob.solve()



    return prob
