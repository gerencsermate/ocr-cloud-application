"""File uploader service"""
import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

NAME = os.getenv("USERNAME", "")

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main HTML page."""
    return templates.TemplateResponse("index.html", {"request": request, "name": NAME})

@app.get("/api/health")
def health_check():
    """Returns a 200 OK status for health checks."""
    return "OK"
