from pydantic import BaseModel, validator
from fastapi import HTTPException
from fastapi import status


class Login(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, email):
        if "@" not in email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email should contain @",
            )
        return email


class Signup(BaseModel):
    user_name : str
    email: str
    password: str
    confirm_password : str


    @validator("email")
    def validate_email(cls, email):
        if "@" not in email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email should contain @",
            )
        return email
    

class Email(BaseModel):
    email: str
    
    @validator("email")
    def validate_email(cls, email):
        if "@" not in email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email should contain @",
            )
        return email
    

class VerifyOTP(BaseModel):
    email: str
    otp: int


class ResetPassword(BaseModel):
    email: str
    password: str
    confirm_password : str



class Update_Profile(BaseModel):
    user_name : str
    email : str
    notified_emails : list


class Password(BaseModel):
    old_password: str
    new_password: str
    confirm_password : str


class Delete_Account(BaseModel):
    password: str
