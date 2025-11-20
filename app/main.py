from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routes.pages import router as pages_router

APP_NAME = "anoushka_portfolio"
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Anoushka Rathod Portfolio",
    description=(
        "A FastAPI-powered portfolio highlighting UX case studies, process-centric storytelling, "
        "and playful interactions for interaction designer Anoushka Rathod."
    ),
    version="0.1.0",
)

static_dir = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(pages_router)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    """Return a simple health response for uptime checks."""
    return {"status": "ok"}
