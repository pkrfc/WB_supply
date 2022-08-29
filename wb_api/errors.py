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
    def __init__(self, error_id: str, *args: object) -> None:
        """Превышено количество запросов.
        Args:
            error_id (str): Error ID.
        """
        super().__init__(*args)
        self.error_id = error_id
