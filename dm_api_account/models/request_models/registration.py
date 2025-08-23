from pydantic import BaseModel, Field, ConfigDict


class Registration(BaseModel):
    model_config = ConfigDict(extra="forbid")
    # extra="forbid" - обязтельно ли проверять при сериализации
    login: str = Field(..., description="Логин")
    password: str = Field(..., description="Пароль")
    email: str = Field(..., description="Email")
