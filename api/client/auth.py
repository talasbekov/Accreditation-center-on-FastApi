from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from pydantic import EmailStr
from sqlalchemy.orm import Session

from core import get_db, configs
from exceptions import BadRequestException
from schemas import LoginForm, RegistrationForm
from services import auth_service

import secrets

router = APIRouter(prefix="/auth", tags=["Authorization"])


@router.get("/", response_class=HTMLResponse)
async def get_login_form(request: Request):
    """Возвращает страницу для входа"""
    return configs.templates.TemplateResponse("login_form.html", {"request": request})


@router.post("/login", summary="Login")
async def login(
    request: Request,
    email: EmailStr = Form(...),  # Получаем каждое поле через Form
    password: str = Form(...),
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    form = LoginForm(email=email, password=password)  # Создаем объект модели
    try:
        auth = auth_service.login(form, db, Authorize)
        try:
            Authorize.set_access_cookies(auth["access_token"])
            print(auth['access_token'], "token")
        except Exception as e:
            print(e)
        # Установка токенов в куки для использования в последующих запросах
        response = RedirectResponse(
            url="/api/client/events", status_code=status.HTTP_303_SEE_OTHER
        )
        response.set_cookie(
            key="access_token_cookie",
            value=auth["access_token"],
            httponly=True,
            path="/",
            secure=True,
            samesite="Lax",
        )
        response.set_cookie(
            key="X-CSRF-Token",
            value=secrets.token_urlsafe(),
            httponly=True,
            path="/",
            secure=True,
            samesite="Lax",
        )
        return response
    except BadRequestException as e:
        # В случае ошибки возвращаем пользователя на форму входа с сообщением об ошибке
        return configs.templates.TemplateResponse(
            "login_form.html", {"request": request, "error": str(e)}
        )


# @router.post("/register", summary="Register")
# async def register(form: RegistrationForm, db: Session = Depends(get_db)):


@router.post(
    "/register/user",
    status_code=status.HTTP_201_CREATED,
    summary="Create User",
)
async def create(
    *,
    db: Session = Depends(get_db),
    request: Request,
    name: str = Form(...),
    email: EmailStr = Form(...),
    workplace: str = Form(...),
    iin: int = Form(...),
    phone_number: str = Form(...),
    admin: str = Form(...),
    password: str = Form(),
    re_password: str = Form(),
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_required()
    form = RegistrationForm(
        name=name,
        email=email,
        workplace=workplace,
        iin=iin,
        phone_number=phone_number,
        admin=admin,
        password=password,
        re_password=re_password,
    )
    try:
        db_obj = auth_service.register(db, form)
        db.add(db_obj)
        db.commit()  # Commit the transaction
        return RedirectResponse(
            url="/api/client/events", status_code=status.HTTP_303_SEE_OTHER
        )
    except BadRequestException as e:
        db.rollback()  # Roll back the transaction on error
        error_message = str(e)
        return configs.templates.TemplateResponse(
            "create_user.html",
            {"request": request, "error": error_message},
        )


@router.get("/refresh", dependencies=[Depends(HTTPBearer())])
def refresh_token(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    return auth_service.refresh_token(db, Authorize)


@router.post("/logout")
def logout(request: Request, Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    response = RedirectResponse(
        url="/api/client/auth", status_code=status.HTTP_303_SEE_OTHER
    )
    response.delete_cookie("access_token")
    response.delete_cookie("X-CSRF-Token")
    return response
