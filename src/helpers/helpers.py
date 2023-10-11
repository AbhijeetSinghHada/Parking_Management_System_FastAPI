from datetime import datetime, date
import logging
from src.configurations.config import error_format
logger = logging.getLogger(__name__)


def convert_user_details_to_dict(lst):
    user_dict = {'name': lst[0][0],
                 'user_id': lst[0][1],
                 'role': [x[2] for x in lst]}
    return user_dict


def return_time_difference(_date, _time):
    _time = (datetime.min + _time).time()
    tdelta = (datetime.now() - datetime.combine(_date, _time))
    return tdelta


def return_date_time_combined(_date, _time):
    _time = (datetime.min + _time).time()
    return datetime.combine(_date, _time)


def return_no_of_hours_elapsed(date_data, time_data):
    tdelta = return_time_difference(date_data, time_data)
    total_seconds = tdelta.total_seconds()
    hours = str(int(total_seconds // 3600)).zfill(2)
    return int(hours)


def return_date_and_time():
    today_date = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    return today_date, current_time


def return_current_date_time():
    datetime_now = datetime.now()
    return datetime_now.strftime("%Y-%m-%d %H:%M")


def formated_error(error_code, error_message, status):
    error = error_format
    error["error"]["code"] = error_code
    error["error"]["message"] = error_message
    error["status"] = status
    return error
