from  pydantic import BaseModel, Field
from typing import Optional

class Author(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB ID - Se genera automáticamente desde el _id de MongoDB, no es necesario enviarlo en POST"
    )

    name: str = Field(
        description="Author First Name",
        pattern= r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Ali", "Jose"]
    )

    lastname: str = Field(
        description="Author Last Name",
        pattern= r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Hazelwood", "Vargas Llosa"]
    )