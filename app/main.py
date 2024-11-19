import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from config import Team
from opstelling import generate_opstelling, create_team_table

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

app = FastAPI(docs_url=None, redoc_url=None)

# Set up Jinja2 templates
templates = Jinja2Templates(directory=f"{dir_path}/templates")
# Mount static files (for CSS)
app.mount("/static", StaticFiles(directory=f"{dir_path}/static"), name="static")


@app.get("/")
async def show_squad(request: Request):
    return templates.TemplateResponse(
        "base.html", {"request": request, "team_members": Team.team_members}
    )


@app.post("/submit")
async def submit_form(
    request: Request,
    available: list[str] = Form(...),
    keepers: list[str] = Form(None),
):
    # List that holds warnings
    warnings: list[str] = []

    # Check the input form data
    if available is None or len(available) < 6:
        warnings.append("- Selecteer minimaal 6 spelers")

    if keepers is None or len(keepers) != 4:
        warnings.append("- Selecteer 4 keepers")

    if available is not None and keepers is not None:
        if not set(keepers).issubset(set(available)):
            warnings.append("- Een van de geselecteerde keepers is niet aanwezig")

    # Create an list with the index values of keepers
    keeper_idx = [available.index(keeper) for keeper in keepers]

    # Create an list with the index values of available team members
    team_idx = [Team.team_members.index(member) for member in available]

    n_team: int = len(available)  # Number of team members
    n_tasks: int = len(Team.positions_base)  # Number of team positions
    n_subs: int = n_team - n_tasks  # The number of subs

    # Determine the amount of substitutes depending on how many members are available
    positions_sub = ["Wissel" for i in range(1, n_subs + 1)]
    positions = Team.positions_base + positions_sub

    matrix = generate_opstelling(n_team, Team.n_periods, team_idx, keeper_idx, n_subs)

    team_table = create_team_table(matrix, available, positions, Team.n_parts)

    # available_members = available
    # [member for member in Team.team_members if member in available]

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            # "team_header": team_table,
            "team_table": team_table,
            "warnings": warnings,
        },
    )
