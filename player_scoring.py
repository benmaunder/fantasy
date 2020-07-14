def get_player_score(p, scoring_coeffs):

    score = (scoring_coeffs["select"] * float(p.selected_by_percent)) + \
            (scoring_coeffs["form"] * float(p.form)) + \
            (scoring_coeffs["points"] * float(p.total_points)) + \
            (scoring_coeffs["ict"] * float(p.ict_index))

    if p.chance_of_playing_next_round is None or p.chance_of_playing_this_round is None:
        score = 0
    elif p.chance_of_playing_next_round < 100 or p.chance_of_playing_this_round < 100:
        score = 0

    return float(score)

