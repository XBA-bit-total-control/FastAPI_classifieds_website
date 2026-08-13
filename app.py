from schemas import AdvertisementsPostInp, AdvertisementsPatchInp
from fastapi import FastAPI, HTTPException, Response
from database import Session, Advertisement
from sqlalchemy import select
from datetime import datetime


app = FastAPI(
    title="Service buy-and-sell Buyalliti",
    description="A service for convenient sale and purchase of all sorts of things",
    version="1.0.0"
)


@app.get(
    path="/advertisement/{advertisement_id}",
    summary="Получить объявление по id"
)
async def get_advertisement_by_id(advertisement_id: int):
    async with Session() as session:
        stml = select(Advertisement).where(Advertisement.id == advertisement_id)
        advertisement = await session.scalar(stml)
        if advertisement:
            return advertisement.to_dict()
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Объявление с id = {advertisement_id} не существует"
            )


@app.get(
    path="/advertisement",
    summary="Получение объявлений по переданным полям"
)
async def get_advertisements_by_fields(
        title: str = None,
        description: str = None,
        price: float = None,
        author: str = None,
        created_at: str = None,
        created_before: str = None,
        created_after: str = None
):
    async with Session() as session:
        stml = select(Advertisement)
        if title:
            stml = stml.where(Advertisement.title.ilike(f"%{title}%"))
        if description:
            stml = stml.where(Advertisement.description.ilike(f"%{description}%"))
        if price:
            stml = stml.where(Advertisement.price == price)
        if author:
            stml = stml.where(Advertisement.author.ilike(f"%{author}%"))
        try:
            if created_at:
                stml = stml.where(Advertisement.created_at == datetime.fromisoformat(created_at))
                if created_before or created_after:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Можно задать точную дату создания или диапазон, но не все вместе"
                    )
            else:
                if created_before:
                    stml = stml.where(Advertisement.created_at <= datetime.fromisoformat(created_before))
                if created_after:
                    stml = stml.where(Advertisement.created_at >= datetime.fromisoformat(created_after))
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Значение для времени указанно не верно - придерживайтесь формата YYYY-MM-DD"
            )

        advertisements = await session.scalars(stml)
        result = [advertisement.to_dict() for advertisement in advertisements]
        if result:
            return result
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Объявлений с такими параметрами не найдено"
            )


@app.post(
    path="/advertisement",
    summary="Создать объявление",
    status_code=201
)
async def create_advertisement(request_data: AdvertisementsPostInp):
    async with Session() as session:

        advertisement = Advertisement(
            title=request_data.title,
            description=request_data.description,
            price=request_data.price,
            author=request_data.author
        )
        session.add(advertisement)
        await session.commit()

        return advertisement.to_dict()


@app.patch(
    path="/advertisement/{advertisement_id}",
    summary="Внести изменение в объявление",
    status_code=200
)
async def change_advertisement(
        advertisement_id: int,
        request_data: AdvertisementsPatchInp
):
    async with Session() as session:
        stml = select(Advertisement).where(Advertisement.id == advertisement_id)
        advertisement = await session.scalar(stml)
        if not advertisement:
            raise HTTPException(
                status_code=404,
                detail=f"Объявления с id = {advertisement_id} не создано"
            )

        request_data = dict(request_data)
        title = request_data.get('title')
        description = request_data.get('description')
        price = request_data.get('price')

        if title:
            advertisement.title = title
        if description:
            advertisement.description = description
        if price:
            advertisement.price = price
        await session.commit()

        return advertisement.to_dict()


@app.delete(
    "/advertisement/{advertisement_id}",
    summary="Удалить объявление"
)
async def delete_advertisement(advertisement_id: int):
    async with Session() as session:
        stml = select(Advertisement).where(Advertisement.id == advertisement_id)
        advertisement = await session.scalar(stml)
        if not advertisement:
            raise HTTPException(
                status_code=404,
                detail=f"Объявление с id = {advertisement_id} не существует"
            )
        await session.delete(advertisement)
        await session.commit()

        return Response(status_code=204)
