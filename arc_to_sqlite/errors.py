from pathlib import Path


class ArcToSqliteError(Exception):
    """
    Base class for exceptions in this module.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UpdateOrInsertError(ArcToSqliteError):
    """
    Raised when an update or insert operation fails.
    """


class ArcExportPathNotFoundError(ArcToSqliteError):
    """
    Raised when the Arc export path is not found.
    """


class ArcExportFilesRowFailedError(ArcToSqliteError):
    """
    Raised when a row fails to be inserted into the database.
    """
