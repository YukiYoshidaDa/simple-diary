class DomainError(Exception):
    """Base class for domain-specific errors."""

    pass


class NotFoundError(DomainError):
    """Requested resource was not found."""

    pass


class ForbiddenError(DomainError):
    """Action is not allowed for the current principal."""

    pass
