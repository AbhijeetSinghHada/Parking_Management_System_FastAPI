import logging
import os
import sys
from fastapi import FastAPI
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.routers.auth import router as auth_router  # nopep8
from src.routers.parkingspace import router as parkingspace_router  # nopep8
from src.routers.slot import router as slot_router  # nopep8
from src.routers.vehicles import router as vehicle_router  # nopep8
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=os.getenv('LOG_FILE_NAME'),)
logger = logging.getLogger(__name__)


app = FastAPI()
app.include_router(auth_router)
app.include_router(parkingspace_router)
app.include_router(slot_router)
app.include_router(vehicle_router)
