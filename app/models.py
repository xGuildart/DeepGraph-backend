from odmantic import AIOEngine, Model, ObjectId, Field
from bson import ObjectId
from typing import List, Generic


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            print(v)
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Genz(Model):
    id: int = Field(key_name="_id", primary_field=True,
                    default_factory=PyObjectId)
    date: str = Field(...)
    category: str = Field(...)
    sentence: str = Field(...)
    sentence_short: str = Field(...)
    sentence_keywords: str = Field(...)
    sentence_sentiment: str = Field(...)
    sentence_sentiment_net: float = Field(...)
    sentence_sent_score: float = Field(...)
    sentence_sentiment_label: int = Field(...)
    sentence_entities: str = Field(...)
    sentence_non_entities: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": 500,
                "date": "2021-02-07",
                "category": "ESG investing",
                "sentence": "But if the right-to-repair issue becomes a legitimate antitrust threat, then Microsoft investors will need to view it as a more serious business risk.",
                "sentence_short": "['right', 'repair', 'issue', 'becomes', 'legitimate', 'antitrust', 'threat', 'Microsoft', 'investors', 'will', 'need', 'to', 'view', 'serious', 'business', 'risk']",
                "sentence_keywords": "[['right', ''], ['repair issue', ''], ['legitimate antitrust threat', ''], ['serious business risk', '']]",
                "sentence_sentiment": "[0.02471153251826763, 0.975288450717926]",
                "sentence_sentiment_net": -0.950576918,
                "sentence_sent_score": -3.675463253,
                "sentence_sentiment_label": 0,
                "sentence_entities": "[['Microsoft', 'ORG']]",
                "sentence_non_entities": "['right', 'repair issue', 'legitimate antitrust threat', 'serious business risk']"
            }
        }


class Young(Model):
    id: int = Field(key_name="_id", primary_field=True,
                    default_factory=PyObjectId)
    date: str = Field(...)
    logits: float = Field(...)
    net_sent: float = Field(...)
    logits_mean: float = Field(...)
    net_sent_mean: float = Field(...)
    MA_logits: float = Field(...)
    MA_net_sent: float = Field(...)
    MA_net_sent_ema_alpha_0: dict = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": 3,
                "date": "2017-10-18",
                "logits": -4.598010027138729,
                "net_sent": -0.9800571324303746,
                "logits_mean": -2.536194609021292,
                "net_sent_mean": -0.7024354821071028,
                "MA_logits": -2.536194609021292,
                "MA_net_sent": 0.4065616930446898,
                "MA_net_sent_ema_alpha_0": {
                    "1": 0.7688551269692835,
                    "3": 0.45195660504396074,
                    "5": 0.12931239925674165
                }
            }
        }
