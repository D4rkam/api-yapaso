from typing import Annotated
from fastapi import Depends

from app.config import get_settings, Settings

settings_dependency = Annotated[Settings, Depends(get_settings)]
