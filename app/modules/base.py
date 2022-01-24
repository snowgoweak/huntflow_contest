from app.config import get_config
from app.utils.common import async_upload_file, async_request


class HuntFlowClient:
    base_url = get_config().hunt_flow.host
    account_id = get_config().hunt_flow.account_id
    token = get_config().hunt_flow.token

    upload_file_url = '/account/{}/upload'.format(account_id)
    create_application_url = '/account/{}/applicants'.format(account_id)

    @classmethod
    async def upload_file(cls, file):
        url = cls.base_url + cls.upload_file_url
        try:
            file_id = await async_upload_file('POST', url, file, cls.token)
            return file_id
        except:
            pass

    @classmethod
    async def create_application(cls, json_body: dict):
        url = cls.base_url + cls.create_application_url
        try:
            response = await async_request('POST', url, json_body=json_body)
            return response
        except:
            pass

    @classmethod
    async def add_to_vacancy(cls, applicant_id: int, json_body: dict):
        url = cls.base_url + '/account /{}/applicants/{}/vacancy'.format(cls.account_id, applicant_id)
        try:
            response = await async_request('POST', url, json_body=json_body)
            return response
        except:
            pass
