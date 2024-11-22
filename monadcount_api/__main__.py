from fastapi import FastAPI
from sentry_sdk.integrations.dramatiq import DramatiqIntegration
from starlette.staticfiles import StaticFiles

from monadcount_api.core import settings
from monadcount_api.components.rest.router import router as rest_router
from monadcount_api.components.homepage.router import router as homepage_router

import sentry_sdk


if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN, traces_sample_rate=1.0, profiles_sample_rate=1.0, integrations=[DramatiqIntegration()]
    )


app = FastAPI(title=settings.NAME, version=settings.VERSION, description=settings.DESCRIPTION)
app.mount("/static", StaticFiles(directory=settings.BASE_DIR / "static"), name="static")
app.include_router(rest_router, prefix="/api/v1")
app.include_router(homepage_router, tags=["Homepage"])
