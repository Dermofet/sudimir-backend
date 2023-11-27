from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.config import config
from backend.middleware import *
from backend.routers.user import router as user_router
from backend.routers.auth import router as auth_router
from backend.routers.service import router_with_token as service_router_with_token
from backend.routers.service import router_without_token as service_router_without_token
from backend.routers.booking import router as booking_router

tags_metadata = [
    {"name": "auth", "description": "Работа с авторизацией"},
    {"name": "user", "description": "Работа с пользователями"},
    {"name": "service", "description": "Работа с услугами"},
    {"name": "booking", "description": "Работа с бронями"},
]

app = FastAPI(
    debug=config.DEBUG,
    openapi_tags=tags_metadata,
    openapi_url=f"{config.BACKEND_PREFIX}/openapi.json",
    title=config.BACKEND_TITLE,
    description=config.BACKEND_DESCRIPTION,
)

# add_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

app.include_router(user_router, tags=["user"])
app.include_router(auth_router, tags=["auth"])
app.include_router(service_router_with_token, tags=["service"])
app.include_router(service_router_without_token, tags=["service"])
app.include_router(booking_router, tags=["booking"])
