from typing import List
from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    status,
    UploadFile,
    File,
    Request,
    Form,
    HTTPException,
)

from fastapi.responses import HTMLResponse, RedirectResponse, Response

from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db, configs
from exceptions import InvalidOperationException, BadRequestException

from schemas import AttendeeRead, AttendeeCreate, RequestCreate, AttendeeUpdate
from services import (
    attendee_service,
    request_service,
    country_service,
    document_service,
    user_service,
)

router = APIRouter(prefix="/attendee", tags=["Attendees"])


@router.post("/{attendee_id}/upload-photo/", summary="Upload Image File")
async def upload_attendee_photo(
    attendee_id: str, photo: UploadFile = File(...), db: Session = Depends(get_db)
):
    attendee = await attendee_service.upload_photo(db, attendee_id, photo)
    return attendee


@router.post("/{attendee_id}/upload-photo-scan/", summary="Upload Image File")
async def upload_attendee_photo_scan(
    attendee_id: str, photo: UploadFile = File(...), db: Session = Depends(get_db)
):
    attendee = await attendee_service.upload_photo_scan(db, attendee_id, photo)
    return attendee


@router.get(
    "/all",
    response_model=List[AttendeeRead],
    summary="Get all Attendees by request",
    response_class=HTMLResponse,
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    request: Request,
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends(),
):
    """
    Get all Requests
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = user_service.get_by_id(db, user_id)
    attendees = attendee_service.get_multi(db, skip, limit)
    return configs.templates.TemplateResponse(
        "all_attendees.html", {"request": request, "attendees": attendees, "user": user}
    )


@router.get(
    "/create/event_{event_id}", summary="Create Attendee", response_class=HTMLResponse
)
async def create_attendee_form(
    *,
    db: Session = Depends(get_db),
    request: Request,
    skip: int = 0,
    limit: int = 10,
    event_id: str,
    Authorize: AuthJWT = Depends(),
):
    """
    Create Attendee
    - **name**: required
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    countries = country_service.get_multi(db, skip, limit)
    document_types = document_service.get_multi(db, skip, limit)
    user = Authorize.get_jwt_subject()

    form = RequestCreate(
        event_id=event_id,
        created_by_id=user,
    )

    try:
        user = user_service.get_by_id(db, user_id)
        request_id = request_service.create(db, form)
        db.commit()
        return configs.templates.TemplateResponse(
            "create_attendee.html",
            {
                "request": request,
                "request_id": request_id,
                "user": user,
                "countries": countries,
                "document_types": document_types,
            },
        )
    except Exception as e:
        raise InvalidOperationException(detail=f"Failed to create event: {str(e)}")


@router.post(
    "/create/attendee/request_{req_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Create Attendee",
)
async def create_attendee(
    *,
    db: Session = Depends(get_db),
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
    sex: str = Form(...),
    country_id: str = Form(...),
    doc_type_id: str = Form(...),
    birth_date: date = Form(...),
    doc_begin: date = Form(...),
    doc_end: date = Form(...),
    photo: UploadFile = File(...),
    doc_scan: UploadFile = File(...),
):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = user_service.get_by_id(db, user_id)
    req = request_service.get_by_id(db, req_id)
    event_id = req.events.id
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
        sex=sex,
        country_id=country_id,
        doc_type_id=doc_type_id,
        request_id=req_id,
    )
    try:
        db_obj = attendee_service.create(db, form)
        await attendee_service.upload_photo(db, db_obj.id, photo)
        await attendee_service.upload_doc_scan(db, db_obj.id, doc_scan)
        # db.add(db_obj)
        db.commit()  # Commit the transaction
        return RedirectResponse(
            url=f"/api/client/attendee/create/event_{event_id}/request_{req_id}",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    except BadRequestException as e:
        db.rollback()  # Roll back the transaction on error
        error_message = str(e)
        return configs.templates.TemplateResponse(
            "create_attendee.html",
            {"request": request, "error": error_message, "user": user},
        )


@router.get(
    "/create/event_{event_id}/request_{req_id}",
    summary="Create Attendee",
    response_class=HTMLResponse,
)
async def create_attendee_form_with_request(
    *,
    db: Session = Depends(get_db),
    request: Request,
    skip: int = 0,
    limit: int = 10,
    event_id: str,
    req_id: str,
    Authorize: AuthJWT = Depends(),
):
    """
    Create Attendee
    - **name**: required
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()

    countries = country_service.get_multi(db, skip, limit)
    document_types = document_service.get_multi(db, skip, limit)
    user = Authorize.get_jwt_subject()
    if req_id is None:
        form = RequestCreate(
            event_id=event_id,
            created_by_id=user,
        )

        try:
            user = user_service.get_by_id(db, user_id)
            request_id = request_service.create(db, form)
            db.commit()
            return configs.templates.TemplateResponse(
                "create_attendee.html",
                {
                    "request": request,
                    "request_id": request_id,
                    "user": user,
                    "countries": countries,
                    "document_types": document_types,
                },
            )
        except Exception as e:
            raise InvalidOperationException(detail=f"Failed to create event: {str(e)}")
    else:
        user = user_service.get_by_id(db, user_id)
        request_id = request_service.get_by_id(db, req_id)
        return configs.templates.TemplateResponse(
            "create_attendee.html",
            {
                "request": request,
                "request_id": request_id,
                "user": user,
                "countries": countries,
                "document_types": document_types,
            },
        )


@router.get(
    "/update/attendee_{attendee_id}",
    summary="Update Attendee",
    response_class=HTMLResponse,
)
async def update_attendee_form(
    *,
    db: Session = Depends(get_db),
    request: Request,
    attendee_id: str,
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10,
):
    """
    Update Attendee
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = user_service.get_by_id(db, user_id)
    countries = country_service.get_multi(db, skip, limit)
    document_types = document_service.get_multi(db, skip, limit)
    try:
        attendee = attendee_service.get_by_id(db, attendee_id)
        if not attendee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Attendee not found"
            )

        return configs.templates.TemplateResponse(
            "update_attendee.html",
            {
                "request": request,
                "attendee": attendee,
                "user": user,
                "countries": countries,
                "document_types": document_types,
            },
        )
    except Exception as e:
        raise InvalidOperationException(
            detail=f"Failed to move to update list: {str(e)}"
        )


