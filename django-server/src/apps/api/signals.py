from bson.json_util import dumps
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import ModelHistory
from .models import (
        Country, CountryDetailsGeneral,
        CountryDetailsEconomy, CountryDetailsDemographicsAge,
        CountryDetailsBusinessExport, CountryDetailsBusinessFDI,
        CountryDetailsBusinessFTA, CountryDetailsBusinessInvestmentReasons,
        CountryDetailsBusinessInvestmentSectors, CountryDetailsMobileUsage,
        CountryDetailsServiceUsage, CountryPolicy, CountryPolicyLine)


@receiver(post_save, sender=Country)
@receiver(post_save, sender=CountryDetailsGeneral)
@receiver(post_save, sender=CountryDetailsEconomy)
@receiver(post_save, sender=CountryDetailsDemographicsAge)
@receiver(post_save, sender=CountryDetailsBusinessExport)
@receiver(post_save, sender=CountryDetailsBusinessFDI)
@receiver(post_save, sender=CountryDetailsBusinessFTA)
@receiver(post_save, sender=CountryDetailsBusinessInvestmentReasons)
@receiver(post_save, sender=CountryDetailsBusinessInvestmentSectors)
@receiver(post_save, sender=CountryDetailsMobileUsage)
@receiver(post_save, sender=CountryDetailsServiceUsage)
@receiver(post_save, sender=CountryPolicy)
@receiver(post_save, sender=CountryPolicyLine)
def create_history(sender, instance, created, **kwargs):
    content_type = ContentType.objects.get_for_model(sender)
    object_id = instance.id
    json_data = dumps(sender.objects.mongo_find_one(
        {'id': object_id}, {'created_at': 0, 'updated_at': 0}))
    history = ModelHistory.objects.filter(
            content_type=content_type, object_id=object_id).first()
    if created or history is None or history.data != json_data:
        ModelHistory.objects.create(
                content_type=content_type, object_id=object_id, data=json_data)
