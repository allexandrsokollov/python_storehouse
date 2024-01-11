from app.db.repos import LocationRepo
from app.services.storehouse_services import SupplierService, PalletService, async_session, LocationService
from app.storehouse_api.models import CreateSupplierModel, CreatePalletModel, CreateLocationModel


async def fill_up():
    supplier_service = SupplierService()
    supplier_one = await supplier_service.create(CreateSupplierModel(name="sup__1"))
    supplier_two = await supplier_service.create(CreateSupplierModel(name="sup__2"))

    pallet_service = PalletService()

    location_service = LocationService()
    locations = []
    for i in range(10):
        for j in range(10):
            for k in range(10):
                new_location = await location_service.create(CreateLocationModel(shelving=i, floor=j, position=k))
                print(new_location.id)
                locations.append(new_location.id)

    for i in range(1000):
        if i % 2 == 0:
            print("creating model")
            location = locations.pop()
            await pallet_service.create(
                CreatePalletModel(
                    title=f"pallet_{i}",
                    description=f"description_{i}",
                    supplier_id=supplier_one.id,
                    location_id=location,
                    user_id=None,
                )
            )
        else:
            location = locations.pop()
            await pallet_service.create(
                CreatePalletModel(
                    title=f"pallet_{i}",
                    description=f"description_{i}",
                    supplier_id=supplier_two.id,
                    location_id=location,
                    user_id=None,
                )
            )

