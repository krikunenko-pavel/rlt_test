import json

from aiogram.filters.command import CommandStart
from aiogram import Router
from aiogram.types import Message
from models import employee_salary
from datetime import datetime, timedelta

import calendar
import logging

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Hello {message.from_user.username}"
    )


@router.message()
async def handle_request(message: Message):
    cl = message.bot.state.mongo_client
    db = message.bot.state.mongo_db
    collection = message.bot.state.mongo_collection

    try:
        user_request = employee_salary.RequestModel(**json.loads(message.text))
    except Exception:
        await message.answer(
            'Невалидный запос. Пример запроса:\n '
            '{"dt_from": "2022-09-01T00:00:00", '
            '"dt_upto": "2022-12-31T23:59:00", '
            '"group_type": "month"}'
        )
    else:
        group_types = {
            'hour': '%Y-%m-%dT%H',
            'day': '%Y-%m-%d',
            'month': '%Y-%m'
        }

        dt_format = group_types[user_request.group_type.value]

        query = [
            {"$match": {"dt": {"$gte": user_request.dt_from, "$lte": user_request.dt_upto}}},
            {"$group": {
                "_id": {"$dateToString": {"format": dt_format, "date": "$dt"}},
                "sum_value": {"$sum": '$value'}}},
            {"$sort": {"_id": 1}},
        ]

        cursor = collection.aggregate(query)

        labels = []
        data = []

        iso_types = {
            'hour': ':00:00',
            'day': 'T00:00:00',
            'month': '-01T00:00:00'
        }

        iso_format = iso_types[user_request.group_type.value]

        for doc in cursor:
            dt_raw = datetime.fromisoformat(doc['_id'] + iso_format)
            dt_iso = datetime.isoformat(dt_raw)
            labels.append(dt_iso)
            data.append(doc['sum_value'])

        result_data = []
        result_labels = []

        current_date = user_request.dt_from

        while current_date <= user_request.dt_upto:
            match user_request.group_type.value:
                case "hour":
                    delta = timedelta(hours=1)
                case "day":
                    delta = timedelta(days=1)
                case _:
                    _, days_in_month = calendar.monthrange(current_date.year, current_date.month)
                    delta = timedelta(days=days_in_month)

            result_labels.append(datetime.isoformat(current_date))

            if datetime.isoformat(current_date) not in labels:
                result_data.append(0)
            else:
                value_index = labels.index(datetime.isoformat(current_date))
                result_data.append(data[value_index])

            current_date += delta

        await message.answer(
            json.dumps(employee_salary.ResponseModel(
                dataset=result_data,
                labels=result_labels
            ).model_dump())
        )
