from sqlalchemy import Integer, LargeBinary
from sqlalchemy_utils import ChoiceType, PasswordType as BasePasswordType


class EnumChoiceType(ChoiceType):
    def __repr__(self):
        return "{}()".format(Integer.__name__)


class PasswordType(BasePasswordType):
    def __repr__(self):
        return "{}()".format(LargeBinary.__name__)