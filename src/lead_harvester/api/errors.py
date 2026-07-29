import uuid
from typing import Any


class BaseAPIException(Exception):
    def __init__(
        self, status_code: int, code: str, message: str, details: dict[str, Any] | None = None
    ):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details or {}
        self.request_id = f"req_{uuid.uuid4().hex[:12]}"


class StaleDataError(BaseAPIException):
    def __init__(self, resource_id: str, expected_version: int, current_version: int):
        super().__init__(
            status_code=409,
            code="stale_resource",
            message="This resource was modified by another reviewer.",
            details={
                "resource_id": str(resource_id),
                "expected_version": expected_version,
                "current_version": current_version,
            },
        )


class AlreadyReviewedError(BaseAPIException):
    def __init__(self, resource_id: str, review_outcome: str):
        super().__init__(
            status_code=409,
            code="already_reviewed",
            message="This resource has already been reviewed and cannot be decided again.",
            details={"resource_id": str(resource_id), "review_outcome": review_outcome},
        )


class ResourceNotFoundError(BaseAPIException):
    def __init__(self, resource_id: str = "unknown"):
        super().__init__(
            status_code=404,
            code="resource_not_found",
            message="The requested resource was not found.",
            details={"resource_id": str(resource_id)},
        )


class AuthorizationError(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=403,
            code="permission_denied",
            message="You do not have permission to perform this action.",
        )


class AuthenticationError(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=401,
            code="not_authenticated",
            message="Valid authentication credentials are required.",
        )
