from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.model.api.auth import LoginRequest, RegisterRequest
from app.services.auth import AuthService
from app.utlis.logger import logger

router = APIRouter(tags=["Authentication"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(name="login.html", request=request)


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(name="register.html", request=request)


@router.post("/register")
async def register_action(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    re_password: str = Form(...),
    as_admin: bool = Form(False),
    auth_service: AuthService = Depends(AuthService),
):
    try:
        reg_data = RegisterRequest(
            username=username,
            password=password,
            re_password=re_password,
            as_admin=as_admin,
        )

        token = await auth_service.create_user(
            reg_data.username, reg_data.password, reg_data.as_admin
        )
        res = RedirectResponse(url="/", status_code=303)
        res.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
        return res

    except ValueError as e:
        logger.error("Registration failed: %s", e)
        return templates.TemplateResponse(
            request=request, name="register.html", context={"error": str(e)}
        )


@router.post("/login")
async def login_action(
    request: Request,
    username: str = Form(),
    password: str = Form(),
    auth_service: AuthService = Depends(AuthService),
):
    try:
        login_data = LoginRequest(username=username, password=password)

        token = await auth_service.get_token_for_user(
            login_data.username, login_data.password
        )

        res = RedirectResponse(url="/", status_code=303)
        res.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
        return res

    except ValueError as e:
        return templates.TemplateResponse(
            request=request, name="login.html", context={"error": str(e)}
        )


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)

    response.delete_cookie(key="access_token")

    return response
