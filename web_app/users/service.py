from web_app.users.model import User
from base.service import BaseService


class UserService(BaseService):
    model = User
    # @classmethod
    # def __init__(cls):
    #     super().__init__()
