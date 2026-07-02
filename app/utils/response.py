from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(message: str, data=None, status_code: int = 200):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": True,
            "message": message,
            "data": jsonable_encoder(data),
        },
    )


def token_response(message: str, access_token: str, user=None):
    return JSONResponse(
        content={
            "status": True,
            "message": message,
            "access_token": access_token,
            "token_type": "bearer",
            "user": jsonable_encoder(user),
        },
    )


def error_response(message: str, status_code: int = 400, data=None):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": False,
            "message": message,
            "data": jsonable_encoder(data),
        },
    )
