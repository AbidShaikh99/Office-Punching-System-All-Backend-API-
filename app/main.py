from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from app.api.auth_routes import auth_router
from app.api.admin_routes import *
from app.api.puch_routes import*
from app.api.report_routes import*
from app.db.database import Base, engine
from app.utils.response import error_response, success_response
from app.config.settings import *

app = FastAPI(title="Company Punching System API")


Base.metadata.create_all(bind=engine)

app.add_exception_handler(
    HTTPException,
    http_exception_handler
)
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,

)


app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(punch_router)
app.include_router(report_router)





