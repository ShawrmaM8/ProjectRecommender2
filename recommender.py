def recommend_projects(user_prefs, all_projects):
    # Rule-based scoring: weighted difference (higher score = better match)
    for p in all_projects:
        p['match_score'] = (
            (10 - abs(user_prefs.get('complexity', 5) - p['complexity'])) * 0.4 +
            (10 - abs(user_prefs.get('scalability', 5) - p['scalability'])) * 0.3 +
            (10 - abs(user_prefs.get('practicality', 5) - p['practicality'])) * 0.3
        )
    # Sort by match_score descending (best to least)
    return sorted(all_projects, key=lambda p: p['match_score'], reverse=True)