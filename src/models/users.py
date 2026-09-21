from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from sqlalchemy import String, DateTime
from database import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models import RequestBase
class UserBase(Base):

    __tablename__ = 'users' 

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    registrated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    requests: Mapped[List['RequestBase']] = relationship(back_populates="user")

    def __repr__(self):
        return f'User(id={self.id}, username={self.username}, hashed_password={self.hashed_password}, registrated_at={self.registrated_at})'

