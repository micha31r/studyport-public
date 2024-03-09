import json
from django.utils import timezone
from django.core import serializers
from django.db.models import Model
from django.db.models.query import QuerySet


def localnow():
    return timezone.localtime(timezone.now())


def deep_serialize(obj, max_depth=0, _depth_count=-1):
    data = []

    if isinstance(obj, QuerySet) or isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
        _depth_count += 1
        for v in obj:
            data.append(deep_serialize(v, max_depth=max_depth, _depth_count=_depth_count))

    elif isinstance(obj, dict):
        _depth_count += 1
        data = {}
        for k, v in obj.items():
            data[k] = deep_serialize(v, max_depth=max_depth, _depth_count=_depth_count)

    elif isinstance(obj, Model):
        if (max_depth != None and _depth_count > max_depth):
            return obj.id

        # Serialize model instance
        data = json.loads(serializers.serialize("json", [obj]))[0]

        for field in obj._meta.get_fields():
            # If not reverse/hidden relationship fields
            if str(field)[0] != "<":
                field_name = str(field).split(".")[-1]
                value = eval("obj." + field_name)

                # Unpack values for many to many fields
                if field.__class__.__name__ == 'ManyToManyField':
                    value = value.all()
                    
                # Replace related models with serialized instances
                if isinstance(value, Model) or isinstance(value, QuerySet):
                    if not isinstance(value, QuerySet):
                        value = [value]
                    serialized_value = deep_serialize(value, max_depth=max_depth, _depth_count=_depth_count)
                    data["fields"][field_name] = serialized_value[0] if isinstance(value, list) else serialized_value
    
    else:
        # Convert none number data types to string
        if not (isinstance(obj, int) or isinstance(obj, float)): obj = str(obj)
        data = obj

    return data


def structure(queryset, fields=[], direction="horizontal"):
    """
    Formats a queryset into a table structure with specific model fields

    Examples
    --------
    Calculate average value:
    data = structure(qs, ["name", "val"], "vertical")
    avg = sum(data["val"]) / len(data["val"])
    """

    # Get all fields if fields is empty
    if not fields and queryset:
        for field in queryset[0]._meta.get_fields():
            if str(field)[0] != "<":
                fields.append(str(field).split(".")[-1])

    # Format data
    if direction == "horizontal":
        data = []
        for model in queryset:
            item = {}
            for field_name in fields:
                item[field_name] = eval("model." + field_name)
            data.append(item)
    else:
        data = {}
        for field_name in fields:
            item = []
            for model in queryset:
                item.append(eval("model." + field_name))
            data[field_name] = item
    return data