class PeakFitError(Exception):
    message: str
    status_code: int

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class ItemNotFoundError(PeakFitError):
    def __init__(self, message="El recurso no existe"):
        self.message = message