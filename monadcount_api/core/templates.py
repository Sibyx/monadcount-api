from fastapi.templating import Jinja2Templates

from monadcount_api.core.conf import settings

templates = Jinja2Templates(
    directory=settings.BASE_DIR / "monadcount_api/templates",
    context_processors=[
        lambda request: {"settings": settings},
    ],
)
