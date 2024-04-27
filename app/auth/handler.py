import jwt
from fastapi import Depends, HTTPException, Request, security, status
from app.utilities.config import APP_SECRET_KEY

async def jwt_cookie_token(request: Request):
    token = request.cookies.get("jwt_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing"
        )
    try:
        return jwt.decode(token, APP_SECRET_KEY, algorithms=["HS256"])
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


async def bearer_authorization_token(
    authorization: str = Depends(security.HTTPBearer()),
) -> dict:
    bearer_token = authorization.credentials

    if not bearer_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing"
        )

    try:
        access_token = jwt.decode(
            bearer_token, APP_SECRET_KEY, algorithms=["HS256"]
        )
        sub = jwt.decode(
            access_token["sub"], APP_SECRET_KEY, algorithms=["HS256"]
        )

        return {**access_token, **sub}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired JWT token"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT token"
        )
