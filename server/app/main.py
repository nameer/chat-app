from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, ORJSONResponse
from pydantic import ValidationError

from app import prestart
from app.core.config import settings
from app.deps import get_user
from app.endpoints import auth, chats, users

from . import __version__


@asynccontextmanager
async def lifespan(_: FastAPI):
    prestart.main()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    root_path=settings.ROOT_PREFIX,
    version=__version__,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


# Set all CORS enabled origins
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=",".join(map(str, settings.CORS_ORIGINS)),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.exception_handler(ValidationError)
async def unicorn_exception_handler(_: Request, exc: ValidationError) -> JSONResponse:
    # Why this handler?
    #   Using Pydantic model in query is not supported by FastAPI:
    #   https://github.com/tiangolo/fastapi/discussions/6873#discussioncomment-5132419
    # Reference: https://fastapi.tiangolo.com/tutorial/handling-errors/#use-the-requestvalidationerror-body
    errors = exc.errors()
    for error in errors:
        error.pop("ctx")
        error["loc"] = ("query",) + error["loc"]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": errors}),
    )


@app.get("/")
def root() -> dict:
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}!",
        "version": __version__,
    }


app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(
    users.router,
    prefix="/users",
    dependencies=[Depends(get_user)],
    tags=["User"],
    responses={
        401: {
            "description": "Not authenticated",
            "content": {
                "application/json": {"example": {"detail": "Not authenticated"}}
            },
        },
        403: {
            "description": "Access denied",
            "content": {
                "application/json": {
                    "example": {"detail": "The user does not have enough privileges"}
                }
            },
        },
        404: {
            "description": "Resource not found",
            "content": {
                "application/json": {
                    "example": {"detail": "The requested resource was not found"}
                }
            },
        },
    },
)
app.include_router(
    chats.router,
    prefix="/chats",
    dependencies=[Depends(get_user)],
    tags=["Chat"],
    responses={
        401: {
            "description": "Not authenticated",
            "content": {
                "application/json": {"example": {"detail": "Not authenticated"}}
            },
        },
        403: {
            "description": "Access denied",
            "content": {
                "application/json": {
                    "example": {"detail": "The user does not have enough privileges"}
                }
            },
        },
        404: {
            "description": "Resource not found",
            "content": {
                "application/json": {
                    "example": {"detail": "The requested resource was not found"}
                }
            },
        },
    },
)
