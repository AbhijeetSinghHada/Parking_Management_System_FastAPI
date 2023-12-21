from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from src.helpers.logger import setup_logger, log_info
from src.routers.auth import router as auth_router
from src.routers.parkingspace import router as parkingspace_router
from src.routers.slot import router as slot_router
from src.routers.vehicles import router as vehicle_router
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     filename='app.log')

# logger = logging.getLogger(__name__)
setup_logger("logs.txt")
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    expose_headers=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(parkingspace_router)
app.include_router(slot_router)
app.include_router(vehicle_router)
