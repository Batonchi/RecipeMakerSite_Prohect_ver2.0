from app.web.users.model import User
from app.base.service import BaseService


class UserService(BaseService):
    model = User
    # @classmethod
    # def __init__(cls):
    #     super().__init__()
