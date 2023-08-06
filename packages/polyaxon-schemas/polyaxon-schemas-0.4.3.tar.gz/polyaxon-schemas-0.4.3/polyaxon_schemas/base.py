# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from collections import Mapping, OrderedDict

from hestia.humanize import humanize_timesince
from hestia.tz_utils import get_time_zone
from hestia.units import to_percentage, to_unit_memory
from marshmallow import RAISE, Schema, ValidationError, post_dump, post_load
from marshmallow.utils import EXCLUDE, utc

from polyaxon_schemas.exceptions import PolyaxonSchemaError
from polyaxon_schemas.utils import to_camel_case


class BaseSchema(Schema):
    """Base schema."""

    class Meta:
        unknown = RAISE
        ordered = True

    @post_load
    def make(self, data):
        return self.schema_config()(**data)

    @post_dump
    def unmake(self, data):
        return self.schema_config().remove_reduced_attrs(data)

    @staticmethod
    def schema_config():
        raise NotImplementedError()


class BaseConfig(object):
    """Base for config classes."""

    SCHEMA = None
    IDENTIFIER = None
    REDUCED_ATTRIBUTES = []  # Attribute to remove in the reduced form if they are null.
    DEFAULT_INCLUDE_ATTRIBUTES = []
    DEFAULT_EXCLUDE_ATTRIBUTES = []
    DATETIME_ATTRIBUTES = []
    MEM_SIZE_ATTRIBUTES = []
    PERCENT_ATTRIBUTES = []
    ROUNDING = 2
    UNKNOWN_BEHAVIOUR = RAISE

    def to_light_dict(self,
                      humanize_values=False,
                      include_attrs=None,
                      exclude_attrs=None,
                      unknown=None):
        unknown = unknown or self.UNKNOWN_BEHAVIOUR
        obj_dict = self.to_dict(humanize_values=humanize_values, unknown=unknown)
        if all([include_attrs, exclude_attrs]):
            raise PolyaxonSchemaError(
                'Only one value `include_attrs` or `exclude_attrs` is allowed.')
        if not any([include_attrs, exclude_attrs]):  # Use Default setup attrs
            include_attrs = self.DEFAULT_INCLUDE_ATTRIBUTES
            exclude_attrs = self.DEFAULT_EXCLUDE_ATTRIBUTES

        if include_attrs:
            exclude_attrs = set(six.iterkeys(obj_dict)) - set(include_attrs)
        for attr in exclude_attrs:
            obj_dict.pop(attr, None)

        return obj_dict

    def to_dict(self, humanize_values=False, unknown=None):
        unknown = unknown or self.UNKNOWN_BEHAVIOUR
        return self.obj_to_dict(self, humanize_values=humanize_values, unknown=unknown)

    def to_schema(self):
        return self.obj_to_schema(self)

    @classmethod
    def humanize_attrs(cls, obj):
        humanized_attrs = {}
        for attr in cls.DATETIME_ATTRIBUTES:
            humanized_attrs[attr] = humanize_timesince(getattr(obj, attr))
        for attr in cls.PERCENT_ATTRIBUTES:
            humanized_attrs[attr] = to_percentage(getattr(obj, attr), cls.ROUNDING)
        for attr in cls.MEM_SIZE_ATTRIBUTES:
            humanized_attrs[attr] = to_unit_memory(getattr(obj, attr))
        return humanized_attrs

    @classmethod
    def obj_to_dict(cls, obj, humanize_values=False, unknown=None):
        unknown = unknown or cls.UNKNOWN_BEHAVIOUR
        humanized_attrs = cls.humanize_attrs(obj) if humanize_values else {}
        data_dict = cls.SCHEMA(unknown=unknown).dump(obj)  # pylint: disable=not-callable

        for k, v in six.iteritems(humanized_attrs):
            data_dict[k] = v
        return data_dict

    @classmethod
    def remove_reduced_attrs(cls, data):
        obj_dict = OrderedDict((key, value) for (key, value) in six.iteritems(data))
        for attr in cls.REDUCED_ATTRIBUTES:
            if obj_dict[attr] is None:
                del obj_dict[attr]

        return obj_dict

    @classmethod
    def obj_to_schema(cls, obj):
        return {cls.IDENTIFIER: cls.obj_to_dict(obj)}

    @classmethod
    def from_dict(cls, value, unknown=None):
        unknown = unknown or cls.UNKNOWN_BEHAVIOUR
        return cls.SCHEMA(unknown=unknown).load(value)  # pylint: disable=not-callable

    @staticmethod
    def localize_date(dt):
        if not dt:
            return dt
        if not dt.tzinfo:
            dt = utc.localize(dt)
        return dt.astimezone(get_time_zone())

    @classmethod
    def to_jsonschema(cls):
        from marshmallow_jsonschema import JSONSchema  # pylint:disable=import-error

        return JSONSchema().dump(cls.SCHEMA())  # pylint:disable=not-callable


class BaseMultiSchema(Schema):
    __multi_schema_name__ = None
    __configs__ = None
    # to support snake case identifier, e.g. glorot_uniform and GlorotUniform
    __support_snake_case__ = False

    class Meta:
        unknown = EXCLUDE

    @post_dump(pass_original=True, pass_many=True)
    def handle_multi_schema_dump(self, data, pass_many, original):
        def handle_item(item):
            if hasattr(item, 'get_config'):
                return self.__configs__[item.__class__.__name__].obj_to_schema(item)
            return item.to_schema()

        if pass_many:
            return [handle_item(item) for item in original]

        return handle_item(original)

    @post_load(pass_original=True, pass_many=True)
    def handle_multi_schema_load(self, data, pass_many, original):
        def make(key, val=None):
            key = to_camel_case(key) if self.__support_snake_case__ else key
            try:
                return (self.__configs__[key].from_dict(val, unknown=EXCLUDE) if val else
                        self.__configs__[key]())
            except KeyError:
                raise ValidationError("`{}` is not a valid value for schema `{}`".format(
                    key, self.__multi_schema_name__))

        def handle_item(item):
            if isinstance(item, six.string_types):
                return make(item)

            if isinstance(item, Mapping):
                if 'class_name' in item:
                    return make(item['class_name'], item['config'])
                if 'model_type' in item:
                    return make(item.pop('model_type'), item)
                assert len(item) == 1
                key, val = list(six.iteritems(item))[0]
                return make(key, val)

        if pass_many:
            return [handle_item(item) for item in original]

        return handle_item(original)
