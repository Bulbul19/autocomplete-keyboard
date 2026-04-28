from pydantic import BaseModel


class InputRequest(BaseModel):
    text: str
    char: str


class SelectRequest(BaseModel):
    text: str
    word: str
