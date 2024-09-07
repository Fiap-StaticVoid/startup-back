from fastapi import HTTPException


class SenhaNaoValida(HTTPException):
    def __init__(self, falhas: list[str]):
        super().__init__(status_code=406, detail={"falhas": falhas})
