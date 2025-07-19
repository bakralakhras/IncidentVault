import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from routes.health import router as health_router
from routes.report import router as report_router


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] "
                    "%(name)s: %(message)s")
logger = logging.getLogger("incidentvault")

app = FastAPI(title="IncidentVault", version="1.0.0")


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except StarletteHTTPException:
        raise
    except RequestValidationError:
        raise
    except Exception:
        logger.exception(f"Unhandled error on {request.url}")
        return JSONResponse(status_code=500, content={
            "detail": "Internal server error"})


@app.get("/")
async def root():
    return {"message": "first run"}

app.include_router(health_router)
app.include_router(report_router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTP {exc.status_code} on {request.url}: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error on {request.url}: {exc.errors()}")
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error on {request.url}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

instrumentator = Instrumentator()
instrumentator.instrument(app)
instrumentator.expose(app)

for route in app.routes:
    print(f"{route.path} -> {route.name}")
