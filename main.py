import json
import time
import socket
import logging
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from jwt import InvalidTokenError
from pydantic import ValidationError
from api import router
from core import configs

# Импортируем необходимые классы из fastapi-jwt
from fastapi_jwt import JwtAccessBearer

# Настройка логирования
logg = logging.getLogger(__name__)
socket.setdefaulttimeout(configs.SOCKET_TIMEOUT)
app = FastAPI(
    title=configs.PROJECT_NAME,
    description=configs.DESCRIPTION,
    version=configs.VERSION,
    openapi_url=f"{configs.API_V1_PREFIX}/openapi.json",
    debug=configs.DEBUG,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=configs.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

app.mount("/media", StaticFiles(directory="media"), name="media")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Инициализируем JwtAccessBearer с вашим секретным ключом
jwt_bearer = JwtAccessBearer(secret_key=configs.SECRET_KEY)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    logg.debug(f"Request: {request.method} {request.url} {request.client.host}")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    if isinstance(response, HTMLResponse):
        try:
            # Получаем токен из заголовка Authorization
            token = request.headers.get("Authorization")
            if token and token.startswith("Bearer "):
                token = token[7:]
                # Проверяем токен и получаем данные пользователя
                credentials = jwt_bearer.verify_token(token)
                user_data = {"user_id": credentials.subject, **credentials.claims}
            else:
                user_data = {}
            content = response.body.decode() if isinstance(response.body, bytes) else response.body
            new_content = configs.templates.TemplateResponse(
                "base.html",
                {"request": request, **user_data, "content": content},
            )
            response.body = new_content.body
            response.headers.update(new_content.headers)
        except InvalidTokenError as e:
            logg.error(f"Ошибка проверки токена: {e}")
        except Exception as e:
            logg.error(f"Ошибка при добавлении данных пользователя в ответ: {e}")
    return response

@app.exception_handler(ValidationError)
def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=400, content={"detail": json.loads(exc.json())})

@app.exception_handler(InvalidTokenError)
def invalid_token_error_handler(request: Request, exc: InvalidTokenError):
    return JSONResponse(status_code=401, content={"detail": str(exc)})

# @app.exception_handler(MissingTokenError)
# def missing_token_error_handler(request: Request, exc: MissingTokenError):
#     return JSONResponse(status_code=401, content={"detail": str(exc)})

@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/api/client/auth")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()

        # Получаем токен из заголовков WebSocket
        token = websocket.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            await websocket.close(code=4401)
            return
        token = token[7:]

        # Проверяем токен
        try:
            jwt_bearer.verify_token(token)
        except InvalidTokenError:
            await websocket.close(code=4401)
            return

        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        logg.info("WebSocket отключился")
    except Exception as e:
        logg.error(f"Ошибка в WebSocket: {e}")
        await websocket.close(code=1011)
