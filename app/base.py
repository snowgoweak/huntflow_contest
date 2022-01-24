import asyncio
import os

import pandas as pd
import aiofiles
from aiocsv import AsyncDictReader
from aiohttp import FormData

from app.config import get_config
from app.modules.base import HuntFlowClient
from app.utils.common import parse_profile

config = get_config()

read_file = pd.read_excel('{}/{}'.format(config.hunt_flow.work_dir, config.hunt_flow.database_name))
read_file.to_csv("Base.csv",
                 index=None,
                 header=True)


async def main():
    async with aiofiles.open('Base.csv', mode='r', encoding="utf-8", newline="") as file:
        async for row in AsyncDictReader(file):
            profile = row
            directory = os.listdir("{}/{}".format(config.hunt_flow.work_dir, profile['Должность']))
            for k in directory:

                if k.split('.')[0].replace('й', 'й').replace(' ', '') == profile['ФИО'].replace(' ', ''):
                    file_name = k
                    break

            path_to_file = "{}/{}/{}".format(config.hunt_flow.work_dir, profile['Должность'], file_name)
            async with aiofiles.open(path_to_file, mode='rb') as resume:
                contents = await resume.read()
                data = FormData()
                data.add_field('file', contents, content_type='application/pdf')
                await HuntFlowClient.upload_file(data)

            json_body = await parse_profile(profile)
            response_body = await HuntFlowClient.create_application(json_body)
            applicant_id = response_body['id']

            response_vacancy_body = await HuntFlowClient.add_to_vacancy(applicant_id, json_body)


asyncio.run(main())
