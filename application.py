from fastapi import FastAPI, Request
from uuid import uuid4
from app.auth.routes import auth_router
from mongoengine import connect
from app.utilities.responses import error_response, success_response
from app.utilities.config import DATABASE_NAME, MONGO_URL
from fastapi.middleware.cors import CORSMiddleware


connect(db=DATABASE_NAME, host=MONGO_URL, tlsAllowInvalidCertificates=True)

application = FastAPI(title="Auth Backend")
application = FastAPI()


application.include_router(auth_router, prefix="/auth", tags=["auth"])



application.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@application.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    return error_response(msg="An unexpected error occurred")


@application.get("/")
def serve():
    return success_response(msg="server is up and running")