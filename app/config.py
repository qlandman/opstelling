""" 
Config file containing basic team information
"""


class Team:
    n_parts: int = 4
    n_subs: int = 2
    n_periods = n_parts * n_subs

    team_members: list[str] = [
        "Benjamin",
        "Can",
        "Hamza",
        "Kees",
        "Lars",
        "Njabulo",
        "Sebas",
        "Vigo",
        "Vik",
    ]

    excl_team: list[str] = []

    positions_base = [
        "Keeper",
        "Aanvaller",
        "Middenvelder",
        "Middenvelder",
        "Verdediger",
        "Verdediger",
    ]
