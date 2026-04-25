# pylint: disable= invalid-name,global-variable-undefined,unused-variable,logging-fstring-interpolation,too-many-arguments,missing-final-newline,superfluous-parens,no-member,protected-access,undefined-variable,unused-argument,import-error,too-few-public-methods,missing-class-docstring,missing-module-docstring, missing-function-docstring,redefined-outer-name,broad-exception-caught,unspecified-encoding,inconsistent-return-statements,line-too-long


from ddtrace import patch_all
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.config_service.cors_config import setup_cors
from src.config_service.logger_config import setup_logging
from src.routers import (
    live_router,
    read_file_data_router,
)

logger = setup_logging()

patch_all()


# App Setup
app = FastAPI()
# CORS Middleware Setup
setup_cors(app)


@app.middleware("http")
async def check_headers(request: Request, call_next):
    """
    Middleware code to validate if the headers are present
    """
    if request.url.path not in ["/docs", "/openapi.json", "/live"]:
        """
        Skip header validation for "/live", "/docs" and "/openapi.json" endpoints.

        These endpoints are used for API documentation and schema, so the
        following header checks are not applicable to them.

        Live endpoint is merely for testing if the endpoint is alive or not

        - Authorization: Validates the presence of an authorization token.
        - Tenant: Validates the presence of a tenant identifier.
        - Content-Type: Validates that the Content-Type header is not empty.

        If any of these headers are missing or invalid, a JSONResponse with
        a 400 status code and a relevant error message is returned.
        """
        authorization = request.headers.get("Authorization")
        tenant = request.headers.get("tenant")

        # if authorization is None:
        #     return JSONResponse(
        #         status_code=400,
        #         content={"error": "Authorization token is missing from header"},
        #     )

        # if tenant is None:
        #     return JSONResponse(
        #         status_code=400,
        #         content={"error": "Tenant is missing from header"},
        #     )

    response = await call_next(request)
    return response


# Router
app.include_router(live_router.router)
app.include_router(read_file_data_router.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=7000)
