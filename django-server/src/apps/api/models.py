from django import forms
from djongo import models
from core.fields import MongoDecimalField
from core.models import Base, Slugged, InfoMeta
from .constants import (
    ServiceType, ValueType, RouteType, FTACoverageType,
    TradeDescriptionType, TradeLinksType, AppStoreType, GenderType)


# The abstract models used for embedded documents are defined below.

class Currency(models.Model):
    name = models.CharField(max_length=55)
    iso_code = models.CharField(max_length=10)
    symbol = models.CharField(max_length=4)

    class Meta:
        abstract = True


class PoliticalStability(models.Model):
    rank = models.PositiveSmallIntegerField()
    total_countries = models.PositiveSmallIntegerField()

    objects = models.DjongoManager()

    class Meta:
        abstract = True


class GenericRangeDistribution(models.Model):
    range_min = models.FloatField(blank=True)
    range_max = models.FloatField(blank=True)
    label = models.CharField(max_length=55, blank=True)
    value = MongoDecimalField(max_digits=24, decimal_places=2)
    logo = models.CharField(max_length=50, choices=[], blank=True)

    objects = models.DjongoManager()

    class Meta:
        abstract = True


class CountryDistribution(models.Model):
    country = models.CharField(max_length=75, choices=[])
    value = MongoDecimalField(max_digits=24, decimal_places=2)

    objects = models.DjongoManager()

    class Meta:
        abstract = True


class GoodsDistribution(models.Model):
    product = models.CharField(max_length=75, choices=[])
    value = MongoDecimalField(max_digits=24, decimal_places=2)

    objects = models.DjongoManager()

    class Meta:
        abstract = True


class CountryGoodsDistribution(models.Model):
    country = models.CharField(max_length=75, choices=[])
    product = models.CharField(max_length=75, choices=[])
    value = MongoDecimalField(max_digits=24, decimal_places=2)

    objects = models.DjongoManager()

    class Meta:
        abstract = True


class YearDistribution(models.Model):
    year = models.CharField(max_length=4)
    value = MongoDecimalField(max_digits=24, decimal_places=2)

    objects = models.DjongoManager()

    class Meta:
        abstract = True


class ServiceDistribution(models.Model):
    product = models.CharField(max_length=75, choices=[])
    value = MongoDecimalField(max_digits=24, decimal_places=2)

    objects = models.DjongoManager()

    class Meta:
        abstract = True


class AppDistribution(models.Model):
    product = models.CharField(max_length=75, choices=[])
    app_store = models.CharField(max_length=75, choices=AppStoreType.CHOICES)

    objects = models.DjongoManager()

    class Meta:
        abstract = True


class GeoCoordinates(models.Model):
    latitude = MongoDecimalField(max_digits=8, decimal_places=5)
    longitude = MongoDecimalField(max_digits=8, decimal_places=5)
    label = models.CharField(max_length=75, blank=True)

    objects = models.DjongoManager()

    class Meta:
        abstract = True


class DescriptionDistribution(models.Model):
    description_type = models.CharField(
        max_length=20, choices=TradeDescriptionType.CHOICES)
    description = models.TextField()

    objects = models.DjongoManager()

    class Meta:
        abstract = True


class LinksDistribution(models.Model):
    link_type = models.CharField(
        max_length=20, choices=TradeLinksType.CHOICES)
    url = models.URLField(max_length=255)

    objects = models.DjongoManager()

    class Meta:
        abstract = True


class CountryIndustryDistribution(models.Model):
    country = models.CharField(max_length=75, choices=[])
    industry = models.CharField(max_length=75, choices=[])

    objects = models.DjongoManager()

    class Meta:
        abstract = True


class MobileActivityDistribution(models.Model):
    activity = models.CharField(max_length=75, choices=[])
    value = MongoDecimalField(max_digits=24, decimal_places=2)

    objects = models.DjongoManager()

    class Meta:
        abstract = True


