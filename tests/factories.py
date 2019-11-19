from factory import Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory

from insta_backend.extensions import db
from insta_backend.models.user.user import User, UserType


class SaFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session


class UserFactory(SaFactory):
    id = Sequence(lambda n: int("{0}".format(n)))
    name = Sequence(lambda n: "user{0}".format(n))
    email = Sequence(lambda n: "email{0}".format(n))
    username = Sequence(lambda n: "username{0}".format(n))
    status = UserType.PUBLIC
    password = '1234'

    class Meta:
        model = User
