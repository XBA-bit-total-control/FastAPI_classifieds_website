from pydantic import BaseModel, Field, field_validator
import re


class UsersPostInp(BaseModel):
    name: str = Field(min_length=2, max_length=155)
    surname: str | None = Field(min_length=3, max_length=205, default=None)

    @field_validator('name')
    def name_validator(cls, value):
        exceptions = re.findall(r"\W+", value)
        if exceptions:
            raise ValueError(f"значение 'name' содержит недопустимые символы [ {' '.join(exceptions)} ]")
        return value

    @field_validator('surname')
    def surname_validator(cls, value):
        exceptions = re.findall(r"\W+", value)
        if exceptions:
            raise ValueError(f"значение 'surname' содержит недопустимые символы [ {' '.join(exceptions)} ]")
        return value


class AdvertisementsPostInp(BaseModel):
    title: str = Field(min_length=5, max_length=200)
    description: str = Field(min_length=30, max_length=600)
    price: float = Field(ge=0, le=499_999_999)
    master: int

    @field_validator('price')
    def price_validator(cls, value):
        decimal_places = len(str(value).split(".")[-1])
        if decimal_places > 2:
            raise ValueError(f"Значение поля 'price' после запятой не должно быть больше 2")
        return value


class AdvertisementsPatchInp(BaseModel):
    title: str | None = Field(min_length=5, max_length=200, default=None)
    description: str | None = Field(min_length=30, max_length=600, default=None)
    price: float | None = Field(ge=0, le=499_999_999, default=None)

    @field_validator('price')
    def price_validator(cls, value):
        decimal_places = len(str(value).split(".")[-1])
        if decimal_places > 2:
            raise ValueError(f"Значение поля 'price' после запятой не должно быть больше 2")
        return value
