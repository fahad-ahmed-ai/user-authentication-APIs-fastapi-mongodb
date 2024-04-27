from .models import User
import bcrypt
from datetime import datetime, timedelta
from bson import ObjectId


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


async def user_exist(email):
    get_user = User.objects(email=email).first()
    if get_user:
        return True
    else:
        return None


async def validate_user(email, password):
    try:
        get_user = User.objects(email=email).first()
        if get_user is None:
            return None
        else:
            stored_hashed_password = get_user.password.encode()

            if bcrypt.checkpw(password.encode("utf-8"), stored_hashed_password):

                is_password_valid = bcrypt.checkpw(
                    password.encode("utf-8"), stored_hashed_password
                )

                if is_password_valid:
                    user_data = {
                        "user_id": str(get_user.id),
                        "email": str(get_user.email),
                        "user_name": str(get_user.user_name),
                        "notified_emails": get_user.notified_emails,
                    }
                    return user_data
                else:
                    return None
            else:
                return None
    except:
        return None


async def store_otp(user_email, otp_digit):
    try:
        get_user = User.objects(email=user_email).first()
        otp_creation_time = datetime.now() + timedelta(minutes=5)
        if get_user:
            get_user.update(otp=otp_digit, otp_creation_time=otp_creation_time)
        else:
            print("No profile found with the given ID.")

    except:
        print("No profile found with the given ID.")


async def get_otp(email):
    try:
        get_user = User.objects(email=email).first()
        if get_user:
            return get_user
        else:
            return None
    except:
        return None


async def get_user_info(email):
    user = User.objects(email=email).first()
    if not user:
        return None
    return str(user.id)


async def update_user_password(email, new_pass):
    user_info = await get_user_info(email)
    if user_info:
        user_id = user_info
        try:
            user = User.objects(id=user_id).first()
            if user:
                hashed_password = hash_password(new_pass)
                user.update(set__password=hashed_password)
                return True
            else:
                return False
        except:
            return False
    else:
        return False


async def change_user_db(user_id, old_password, new_passowrd):
    try:
        get_user = User.objects(id=user_id).first()
        if get_user is None:
            return None
        else:
            stored_hashed_password = get_user.password.encode()

            if bcrypt.checkpw(old_password.encode("utf-8"), stored_hashed_password):

                is_password_valid = bcrypt.checkpw(
                    old_password.encode("utf-8"), stored_hashed_password
                )

                if is_password_valid:
                    get_user.update(set__password=hash_password(new_passowrd))
                    return True
                else:
                    return None
            else:
                return None
    except:
        return None


def validate_user_password(user_id, password):
    try:
        get_user = User.objects(id=user_id).first()
        if get_user is None:
            return None
        else:
            stored_hashed_password = get_user.password.encode()

            if bcrypt.checkpw(password.encode("utf-8"), stored_hashed_password):

                is_password_valid = bcrypt.checkpw(
                    password.encode("utf-8"), stored_hashed_password
                )
                if is_password_valid:
                    return get_user
                else:
                    return None
            else:
                return None
    except:
        return None


async def get_user_by_id(user_id):
    try:
        user = User.objects(id=user_id).first()
        if not user:
            return None
        return user
    except:
        return None