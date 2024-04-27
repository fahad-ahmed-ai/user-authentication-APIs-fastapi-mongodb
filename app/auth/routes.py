from fastapi import APIRouter
from .views import (
    login,
    signup,
    forget_password,
    verify_otp,
    change_password,
    logout,
    reset_user_password,
    delete_user_account,
    verify_token
)

auth_router = APIRouter()


auth_router.post("/login")(login)
auth_router.post("/signup")(signup)
auth_router.post("/logout")(logout)
auth_router.post("/send_otp")(forget_password)
auth_router.post("/verify_otp")(verify_otp)
auth_router.put("/change_password")(change_password)
auth_router.put("/reset_user_password")(reset_user_password)
auth_router.delete("/delete_user_account")(delete_user_account)
auth_router.get("/verify_token")(verify_token)
