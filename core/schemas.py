from pydantic import BaseModel, field_validator


class BasePersonSchema(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("نام نمی‌تواند خالی یا فقط فاصله باشد.")

        if len(value) < 2:
            raise ValueError("طول نام باید حداقل ۲ کاراکتر باشد.")

        return value.title()


class PersonCreateSchema(BasePersonSchema):
    pass


class PersonResponseSchema(BasePersonSchema):
    id: int


class PersonUpdateSchema(BasePersonSchema):
    pass
