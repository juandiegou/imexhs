# FastAPI application with CRUD operations using PostgreSQL

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from .routers.data_router import router as data_router
from .routers.device_router import router as device_router

app = FastAPI(debug=True)

app.include_router(data_router)
app.include_router(device_router)


# manage all exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc):
    """
    Handle HTTP exceptions and return a JSON response.

    Parameters:
    - _: The request object (not used).
    - exc: The HTTPException instance.

    Returns:
    - JSONResponse: A JSON response with the error detail and status code.
    """
    return JSONResponse(
        content={"error": exc.detail},
        status_code=exc.status_code
    )
    
