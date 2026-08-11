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


class User(Base):
    __tablename__ = 'users'

    name: Mapped[str] = MappedColumn(String(155))
    surname: Mapped[str] = MappedColumn(String(205), nullable=True)

    def id_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname
        }


class Advertisement(Base):
    __tablename__ = 'advertisements'

    title: Mapped[str] = MappedColumn(String(200), unique=True)
    description: Mapped[str] = MappedColumn(String(600))
    price: Mapped[int] = MappedColumn(Numeric(precision=9, scale=2))
    master: Mapped[int] = MappedColumn(Integer, ForeignKey('users.id'))
    created_at: Mapped[datetime] = MappedColumn(DateTime, default=func.now())

    def is_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'master': self.master,
            'created_at': self.created_at
        }


async def open_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()
