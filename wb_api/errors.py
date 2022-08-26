class UnexpectedError(BaseException):
    def __init__(self, error_id: str, *args: object) -> None:
        """Неожиданная ошибка.
        Args:
            error_id (str): Error ID.
        """
        super().__init__(*args)
        self.error_id = error_id


class UnauthorizedError(ValueError):
    def __init__(self, error_id: str, *args: object) -> None:
        """Ошибка авторизации.
        Args:
            error_id (str): Error ID.
        """
        super().__init__(*args)
        self.error_id = error_id


class RPSError(BaseException):
    def __init__(self, secs: int, error_id: str, *args: object) -> None:
        """Превышено количество запросов.
        Args:
            secs (int): Retry-After seconds.
            error_id (str): Error ID.
        """
        super().__init__(*args)
        self.secs = round(secs / 1000) + 1
        self.error_id = error_id
