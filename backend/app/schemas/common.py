from pydantic import BaseModel


class SuccessResponse(BaseModel):
    """Standard success response format."""
    success: bool = True
    message: str = ""
    data: dict = {}


class ErrorResponse(BaseModel):
    """Standard error response format."""
    success: bool = False
    error_code: str = ""
    message: str = ""
