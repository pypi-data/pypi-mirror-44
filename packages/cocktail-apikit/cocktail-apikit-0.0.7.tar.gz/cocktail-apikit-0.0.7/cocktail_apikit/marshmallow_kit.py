"""
Marshmallow tool kit will be used by backend api projects
"""
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from marshmallow import Schema, pre_dump, post_load
from marshmallow.fields import DateTime, UUID

from cocktail_apikit import MONGO_ID_FIELD_NAME
from .constants import (
    MARSHMALLOW_NESTED_FIELDS, MARSHMALLOW_LIST_FIELDS, MARSHMALLOW_DICT_FIELDS, MARSHMALLOW_SCALAR_FIELDS
)


############################################################
# Customized marshmallow fields
############################################################


class IntegerTimeStamp(DateTime):
    """
    Convert value between int and datetime string
    """

    def _serialize(self, value, attr, obj):
        """
        Convert a **integer** timestamp value & **string** datetime  value
        """
        if isinstance(value, int):
            value = datetime.utcfromtimestamp(value)
        return super()._serialize(value, attr, obj)

    def _deserialize(self, value, attr, data):
        """
        Convert a **string** datetime  value to **integer** timestamp  value
        """
        value = super()._deserialize(value, attr, data)
        if not value:
            return None
        return int(value.timestamp())


class DecimalTimeStamp(DateTime):
    """
    Convert value between **Decimal** timestamp value and **string** datetime  value
    """

    def _serialize(self, value, attr, obj):
        """
        Convert a **Decial** timestamp value to **string** datetime  value
        """
        if isinstance(value, Decimal):
            value = datetime.utcfromtimestamp(float(value))
        return super()._serialize(value, attr, obj)

    def _deserialize(self, value, attr, data):
        """
        Convert a **string** datetime  value to **Decimal** timestamp value
        """
        value = super()._deserialize(value, attr, data)
        if not value:
            return None
        return Decimal(value.timestamp())


############################################################
# Customized Base Schema which will by used by all other api projects
############################################################
class SchemaMongoMixin:
    """
    This mixin class will help marshmallow schema class generate a collection of valid mongo-style query field names
    """

    @pre_dump
    def pre_dump_process(self, data):
        data['id'] = data.get(MONGO_ID_FIELD_NAME, None)
        data = self._extra_pre_dump_process(data)
        return data

    def _extra_pre_dump_process(self, data):
        """
        Any other extra pre dump process can be added here
        """
        return data

    @post_load
    def post_load_process(self, data):

        # auto generate these field after load data from client input
        if 'created_at' not in data:
            data['created_at'] = datetime.now().astimezone(timezone.utc)

        if 'updated_at' not in data:
            data['updated_at'] = datetime.now().astimezone(timezone.utc)

        # after load auto generate this field for mongodb to store
        if MONGO_ID_FIELD_NAME not in data:
            data[MONGO_ID_FIELD_NAME] = uuid.uuid4()

        data = self._extra_post_load_process(data)
        return data

    def _extra_post_load_process(self, data):
        """
        Any other extra post load process can be added here
        """
        return data

    @classmethod
    def valid_mongo_query_fields(cls):
        """
        Use class level cache Schema's valid mongo style's query  field names to avoid call the real method repeatedly
        """
        if getattr(cls, '_valid_mongo_query_fields', False):
            # print('reuse class attribute')
            return getattr(cls, '_valid_mongo_query_fields')

        # pylint: disable=too-many-branches
        def _fetch_valid_field_name_from_schema_fields(prefix: str = '', fields: dict = None):

            # print('initiating')
            field_names = set()

            for field, value in fields.items():

                sub_prefix = '{}.{}'.format(prefix, field) if prefix else field

                # Nested field
                if isinstance(value, MARSHMALLOW_NESTED_FIELDS):
                    field_names.update(_fetch_valid_field_name_from_schema_fields(sub_prefix, value.nested.fields))
                    continue

                # List fields
                if isinstance(value, MARSHMALLOW_LIST_FIELDS):
                    if isinstance(value.container, MARSHMALLOW_NESTED_FIELDS):
                        try:
                            field_names.update(
                                _fetch_valid_field_name_from_schema_fields(sub_prefix, value.container.nested.fields))
                        except AttributeError:
                            continue
                        else:
                            continue

                # Dict fields
                if isinstance(value, MARSHMALLOW_DICT_FIELDS):
                    field_names.update(_fetch_valid_field_name_from_schema_fields(sub_prefix, value.metadata))
                    continue

                # Scalar value field
                if isinstance(value, MARSHMALLOW_SCALAR_FIELDS):
                    field_names.add(sub_prefix)

            return field_names

        valid_mongo_query_fields = _fetch_valid_field_name_from_schema_fields(fields=cls._declared_fields)
        valid_mongo_query_fields.add(MONGO_ID_FIELD_NAME)
        setattr(cls, '_valid_mongo_query_fields', valid_mongo_query_fields)
        return getattr(cls, '_valid_mongo_query_fields')


class BaseSchema(Schema, SchemaMongoMixin):
    id = UUID(required=False, dump_only=True, description='ID of a schema record')
    created_at = DateTime(required=False,  description='Schema creation time')
    updated_at = DateTime(required=False,  description='Schema object update time')
    deleted_at = DateTime(required=False,  description='Schema object delete time')
