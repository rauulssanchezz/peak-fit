import logging
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from backend.app.errors.exceptions import PeakFitError

logger = logging.getLogger("uvicorn.error")

async def peakfit_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, PeakFitError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.message, 
                "code": "APP_ERROR"
            }
        )
    
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )

async def sqlalchemy_exception_handler(request: Request, exc: Exception):
    logger.error(f"Database Error: {str(exc)}")
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error de comunicación con la base de datos",
            "code": "DB_INTERNAL_ERROR"
        }
    )

def register_error_handlers(app: FastAPI):
    app.add_exception_handler(PeakFitError, peakfit_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)