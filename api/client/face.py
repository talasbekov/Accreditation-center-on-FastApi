import websockets
import cv2
import face_recognition
from typing import List


from fastapi import Depends, UploadFile, File, APIRouter, status, WebSocket, WebSocketDisconnect

from sqlalchemy.orm import Session
from websockets import InvalidStatusCode

from core import get_db
from schemas import FaceBlackListRead, FaceBlackListCreate, FaceBlackListUpdate
from services import face_service

router = APIRouter(prefix="/face", tags=["Faces"])


@router.post("/{face_id}/upload-face-photo/", summary="Upload Image File")
async def upload_face_photo(
    face_id: str, photo: UploadFile = File(...), db: Session = Depends(get_db)
):
    face = await face_service.upload_face_photo(db, face_id, photo)
    return face


@router.get(
    "",
    response_model=List[FaceBlackListRead],
    summary="Get all Cities",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all FaceBlackLists

    """
    return face_service.get_multi(db, skip, limit)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=FaceBlackListRead,
    summary="Create FaceBlackList",
)
async def create(*, db: Session = Depends(get_db), body: FaceBlackListCreate):
    """
    Create FaceBlackList

    - **name**: required
    """
    return face_service.create(db, body)


@router.get(
    "/{id}/",
    response_model=FaceBlackListRead,
    summary="Get FaceBlackList by id",
)
async def get_by_id(
    *,
    db: Session = Depends(get_db),
    id: str,
):
    """
    Get FaceBlackList by id

    - **id**: UUID - required.
    """

    return face_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
    response_model=FaceBlackListRead,
    summary="Update FaceBlackList",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: FaceBlackListUpdate,
):
    """
    Update FaceBlackList

    """
    return face_service.update(
        db, db_obj=face_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete FaceBlackList",
)
async def delete(
    *,
    db: Session = Depends(get_db),
    id: str,
):
    """
    Delete FaceBlackList

    - **id**: UUId - required
    """

    face_service.remove(db, str(id))


@router.websocket("/ws/video")
async def video_stream(websocket: WebSocket):
    try:
        await websocket.accept()
        cap = cv2.VideoCapture(0)  # Открыть камеру
        if not cap.isOpened():
            print("Ошибка: камера не открылась")
            await websocket.send_json({"error": "Camera not available"})
            await websocket.close(code=1003)  # WebSocket Code: "Unsupported Data"
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Ошибка: кадр не получен")
                break

            # Кодирование кадра в JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            # Отправка кадра клиенту
            await websocket.send_bytes(buffer.tobytes())

    except WebSocketDisconnect:
        print("Клиент отключился")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        await websocket.close(code=1011)  # Код WebSocket: "Internal Error"
    finally:
        if cap.isOpened():
            cap.release()  # Освободить ресурс камеры
            print("Камера освобождена")



@router.websocket("/ws/recognize")
async def recognize_faces(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    cap = cv2.VideoCapture(0)  # Открыть камеру
    try:
        if not cap.isOpened():
            print("Ошибка: камера не открылась")
            await websocket.close(code=1003)
            return
        # Получить закодированные лица из черного списка
        known_encodings = face_service.encode_faces_from_blacklist(db)
        if not known_encodings:
            print("Ошибка: нет данных в черном списке")
            await websocket.send_json({"error": "No faces in blacklist"})
            await websocket.close(code=1003)
            return

        frame_count = 0
        while True:
            frame_count += 1
            ret, frame = cap.read()
            if not ret:
                print("Ошибка: кадр не получен")
                break

            # Обрабатываем каждый 10-й кадр
            if frame_count % 10 != 0:
                await websocket.receive_text()  # Ожидание следующего сообщения
                continue

            rgb_frame = frame[:, :, ::-1]  # Преобразование в RGB
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            matches = [any(face_recognition.compare_faces(known_encodings, enc)) for enc in face_encodings]

            if any(matches):
                await websocket.send_json({"alert": "Person in blacklist detected!"})
            else:
                await websocket.send_json({"status": "No match"})
    except WebSocketDisconnect:
        print("Клиент отключился")
    except Exception as e:
        print(f"Ошибка в процессе распознавания: {e}")
    finally:
        cap.release()
        print("Камера освобождена")



@router.websocket("/ws/check")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        print("Попытка подключения к WebSocket...")
        async with websockets.connect("ws://localhost:8000/face/ws/recognize") as server_socket:
            print("Соединение установлено")
            await server_socket.send("Ping")
            response = await server_socket.recv()
            print("Ответ сервера:", response)
            await websocket.send_text(f"Ответ сервера: {response}")
    except InvalidStatusCode as e:
        print(f"Ошибка подключения: статус {e.status_code}")
        await websocket.send_text(f"Ошибка подключения: статус {e.status_code}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        await websocket.send_text(f"Ошибка подключения: {e}")
    finally:
        await websocket.close()
