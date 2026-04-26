

from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.auth import AuthService
from app.services.file import FileService


router = APIRouter(tags=["File Upload"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/upload", response_class=HTMLResponse)
async def login_page(
    request: Request,
    access_token: Annotated[str | None, Cookie()] = None,
    auth_service: AuthService = Depends(AuthService),
    file_service: FileService = Depends(FileService)
):
    try:
        if not access_token:
            raise ValueError("Missing cookie!")

        user_data = auth_service.validate_token(access_token)
        if not user_data:
            raise ValueError("Invalid cookie!")
        
        files = await file_service.list_files_for_user(user_id=user_data.user_id)
    
            
        return templates.TemplateResponse(request=request, name="upload.html", context={
            "files": files
        })
        
    except Exception as e:
        return templates.TemplateResponse(request=request ,name="upload.html", context={
            "error": str(e)
        })

@router.post("/upload")
async def handle_upload(
    request: Request, 
    file: UploadFile = File(),
    description: str = Form(),
    access_token: Annotated[str | None, Cookie()] = None,
    auth_service: AuthService = Depends(AuthService),
    file_service: FileService = Depends(FileService)
):
    try:
        if not access_token:
            raise ValueError("Missing cookie!")

        user_data = auth_service.validate_token(access_token)
        if not user_data:
            raise ValueError("Invalid cookie!")
        
        await file_service.upload_file(uploaded_filename=file.filename,file=file.file, uploader_id=user_data.user_id, description=description)
        
        return RedirectResponse(
            url="/upload", 
            status_code=303
        )
        
    except Exception as e:
        return templates.TemplateResponse(request=request ,name="upload.html", context={
            "error": str(e)
        })