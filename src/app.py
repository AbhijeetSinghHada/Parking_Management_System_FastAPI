from fastapi import FastAPI
import logging
from src.helpers.logger import setup_logger, log_info
from src.routers.auth import router as auth_router
from src.routers.parkingspace import router as parkingspace_router
from src.routers.slot import router as slot_router
from src.routers.vehicles import router as vehicle_router
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='app.log')

logger = logging.getLogger(__name__)
app = FastAPI()
app.include_router(auth_router)
app.include_router(parkingspace_router)
app.include_router(slot_router)
app.include_router(vehicle_router)
