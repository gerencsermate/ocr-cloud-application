"""Notification sender service"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/api/health")
def health_check():
    """Returns a 200 OK status for health checks."""
    return "OK"
