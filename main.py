from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# from app.api.api_v1.api import api_router
from app.core.config import settings
from app.api.v1.api import api_router

app = FastAPI(
    title=settings.app_name, openapi_url=f"{settings.api_str}/openapi.json"
)

# Set all CORS enabled origins
if settings.backend_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.backend_cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.api_str)