from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Searches(models.Model):
    """
    The Searches model
    """

    id = fields.IntField(pk=True)
    search_phrase = fields.CharField(max_length=255, unique=True)
    region = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)

    stats: fields.ReverseRelation['Stats']


class Stats(models.Model):
    """
    The Stats model
    """

    id = fields.IntField(pk=True)
    announcement_amount = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)

    search: fields.ForeignKeyRelation[Searches] = fields.ForeignKeyField(
        model_name='models.Searches', related_name='stats'
    )


SearchesModel = pydantic_model_creator(Searches, name="Searches")
SearchesModelReadonly = pydantic_model_creator(Searches, name="SearchesIn", exclude_readonly=True)

StatsModel = pydantic_model_creator(Stats, name="Stats")
StatsModelReadonly = pydantic_model_creator(Stats, name="StatsIn", exclude_readonly=True)