import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from .config import Team
from .opstelling import generate_opstelling, create_team_table

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
    keeper_p1: str | None = Form(None),  # Made optional to check explicitly
    keeper_p2: str | None = Form(None),  # Made optional to check explicitly
    keeper_p3: str | None = Form(None),  # Made optional to check explicitly
    keeper_p4: str | None = Form(None),  # Made optional to check explicitly
):
    # List that holds warnings
    warnings: list[str] = []
    # Check the input form data
    if available is None or len(available) < 6:
        warnings.append("- Selecteer minimaal 6 spelers")

    # Collect period keepers
    period_keepers = [keeper_p1, keeper_p2, keeper_p3, keeper_p4]

    # Check if a keeper is selected for each period
    if None in period_keepers:
        warnings.append("- Selecteer een keeper voor elke periode")

    # Check if selected keepers are available (only if all keepers were selected)
    elif available is not None:
        unavailable_keepers = [k for k in period_keepers if k not in available]
        if unavailable_keepers:
            warnings.append(
                f"- De volgende geselecteerde keepers zijn niet aanwezig: {', '.join(unavailable_keepers)}"
            )

    if len(warnings) == 0:
        # Create a list with the index values of period keepers
        keeper_indices = [Team.team_members.index(k) for k in period_keepers]
        # Create a list with the index values of available team members
        team_idx = [Team.team_members.index(member) for member in available]
        n_team: int = len(available)  # Number of team members
        n_tasks: int = len(Team.positions_base)  # Number of team positions
        n_subs: int = n_team - n_tasks  # The number of subs

        # Determine the amount of substitutes depending on how many members are available
        positions_sub = ["Wissel" for i in range(1, n_subs + 1)]
        positions = Team.positions_base + positions_sub

        matrix = generate_opstelling(
            n_team, Team.n_periods, team_idx, keeper_indices, n_subs
        )
        team_table: list = create_team_table(
            matrix, Team.team_members, positions, Team.n_parts
        )
    else:
        team_table = []

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            # "team_header": team_table,
            "team_table": team_table,
            "warnings": warnings,
        },
    )


@app.get("/health")
async def health_check():
    """
    Simple health check endpoint, returning a JSONResponse with a status of "OK"
    and a HTTP status code of 200.
    """
    return JSONResponse(content={"status": "OK"}, status_code=200)