class IndustrySectorDistribution(models.Model):
    industry_sector = models.CharField(max_length=75, choices=[])
    value = MongoDecimalField(max_digits=24, decimal_places=2)

    objects = models.DjongoManager()

    class Meta:
        abstract = True


class IndustrySectorDescription(models.Model):
    industry_sector = models.CharField(max_length=75, choices=[])
    description = models.TextField(blank=True)

    objects = models.DjongoManager()

    class Meta:
        abstract = True


class ServiceGenderDistribution(models.Model):
    product = models.CharField(max_length=75, choices=[])
    gender = models.CharField(max_length=20, choices=GenderType.CHOICES)
    value = MongoDecimalField(max_digits=24, decimal_places=2)

    objects = models.DjongoManager()

    class Meta:
        abstract = True


# The model forms used for rendering a few embedded models are defined below.

class CountryDistributionForm(forms.ModelForm):
    class Meta:
        model = CountryDistribution
        fields = ('country', 'value')
        widgets = {
            'country': forms.widgets.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        country_choices = [('', '---------')]
        country_choices.extend(
            [(c.slug, c.name) for c in Country.objects.all().order_by('name')])
        self.fields['country'].widget.choices = country_choices


class GoodsDistributionForm(forms.ModelForm):
    class Meta:
        model = GoodsDistribution
        fields = ('product', 'value')
        widgets = {
            'product': forms.widgets.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        goods_choices = [('', '---------')]
        goods_choices.extend(
            [(c.slug, '{} - {}'.format(
                c.name,
                'L2' if c.parent_id else 'L1'
                )) for c in Goods.objects.all().order_by('name')])
        self.fields['product'].widget.choices = goods_choices


class CountryGoodsDistributionForm(forms.ModelForm):
    class Meta:
        model = CountryGoodsDistribution
        fields = ('country', 'product', 'value')
        widgets = {
            'country': forms.widgets.Select(),
            'product': forms.widgets.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        country_choices = [('', '---------')]
        country_choices.extend(
            [(c.slug, c.name) for c in Country.objects.all().order_by('name')])
        goods_choices = [('', '---------')]
        goods_choices.extend(
            [(c.slug, '{} - {}'.format(
                c.name,
                'L2' if c.parent_id else 'L1'
                )) for c in Goods.objects.all().order_by('name')])
        self.fields['product'].widget.choices = goods_choices
        self.fields['country'].widget.choices = country_choices


class ServiceDistributionForm(forms.ModelForm):
    class Meta:
        model = ServiceDistribution
        fields = ('product', 'value')
        widgets = {
            'product': forms.widgets.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        service_choices = [('', '---------')]
        service_choices.extend(
            [(c.slug, c.name) for c in Service.objects.all().order_by('name')])
        self.fields['product'].widget.choices = service_choices


class AppDistributionForm(forms.ModelForm):
    class Meta:
        model = AppDistribution
        fields = ('product', 'app_store')
        widgets = {
            'product': forms.widgets.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        service_choices = [('', '---------')]
        service_choices.extend(
            [(c.slug, c.name) for c in Service.objects.all().order_by('name')])
        self.fields['product'].widget.choices = service_choices


class MobileActivityDistributionForm(forms.ModelForm):
    class Meta:
        model = MobileActivityDistribution
        fields = ('activity', 'value')
        widgets = {
            'activity': forms.widgets.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        activity_choices = [('', '---------')]
        activity_choices.extend(
            [(c.slug, c.name)
                for c in MobileWebActivity.objects.all().order_by('name')])
        self.fields['activity'].widget.choices = activity_choices


class LanguageForm(forms.ModelForm):
    class Meta:
        model = InfoMeta
        fields = ('title',)
        widgets = {
            'title': forms.widgets.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        language_choices = [('', '---------')]
        language_choices.extend(
            [(c.slug, c.name)
                for c in Language.objects.all().order_by('name')])
        self.fields['title'].widget.choices = language_choices


class ReligionForm(forms.ModelForm):
    class Meta:
        model = InfoMeta
        fields = ('title',)
        widgets = {
            'title': forms.widgets.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        religion_choices = [('', '---------')]
        religion_choices.extend(
            [(c.slug, c.name)
                for c in Religion.objects.all().order_by('name')])
        self.fields['title'].widget.choices = religion_choices


class GenericRangeDistributionForm(forms.ModelForm):
    class Meta:
        model = GenericRangeDistribution
        fields = ('range_min', 'range_max', 'label', 'value', 'logo')
        widgets = {
            'logo': forms.widgets.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        image_choices = [('', '---------')]
        image_choices.extend(
            [(c.slug, c.name) for c in GenericImage.objects.all()])
        self.fields['logo'].widget.choices = image_choices


class CountryIndustryDistributionForm(forms.ModelForm):
    class Meta:
        model = CountryIndustryDistribution
        fields = ('country', 'industry')
        widgets = {
            'country': forms.widgets.Select(),
            'industry': forms.widgets.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        country_choices = [('', '---------')]
        country_choices.extend(
            [(c.slug, c.name) for c in Country.objects.all().order_by('name')])
        industry_choices = [('', '---------')]
        industry_choices.extend(
            [(i.slug, '{} - {}'.format(
                i.name,
                'L2' if i.parent_id else 'L1'
                )) for i in IndustrySector.objects.all().order_by('name')])
        self.fields['country'].widget.choices = country_choices
        self.fields['industry'].widget.choices = industry_choices


class IndustrySectorDistributionForm(forms.ModelForm):
    class Meta:
        model = IndustrySectorDistribution
        fields = ('industry_sector', 'value')
        widgets = {
            'industry_sector': forms.widgets.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        industry_choices = [('', '---------')]
        industry_choices.extend(
            [(i.slug, '{} - {}'.format(
                i.name,
                'L2' if i.parent_id else 'L1'
                )) for i in IndustrySector.objects.all().order_by('name')])
        self.fields['industry_sector'].widget.choices = industry_choices


class IndustrySectorDescriptionForm(forms.ModelForm):
    class Meta:
        model = IndustrySectorDescription
        fields = ('industry_sector', 'description')
        widgets = {
            'industry_sector': forms.widgets.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        industry_choices = [('', '---------')]
        industry_choices.extend(
            [(i.slug, '{} - {}'.format(
                i.name,
                'L2' if i.parent_id else 'L1'
                )) for i in IndustrySector.objects.all().order_by('name')])
        self.fields['industry_sector'].widget.choices = industry_choices


class ServiceGenderDistributionForm(forms.ModelForm):
    class Meta:
        model = ServiceGenderDistribution
        fields = ('product', 'gender', 'value')
        widgets = {
            'product': forms.widgets.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        service_choices = [('', '---------')]
        service_choices.extend(
            [(c.slug, c.name) for c in Service.objects.all().order_by('name')])
        self.fields['product'].widget.choices = service_choices


# The models used for lookup purposes are defined below.

class Language(Base, Slugged):

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'


class Religion(Base, Slugged):
    logo = models.ImageField(upload_to='goods_logos', blank=True)

    class Meta:
        verbose_name = 'Religion'
        verbose_name_plural = 'Religions'


class Service(Base, Slugged):
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='service_logos', blank=True)
    color = models.CharField(max_length=7, blank=True)
    company = models.CharField(max_length=75)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'


class Goods(Base, Slugged):
    logo = models.ImageField(upload_to='goods_logos', blank=True)
    hs92_id = models.CharField(max_length=8, blank=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True)

    class Meta:
        verbose_name = 'Goods'
        verbose_name_plural = 'Goods'


class Sector(Base, Slugged):
    logo = models.ImageField(upload_to='sector_logos', blank=True)

    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectors'


class SubSector(Base, Slugged):
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT)
    logo = models.ImageField(upload_to='subsector_logos', blank=True)

    class Meta:
        verbose_name = 'Sub-Sector'
        verbose_name_plural = 'Sub-Sectors'


class IndustrySector(Base, Slugged):
    logo = models.ImageField(upload_to='industry_sector_logos', blank=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True)

    class Meta:
        verbose_name = 'Industry Sector'
        verbose_name_plural = 'Industry Sectors'


class GenericImage(Base, Slugged):
    logo = models.ImageField(upload_to='generic_images', blank=True)

    class Meta:
        verbose_name = 'Generic Image'
        verbose_name_plural = 'Generic Images'


class MobileWebActivity(Base, Slugged):
    logo = models.ImageField(upload_to='activity_logos', blank=True)

    class Meta:
        verbose_name = 'Mobile/Web Activity'
        verbose_name_plural = 'Mobile/Web Activities'


# The primary models used for handling country data are defined below.

class Country(Base, Slugged):
    calling_code = models.PositiveSmallIntegerField()
    iso_code = models.CharField(max_length=10, unique=True)
    capital = models.CharField(max_length=75)
    currency = models.EmbeddedModelField(model_container=Currency)
    marker_latitude = models.DecimalField(max_digits=8, decimal_places=5)
    marker_longitude = models.DecimalField(max_digits=8, decimal_places=5)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class CountryDetailsGeneral(Base):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    area = models.BigIntegerField()
    population = models.BigIntegerField()
    languages = models.ArrayModelField(
            model_container=InfoMeta,
            model_form_class=LanguageForm)
    religions = models.ArrayModelField(
            model_container=InfoMeta,
            model_form_class=ReligionForm)
    highlights = models.ArrayModelField(model_container=InfoMeta, blank=True)
    extra_comments = models.TextField(blank=True)

    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name = 'Country Details - General'
        verbose_name_plural = 'Country Details - General'


class CountryDetailsEconomy(Base):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    gdp_total = models.DecimalField(
            max_digits=24, decimal_places=2, blank=True)
    gdp_per_capita = models.DecimalField(max_digits=10, decimal_places=2)
    gdp_growth_rate = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True)
    unemployment_rate = models.DecimalField(max_digits=5, decimal_places=2)
    political_stability_index = models.EmbeddedModelField(
            model_container=PoliticalStability)
    economy_details_year = models.CharField(max_length=20, blank=True)
    highlights = models.ArrayModelField(model_container=InfoMeta, blank=True)
    extra_comments = models.TextField(blank=True)

    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name = 'Country Details - Economy'
        verbose_name_plural = 'Country Details - Economy'


class CountryDetailsDemographicsAge(Base):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    median = models.DecimalField(max_digits=5, decimal_places=2)
    distribution = models.ArrayModelField(
            model_container=GenericRangeDistribution,
            model_form_class=GenericRangeDistributionForm)
    distribution_indicator = models.CharField(max_length=75, blank=True)
    distribution_year = models.CharField(max_length=20, blank=True)
    distribution_value_type = models.CharField(
            max_length=20, choices=ValueType.CHOICES,
            default=ValueType.PERCENTAGE)
    highlights = models.ArrayModelField(model_container=InfoMeta, blank=True)
    extra_comments = models.TextField(blank=True)

    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name = 'Country Details - Age Demographics'
        verbose_name_plural = 'Country Details - Age Demographics'


class CountryDetailsBusinessImport(Base):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    partner_countries = models.ArrayModelField(
            model_container=CountryDistribution,
            model_form_class=CountryDistributionForm)
    partner_countries_indicator = models.CharField(max_length=75, blank=True)
    partner_countries_year = models.CharField(max_length=20, blank=True)
    partner_countries_value_type = models.CharField(
            max_length=20, choices=ValueType.CHOICES,
            default=ValueType.PERCENTAGE)
    partner_countries_products = models.ArrayModelField(
            model_container=CountryGoodsDistribution,
            model_form_class=CountryGoodsDistributionForm)
    partner_countries_products_indicator = models.CharField(
        max_length=75, blank=True)
    partner_countries_products_year = models.CharField(
        max_length=20, blank=True)
    partner_countries_products_value_type = models.CharField(
            max_length=20, choices=ValueType.CHOICES,
            default=ValueType.PERCENTAGE)
    imported_items = models.ArrayModelField(
            model_container=GoodsDistribution,
            model_form_class=GoodsDistributionForm)
    imported_items_indicator = models.CharField(max_length=75, blank=True)
    imported_items_year = models.CharField(max_length=20, blank=True)
    imported_items_value_type = models.CharField(
            max_length=20, choices=ValueType.CHOICES,
            default=ValueType.PERCENTAGE)
    total_yearly_imports = models.ArrayModelField(
        model_container=YearDistribution, blank=True)
    highlights = models.ArrayModelField(model_container=InfoMeta, blank=True)
    extra_comments = models.TextField(blank=True)

    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name = 'Country Details - Business Imports'
        verbose_name_plural = 'Country Details - Business Imports'


class CountryDetailsBusinessExport(Base):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    trade_to_gdp_ratio = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True)
    partner_countries = models.ArrayModelField(
            model_container=CountryDistribution,
            model_form_class=CountryDistributionForm)
    partner_countries_indicator = models.CharField(max_length=75, blank=True)
    partner_countries_year = models.CharField(max_length=20, blank=True)
    partner_countries_value_type = models.CharField(
            max_length=20, choices=ValueType.CHOICES,
            default=ValueType.PERCENTAGE)
    partner_countries_products = models.ArrayModelField(
            model_container=CountryGoodsDistribution,
            model_form_class=CountryGoodsDistributionForm)
    partner_countries_products_indicator = models.CharField(
        max_length=75, blank=True)
    partner_countries_products_year = models.CharField(
        max_length=20, blank=True)
    partner_countries_products_value_type = models.CharField(
            max_length=20, choices=ValueType.CHOICES,
            default=ValueType.PERCENTAGE)
    exported_items = models.ArrayModelField(
            model_container=GoodsDistribution,
            model_form_class=GoodsDistributionForm)
    exported_items_indicator = models.CharField(max_length=75, blank=True)
    exported_items_year = models.CharField(max_length=20, blank=True)
    exported_items_value_type = models.CharField(
            max_length=20, choices=ValueType.CHOICES,
            default=ValueType.PERCENTAGE)
    total_yearly_exports = models.ArrayModelField(
        model_container=YearDistribution, blank=True)
    highlights = models.ArrayModelField(model_container=InfoMeta, blank=True)
    extra_comments = models.TextField(blank=True)

    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name = 'Country Details - Business Exports'
        verbose_name_plural = 'Country Details - Business Exports'


class CountryDetailsBusinessFDI(Base):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    yearly_net_inflow = models.ArrayModelField(
        model_container=YearDistribution)
    net_inflow_indicator = models.CharField(max_length=75, blank=True)
    net_inflow_year = models.CharField(max_length=20, blank=True)
    net_inflow_value_type = models.CharField(
            max_length=20, choices=ValueType.CHOICES,
            default=ValueType.PERCENTAGE)
    investor_countries = models.ArrayModelField(
            model_container=CountryDistribution,
            model_form_class=CountryDistributionForm)
    investor_countries_indicator = models.CharField(max_length=75, blank=True)
    investor_countries_year = models.CharField(max_length=20, blank=True)
    investor_countries_value_type = models.CharField(
            max_length=20, choices=ValueType.CHOICES,
            default=ValueType.PERCENTAGE)
    top_sectors = models.ArrayModelField(
            model_container=IndustrySectorDistribution,
            model_form_class=IndustrySectorDistributionForm,
            blank=True)
    top_sectors_indicator = models.CharField(max_length=75, blank=True)
    top_sectors_year = models.CharField(max_length=20, blank=True)
    top_sectors_value_type = models.CharField(
            max_length=20, choices=ValueType.CHOICES,
            default=ValueType.PERCENTAGE)
    highlights = models.ArrayModelField(model_container=InfoMeta, blank=True)
    extra_comments = models.TextField(blank=True)

    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name = 'Country Details - Business FDIs'
        verbose_name_plural = 'Country Details - Business FDIs'


class CountryDetailsFTA(Base, Slugged):
    description = models.TextField(blank=True)
    associated_countries = models.ManyToManyField(
        Country, blank=True)
    coverage_type = models.CharField(
        max_length=20, choices=FTACoverageType.CHOICES)
    trade_descriptions = models.ArrayModelField(
        model_container=DescriptionDistribution, blank=True)
    trade_links = models.ArrayModelField(
        model_container=LinksDistribution, blank=True)
    industry_country_benefits = models.ArrayModelField(
        model_container=CountryIndustryDistribution,
        model_form_class=CountryIndustryDistributionForm, blank=True)
    highlights = models.ArrayModelField(model_container=InfoMeta, blank=True)
    extra_comments = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Country Details - FTA'
        verbose_name_plural = 'Country Details - FTAs'


class CountryDetailsBusinessFTA(Base):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    associated_countries = models.ManyToManyField(
        Country, related_name='business_details', blank=True)
    highlights = models.ArrayModelField(model_container=InfoMeta, blank=True)

    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name = 'Country Details - Business FTAs'
        verbose_name_plural = 'Country Details - Business FTAs'


class CountryDetailsBusinessInvestmentReasons(Base):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    reasons = models.ArrayModelField(model_container=InfoMeta)
    links = models.ArrayModelField(
        model_container=LinksDistribution, blank=True)
    highlights = models.ArrayModelField(model_container=InfoMeta, blank=True)
    extra_comments = models.TextField(blank=True)

    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name = 'Country Details - Investment Reasons'
        verbose_name_plural = 'Country Details - Investment Reasons'


class CountryDetailsBusinessInvestmentSectors(Base):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    key_sectors = models.ManyToManyField(SubSector, blank=True)
    key_industry_sectors = models.ArrayModelField(
        model_container=IndustrySectorDescription,
        model_form_class=IndustrySectorDescriptionForm)
    highlights = models.ArrayModelField(model_container=InfoMeta, blank=True)
    extra_comments = models.TextField(blank=True)

    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name = 'Country Details - Investment Sectors'
        verbose_name_plural = 'Country Details - Investment Sectors'


class CountryDetailsMobileUsage(Base):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    total_phones = models.BigIntegerField()
    distribution = models.ArrayModelField(
        model_container=GoodsDistribution,
        model_form_class=GoodsDistributionForm)
    distribution_indicator = models.CharField(max_length=75, blank=True)
    distribution_year = models.CharField(max_length=20, blank=True)
    distribution_value_type = models.CharField(
        max_length=20, choices=ValueType.CHOICES,
        default=ValueType.PERCENTAGE)
    top_activities = models.ArrayModelField(
        model_container=MobileActivityDistribution,
        model_form_class=MobileActivityDistributionForm,
        blank=True)
    top_activities_indicator = models.CharField(max_length=75, blank=True)
    top_activities_year = models.CharField(max_length=20, blank=True)
    top_activities_value_type = models.CharField(
        max_length=20, choices=ValueType.CHOICES,
        default=ValueType.PERCENTAGE)
    traffic_distribution = models.ArrayModelField(
        model_container=GoodsDistribution,
        model_form_class=GoodsDistributionForm,
        blank=True)
    traffic_distribution_indicator = models.CharField(
        max_length=75, blank=True)
    traffic_distribution_year = models.CharField(max_length=20, blank=True)
    traffic_distribution_value_type = models.CharField(
        max_length=20, choices=ValueType.CHOICES,
        default=ValueType.PERCENTAGE)
    top_messaging_apps = models.ArrayModelField(
        model_container=ServiceDistribution,
        model_form_class=ServiceDistributionForm,
        blank=True)
    top_messaging_apps_indicator = models.CharField(max_length=75, blank=True)
    top_messaging_apps_year = models.CharField(max_length=20, blank=True)
    top_messaging_apps_value_type = models.CharField(
        max_length=20, choices=ValueType.CHOICES,
        default=ValueType.PERCENTAGE)
    top_apps = models.ArrayModelField(
        model_container=AppDistribution,
        model_form_class=AppDistributionForm,
        blank=True)
    top_apps_indicator = models.CharField(max_length=75, blank=True)
    top_apps_year = models.CharField(max_length=20, blank=True)
    highlights = models.ArrayModelField(model_container=InfoMeta, blank=True)
    extra_comments = models.TextField(blank=True)

    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name = 'Country Details - Mobile Usage'
        verbose_name_plural = 'Country Details - Mobile Usage'


class CountryDetailsServicesUsage(Base):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    social_media_distribution = models.ArrayModelField(
        model_container=ServiceDistribution,
        model_form_class=ServiceDistributionForm,
        blank=True)
    social_media_distribution_indicator = models.CharField(
        max_length=75, blank=True)
    social_media_distribution_year = models.CharField(
        max_length=20, blank=True)
    social_media_distribution_value_type = models.CharField(
        max_length=20, choices=ValueType.CHOICES,
        default=ValueType.PERCENTAGE)
    social_media_insights = models.ArrayModelField(
        model_container=InfoMeta, blank=True)
    social_media_gender_profile = models.ArrayModelField(
        model_container=ServiceGenderDistribution,
        model_form_class=ServiceGenderDistributionForm,
        blank=True)
    social_media_gender_profile_indicator = models.CharField(
        max_length=75, blank=True)
    social_media_gender_profile_year = models.CharField(
        max_length=20, blank=True)
    social_media_gender_profile_value_type = models.CharField(
        max_length=20, choices=ValueType.CHOICES,
        default=ValueType.PERCENTAGE)
    social_media_mobile_usage = models.ArrayModelField(
        model_container=ServiceDistribution,
        model_form_class=ServiceDistributionForm,
        blank=True)
    social_media_mobile_usage_indicator = models.CharField(
        max_length=75, blank=True)
    social_media_mobile_usage_year = models.CharField(
        max_length=20, blank=True)
    social_media_mobile_usage_value_type = models.CharField(
        max_length=20, choices=ValueType.CHOICES,
        default=ValueType.PERCENTAGE)
    social_media_daily_platform_usage = models.ArrayModelField(
        model_container=ServiceDistribution,
        model_form_class=ServiceDistributionForm,
        blank=True)
    social_media_daily_platform_usage_indicator = models.CharField(
        max_length=75, blank=True)
    social_media_daily_platform_usage_year = models.CharField(
        max_length=20, blank=True)
    social_media_daily_platform_usage_value_type = models.CharField(
        max_length=20, choices=ValueType.CHOICES,
        default=ValueType.PERCENTAGE)
    ecommerce_distribution = models.ArrayModelField(
        model_container=ServiceDistribution,
        model_form_class=ServiceDistributionForm,
        blank=True)
    ecommerce_distribution_indicator = models.CharField(
        max_length=75, blank=True)
    ecommerce_distribution_year = models.CharField(max_length=20, blank=True)
    ecommerce_distribution_value_type = models.CharField(
        max_length=20, choices=ValueType.CHOICES,
        default=ValueType.PERCENTAGE)
    ecommerce_penetration = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True)
    ecommerce_penetration_indicator = models.CharField(
        max_length=255, blank=True)
    ecommerce_market_value = models.DecimalField(
        max_digits=24, decimal_places=2, blank=True)
    ecommerce_insights = models.ArrayModelField(
        model_container=InfoMeta, blank=True)
    digital_payments_distribution = models.ArrayModelField(
        model_container=ServiceDistribution,
        model_form_class=ServiceDistributionForm,
        blank=True)
    digital_payments_distribution_indicator = models.CharField(
        max_length=75, blank=True)
    digital_payments_distribution_year = models.CharField(
        max_length=20, blank=True)
    digital_payments_distribution_value_type = models.CharField(
        max_length=20, choices=ValueType.CHOICES,
        default=ValueType.PERCENTAGE)
    fin_account_ownership = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True)
    credit_card_ownership = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True)
    digital_transactions_last_year = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True)
    digital_payments_insights = models.ArrayModelField(
        model_container=InfoMeta, blank=True)
    highlights = models.ArrayModelField(model_container=InfoMeta, blank=True)
    extra_comments = models.TextField(blank=True)

    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name = 'Country Details - Services Usage'
        verbose_name_plural = 'Country Details - Services Usage'


class CountryDetailsServiceUsage(Base):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    service_type = models.CharField(max_length=30, choices=ServiceType.CHOICES)
    distribution = models.ArrayModelField(
            model_container=ServiceDistribution,
            model_form_class=ServiceDistributionForm)
    distribution_indicator = models.CharField(max_length=75, blank=True)
    distribution_year = models.CharField(max_length=20, blank=True)
    distribution_value_type = models.CharField(
            max_length=20, choices=ValueType.CHOICES,
            default=ValueType.PERCENTAGE)
    highlights = models.ArrayModelField(model_container=InfoMeta, blank=True)
    extra_comments = models.TextField(blank=True)

    def __str__(self):
        return '{} - {}'.format(self.service_type, self.country.name)

    class Meta:
        verbose_name = 'Country Details - Service Usage'
        verbose_name_plural = 'Country Details - Service Usage'


class CountryPolicy(Base, Slugged):
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    origin_country = models.ForeignKey(Country, on_delete=models.PROTECT)
    associated_countries = models.ManyToManyField(
            Country, related_name='policy_countries', blank=True)

    def __str__(self):
        return '{} - {}'.format(self.origin_country.name, self.name)

    class Meta:
        verbose_name = 'Policy'
        verbose_name_plural = 'Policies'


class CountryPolicyRegion(Base):
    policy = models.ForeignKey(
            CountryPolicy, related_name='regions', on_delete=models.PROTECT)
    region = models.CharField(max_length=75)
    region_latitude = models.DecimalField(max_digits=8, decimal_places=5)
    region_longitude = models.DecimalField(max_digits=8, decimal_places=5)
    region_zoom = models.FloatField(default=4.0)
    countries = models.ManyToManyField(Country, blank=True)

    def __str__(self):
        return '{} - {} - {}'.format(
                self.policy.origin_country.name, self.region,
                self.policy.name)

    class Meta:
        verbose_name = 'Policy Region'
        verbose_name_plural = 'Policy Regions'


class CountryPolicyLine(Base):
    policy = models.ForeignKey(
            CountryPolicy, related_name='lines', on_delete=models.PROTECT)
    color = models.CharField(max_length=7)
    width = models.FloatField()
    route_type = models.CharField(
            max_length=50, choices=RouteType.CHOICES, default=RouteType.LAND)
    waypoints = models.ArrayModelField(model_container=GeoCoordinates)

    def __str__(self):
        return '{} - {}'.format(
                self.policy.origin_country.name, self.policy.name)

    class Meta:
        verbose_name = 'Policy Line'
        verbose_name_plural = 'Policy Lines'


# The following model is for storing lead generation data

class Lead(Base):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=75)
    company = models.CharField(max_length=75, blank=True)
    description = models.TextField(blank=True)
    source_ip = models.CharField(max_length=50, blank=True)
    lead_owner = models.CharField(
            max_length=75, default='weiliang.ho@goldenequator.com')
    lead_source = models.CharField(max_length=50, default='Insights')

    def __str__(self):
        return '{} - {}'.format(self.email, self.company)

    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
