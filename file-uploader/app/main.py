from contextlib import asynccontextmanager
from beanie import init_beanie
import dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates

from app.api.auth_router import router as auth_router
from app.utlis.config import init_config
from app.utlis.logger import init_logger
from app.utlis.database import Database
from app.services.auth import AuthService
from app.model.db.user import User
from app.utlis.config import get_configuration


@asynccontextmanager
async def lifespan(app: FastAPI):
    dotenv.load_dotenv()

    init_config()
    init_logger()

    db = Database()
    await db.initialize()
    
    yield  
    
    db.close()

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="app/templates")
app.include_router(auth_router)

@app.get("/")
async def index(request: Request, auth_service: AuthService = Depends(AuthService)):
    token = request.cookies.get("access_token")
    user_data = None
    if token:
        user_data = auth_service.validate_token(token)
    
    return templates.TemplateResponse(request=request, name="index.html", context={
        "user": user_data
    })