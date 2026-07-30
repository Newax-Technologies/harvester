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


class RecordAlreadyCanonicalizedError(BaseAPIException):
    def __init__(self, raw_record_id: str):
        super().__init__(
            status_code=409,
            code="already_canonicalized",
            message=(
                "The incoming record for this candidate has already been "
                "canonicalized (via a sibling candidate or automated "
                "resolution) and cannot be decided again."
            ),
            details={"raw_record_id": str(raw_record_id)},
        )


class TargetHasPendingConflictError(BaseAPIException):
    def __init__(self, target_raw_record_id: str):
        super().__init__(
            status_code=409,
            code="target_has_pending_conflict",
            message=(
                "The target record for this decision is itself unresolved and has "
                "its own pending candidate awaiting review. Resolve that candidate "
                "first, or this decision would silently hide it from the review "
                "queue once the target becomes canonicalized."
            ),
            details={"target_raw_record_id": str(target_raw_record_id)},
        )


class DraftBeingSentError(BaseAPIException):
    def __init__(self, draft_id: str):
        super().__init__(
            status_code=409,
            code="draft_being_sent",
            message=(
                "This draft has already been claimed by an outreach send and cannot "
                "be edited or decided on. The automator loaded its current body/"
                "status into memory before this claim; a mutation here would not "
                "change what's actually sent, and could leave the database "
                "recording content different from what was delivered."
            ),
            details={"draft_id": str(draft_id)},
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
