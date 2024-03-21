# import factory
# from factory.django import DjangoModelFactory
#
# from .models import (
#     Company,
#     Service,
#     ServiceCollection,
#     Contacts,
#     ReviewServiceModerator,
#     ReviewCompanyModerator,
# )
# from nft_tokens.factories import CollectionFactory
# from tools.factories import BaseModelFactory, TimeStampedModelFactory
#
#
# class CompanyFactory(
#     BaseModelFactory, TimeStampedModelFactory, DjangoModelFactory
# ):
#     class Meta:
#         model = Company
#
#     name = factory.Sequence(lambda n: f"Company {n}")
#     logo = factory.Faker("url")
#     owner = factory.Faker("name")
#     status_moderator = factory.Iterator(
#         [choice[0] for choice in StatusModeratorChoices.choices]
#     )
#
#
# class ServiceFactory(
#     BaseModelFactory, TimeStampedModelFactory, DjangoModelFactory
# ):
#     class Meta:
#         model = Service
#
#     company = factory.SubFactory(CompanyFactory)
#     type = factory.Iterator(
#         [choice[0] for choice in TypeServiceChoices.choices]
#     )
#     preview = factory.Faker("sentence")
#     description = factory.Faker("text")
#     status_moderator = factory.Iterator(
#         [choice[0] for choice in StatusModeratorChoices.choices]
#     )
#     active = factory.Faker("boolean")
#
#
# class ServiceCollectionFactory(
#     BaseModelFactory, TimeStampedModelFactory, DjangoModelFactory
# ):
#     class Meta:
#         model = ServiceCollection
#
#     service = factory.SubFactory(ServiceFactory)
#     collection = factory.SubFactory(CollectionFactory)
#
#
# class ContactsFactory(
#     BaseModelFactory, TimeStampedModelFactory, DjangoModelFactory
# ):
#     class Meta:
#         model = Contacts
#
#     service = factory.SubFactory(ServiceFactory)
#     country = factory.Faker("country")
#     state = factory.Faker("state")
#     city = factory.Faker("city")
#     address = factory.Faker("address")
#     site = factory.Faker("url")
#     phone = factory.Faker("phone_number")
#     email = factory.Faker("email")
#     social = factory.Faker("url")
#
#
# class ReviewServiceModeratorFactory(
#     BaseModelFactory, TimeStampedModelFactory, DjangoModelFactory
# ):
#     class Meta:
#         model = ReviewServiceModerator
#
#     service = factory.SubFactory(ServiceFactory)
#     title = factory.Faker("sentence")
#     description = factory.Faker("text")
#     moderator = factory.Faker("name")
#     wallet = factory.Faker("cryptocurrency_address")
#
#
# class ReviewCompanyModeratorFactory(
#     BaseModelFactory, TimeStampedModelFactory, DjangoModelFactory
# ):
#     class Meta:
#         model = ReviewCompanyModerator
#
#     company = factory.SubFactory(CompanyFactory)
#     title = factory.Faker("sentence")
#     description = factory.Faker("text")
#     moderator = factory.Faker("name")
#     wallet = factory.Faker("cryptocurrency_address")
