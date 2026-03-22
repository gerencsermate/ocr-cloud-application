"""File uploader service"""
import os

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

NAME = os.getenv("USERNAME", "")

TEMPLATE_FOLDER = Path(__file__).parent / "templates"

app = FastAPI()

templates = Jinja2Templates(directory=str(TEMPLATE_FOLDER))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main HTML page."""
    return templates.TemplateResponse(name="index.html", request=request, context={"name": NAME})

@app.get("/api/health")
def health_check():
    """Returns a 200 OK status for health checks."""
    return "OK"
