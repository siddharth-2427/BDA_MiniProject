from fastapi import HTTPException, status

class PipelineConflictError(HTTPException):
    def __init__(self, detail: str = "Pipeline run is already in progress."):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class DatasetValidationError(HTTPException):
    def __init__(self, errors: list):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Dataset validation failed", "errors": errors}
        )

class ResourceNotFoundError(HTTPException):
    def __init__(self, resource_name: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource_name} not found."
        )
