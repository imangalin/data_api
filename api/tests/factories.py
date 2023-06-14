import factory
from datetime import datetime, timedelta

from django.contrib.auth.models import User


from account.models import Account, AccountDataType, DataRegion

factory.Faker._DEFAULT_LOCALE = "ru_RU"


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("email")

    class Meta:
        model = User


class AccountDataTypeFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("company")

    class Meta:
        model = AccountDataType


class AccountFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.Faker("name")
    company = factory.Faker("company")
    active = True
    access_start = datetime.today()
    access_expiration = factory.LazyAttribute(
        lambda self: self.access_start + timedelta(days=30)
    )

    class Meta:
        model = Account
