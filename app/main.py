from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from app.api.api import api_router
from app.frontend.frontend import frontend_router
from app.utils.robots import robots_router
from app.utils.sitemap import sitemap_router
from app.utils.favicon import favicon_router
from .settings import settings
import anyio
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Iterator
import uvicorn

api_description = """
## Computer Craft - ccTweaked
- [ccTweaked](https://tweaked.cc/)

## API Documentation:
- [Stoplight](https://efficiency-6.soulant.com/api/docs)
- [Swagger UI](https://efficiency-6.soulant.com/api/swagger)
- [ReDoc](https://efficiency-6.soulant.com/api/redoc)
"""


@asynccontextmanager
async def lifespan(app: FastAPI) -> Iterator[None] | AsyncGenerator[Any, Any]:
    """
    Context manager to set the default thread limiter for the application.
    """
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 100
    yield


app = FastAPI(
    title="Gogeloo - Efficiency 6",
    description=api_description,
    version="1.1.0",
    contact={
        "name": "Efficiency 6",
        "url": "https://github.com/Gogeloo",
    },
    docs_url="/api/swagger",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)


app.add_middleware(GZipMiddleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="app/frontend/static"), name="static")
templates = Jinja2Templates(directory="app/frontend/templates")


@app.on_event("startup")
async def startup_event():
    """Startup event for the application."""
    pass


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event for the application."""
    pass


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404 and not request.url.path.startswith("/api"):
        return templates.TemplateResponse("404.html", {"request": request})
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail)},
    )


@app.get("/api/openapi.json", tags=["Documentation Formats"], include_in_schema=False)
async def get_openapi():
    return JSONResponse(app.openapi())


@app.get("/api", include_in_schema=False)
async def api_root():
    return RedirectResponse(url="/api/docs")


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/api/docs")


@app.get("/api/docs", tags=["Documentation Formats"], response_class=HTMLResponse, include_in_schema=False)
async def stoplight() -> HTMLResponse:
    """
    Renders an HTML page with a stoplight using the Stoplight Elements library.
    """
    return HTMLResponse("""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <style>
            html,
            body {
              height: 100%;
            }
          </style>
        <title>LimeTip API</title>

        <script src="https://unpkg.com/@stoplight/elements/web-components.min.js"></script>
        <link rel="stylesheet" href="https://unpkg.com/@stoplight/elements/styles.min.css">
      </head>
      <body>

        <elements-api
          apiDescriptionUrl="openapi.json"
          router="hash"
        />

      </body>
    </html>""")


app.include_router(api_router, prefix="/api/v1")
# app.include_router(frontend_router, tags=["Frontend"])
# app.include_router(robots_router)
# app.include_router(sitemap_router)
# app.include_router(favicon_router)

if __name__ == "__main__":
  # uvicorn.run(app, loop="uvloop")
  pass