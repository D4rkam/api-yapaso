from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import get_db


db_dependency = Annotated[Session, Depends(get_db)]
