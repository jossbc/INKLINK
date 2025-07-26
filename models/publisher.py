from  pydantic import BaseModel, Field
from typing import Optional

class Publisher(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB ID - Se genera automáticamente desde el _id de MongoDB, no es necesario enviarlo en POST"
    )

    name: str = Field(
        description="Publishers name",
        pattern= r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Penguin", "Planeta"]
    )