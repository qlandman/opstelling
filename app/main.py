from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

from fastapi.staticfiles import StaticFiles
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

app = FastAPI(docs_url=None, redoc_url=None)

# Set up Jinja2 templates
templates = Jinja2Templates(directory=f"{dir_path}/templates")

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

# Mount static files (for CSS)
app.mount("/static", StaticFiles(directory=f"{dir_path}/static"), name="static")


@app.get("/")
async def read_form(request: Request):
    return templates.TemplateResponse(
        "form.html", {"request": request, "team_members": team_members}
    )


@app.post("/submit")
async def submit_form(request: Request, available: list[str] = Form(...)):
    available_members = [member for member in team_members if member in available]
    return templates.TemplateResponse(
        "result.html", {"request": request, "available_members": available_members}
    )
