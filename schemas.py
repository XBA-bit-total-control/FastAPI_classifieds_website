from pydantic import BaseModel, Field, field_validator


class AdvertisementsPostInp(BaseModel):
    title: str = Field(min_length=5, max_length=200)
    description: str = Field(min_length=30, max_length=600)
    price: float = Field(ge=0, le=499_999_999)
    autor: str

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
