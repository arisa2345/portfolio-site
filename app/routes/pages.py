from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
DATA_DIR = BASE_DIR / "data"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@lru_cache(maxsize=1)
def load_json(file_name: str) -> list[dict[str, Any]]:
    """Load shared JSON fixtures for starter content."""
    file_path = DATA_DIR / file_name
    if not file_path.exists():
        return []
    return json_load(file_path)


def json_load(path: Path) -> list[dict[str, Any]]:
    """Wrapper around JSON parsing so it can be mocked easily later."""
    import json

    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    case_studies = load_json("case_studies.json")[:3]
    experience = load_json("experience.json")[:3]
    experiments = load_json("experiments.json")[:4]
    context = {
        "request": request,
        "case_studies": case_studies,
        "experience": experience,
        "experiments": experiments,
    }
    return templates.TemplateResponse("home.html", context)


@router.get("/work", response_class=HTMLResponse)
async def work(request: Request) -> HTMLResponse:
    context = {"request": request, "case_studies": load_json("case_studies.json")}
    return templates.TemplateResponse("work.html", context)


@router.get("/work/{slug}", response_class=HTMLResponse)
async def case_study(request: Request, slug: str) -> HTMLResponse:
    case_studies = load_json("case_studies.json")
    case = next((item for item in case_studies if item["slug"] == slug), None)
    if case is None:
        raise HTTPException(status_code=404, detail="Case study not found")
    context = {"request": request, "case": case}
    return templates.TemplateResponse("case_study.html", context)


@router.get("/experience", response_class=HTMLResponse)
async def experience(request: Request) -> HTMLResponse:
    context = {"request": request, "experience": load_json("experience.json")}
    return templates.TemplateResponse("experience.html", context)


@router.get("/playground", response_class=HTMLResponse)
async def playground(request: Request) -> HTMLResponse:
    context = {"request": request, "experiments": load_json("experiments.json")}
    return templates.TemplateResponse("playground.html", context)


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request) -> HTMLResponse:
    context = {"request": request, "bio": load_json("bio.json")}
    return templates.TemplateResponse("about.html", context)


@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request) -> HTMLResponse:
    context = {"request": request}
    return templates.TemplateResponse("contact.html", context)
