from bson.json_util import dumps, loads
from collections import OrderedDict
from django.db.models.fields.reverse_related import ManyToOneRel


def sync_mongo_field_order(model, dry_run=True):
    all_records = loads(dumps(model.objects.mongo_find()))
    if not all_records:
        return

    field_order = [
            field.column for field in model._meta.get_fields()
            if not isinstance(field, ManyToOneRel)]
    fixed_records = []
    for record in all_records:
        record_dict = OrderedDict()
        record_dict['_id'] = record['_id']
        for field in field_order:
            record_dict[field] = record.get(field)
        fixed_records.append(record_dict)

    if dry_run:
        print(fixed_records)
        return

    model.objects.mongo_delete_many({})
    model.objects.mongo_insert_many(fixed_records)
