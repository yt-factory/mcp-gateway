from typing import Optional

from pydantic import BaseModel


class MCPResponse(BaseModel):
    success: bool
    error: Optional[str] = None
