from app.services.storehouse_services import SupplierService, PalletService
from app.storehouse_api.models import CreateSupplierModel, CreatePalletModel


async def fill_up():
    supplier_service = SupplierService()
    supplier_one = await supplier_service.create(CreateSupplierModel(name="sup__1"))
    supplier_two = await supplier_service.create(CreateSupplierModel(name="sup__2"))

    pallet_service = PalletService()

    for i in range(1200):
        if i % 2 == 0:
            await pallet_service.create(CreatePalletModel(title=f"pallet_{i}", description=f"description_{i}",
                                                          supplier_id=supplier_one.id, location_id=None,
                                                          user_id=None))
        else:
            await pallet_service.create(CreatePalletModel(title=f"pallet_{i}", description=f"description_{i}",
                                                          supplier_id=supplier_two.id, location_id=None,
                                                          user_id=None))
