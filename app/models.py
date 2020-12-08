from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from datetime import datetime


class Searches(models.Model):
    """
    The Searches model
    """

    id = fields.IntField(pk=True)
    search_phrase = fields.CharField(max_length=255)
    region = fields.CharField(max_length=255)
    location_id = fields.IntField(null=True, default=None)
    created_at = fields.DatetimeField(auto_now_add=True)

    stats: fields.ReverseRelation['Stats']

    class Meta:
        unique_together = ("search_phrase", "region")

    class PydanticMeta:
        exclude = ["location_id"]


class Stats(models.Model):
    """
    The Stats model
    """

    id = fields.IntField(pk=True)
    ads_amount = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)

    search: fields.ForeignKeyRelation[Searches] = fields.ForeignKeyField(
        model_name='models.Searches', related_name='stats'
    )

    def created_at_timestamp(self) -> float:
        return self.created_at.timestamp()

    class PydanticMeta:
        computed = ['created_at_timestamp']
        exclude = ['id']



SearchesModel = pydantic_model_creator(Searches, name="Searches")
SearchesModelReadonly = pydantic_model_creator(Searches, name="SearchesIn", exclude_readonly=True)

StatsModel = pydantic_model_creator(Stats, name="Stats")