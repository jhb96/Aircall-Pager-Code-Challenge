
from pydantic import BaseModel

class Alert(BaseModel):
    service_id: str
    message: str
