"""The models module contains the tortoise orm classes and pydantic models
generated from tortoise orm models."""

from dataclasses import dataclass

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Searches(models.Model):
    """The Searches model."""

    id = fields.IntField(pk=True)
    search_phrase = fields.CharField(max_length=255)
    region = fields.CharField(max_length=255)
    location_id = fields.IntField(null=True, default=None)
    created_at = fields.DatetimeField(auto_now_add=True)

    stats: fields.ReverseRelation['Stats']

    @dataclass
    class Meta:
        """This meta class is used to create paired unique index."""

        unique_together = ("search_phrase", "region")

    @dataclass
    class PydanticMeta:
        """This meta class is used to exclude field from pydantic output
        model."""

        exclude = ["location_id"]


class Stats(models.Model):
    """The Stats model."""

    id = fields.IntField(pk=True)
    ads_amount = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)

    search: fields.ForeignKeyRelation[Searches] = fields.ForeignKeyField(
        model_name='models.Searches', related_name='stats'
    )

    def created_at_timestamp(self) -> float:
        """

        :return: timestamp from record created_at datetime field
        :rtype: float
        """

        return self.created_at.timestamp()

    @dataclass
    class PydanticMeta:
        """This meta class is used to exclude from pydantic output model and
        add field into pydantic output model."""

        computed = ['created_at_timestamp']
        exclude = ['id']


SearchesModel = pydantic_model_creator(Searches, name="Searches")
SearchesModelReadonly = pydantic_model_creator(Searches, name="SearchesIn", exclude_readonly=True)

StatsModel = pydantic_model_creator(Stats, name="Stats")
