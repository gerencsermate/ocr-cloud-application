from contextlib import asynccontextmanager
import dotenv
from fastapi import FastAPI


from app.utils.config import init_config
from app.utils.logger import init_logger
from app.api.ocr import router as ocr_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    dotenv.load_dotenv()

    init_config()
    init_logger()

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(ocr_router)


@app.get("/api/health")
def health_check():
    """Returns a 200 OK status for health checks."""
    return "OK"
