from fastapi.responses import JSONResponse


def success_response(msg, data=""):
    response_content = {"error": "", "message": msg, "data": data, "status_code": 200}
    return JSONResponse(content=response_content, status_code=200)


def not_found_response(msg, data=""):
    response_content = {"error": "", "message": msg, "data": data, "status_code": 404}
    return JSONResponse(content=response_content, status_code=404)


def unauthorized_response(msg, data=""):
    response_content = {"error": "", "message": msg, "data": data, "status_code": 401}
    return JSONResponse(content=response_content, status_code=401)


def error_response(msg, exception=None):
    response_content = {
        "error": repr(exception) if exception else "",
        "message": msg,
        "data": "",
        "status_code": 500,
    }
    return JSONResponse(content=response_content, status_code=500)
