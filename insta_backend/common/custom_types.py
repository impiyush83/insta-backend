from sqlalchemy import Integer
from sqlalchemy_utils import ChoiceType


class EnumChoiceType(ChoiceType):
    def __repr__(self):
        return "{}()".format(Integer.__name__)
