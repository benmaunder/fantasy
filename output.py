import re


def summary(prob):
    div = '---------------------------------------\n'
    print(f"{div}\nOptimised Fantasy Team:\n")
    for v in prob.variables():
        if v.varValue != 0:
            print(v.name, "=", v.varValue)
    print(div)


def total_team_value(prob, players):
    tot_players = 0
    tot_cost = 0.0
    tot_selected = 0.0
    tot_points = 0.0
    tot_ict = 0.0
    tot_form = 0.0

    for v in prob.variables():
        if v.varValue != 0:
            matches = re.search('([A-Z][A-Z])_([^\n]*)', v.name)
            position = matches.group(1)
            name = matches.group(2).replace('_', ' ')
            for p in players:
                actual_name = p.first_name + " " + p.second_name
                if actual_name.replace('-', ' ') == name:
                    tot_cost += float(p.now_cost)
                    tot_selected += float(p.selected_by_percent)
                    tot_points += float(p.total_points)
                    tot_ict += float(p.ict_index)
                    tot_form += float(p.form)
                    tot_players += 1
                    print(f"{position}: {name}: £{p.now_cost/10.0}M")

    print(f"\ntotal team value: £{round(tot_cost/10.0,1)}M")
    print(f"average percentage selected: {round(tot_selected / tot_players,2)}%")
    print(f"average total points: {round(tot_points / tot_players,1)}")
    print(f"average ICT rating: {round(tot_ict / tot_players,1)}")
    print(f"average form: {round(tot_form / tot_players,2)}")
