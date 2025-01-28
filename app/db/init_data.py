import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Building, Activity, Organization
from app.db.database import get_db

async def init_data(session: AsyncSession):
    result = await session.execute(select(Building))
    
    if result.scalars().first():
        print("Data already initialized.")
        return

    # Buildings
    building1 = Building(address="г. Москва, ул. Ленина 1, офис 3", latitude=55.7558, longitude=37.6173)
    building2 = Building(address="г. Санкт-Петербург, Невский пр., 10", latitude=59.9343, longitude=30.3351)
    building3 = Building(address="г. Новосибирск, ул. Красный проспект, 50", latitude=55.0302, longitude=82.9204)
    building4 = Building(address="г. Казань, ул. Баумана, 17", latitude=55.7963, longitude=49.1088)

    # Activities
    activity_food = Activity(name="Еда")
    activity_meat = Activity(name="Мясная продукция", parent=activity_food)
    activity_milk = Activity(name="Молочная продукция", parent=activity_food)
    activity_cars = Activity(name="Автомобили")
    activity_parts = Activity(name="Запчасти", parent=activity_cars)
    activity_accessories = Activity(name="Аксессуары", parent=activity_cars)

    # Organizations
    org1 = Organization(
        name="ООО 'Рога и Копыта'",
        phone_numbers=["2-222-222", "3-333-333"],
        building=building1,
        activities=[activity_meat]
    )
    org2 = Organization(
        name="ЗАО 'Молоко и Ко'",
        phone_numbers=["8-800-555-35-35"],
        building=building2,
        activities=[activity_food, activity_milk]
    )
    org3 = Organization(
        name="ООО 'АвтоМир'",
        phone_numbers=["7-777-777"],
        building=building1,
        activities=[activity_cars, activity_parts]
    )
    org4 = Organization(
        name="ИП 'Гастроном'",
        phone_numbers=["8-913-444-55-66"],
        building=building3,
        activities=[activity_food]
    )
    org5 = Organization(
        name="АО 'ТехСнаб'",
        phone_numbers=["7-495-123-45-67"],
        building=building4,
        activities=[activity_cars, activity_accessories]
    )

    session.add_all([
        building1, building2, building3, building4,
        activity_food, activity_meat, activity_milk, activity_cars, activity_parts, activity_accessories,
        org1, org2, org3, org4, org5
    ])
    await session.commit()
    print("Test data initialized.")

async def main():
    async for session in get_db(): 
        await init_data(session) 

if __name__ == "__main__":
    asyncio.run(main())