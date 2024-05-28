from typing import List

from fastapi import APIRouter, Depends, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_jwt_auth import AuthJWT

from sqlalchemy.orm import Session
from pydantic import EmailStr

from core import get_db, configs
from exceptions import InvalidOperationException, BadRequestException

from schemas import UserRead, UserUpdate, UserCreate
from services import user_service, event_service
router = APIRouter(
    prefix="/users", tags=["Users"]
)


@router.get(
    "",
    response_model=List[UserRead],
    summary="Get all Users",
    response_class=HTMLResponse
)
async def get_all(
    request: Request,
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    Authorize: AuthJWT = Depends()
):
    """
    Get all Events
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = user_service.get_by_id(db, user_id)
    users = user_service.get_multi(db, skip, limit)
    return configs.templates.TemplateResponse(
        "users.html",
        {
            "request": request,
            "users": users,
            "user": user,
        }
    )


@router.get(
    "/create",
    response_model=UserRead,
    summary="Create User",
    response_class=HTMLResponse
)
async def create_form(
    *,
    request: Request,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    """
    Create Event
    - **name**: required
    """
    Authorize.jwt_required()
    events = event_service.get_multi(db)
    try:
        return configs.templates.TemplateResponse(
            "create_user.html",
            {
                "request": request,
                "events": events
            }
        )
    except Exception as e:
        raise InvalidOperationException(
            detail=f"Failed to create event: {str(e)}"
        )


@router.post(
    "/create/user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,
    summary="Create User",
)
async def create(
    *, db: Session = Depends(get_db),
    request: Request,
    Authorize: AuthJWT = Depends(),
    name: str = Form(...),
    email: EmailStr = Form(...),
    workplace: str = Form(...),
    iin: int = Form(...),
    phone_number: str = Form(...),
    admin: str = Form(...),
    password: str = Form(),
    re_password: str = Form()
):
    Authorize.jwt_required()
    # not None
    form = UserCreate(
        name=name,
        email=email,
        workplace=workplace,
        iin=iin,
        phone_number=phone_number,
        admin=admin,
        password=password,
        re_password=re_password
    )
    print(form)
    try:
        db_obj = user_service.create(db, form)
        db.add(db_obj)
        db.commit()  # Commit the transaction
        return RedirectResponse(url="/api/client/users", status_code=status.HTTP_303_SEE_OTHER)
    except BadRequestException as e:
        db.rollback()  # Roll back the transaction on error
        return configs.templates.TemplateResponse("create_event.html", {"request": request, "error": str(e)})


@router.get(
    "/{id}/",
    summary="Get User's data",
    response_class=HTMLResponse
)
async def get_data_of_user(
    *, request: Request, Authorize: AuthJWT = Depends()
):
    """
    Get User by id

    - **id**: UUID - required.
    """
    Authorize.jwt_required()
    user = Authorize.get_jwt_subject()
    user_email = Authorize.get_raw_jwt()['email']
    print(user_email)
    return configs.templates.TemplateResponse("base.html",
                                              {"request": request, "user": user, "user_email": user_email})


@router.put(
    "/{id}/",
    response_model=UserRead,
    summary="Update User",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: UserUpdate,
    Authorize: AuthJWT = Depends()
):
    """
    Update User

    """
    Authorize.jwt_required()
    return user_service.update(
        db, db_obj=user_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete User",
)
async def delete(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Delete User

    - **id**: UUId - required
    """
    Authorize.jwt_required()
    user_service.remove(db, str(id))
