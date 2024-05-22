from typing import List
from datetime import date

from fastapi import APIRouter, Depends, status, UploadFile, File, Request, Form

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db, configs
from exceptions import InvalidOperationException, BadRequestException

from schemas import AttendeeRead, AttendeeCreate, RequestCreate
from services import attendee_service, request_service, sex_service, country_service, document_service

router = APIRouter(
    prefix="/attendee", tags=["Attendees"]
)

templates = Jinja2Templates(directory='templates')


@router.post("/{attendee_id}/upload-photo/",
             summary="Upload Image File")
async def upload_attendee_photo(
    attendee_id: str,
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    attendee = await attendee_service.upload_photo(db, attendee_id, photo)
    return attendee


@router.post("/{attendee_id}/upload-photo-scan/",
             summary="Upload Image File")
async def upload_attendee_photo_scan(
    attendee_id: str,
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    attendee = await attendee_service.upload_photo_scan(db, attendee_id, photo)
    return attendee


@router.get(
    "/all",
    response_model=List[AttendeeRead],
    summary="Get all Attendees by request",
    response_class=HTMLResponse
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    request: Request,
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
    Get all Requests
    """
    Authorize.jwt_required()
    user_email = Authorize.get_raw_jwt()['email']
    attendees = attendee_service.get_multi(db, skip, limit)
    return configs.templates.TemplateResponse(
        "all_attendees.html",
        {
            "request": request,
            "attendees": attendees,
            "user_email": user_email
        }
    )


@router.get(
    "/create/event_{event_id}",
    summary="Create Attendee",
    response_class=HTMLResponse
)
async def create_attendee_form(
    *,
    db: Session = Depends(get_db),
    request: Request,
    skip: int = 0,
    limit: int = 10,
    event_id: str,
    Authorize: AuthJWT = Depends()
):
    """
    Create Attendee
    - **name**: required
    """
    Authorize.jwt_required()
    user_email = Authorize.get_raw_jwt()['email']
    sexes = sex_service.get_multi(db, skip, limit)
    countries = country_service.get_multi(db, skip, limit)
    document_types = document_service.get_multi(db, skip, limit)
    user = Authorize.get_jwt_subject()

    form = RequestCreate(
        event_id=event_id,
        created_by_id=user,
    )

    try:
        request_id = request_service.create(db, form)
        db.commit()
        return configs.templates.TemplateResponse(
            "create_attendee.html",
            {
                "request": request,
                "request_id": request_id,
                "user_email": user_email,
                "sexes": sexes,
                "countries": countries,
                "document_types": document_types,
            }
        )
    except Exception as e:
        raise InvalidOperationException(
            detail=f"Failed to create event: {str(e)}"
        )


@router.post(
    "/create/attendee/request_{req_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Create Attendee",
)
async def create_attendee(
    *, db: Session = Depends(get_db),
    request: Request,
    Authorize: AuthJWT = Depends(),
    req_id: str,
    surname: str = Form(...),
    firstname: str = Form(...),
    patronymic: str = Form(...),
    post: str = Form(...),
    doc_series: str = Form(...),
    iin: str = Form(...),
    doc_number: str = Form(...),
    doc_issue: str = Form(...),
    visit_object: str = Form(...),
    transcription: str = Form(...),
    sex_id: str = Form(...),
    country_id: str = Form(...),
    doc_type_id: str = Form(...),
    birth_date: date = Form(...),
    doc_begin: date = Form(...),
    doc_end: date = Form(...),
    photo: UploadFile = File(...),
    doc_scan: UploadFile = File(...),
):
    Authorize.jwt_required()
    user_email = Authorize.get_raw_jwt()['email']
    req = request_service.get_by_id(db, req_id)
    event_id = req.events.id
    print(event_id)
    form = AttendeeCreate(
        surname=surname,
        firstname=firstname,
        patronymic=patronymic,
        post=post,
        doc_series=doc_series,
        iin=iin,
        doc_number=doc_number,
        doc_issue=doc_issue,
        visit_object=visit_object,
        transcription=transcription,
        birth_date=birth_date,
        doc_begin=doc_begin,
        doc_end=doc_end,
        photo=None,
        doc_scan=None,
        sex_id=sex_id,
        country_id=country_id,
        doc_type_id=doc_type_id,
        request_id=req_id
    )
    try:
        db_obj = attendee_service.create(db, form)
        await attendee_service.upload_photo(db, db_obj.id, photo)
        await attendee_service.upload_doc_scan(db, db_obj.id, doc_scan)
        # db.add(db_obj)
        db.commit()  # Commit the transaction
        return RedirectResponse(
            url=f"/api/client/attendee/create/event_{event_id}/request_{req_id}", status_code=status.HTTP_303_SEE_OTHER
        )
    except BadRequestException as e:
        db.rollback()  # Roll back the transaction on error
        error_message = str(e)
        return configs.templates.TemplateResponse(
            "create_attendee.html", {
                "request": request,
                "error": error_message,
                "user_email": user_email
            }
        )


@router.get(
    "/create/event_{event_id}/request_{req_id}",
    summary="Create Attendee",
    response_class=HTMLResponse
)
async def create_attendee_form_with_request(
    *,
    db: Session = Depends(get_db),
    request: Request,
    skip: int = 0,
    limit: int = 10,
    event_id: str,
    req_id: str,
    Authorize: AuthJWT = Depends()
):
    """
    Create Attendee
    - **name**: required
    """
    Authorize.jwt_required()
    user_email = Authorize.get_raw_jwt()['email']
    sexes = sex_service.get_multi(db, skip, limit)
    countries = country_service.get_multi(db, skip, limit)
    document_types = document_service.get_multi(db, skip, limit)
    user = Authorize.get_jwt_subject()
    print(req_id)
    if req_id is None:
        form = RequestCreate(
            event_id=event_id,
            created_by_id=user,
        )

        try:
            request_id = request_service.create(db, form)
            db.commit()
            return configs.templates.TemplateResponse(
                "create_attendee.html",
                {
                    "request": request,
                    "request_id": request_id,
                    "user_email": user_email,
                    "sexes": sexes,
                    "countries": countries,
                    "document_types": document_types,
                }
            )
        except Exception as e:
            raise InvalidOperationException(
                detail=f"Failed to create event: {str(e)}"
            )
    else:
        request_id = request_service.get_by_id(db, req_id)
        print(request_id)
        return configs.templates.TemplateResponse(
            "create_attendee.html",
            {
                "request": request,
                "request_id": request_id,
                "user_email": user_email,
                "sexes": sexes,
                "countries": countries,
                "document_types": document_types,
            }
        )
