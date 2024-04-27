import json
import random
from fastapi import Depends, HTTPException, Request
from .handler import jwt_cookie_token
from .schemas import (
    Login,
    Signup,
    Email,
    VerifyOTP,
    ResetPassword,
    Password,
    Delete_Account,
)
from .db import (
    validate_user,
    user_exist,
    store_otp,
    get_otp,
    get_user_info,
    update_user_password,
    change_user_db,
    validate_user_password,
)
import jwt
from .models import User
from app.utilities.config import APP_SECRET_KEY
from app.utilities.responses import (
    success_response,
    not_found_response,
    error_response,
    unauthorized_response,
)
from datetime import datetime, timezone, timedelta
from .db import hash_password
import sentry_sdk
from fastapi import Response
from .utils import Send_OTP
from .db import get_user_by_id


async def login(_schema: Login):
    try:
        email = _schema.email.lower()
        user_info = await validate_user(email, _schema.password)
        if user_info is None:
            return not_found_response(msg="Email & Password is Invalid")

        user_data = {
            "user_id": user_info["user_id"],
        }
        id_token = jwt.encode(user_data, APP_SECRET_KEY, algorithm="HS256")

        response = success_response(
            msg="Authorized",
            data={"user_data": user_info, "jwt_token": id_token},
        )

        expiration_date = datetime.now(timezone.utc) + timedelta(days=7)

        response.set_cookie(
            key="jwt_token",
            value=id_token,
            expires=expiration_date,
            samesite="none",
            secure=True,
        )
        return response

    except Exception as e:
        return error_response(msg="Failed", exception=e)


async def signup(_schema: Signup):
    try:
        email = _schema.email.lower()
        user_info = await user_exist(email)
        if _schema.password != _schema.confirm_password:
            return unauthorized_response(
                msg="Password and Confirm Password should be same"
            )
        if user_info is not None:
            return unauthorized_response(msg="User Already Exists")
        else:
            user = User(
                user_name=_schema.user_name,
                email=_schema.email,
                password=hash_password(_schema.password),
            )
            user.save()

            user_data = {
                "user_id": str(user.id),
            }

            id_token = jwt.encode(user_data, APP_SECRET_KEY, algorithm="HS256")

            response = success_response(
                msg="User Created Successfully",
                data={
                    "user_id": str(user.id),
                },
            )

            expiration_date = datetime.now(timezone.utc) + timedelta(days=7)

            response.set_cookie(
                key="jwt_token", value=id_token, expires=expiration_date
            )
            return response

    except Exception as e:
        return error_response(msg="Failed", exception=e)


def logout():
    try:
        response = Response(
            content=json.dumps({"message": "Logged out"}), media_type="application/json"
        )
        response.delete_cookie(key="jwt_token", samesite="none", secure=True)
        return response

    except Exception as e:
        sentry_sdk.capture_exception(e)
        return error_response(message="Failed", exception=e)


async def forget_password(schema: Email):
    try:
        user_email = schema.email.lower()
        user_info = await user_exist(user_email)
        if user_info is None:
            return not_found_response(msg="Email Not Found")
        otp_code = random.randint(10000, 99999)

        # response = send_email(
        #     recipient=user_email,
        #     subject="Password Reset Request",
        #     otp_code = otp_code
        # )

        response = Send_OTP(user_email, otp_code)
        await store_otp(user_email, otp_code)
        return response

    except Exception as e:
        return error_response(msg="Failed", exception=e)


async def verify_otp(_schema: VerifyOTP):
    try:
        email = _schema.email.lower()
        otp = _schema.otp
        current_time = datetime.now()
        profile_otp = await get_otp(email)
        if profile_otp:
            if (
                int(otp) == int(profile_otp.otp)
                and current_time < profile_otp.otp_creation_time
            ):
                return success_response(msg="verified")
            else:
                return success_response(msg="not verified")
        else:
            return unauthorized_response(msg="Unknown Error")
    except Exception as e:
        return error_response(msg="Failed", exception=e)


async def change_password(_schema: ResetPassword):
    try:
        email = _schema.email
        email = email.lower()
        new_pass = _schema.password

        if _schema.password != _schema.confirm_password:
            return unauthorized_response(
                msg="Password and Confirm Password should be same"
            )

        get_info = await get_user_info(email)

        if get_info:
            res = await update_user_password(email, new_pass)
            if res:
                return success_response(msg="Password Updated")
            else:
                return unauthorized_response(msg="Password Update Failed")
        else:
            return unauthorized_response(msg="Password Update Failed")

    except Exception as e:
        return error_response(msg="Failed", exception=e)


async def reset_user_password(_schema: Password, user: str = Depends(jwt_cookie_token)):
    try:

        if _schema.new_password != _schema.confirm_password:
            return unauthorized_response(
                msg="Password and Confirm Password should be same"
            )

        user_info = await change_user_db(
            user["user_id"], _schema.old_password, _schema.new_password
        )

        if user_info is True:
            return success_response(msg="Password Changed")

        else:
            return unauthorized_response(msg="Old Password is Incorrect")

    except Exception as e:
        return error_response(msg="Failed", exception=e)


async def delete_user_account(
    _schema: Delete_Account, user: str = Depends(jwt_cookie_token)
):
    try:
        get_user_query = validate_user_password(user["user_id"], _schema.password)
        if get_user_query is None:
            return unauthorized_response(msg="Password is Incorrect")
        else:
            get_user_query.delete()
            return success_response(msg="User Deleted Successfully")
    except Exception as e:
        return error_response(msg="Failed", exception=e)


async def verify_token(request: Request):
    try:
        jwt_token = request.cookies.get("jwt_token")
        decoded_token = jwt.decode(jwt_token, APP_SECRET_KEY, algorithms=["HS256"])
        get_user = await get_user_by_id(decoded_token["user_id"])
        user_dict = {
            "user_data": {
                "user_id": str(get_user.id),
                "email": get_user.email,
                "user_name": get_user.user_name,
                "notified_emails": get_user.notified_emails,
            },
        }
        return success_response(msg="Token is Valid", data=user_dict)
    except Exception as e:
        return error_response(msg="Token is Invalid", exception=e)
