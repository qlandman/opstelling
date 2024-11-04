import numpy as np
import random
import os

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

app = FastAPI(docs_url=None, redoc_url=None)

# Set up Jinja2 templates
templates = Jinja2Templates(directory=f"{dir_path}/templates")
# Mount static files (for CSS)
app.mount("/static", StaticFiles(directory=f"{dir_path}/static"), name="static")

## Specific config for the Team calculation
n_periods: int = 8

team_members: list[str] = [
    "Benjamin",
    "Vik",
    "Vigo",
    "Can",
    "Njabulo",
    "Lars",
    "Sebas",
    "Kees",
    "Hamza",
]

excl_team: list[str] = []

tasks_base = [
    "Keeper",
    "Aanvaller",
    "Middenvelder 1",
    "Middenvelder 2",
    "Verdediger 1",
    "Verdediger 2",
]

headers = [f"Periode {i + 1}" for i in range(n_periods)]

keepers: list[str] = ["Hamza", "Vik", "Vigo", "Njabulo"]
keeper_idx = [team_members.index(keeper) for keeper in keepers]
random.shuffle(keeper_idx)

team: list[str] = [i for i in team_members if i not in excl_team]
team_idx = [team_members.index(member) for member in team]
random.shuffle(team_idx)

n_team: int = len(team)  # Number of team members
n_tasks: int = len(tasks_base)  # Number of team positions
n_subs: int = n_team - n_tasks  # The number of subs

tasks_sub = [f"Wissel {i}" for i in range(1, n_subs + 1)]
tasks = tasks_base + tasks_sub

# Create the matrix where rows are n team members playing and columns the
# n of periods
matrix: np.array = np.full((n_team, n_periods), -1).astype(int)


@app.get("/")
async def show_squad(request: Request):
    return templates.TemplateResponse(
        "base.html", {"request": request, "team_members": team_members}
    )


@app.post("/submit")
async def submit_form(
    request: Request, available: list[str] = Form(...), keepers: list[str] = Form(...)
):
    print(keepers)
    # matrix: np.array = np.full((n_team, n_periods), -1).astype(int)

    # # Set the keepers
    # matrix[0, np.arange(len(keeper_idx)) * 2] = keeper_idx
    # matrix[0, np.arange(len(keeper_idx)) * 2 + 1] = keeper_idx

    # # Set the substitutes for each period
    # sub_list: list = team_idx * (n_subs + 1)

    # for i in range(n_periods):
    #     for j in range(1, n_subs + 1):
    #         # t represents the first team member id from the list
    #         t: int = sub_list[0]

    #         # Check if the team member is already in the column
    #         if np.isin(t, matrix[:, i]):
    #             # Take the next element in the list given t is Keeper
    #             t = sub_list[1]
    #             # Check if team member was sub in previous period, if yes take next
    #             if np.isin(t, matrix[-n_subs:, i - 1]):
    #                 t = sub_list.pop(2)
    #             else:
    #                 t = sub_list.pop(1)
    #             matrix[j * -1, i] = t
    #         else:
    #             sub_list.remove(t)
    #             matrix[j * -1, i] = t

    # # Aanvallers for each period

    # for i in range(n_periods):
    #     for j in range(5):
    #         print
    #     if (i + 1) % 2 == 0:
    #         # We are substituting in the period
    #         # Get the previous attacker and check if he is substitute

    #         p_attack = matrix[1, i - 1]  # get attacker from previous period
    #         p_mid1 = matrix[2, i - 1]
    #         # p_mid2 = matrix[3,i-1]
    #         # p_def1 = matrix[4,i-1]
    #         # p_def2 = matrix[5,i-1]
    #         print(p_attack)
    #         if p_attack in matrix[:, i]:
    #             print(
    #                 f"the current attacker {team_members[p_attack]} is now sub in period {i+1}"
    #             )
    #             loc_sub = np.where(matrix[:, i] == p_attack)[0][0]
    #             print(loc_sub)
    #             matrix[1, i] = matrix[loc_sub, i - 1]
    #         else:
    #             matrix[1, i] = matrix[1, i - 1]

    #         if p_mid1 in matrix[:, i]:
    #             print(
    #                 f"the current Mid1 {team_members[p_mid1]} is now sub in period {i+1}"
    #             )
    #             loc_sub = np.where(matrix[:, i] == p_mid1)[0][0]
    #             matrix[2, i] = matrix[loc_sub, i - 1]
    #         else:
    #             matrix[2, i] = matrix[2, i - 1]

    #     else:
    #         unique_values, counts = np.unique(
    #             np.append(matrix[1, :], team_idx), return_counts=True
    #         )

    #         # Sort the unique values and their counts
    #         sorted_indices = np.argsort(counts)
    #         sorted_values = unique_values[sorted_indices]

    #         val = np.array([el for el in sorted_values if el not in matrix[:, i]])

    #         matrix[1, i] = val[0]
    #         matrix[2, i] = val[1]

    # Set the substitutes for each period
    warnings = []
    available_members = [member for member in team_members if member in available]
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "available_members": available_members,
            "warnings": warnings,
        },
    )
