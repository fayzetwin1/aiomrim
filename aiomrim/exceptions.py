class APIConnectionError(Exception):
    """Exception raised for errors in the API connection."""
    pass

class APITimeoutError(Exception):
    """Exception raised for API timeout errors."""
    pass

class APIResponseError(Exception):
    """Exception raised for invalid API responses."""
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code
