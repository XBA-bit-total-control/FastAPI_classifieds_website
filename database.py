from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy import Integer, String, DateTime, Numeric, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, MappedColumn, Mapped
from dotenv import load_dotenv
from datetime import datetime

import os


load_dotenv()

DNS = (f"{os.getenv("POSTGRES_DRIVER")}://{os.getenv("POSTGRES_USER")}:"
       f"{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:"
       f"{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}")

engine = create_async_engine(DNS)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    id: Mapped[int] = MappedColumn(Integer, primary_key=True)


class Advertisement(Base):
    __tablename__ = 'advertisements'

    title: Mapped[str] = MappedColumn(String(200), nullable=False)
    description: Mapped[str] = MappedColumn(String(600), nullable=False)
    price: Mapped[float] = MappedColumn(Numeric(precision=11, scale=2), nullable=False)
    autor: Mapped[str] = MappedColumn(String(100), nullable=False)
    created_at: Mapped[datetime] = MappedColumn(DateTime, default=func.now(), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'master': self.autor,
            'created_at': self.created_at.isoformat()
        }


async def open_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()
