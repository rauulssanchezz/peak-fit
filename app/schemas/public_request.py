from pydantic import BaseModel, Field

class PublicRequest(BaseModel):
    limit: int = Field(20, gt=0, lt=50)
    offset: int = Field(0, ge=0)