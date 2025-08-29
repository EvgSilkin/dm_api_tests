from pydantic import BaseModel, Field, ConfigDict


class ResetPassword(BaseModel):
    model_config = ConfigDict(extra="forbid")
    # extra="forbid" - обязтельно ли проверять при сериализации
    login: str = Field(..., description="Логин")
    email: str = Field(..., description="Email")
