from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# # Mount static files (for CSS)
# app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/submit")
async def submit_form(
    request: Request,
    speler: str = Form(...),
    keeper: bool = Form(False),
    aanwezig: bool = Form(True),
):
    return templates.TemplateResponse(
        "result.html",
        {"request": request, "speler": speler, "keeper": keeper, "aanwezig": aanwezig},
    )
