from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator


class BasePersonSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description="Enter person name")

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("نام نمی‌تواند خالی یا فقط فاصله باشد.")

        if len(value) < 2:
            raise ValueError("طول نام باید حداقل ۲ کاراکتر باشد.")

        return value.title()

    @field_serializer("name" , mode="plain")
    def serialize_name(value):
        return value.title()


class PersonCreateSchema(BasePersonSchema):
    pass


class PersonResponseSchema(BasePersonSchema):
    id: int = Field(... , description="Unique user identifier")


class PersonUpdateSchema(BasePersonSchema):
    pass
