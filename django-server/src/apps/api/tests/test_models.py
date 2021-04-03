from django.test import TestCase
from ..constants import ServiceType
from core.models import InfoMeta
from ..models import (
        Currency, Country, CountryDetailsGeneral, CountryDetailsEconomy,
        CountryDetailsDemographicsAge, CountryDetailsBusinessExport,
        CountryDetailsBusinessFDI, CountryDetailsBusinessFTA,
        CountryDetailsBusinessInvestmentReasons,
        CountryDetailsBusinessInvestmentSectors, CountryDetailsMobileUsage,
        CountryDetailsServiceUsage, Language, Religion, Service,
        Goods, Sector, SubSector, CountryPolicy, CountryPolicyLine, Lead,
        GenericImage, CountryPolicyRegion, PoliticalStability,
        GenericRangeDistribution, CountryDistribution, GoodsDistribution,
        ServiceDistribution, GeoCoordinates)


class LanguageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        kwargs = {
            'name': 'English',
        }
        cls.instance = Language.objects.create(**kwargs)

    def test_object_str(self):
        instance = Language.objects.get(id=self.instance.id)
        self.assertEquals(str(instance), instance.name)


class ReligionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        kwargs = {
            'name': 'Christianity',
        }
        cls.instance = Religion.objects.create(**kwargs)

    def test_object_str(self):
        instance = Religion.objects.get(id=self.instance.id)
        self.assertEquals(str(instance), instance.name)


class ServiceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        kwargs = {
            'name': 'Amazon',
            'description': 'An e-commerce company started by Jeff Bezos.',
            'color': '#000000',
            'company': 'Amazon Inc.',
        }
        cls.instance = Service.objects.create(**kwargs)

    def test_object_str(self):
        instance = Service.objects.get(id=self.instance.id)
        self.assertEquals(str(instance), instance.name)


class GoodsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        kwargs = {
            'name': 'Cars',
        }
        cls.instance = Goods.objects.create(**kwargs)

    def test_object_str(self):
        instance = Goods.objects.get(id=self.instance.id)
        self.assertEquals(str(instance), instance.name)


class SectorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        kwargs = {
            'name': 'Energy',
        }
        cls.instance = Sector.objects.create(**kwargs)

    def test_object_str(self):
        instance = Sector.objects.get(id=self.instance.id)
        self.assertEquals(str(instance), instance.name)


class SubSectorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        sector_kwargs = {
            'name': 'ICT',
        }
        sector = Sector.objects.create(**sector_kwargs)
        kwargs = {
            'name': 'IOT',
            'sector': sector,
        }
        cls.instance = SubSector.objects.create(**kwargs)

    def test_object_str(self):
        instance = SubSector.objects.get(id=self.instance.id)
        self.assertEquals(str(instance), instance.name)


class GenericImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        kwargs = {
            'name': 'Sample Image',
        }
        cls.instance = GenericImage.objects.create(**kwargs)

    def test_object_str(self):
        instance = GenericImage.objects.get(id=self.instance.id)
        self.assertEquals(str(instance), instance.name)


class CountryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.mongo_delete_many({})
        currency_kwargs = {
            'name': 'Indian rupee',
            'iso_code': 'INR',
            'symbol': '₹',
        }
        currency = Currency(**currency_kwargs)
        kwargs = {
            'name': 'India',
            'calling_code': 91,
            'iso_code': 'IN',
            'capital': 'New Delhi',
            'currency': currency,
            'marker_latitude': 1.11111,
            'marker_longitude': 1.11111,
        }
        cls.instance = Country.objects.create(**kwargs)

    def test_object_str(self):
        instance = Country.objects.get(id=self.instance.id)
        self.assertEquals(str(instance), instance.name)


class CountryDetailsGeneralModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.mongo_delete_many({})
        language_kwargs = {
            'title': 'english',
        }
        language = InfoMeta(**language_kwargs)
        religion_kwargs = {
            'title': 'christiality',
        }
        religion = InfoMeta(**religion_kwargs)
        currency_kwargs = {
            'name': 'Indian rupee',
            'iso_code': 'INR',
            'symbol': '₹',
        }
        currency = Currency(**currency_kwargs)
        highlights_kwargs = {
            'title': 'Sample Title',
            'description': 'Sample Description',
        }
        highlights = InfoMeta(**highlights_kwargs)
        country_kwargs = {
            'name': 'India',
            'calling_code': 91,
            'iso_code': 'IN',
            'capital': 'New Delhi',
            'currency': currency,
            'marker_latitude': 1.11111,
            'marker_longitude': 1.11111,
        }
        country = Country.objects.create(**country_kwargs)
        kwargs = {
            'country': country,
            'area': 12345678,
            'population': 12345678,
            'languages': [language],
            'religions': [religion],
            'highlights': [highlights],
        }
        country_details_general = CountryDetailsGeneral.objects.create(
                **kwargs)
        cls.instance = country_details_general

    def test_object_str(self):
        instance = CountryDetailsGeneral.objects.get(id=self.instance.id)
        self.assertEquals(str(instance), instance.country.name)


class CountryDetailsEconomyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.mongo_delete_many({})
        currency_kwargs = {
            'name': 'Indian rupee',
            'iso_code': 'INR',
            'symbol': '₹',
        }
        currency = Currency(**currency_kwargs)
        highlights_kwargs = {
            'title': 'Sample Title',
            'description': 'Sample Description',
        }
        highlights = InfoMeta(**highlights_kwargs)
        country_kwargs = {
            'name': 'India',
            'calling_code': 91,
            'iso_code': 'IN',
            'capital': 'New Delhi',
            'currency': currency,
            'marker_latitude': 1.11111,
            'marker_longitude': 1.11111,
        }
        country = Country.objects.create(**country_kwargs)
        political_stability_kwargs = {
            'rank': 1,
            'total_countries': 198,
        }
        political_stability = PoliticalStability(**political_stability_kwargs)
        kwargs = {
            'country': country,
            'gdp_total': 12345678,
            'gdp_per_capita': 12345678,
            'unemployment_rate': 10,
            'political_stability_index': political_stability,
            'highlights': [highlights],
        }
        country_details_economy = CountryDetailsEconomy.objects.create(
                **kwargs)
        cls.instance = country_details_economy

    def test_object_str(self):
        instance = CountryDetailsEconomy.objects.get(id=self.instance.id)
        self.assertEquals(str(instance), instance.country.name)


class CountryDetailsDemographicsAgeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.mongo_delete_many({})
        currency_kwargs = {
            'name': 'Indian rupee',
            'iso_code': 'INR',
            'symbol': '₹',
        }
        currency = Currency(**currency_kwargs)
        highlights_kwargs = {
            'title': 'Sample Title',
            'description': 'Sample Description',
        }
        highlights = InfoMeta(**highlights_kwargs)
        country_kwargs = {
            'name': 'India',
            'calling_code': 91,
            'iso_code': 'IN',
            'capital': 'New Delhi',
            'currency': currency,
            'marker_latitude': 1.11111,
            'marker_longitude': 1.11111,
        }
        country = Country.objects.create(**country_kwargs)
        distribution_kwargs = {
            'range_min': 1,
            'range_max': 10,
            'label': 'Sample',
            'value': 12345678
        }
        distribution = GenericRangeDistribution(**distribution_kwargs)
        kwargs = {
            'country': country,
            'median': 50,
            'distribution': [distribution],
            'distribution_indicator': 'Distribution',
            'distribution_year': '2018',
            'highlights': [highlights],
        }
        country_demographics = CountryDetailsDemographicsAge.objects.create(
                **kwargs)
        cls.instance = country_demographics

    def test_object_str(self):
        instance = CountryDetailsDemographicsAge.objects.get(
                id=self.instance.id)
        self.assertEquals(str(instance), instance.country.name)


class CountryDetailsBusinessExportModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.mongo_delete_many({})
        currency_kwargs = {
            'name': 'Indian rupee',
            'iso_code': 'INR',
            'symbol': '₹',
        }
        currency = Currency(**currency_kwargs)
        highlights_kwargs = {
            'title': 'Sample Title',
            'description': 'Sample Description',
        }
        highlights = InfoMeta(**highlights_kwargs)
        country_kwargs = {
            'name': 'India',
            'calling_code': 91,
            'iso_code': 'IN',
            'capital': 'New Delhi',
            'currency': currency,
            'marker_latitude': 1.11111,
            'marker_longitude': 1.11111,
        }
        country = Country.objects.create(**country_kwargs)
        country_distribution_kwargs = {
            'country': 'india',
            'value': 12345678
        }
        country_distribution = CountryDistribution(
                **country_distribution_kwargs)
        goods_distribution_kwargs = {
            'product': 'cars',
            'value': 12345678
        }
        goods_distribution = GoodsDistribution(**goods_distribution_kwargs)
        kwargs = {
            'country': country,
            'partner_countries': [country_distribution],
            'partner_countries_indicator': 'Partners',
            'partner_countries_year': '2018',
            'exported_items': [goods_distribution],
            'exported_items_indicator': 'Distribution',
            'exported_items_year': '2018',
            'highlights': [highlights],
        }
        country_export = CountryDetailsBusinessExport.objects.create(
                **kwargs)
        cls.instance = country_export

    def test_object_str(self):
        instance = CountryDetailsBusinessExport.objects.get(
                id=self.instance.id)
        self.assertEquals(str(instance), instance.country.name)


class CountryDetailsBusinessFDIModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.mongo_delete_many({})
        currency_kwargs = {
            'name': 'Indian rupee',
            'iso_code': 'INR',
            'symbol': '₹',
        }
        currency = Currency(**currency_kwargs)
        highlights_kwargs = {
            'title': 'Sample Title',
            'description': 'Sample Description',
        }
        highlights = InfoMeta(**highlights_kwargs)
        country_kwargs = {
            'name': 'India',
            'calling_code': 91,
            'iso_code': 'IN',
            'capital': 'New Delhi',
            'currency': currency,
            'marker_latitude': 1.11111,
            'marker_longitude': 1.11111,
        }
        country = Country.objects.create(**country_kwargs)
        country_distribution_kwargs = {
            'country': 'india',
            'value': 12345678
        }
        country_distribution = CountryDistribution(
                **country_distribution_kwargs)
        distribution_kwargs = {
            'range_min': 1,
            'range_max': 10,
            'label': 'Sample',
            'value': 12345678
        }
        distribution = GenericRangeDistribution(**distribution_kwargs)
        kwargs = {
            'country': country,
            'net_inflow': [distribution],
            'net_inflow_indicator': 'Inflow',
            'net_inflow_year': '2018',
            'investor_countries': [country_distribution],
            'investor_countries_indicator': 'Distribution',
            'investor_countries_year': '2018',
            'highlights': [highlights],
        }
        country_fdi = CountryDetailsBusinessFDI.objects.create(
                **kwargs)
        cls.instance = country_fdi

    def test_object_str(self):
        instance = CountryDetailsBusinessFDI.objects.get(
                id=self.instance.id)
        self.assertEquals(str(instance), instance.country.name)


class CountryDetailsBusinessFTAModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.mongo_delete_many({})
        currency_kwargs = {
            'name': 'Indian rupee',
            'iso_code': 'INR',
            'symbol': '₹',
        }
        currency = Currency(**currency_kwargs)
        highlights_kwargs = {
            'title': 'Sample Title',
            'description': 'Sample Description',
        }
        highlights = InfoMeta(**highlights_kwargs)
        country_kwargs = {
            'name': 'India',
            'calling_code': 91,
            'iso_code': 'IN',
            'capital': 'New Delhi',
            'currency': currency,
            'marker_latitude': 1.11111,
            'marker_longitude': 1.11111,
        }
        country = Country.objects.create(**country_kwargs)
        kwargs = {
            'country': country,
            'highlights': [highlights],
        }
        country_fta = CountryDetailsBusinessFTA.objects.create(
                **kwargs)
        country_fta.associated_countries.add(country)
        cls.instance = country_fta

    def test_object_str(self):
        instance = CountryDetailsBusinessFTA.objects.get(
                id=self.instance.id)
        self.assertEquals(str(instance), instance.country.name)


class CountryDetailsBusinessInvestmentReasonsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.mongo_delete_many({})
        currency_kwargs = {
            'name': 'Indian rupee',
            'iso_code': 'INR',
            'symbol': '₹',
        }
        currency = Currency(**currency_kwargs)
        highlights_kwargs = {
            'title': 'Sample Title',
            'description': 'Sample Description',
        }
        highlights = InfoMeta(**highlights_kwargs)
        country_kwargs = {
            'name': 'India',
            'calling_code': 91,
            'iso_code': 'IN',
            'capital': 'New Delhi',
            'currency': currency,
            'marker_latitude': 1.11111,
            'marker_longitude': 1.11111,
        }
        country = Country.objects.create(**country_kwargs)
        kwargs = {
            'country': country,
            'reasons': [highlights],
            'highlights': [highlights],
        }
        country_investment_reasons = (
                CountryDetailsBusinessInvestmentReasons.objects.create(
                    **kwargs))
        cls.instance = country_investment_reasons

    def test_object_str(self):
        instance = CountryDetailsBusinessInvestmentReasons.objects.get(
                id=self.instance.id)
        self.assertEquals(str(instance), instance.country.name)


class CountryDetailsBusinessInvestmentSectorsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.mongo_delete_many({})
        currency_kwargs = {
            'name': 'Indian rupee',
            'iso_code': 'INR',
            'symbol': '₹',
        }
        currency = Currency(**currency_kwargs)
        highlights_kwargs = {
            'title': 'Sample Title',
            'description': 'Sample Description',
        }
        highlights = InfoMeta(**highlights_kwargs)
        country_kwargs = {
            'name': 'India',
            'calling_code': 91,
            'iso_code': 'IN',
            'capital': 'New Delhi',
            'currency': currency,
            'marker_latitude': 1.11111,
            'marker_longitude': 1.11111,
        }
        country = Country.objects.create(**country_kwargs)
        sector_kwargs = {
            'name': 'ICT',
        }
        sector = Sector.objects.create(**sector_kwargs)
        sub_sector_kwargs = {
            'name': 'IOT',
            'sector_id': sector.id,
        }
        sub_sector = SubSector.objects.create(**sub_sector_kwargs)
        kwargs = {
            'country': country,
            'highlights': [highlights],
        }
        country_investment_sectors = (
                CountryDetailsBusinessInvestmentSectors.objects.create(
                    **kwargs))
        country_investment_sectors.key_sectors.add(sub_sector)
        cls.instance = country_investment_sectors

    def test_object_str(self):
        instance = CountryDetailsBusinessInvestmentSectors.objects.get(
                id=self.instance.id)
        self.assertEquals(str(instance), instance.country.name)


class CountryDetailsMobileUsageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.mongo_delete_many({})
        currency_kwargs = {
            'name': 'Indian rupee',
            'iso_code': 'INR',
            'symbol': '₹',
        }
        currency = Currency(**currency_kwargs)
        highlights_kwargs = {
            'title': 'Sample Title',
            'description': 'Sample Description',
        }
        highlights = InfoMeta(**highlights_kwargs)
        country_kwargs = {
            'name': 'India',
            'calling_code': 91,
            'iso_code': 'IN',
            'capital': 'New Delhi',
            'currency': currency,
            'marker_latitude': 1.11111,
            'marker_longitude': 1.11111,
        }
        country = Country.objects.create(**country_kwargs)
        goods_distribution_kwargs = {
            'product': 'cars',
            'value': 12345678
        }
        goods_distribution = GoodsDistribution(**goods_distribution_kwargs)
        kwargs = {
            'country': country,
            'total_phones': 12345678,
            'distribution': [goods_distribution],
            'distribution_indicator': 'Distribution',
            'distribution_year': '2018',
            'highlights': [highlights],
        }
        country_mobile = CountryDetailsMobileUsage.objects.create(
                **kwargs)
        cls.instance = country_mobile

    def test_object_str(self):
        instance = CountryDetailsMobileUsage.objects.get(
                id=self.instance.id)
        self.assertEquals(str(instance), instance.country.name)


class CountryDetailsServiceUsageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.mongo_delete_many({})
        currency_kwargs = {
            'name': 'Indian rupee',
            'iso_code': 'INR',
            'symbol': '₹',
        }
        currency = Currency(**currency_kwargs)
        highlights_kwargs = {
            'title': 'Sample Title',
            'description': 'Sample Description',
        }
        highlights = InfoMeta(**highlights_kwargs)
        country_kwargs = {
            'name': 'India',
            'calling_code': 91,
            'iso_code': 'IN',
            'capital': 'New Delhi',
            'currency': currency,
            'marker_latitude': 1.11111,
            'marker_longitude': 1.11111,
        }
        country = Country.objects.create(**country_kwargs)
        service_distribution_kwargs = {
            'product': 'cars',
            'value': 12345678
        }
        service_distribution = ServiceDistribution(
                **service_distribution_kwargs)
        kwargs = {
            'country': country,
            'service_type': ServiceType.SOCIAL_MEDIA,
            'distribution': [service_distribution],
            'distribution_indicator': 'Distribution',
            'distribution_year': '2018',
            'highlights': [highlights],
        }
        country_service = CountryDetailsServiceUsage.objects.create(
                **kwargs)
        cls.instance = country_service

    def test_object_str(self):
        instance = CountryDetailsServiceUsage.objects.get(
                id=self.instance.id)
        self.assertEquals(str(instance), '{} - {}'.format(
            instance.service_type, instance.country.name))


class CountryPolicyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.mongo_delete_many({})
        currency_kwargs = {
            'name': 'Indian rupee',
            'iso_code': 'INR',
            'symbol': '₹',
        }
        currency = Currency(**currency_kwargs)
        country_kwargs = {
            'name': 'India',
            'calling_code': 91,
            'iso_code': 'IN',
            'capital': 'New Delhi',
            'currency': currency,
            'marker_latitude': 1.11111,
            'marker_longitude': 1.11111,
        }
        country = Country.objects.create(**country_kwargs)
        kwargs = {
            'name': 'Sample Policy',
            'description': 'Sample Description',
            'short_description': 'Short Description',
            'origin_country': country,
        }
        country_policy = CountryPolicy.objects.create(**kwargs)
        country_policy.associated_countries.add(country)
        cls.instance = country_policy

    def test_object_str(self):
        instance = CountryPolicy.objects.get(id=self.instance.id)
        self.assertEquals(str(instance), '{} - {}'.format(
            instance.origin_country.name, instance.name))


class CountryPolicyRegionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.mongo_delete_many({})
        currency_kwargs = {
            'name': 'Indian rupee',
            'iso_code': 'INR',
            'symbol': '₹',
        }
        currency = Currency(**currency_kwargs)
        country_kwargs = {
            'name': 'India',
            'calling_code': 91,
            'iso_code': 'IN',
            'capital': 'New Delhi',
            'currency': currency,
            'marker_latitude': 1.11111,
            'marker_longitude': 1.11111,
        }
        country = Country.objects.create(**country_kwargs)
        policy_kwargs = {
            'name': 'Sample Policy',
            'description': 'Sample Description',
            'short_description': 'Short Description',
            'origin_country': country,
        }
        country_policy = CountryPolicy.objects.create(**policy_kwargs)
        country_policy.associated_countries.add(country)
        kwargs = {
            'policy': country_policy,
            'region': 'Eastern',
            'region_latitude': 1.11111,
            'region_longitude': 1.11111,
            'region_zoom': 2.5,
        }
        country_policy_region = CountryPolicyRegion.objects.create(**kwargs)
        country_policy_region.countries.add(country)
        cls.instance = country_policy_region

    def test_object_str(self):
        instance = CountryPolicyRegion.objects.get(id=self.instance.id)
        self.assertEquals(str(instance), '{} - {} - {}'.format(
            instance.policy.origin_country.name, instance.region,
            instance.policy.name))


class CountryPolicyLineModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.mongo_delete_many({})
        currency_kwargs = {
            'name': 'Indian rupee',
            'iso_code': 'INR',
            'symbol': '₹',
        }
        currency = Currency(**currency_kwargs)
        country_kwargs = {
            'name': 'India',
            'calling_code': 91,
            'iso_code': 'IN',
            'capital': 'New Delhi',
            'currency': currency,
            'marker_latitude': 1.11111,
            'marker_longitude': 1.11111,
        }
        country = Country.objects.create(**country_kwargs)
        policy_kwargs = {
            'name': 'Sample Policy',
            'description': 'Sample Description',
            'short_description': 'Short Description',
            'origin_country': country,
        }
        country_policy = CountryPolicy.objects.create(**policy_kwargs)
        country_policy.associated_countries.add(country)
        waypoint_kwargs = {
            'latitude': 1.11111,
            'longitude': 1.11111,
            'label': 'Waypoint 1',
        }
        waypoint = GeoCoordinates(**waypoint_kwargs)
        kwargs = {
            'policy': country_policy,
            'color': '#000000',
            'width': 1.5,
            'waypoints': [waypoint],
        }
        country_policy_line = CountryPolicyLine.objects.create(**kwargs)
        cls.instance = country_policy_line

    def test_object_str(self):
        instance = CountryPolicyLine.objects.get(id=self.instance.id)
        self.assertEquals(str(instance), '{} - {}'.format(
            instance.policy.origin_country.name, instance.policy.name))


class LeadModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        kwargs = {
            'first_name': 'Adam',
            'last_name': 'Warlock',
            'email': 'adam.warlock@marvel.com',
            'company': 'Marvel Inc.',
            'description': 'The Marvel Superhero.',
            'source_ip': '127.0.0.1',
        }
        lead = Lead.objects.create(**kwargs)
        cls.instance = lead

    def test_object_str(self):
        instance = Lead.objects.get(id=self.instance.id)
        self.assertEquals(str(instance), '{} - {}'.format(
            instance.email, instance.company))
