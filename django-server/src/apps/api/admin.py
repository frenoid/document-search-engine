from django.contrib import admin
from djongo.admin import ModelAdmin
from .models import (
        Country, CountryDetailsGeneral, CountryDetailsEconomy,
        CountryDetailsDemographicsAge, CountryDetailsBusinessExport,
        CountryDetailsBusinessFDI, CountryDetailsBusinessFTA,
        CountryDetailsBusinessInvestmentReasons, CountryDetailsFTA,
        CountryDetailsBusinessInvestmentSectors, CountryDetailsMobileUsage,
        CountryDetailsServiceUsage, Language, Religion, Service,
        Goods, Sector, SubSector, CountryPolicy, CountryPolicyLine, Lead,
        GenericImage, CountryPolicyRegion, CountryDetailsBusinessImport,
        IndustrySector, MobileWebActivity, CountryDetailsServicesUsage)


@admin.register(Language)
class LanguageAdmin(ModelAdmin):
    pass


@admin.register(Religion)
class ReligionAdmin(ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    pass


@admin.register(Goods)
class GoodsAdmin(ModelAdmin):
    pass


@admin.register(Sector)
class SectorAdmin(ModelAdmin):
    pass


@admin.register(SubSector)
class SubSectorAdmin(ModelAdmin):
    pass


@admin.register(IndustrySector)
class IndustrySectorAdmin(ModelAdmin):
    pass


@admin.register(MobileWebActivity)
class MobileWebActivityAdmin(ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(ModelAdmin):
    pass


@admin.register(CountryDetailsGeneral)
class CountryDetailsGeneralAdmin(ModelAdmin):
    pass


@admin.register(CountryDetailsEconomy)
class CountryDetailsEconomyAdmin(ModelAdmin):
    pass


@admin.register(CountryDetailsDemographicsAge)
class CountryDetailsDemographicsAgeAdmin(ModelAdmin):
    pass


@admin.register(CountryDetailsBusinessImport)
class CountryDetailsBusinessImportAdmin(ModelAdmin):
    pass


@admin.register(CountryDetailsBusinessExport)
class CountryDetailsBusinessExportAdmin(ModelAdmin):
    pass


@admin.register(CountryDetailsBusinessFDI)
class CountryDetailsBusinessFDIAdmin(ModelAdmin):
    pass


@admin.register(CountryDetailsBusinessFTA)
class CountryDetailsBusinessFTAAdmin(ModelAdmin):
    filter_horizontal = ('associated_countries',)


@admin.register(CountryDetailsFTA)
class CountryDetailsFTAAdmin(ModelAdmin):
    filter_horizontal = ('associated_countries',)


@admin.register(CountryDetailsBusinessInvestmentReasons)
class CountryDetailsBusinessInvestmentReasonsAdmin(ModelAdmin):
    pass


@admin.register(CountryDetailsBusinessInvestmentSectors)
class CountryDetailsBusinessInvestmentSectorsAdmin(ModelAdmin):
    filter_horizontal = ('key_sectors',)


@admin.register(CountryDetailsMobileUsage)
class CountryDetailsMobileUsageAdmin(ModelAdmin):
    pass


@admin.register(CountryDetailsServiceUsage)
class CountryDetailsServiceUsageAdmin(ModelAdmin):
    pass


@admin.register(CountryDetailsServicesUsage)
class CountryDetailsServicesUsageAdmin(ModelAdmin):
    pass


@admin.register(CountryPolicy)
class CountryPolicyAdmin(ModelAdmin):
    filter_horizontal = ('associated_countries',)


@admin.register(CountryPolicyRegion)
class CountryPolicyRegionAdmin(ModelAdmin):
    filter_horizontal = ('countries',)


@admin.register(CountryPolicyLine)
class CountryPolicyLineAdmin(ModelAdmin):
    pass


@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    pass


@admin.register(GenericImage)
class GenericImageAdmin(ModelAdmin):
    pass
