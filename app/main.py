import logging.config
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from app.routes.client_routes import router as client_router
from app.routes.project_routes import router as project_router
from app.routes.activity_routes import router as activity_router

from app.core.database import Base, engine

from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(client_router)
app.include_router(project_router)
app.include_router(activity_router)




@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

tags_metadata = [
    {
        "name": "Clients",
        "description": "Client management",
    },
    {
        "name": "Projects",
        "description": "Management of projects associated with clients",
    },
    {
        "name": "Activities",
        "description": "Recording and querying activities in projects",
    },
]

app.openapi_tags = tags_metadata


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "API Key para autenticação. Use: dev_api_key_super_secret"
        }
    }

    openapi_schema["security"] = [{"ApiKeyAuth": []}]

    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"ApiKeyAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - API Documentation",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
    )


@app.get("/", tags=["Root"])
def read_root():
    """
    Root route of the API.

    Returns a welcome message.
    """
    return {"message": "Welcome to TaskFlow Manager! Access /docs for API documentation."}
