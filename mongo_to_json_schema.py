import json

from schematics.types.base import (BaseType, NumberType, IntType, LongType, FloatType,
                                   DecimalType, BooleanType, StringType)
from schematics.types.compound import ModelType, ListType

__version__ = '1.0'


SCHEMATIC_TYPE_TO_JSON_TYPE = {
    NumberType: 'number',
    IntType: 'integer',
    LongType: 'integer',
    FloatType: 'number',
    DecimalType: 'number',
    BooleanType: 'boolean',
    StringType: 'string',
}

# Schema Serialization

# Parameters for serialization to JSONSchema
schema_kwargs_to_schematics = {
    'maxLength': 'max_length',
    'minLength': 'min_length',
    'pattern': 'regex',
    'minimum': 'min_value',
    'maximum': 'max_value',
}



def jsonschema_for_fields_list(model):

    # i = 0
    properties = {}
    required = []
    # Loop over each field and either evict it or convert it


    # for field_name, field_instance in model._fields.iteritems():


    # for group


        # Break 3-tuple out
        # serialized_name = getattr(field_instance, 'serialized_name', None) or field_name

        # if isinstance(field_instance, ModelType):
        #     properties[serialized_name] = jsonschema_for_model(field_instance.model_class)

        # elif isinstance(field_instance, ListType):
            # properties[serialized_name] = jsonschema_for_model(field_instance.model_class, 'array')
            # properties[serialized_name] = jsonschema_for_model(field_instance.__class__, 'array')
            # properties[serialized_name] = jsonschema_for_model_list(field_instance.__class__, 'array')

        # Convert field as single model
        # if isinstance(field_instance, BaseType):



            # properties[serialized_name] = {
            #     "type": SCHEMATIC_TYPE_TO_JSON_TYPE.get(field_instance.__class__, 'string')
            # }

        # if getattr(field_instance, 'required', False):
        #     required.append(serialized_name)

        # i += 1

    return properties, required


def jsonschema_for_model_list(model, _type='object'):

    properties, required = jsonschema_for_fields_list(model)

    schema = {
        'type': _type,
        # 'title': model.__name__,
        'title': 'd_title',
        # 'properties': properties,
    }

    # if required:
    #     schema['required'] = required

    if _type == 'array':
        schema = {
            'type': 'array',
            # 'title': '%s Set' % (model.__name__),
            'title': 'd_title Set',
            'items': schema,
        }

    return schema















def jsonschema_for_fields(model):


    i = 0
    properties = {}
    required = []
    # Loop over each field and either evict it or convert it
    for field_name, field_instance in model._fields.iteritems():
        # Break 3-tuple out
        serialized_name = getattr(field_instance, 'serialized_name', None) or field_name

        if isinstance(field_instance, ModelType):
            properties[serialized_name] = jsonschema_for_model(field_instance.model_class)

        elif isinstance(field_instance, ListType):
            if hasattr(field_instance, 'model_class'):

                properties[serialized_name] = jsonschema_for_model(field_instance.model_class, 'array')
                # properties[serialized_name] = jsonschema_for_model(field_instance.__class__, 'array')
                # properties[serialized_name] = jsonschema_for_model_list(field_instance, 'array')



            else:


                # properties[serialized_name] = jsonschema_for_model(field_instance.field.__class__, 'array')

                # properties[serialized_name] = {
                #     "type": SCHEMATIC_TYPE_TO_JSON_TYPE.get(field_instance.field.__class__, 'string')
                # }


                # properties, required = jsonschema_for_fields(model)

                schema = {
                    'type': 'array',
                    "items": {
                        "type": SCHEMATIC_TYPE_TO_JSON_TYPE.get(field_instance.field.__class__, 'string')
                    }
                }

                # if required:
                #     schema['required'] = required

                properties[serialized_name] = schema

        # Convert field as single model
        elif isinstance(field_instance, BaseType):
            # TODO modify if
            if field_name == 'created':

                properties[serialized_name] = {
                    "type": 'string',
                    "format": 'date-time',
                }

            properties[serialized_name] = {
                "type": SCHEMATIC_TYPE_TO_JSON_TYPE.get(field_instance.__class__, 'string')
            }

        if getattr(field_instance, 'required', False):
            required.append(serialized_name)

        # if field_instance.default != None:
        if hasattr(field_instance, 'default'):
            if field_instance.default is not None:
                properties[serialized_name]['default'] = field_instance.default

        if hasattr(field_instance, 'min_size'):
            properties[serialized_name]['minItems'] = field_instance.min_size

        if hasattr(field_instance, 'max_size'):
            properties[serialized_name]['maxItems'] = field_instance.max_size

        i += 1

    return properties, required


def jsonschema_for_model(model, _type='object'):

    properties, required = jsonschema_for_fields(model)

    schema = {
        'type': _type,
        # 'title': model.__name__,
        'title': 'd_title',
        'properties': properties,
    }

    if required:
        schema['required'] = required

    if _type == 'array':
        schema = {
            'type': 'array',
            # 'title': '%s Set' % (model.__name__),
            'title': 'd_title Set',
            'items': schema,
        }

    return schema


def to_jsonschema(model):
    """Returns a representation of this schema class as a JSON schema."""
    return json.dumps(jsonschema_for_model(model))

