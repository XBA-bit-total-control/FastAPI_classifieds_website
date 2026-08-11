from schemas import UsersPostInp, AdvertisementsPostInp, AdvertisementsPatchInp
from fastapi import FastAPI, HTTPException, Response
from database import Session, User, Advertisement
from sqlalchemy import select
from datetime import datetime


app = FastAPI(
    title="Service buy-and-sell Buyalliti",
    description="A service for convenient sale and purchase of all sorts of things",
    version="1.0.0"
)


@app.post(
    path="/users",
    summary="Создать пользователя",
    status_code=201
)
async def create_user(request_data: UsersPostInp):
    async with Session() as session:
        user = User(
            name=request_data.name,
            surname=request_data.surname
        )
        session.add(user)
        await session.commit()

        return user.id_dict()


@app.get(
    path="/advertisements/{advertisement_id}",
    summary="Получить объявление по id"
)
async def get_advertisement_by_id(advertisement_id: int):
    async with Session() as session:
        stml = select(Advertisement).where(Advertisement.id == advertisement_id)
        advertisement = await session.scalar(stml)
        if advertisement:
            return advertisement.is_dict()
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Объявление с id = {advertisement_id} не существует"
            )


@app.get(
    path="/advertisements",
    summary="Получение объявлений по переданным полям"
)
async def get_advertisements_by_fields(
        title: str = None,
        description: str = None,
        price: float = None,
        master: int = None,
        created_at: str = None,
        created_before: str = None,
        created_after: str = None
):
    async with Session() as session:
        stml = select(Advertisement)
        if title:
            stml = stml.where(Advertisement.title == title)
        if description:
            stml = stml.where(Advertisement.description == description)
        if price:
            stml = stml.where(Advertisement.price == price)
        if master:
            stml = stml.where(Advertisement.master == master)
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
        result = [advertisement.is_dict() for advertisement in advertisements]
        if result:
            return result
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Объявлений с такими параметрами не найдено"
            )


@app.post(
    path="/advertisements",
    summary="Создать объявление",
    status_code=201
)
async def create_advertisement(request_data: AdvertisementsPostInp):
    async with Session() as session:
        stml_1 = select(Advertisement.id).where(Advertisement.title == request_data.title)
        exist = await session.scalar(stml_1)
        if exist:
            raise HTTPException(
                status_code=404,
                detail=f"Объявление с таким названием уже существует"
            )

        stml_2 = select(User.id).where(User.id == request_data.master)
        user = await session.scalar(stml_2)
        if not user:
            return HTTPException(
                status_code=404,
                detail=f"Пользователя с id = {request_data.master} не существует"
            )

        advertisement = Advertisement(
            title=request_data.title,
            description=request_data.description,
            price=request_data.price,
            master=request_data.master
        )
        session.add(advertisement)
        await session.commit()

        return advertisement.is_dict()


@app.patch(
    path="/advertisements/{advertisement_id}",
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
            stml_1 = select(Advertisement.title).where(Advertisement.title == title)
            exist = await session.scalar(stml_1)
            if exist:
                raise HTTPException(
                    status_code=404,
                    detail=f"Объявление с переданным новым названием уже существует"
                )
            else:
                advertisement.title = title
        if description:
            advertisement.description = description
        if price:
            advertisement.price = price
        await session.commit()

        return advertisement.is_dict()


@app.delete(
    "/advertisements/{advertisement_id}",
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