@router.patch(
    "/update/patch/attendee_{attendee_id}",
    status_code=status.HTTP_200_OK,
    summary="Update Attendee",
)
async def update_attendee(
    *,
    db: Session = Depends(get_db),
    request: Request,
    attendee_id: str,
    surname: str = Form(None),
    firstname: str = Form(None),
    patronymic: str = Form(None),
    post: str = Form(None),
    doc_series: str = Form(None),
    iin: str = Form(None),
    doc_number: str = Form(None),
    doc_issue: str = Form(None),
    visit_object: str = Form(None),
    transcription: str = Form(None),
    sex: str = Form(None),
    country_id: str = Form(None),
    doc_type_id: str = Form(None),
    birth_date: date = Form(None),
    doc_begin: date = Form(None),
    doc_end: date = Form(None),
    photo: UploadFile = File(None),
    doc_scan: UploadFile = File(None),
):
    # Fetch the existing attendee from the database
    attendee = attendee_service.get_by_id(db, attendee_id)
    if not attendee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendee not found",
        )
    updated_data = AttendeeUpdate(
        surname=surname or attendee.surname,
        firstname=firstname or attendee.firstname,
        patronymic=patronymic or attendee.patronymic,
        post=post or attendee.post,
        doc_series=doc_series or attendee.doc_series,
        iin=iin or attendee.iin,
        doc_number=doc_number or attendee.doc_number,
        doc_issue=doc_issue or attendee.doc_issue,
        visit_object=visit_object or attendee.visit_object,
        transcription=transcription or attendee.transcription,
        birth_date=birth_date or attendee.birth_date,
        doc_begin=doc_begin or attendee.doc_begin,
        doc_end=doc_end or attendee.doc_end,
        sex=sex or attendee.sex,
        country_id=country_id or attendee.country_id,
        doc_type_id=doc_type_id or attendee.doc_type_id,
        request_id=attendee.request_id,
    )
    try:
        obj = attendee_service.update(db=db, db_obj=attendee, obj_in=updated_data)
        # Upload new photo and doc_scan if provided
        await attendee_service.upload_photo(db, obj.id, photo)
        await attendee_service.upload_doc_scan(db, obj.id, doc_scan)
        db.commit()
        return RedirectResponse(
            url=f"/api/client/requests/request_{obj.request_id}/attendees",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    except Exception as e:
        raise InvalidOperationException(detail=f"Failed to update attendee: {str(e)}")


@router.delete(
    "/delete/attendee_{attendee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Attendee",
)
async def remove_attendee(
    request: Request,
    attendee_id: str,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_required()
    try:
        # Perform the delete operation
        attendee_service.remove(db, attendee_id)
        db.commit()  # Commit the transaction
        return Response(status_code=status.HTTP_200_OK)
    except BadRequestException:
        db.rollback()  # Roll back the transaction on error
        return configs.templates.TemplateResponse(
            "all_attendees.html",
            {
                "request": request,
            },
        )


@router.post("/reload/", summary="Reload Attendees")
async def reload(request: Request,
                 db: Session = Depends(get_db),
                 skip: int = 0,
                 limit: int = 100,
                 Authorize: AuthJWT = Depends(),
                 ):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = user_service.get_by_id(db, user_id)
    print(user_id)
    print(user)
    # Вызов сервиса для перезагрузки данных
    attendees_count = await attendee_service.reload(db)
    attendees = attendee_service.get_multi(db, skip, limit)
    # Возврат HTML-шаблона с данными
    return configs.templates.TemplateResponse(
        "all_attendees.html", {
        "request": request, "attendees": attendees, "attendees_count": attendees_count, "user": user
        }
    )
