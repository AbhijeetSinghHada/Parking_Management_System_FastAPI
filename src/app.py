from fastapi import FastAPI
from src.routers.auth import router as auth_router
from src.routers.parkingspace import router as parkingspace_router
from src.routers.slot import router as slot_router
from src.routers.vehicles import router as vehicle_router
from src.helpers.logger import setup_logger
setup_logger()


app = FastAPI()
app.include_router(auth_router)
app.include_router(parkingspace_router)
app.include_router(slot_router)
app.include_router(vehicle_router)
