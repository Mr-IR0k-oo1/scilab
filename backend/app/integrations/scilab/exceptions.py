class ScilabException(Exception):
    """Base exception for all Scilab integration errors."""
    pass


class ScilabNotFoundException(ScilabException):
    """Raised when Scilab binary executable cannot be located."""
    pass


class ScilabExecutionTimeoutException(ScilabException):
    """Raised when command or script execution times out."""
    def __init__(self, execution_id: str, timeout_seconds: float):
        self.execution_id = execution_id
        self.timeout_seconds = timeout_seconds
        super().__init__(f"Execution '{execution_id}' timed out after {timeout_seconds}s")


class ScilabSecurityException(ScilabException):
    """Raised when a path traversal or unapproved script path execution is attempted."""
    pass


class ScilabSessionStateError(ScilabException):
    """Raised when an invalid session state transition is attempted."""
    pass


class ScilabMaxOutputExceededException(ScilabException):
    """Raised when output exceeds configured maximum byte threshold."""
    pass
