from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from config import settings


async def on_not_found(request, exc):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Not found."
    )


async def on_validation_error(request, exc):
    if settings.DEBUG:
        return JSONResponse(
            content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
            status_code=400
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Invalid request data or parameters.'
    )


def init_app() -> FastAPI:
    app = FastAPI(
        debug=settings.DEBUG
    )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        raise exc

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    v1_router = APIRouter(prefix='/api/v1')
    # v1_router.include_router(auth_router)

    app.include_router(v1_router)
    app.exception_handler(RequestValidationError)(on_validation_error)
    # app.exception_handler(DoesNotExists)(on_not_found)

    return app
