from django.conf import settings
from django.shortcuts import reverse
from rest_framework.test import APITestCase
from ..constants import ServiceType
from core.models import InfoMeta
from ..models import (
        Currency, Country, CountryDetailsGeneral, CountryDetailsEconomy,
        CountryDetailsDemographicsAge, CountryDetailsBusinessExport,
        CountryDetailsBusinessFDI, CountryDetailsBusinessFTA,
        CountryDetailsBusinessInvestmentReasons,
        CountryDetailsBusinessInvestmentSectors, CountryDetailsMobileUsage,
        CountryDetailsServiceUsage, Sector, SubSector, CountryPolicy,
        CountryPolicyLine, CountryPolicyRegion, PoliticalStability,
        GenericRangeDistribution, CountryDistribution, GoodsDistribution,
        ServiceDistribution, GeoCoordinates)
from ..serializers import (
        CountrySerializer,
        CountryDetailsGeneralSerializer,
        CountryDetailsEconomySerializer,
        CountryDetailsDemographicsAgeSerializer,
        CountryDetailsBusinessExportSerializer,
        CountryDetailsBusinessFDISerializer,
        CountryDetailsBusinessFTASerializer,
        CountryDetailsBusinessInvestmentReasonsSerializer,
        CountryDetailsBusinessInvestmentSectorsSerializer,
        CountryDetailsMobileUsageSerializer,
        CountryDetailsServiceUsageSerializer, CountryPolicySerializer)


class HomeAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        auth_headers = {
            'HTTP_AUTHORIZATION': '{} {}'.format(
                'Bearer',
                settings.API_AUTH_TOKEN),
        }
        cls.auth_headers = auth_headers

    def test_get_noauth(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 403)

    def test_get(self):
        response = self.client.get(reverse('home'), **self.auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        data = {}
        response = self.client.post(reverse('home'), data, **self.auth_headers)
        self.assertEqual(response.status_code, 405)

    def test_put(self):
        data = {}
        response = self.client.put(reverse('home'), data, **self.auth_headers)
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        data = {}
        response = self.client.delete(
                reverse('home'), data, **self.auth_headers)
        self.assertEqual(response.status_code, 405)


class CountriesListAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.mongo_delete_many({})
        auth_headers = {
            'HTTP_AUTHORIZATION': '{} {}'.format(
                'Bearer',
                settings.API_AUTH_TOKEN),
        }
        cls.auth_headers = auth_headers
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
        Country.objects.create(**kwargs)
        kwargs['iso_code'] = 'IN1'
        kwargs['is_hidden'] = True
        Country.objects.create(**kwargs)

    def test_get_noauth(self):
        response = self.client.get(reverse('countries_list'))
        self.assertEqual(response.status_code, 403)

    def test_get(self):
        countries = Country.objects.filter(is_hidden=False)
        response = self.client.get(
                reverse('countries_list'), **self.auth_headers)
        request = response.wsgi_request
        context = {
            'request': request
        }
        serializer = CountrySerializer(countries, many=True, context=context)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_post(self):
        data = {}
        response = self.client.post(
                reverse('countries_list'), data, **self.auth_headers)
        self.assertEqual(response.status_code, 405)

    def test_put(self):
        data = {}
        response = self.client.put(
                reverse('countries_list'), data, **self.auth_headers)
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        data = {}
        response = self.client.delete(
                reverse('countries_list'), data, **self.auth_headers)
        self.assertEqual(response.status_code, 405)


class CountryDetailsAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.mongo_delete_many({})
        auth_headers = {
            'HTTP_AUTHORIZATION': '{} {}'.format(
                'Bearer',
                settings.API_AUTH_TOKEN),
        }
        cls.auth_headers = auth_headers
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
        general_kwargs = {
            'country': country,
            'area': 12345678,
            'population': 12345678,
            'languages': [language],
            'religions': [religion],
            'highlights': [highlights],
        }
        CountryDetailsGeneral.objects.create(**general_kwargs)
        political_stability_kwargs = {
            'rank': 1,
            'total_countries': 198,
        }
        political_stability = PoliticalStability(**political_stability_kwargs)
        economy_kwargs = {
            'country': country,
            'gdp_total': 12345678,
            'gdp_per_capita': 12345678,
            'unemployment_rate': 10,
            'political_stability_index': political_stability,
            'highlights': [highlights],
        }
        CountryDetailsEconomy.objects.create(**economy_kwargs)
        distribution_kwargs = {
            'range_min': 1,
            'range_max': 10,
            'label': 'Sample',
            'value': 12345678
        }
        distribution = GenericRangeDistribution(**distribution_kwargs)
        demographics_kwargs = {
            'country': country,
            'median': 50,
            'distribution': [distribution],
            'distribution_indicator': 'Distribution',
            'distribution_year': '2018',
            'highlights': [highlights],
        }
        CountryDetailsDemographicsAge.objects.create(**demographics_kwargs)
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
        export_kwargs = {
            'country': country,
            'partner_countries': [country_distribution],
            'partner_countries_indicator': 'Partners',
            'partner_countries_year': '2018',
            'exported_items': [goods_distribution],
            'exported_items_indicator': 'Distribution',
            'exported_items_year': '2018',
            'highlights': [highlights],
        }
        CountryDetailsBusinessExport.objects.create(**export_kwargs)
        fdi_kwargs = {
            'country': country,
            'net_inflow': [distribution],
            'net_inflow_indicator': 'Inflow',
            'net_inflow_year': '2018',
            'investor_countries': [country_distribution],
            'investor_countries_indicator': 'Distribution',
            'investor_countries_year': '2018',
            'highlights': [highlights],
        }
        CountryDetailsBusinessFDI.objects.create(**fdi_kwargs)
        fta_kwargs = {
            'country': country,
            'highlights': [highlights],
        }
        country_fta = CountryDetailsBusinessFTA.objects.create(
                **fta_kwargs)
        country_fta.associated_countries.add(country)
        reasons_kwargs = {
            'country': country,
            'reasons': [highlights],
            'highlights': [highlights],
        }
        CountryDetailsBusinessInvestmentReasons.objects.create(
                **reasons_kwargs)
        sector_kwargs = {
            'name': 'ICT',
        }
        sector = Sector.objects.create(**sector_kwargs)
        sub_sector_kwargs = {
            'name': 'IOT',
            'sector_id': sector.id,
        }
        sub_sector = SubSector.objects.create(**sub_sector_kwargs)
        investment_sector_kwargs = {
            'country': country,
            'highlights': [highlights],
        }
        country_investment_sectors = (
                CountryDetailsBusinessInvestmentSectors.objects.create(
                    **investment_sector_kwargs))
        country_investment_sectors.key_sectors.add(sub_sector)
        mobile_kwargs = {
            'country': country,
            'total_phones': 12345678,
            'distribution': [goods_distribution],
            'distribution_indicator': 'Distribution',
            'distribution_year': '2018',
            'highlights': [highlights],
        }
        CountryDetailsMobileUsage.objects.create(**mobile_kwargs)
        service_distribution_kwargs = {
            'product': 'cars',
            'value': 12345678
        }
        service_distribution = ServiceDistribution(
                **service_distribution_kwargs)
        service_kwargs = {
            'country': country,
            'service_type': ServiceType.SOCIAL_MEDIA,
            'distribution': [service_distribution],
            'distribution_indicator': 'Distribution',
            'distribution_year': '2018',
            'highlights': [highlights],
        }
        CountryDetailsServiceUsage.objects.create(**service_kwargs)
        service_kwargs['service_type'] = ServiceType.E_COMMERCE
        CountryDetailsServiceUsage.objects.create(**service_kwargs)

    def test_get_noauth(self):
        response = self.client.get(reverse(
            'country_details',
            kwargs={'iso_code': 'IN'}))
        self.assertEqual(response.status_code, 403)

    def test_get_country(self):
        country = Country.objects.get(iso_code='IN', is_hidden=False)
        response = self.client.get(
                reverse('country_details', kwargs={'iso_code': 'IN'}),
                **self.auth_headers)
        request = response.wsgi_request
        context = {
            'request': request
        }

        country_serializer = CountrySerializer(country, context=context)

        country_general = CountryDetailsGeneral.objects.filter(
                country=country, is_hidden=False)
        general_serializer = CountryDetailsGeneralSerializer(
                country_general[0], context=context)

        country_economy = CountryDetailsEconomy.objects.filter(
                country=country, is_hidden=False)
        economy_serializer = CountryDetailsEconomySerializer(
                country_economy[0], context=context)

        country_age = CountryDetailsDemographicsAge.objects.filter(
                country=country, is_hidden=False)
        age_serializer = CountryDetailsDemographicsAgeSerializer(
                country_age[0], context=context)

        country_export = CountryDetailsBusinessExport.objects.filter(
                country=country, is_hidden=False)
        export_serializer = CountryDetailsBusinessExportSerializer(
                country_export[0], context=context)

        country_fdi = CountryDetailsBusinessFDI.objects.filter(
                country=country, is_hidden=False)
        fdi_serializer = CountryDetailsBusinessFDISerializer(
                country_fdi[0], context=context)

        country_fta = CountryDetailsBusinessFTA.objects.filter(
                country=country, is_hidden=False)
        fta_serializer = CountryDetailsBusinessFTASerializer(
                country_fta[0], context=context)

        country_investment_reasons = (
                CountryDetailsBusinessInvestmentReasons.objects.filter(
                    country=country, is_hidden=False))
        reasons_serializer = (
                    CountryDetailsBusinessInvestmentReasonsSerializer(
                        country_investment_reasons[0], context=context))

        country_investment_sectors = (
                CountryDetailsBusinessInvestmentSectors.objects.filter(
                    country=country, is_hidden=False))
        sectors_serializer = (
                    CountryDetailsBusinessInvestmentSectorsSerializer(
                        country_investment_sectors[0], context=context))

        country_mobile_usage = CountryDetailsMobileUsage.objects.filter(
                country=country, is_hidden=False)
        mobile_serializer = CountryDetailsMobileUsageSerializer(
                country_mobile_usage[0], context=context)

        country_social_media = CountryDetailsServiceUsage.objects.filter(
                country=country, is_hidden=False,
                service_type=ServiceType.SOCIAL_MEDIA)
        social_media_serializer = CountryDetailsServiceUsageSerializer(
                country_social_media[0], context=context)

        country_ecommerce = CountryDetailsServiceUsage.objects.filter(
                country=country, is_hidden=False,
                service_type=ServiceType.E_COMMERCE)
        ecommerce_serializer = CountryDetailsServiceUsageSerializer(
                country_ecommerce[0], context=context)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['country'], country_serializer.data)
        self.assertEqual(response.data['general'], general_serializer.data)
        self.assertEqual(response.data['economy'], economy_serializer.data)
        self.assertEqual(
                response.data['demographics']['age'], age_serializer.data)
        self.assertEqual(
                response.data['business']['export'], export_serializer.data)
        self.assertEqual(
                response.data['business']['fdi'], fdi_serializer.data)
        self.assertEqual(
                response.data['business']['fta'], fta_serializer.data)
        self.assertEqual(
                response.data['business']['reasons_to_invest'],
                reasons_serializer.data)
        self.assertEqual(
                response.data['business']['investment_sectors'],
                sectors_serializer.data)
        self.assertEqual(
                response.data['business']['demographics']['mobile_usage'],
                mobile_serializer.data)
        self.assertEqual(
                response.data['business']['demographics']['social_media'],
                social_media_serializer.data)
        self.assertEqual(
                response.data['business']['demographics']['ecommerce'],
                ecommerce_serializer.data)

    def test_post(self):
        data = {}
        response = self.client.post(
                reverse('country_details', kwargs={'iso_code': 'IN'}),
                data, **self.auth_headers)
        self.assertEqual(response.status_code, 405)

    def test_put(self):
        data = {}
        response = self.client.put(
                reverse('country_details', kwargs={'iso_code': 'IN'}),
                data, **self.auth_headers)
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        data = {}
        response = self.client.delete(
                reverse('country_details', kwargs={'iso_code': 'IN'}),
                data, **self.auth_headers)
        self.assertEqual(response.status_code, 405)


class PolicyAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.mongo_delete_many({})
        auth_headers = {
            'HTTP_AUTHORIZATION': '{} {}'.format(
                'Bearer',
                settings.API_AUTH_TOKEN),
        }
        cls.auth_headers = auth_headers
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
        region_kwargs = {
            'policy': country_policy,
            'region': 'Eastern',
            'region_latitude': 1.11111,
            'region_longitude': 1.11111,
            'region_zoom': 2.5,
        }
        policy_region = CountryPolicyRegion.objects.create(**region_kwargs)
        policy_region.countries.add(country)
        waypoint_kwargs = {
            'latitude': 1.11111,
            'longitude': 1.11111,
            'label': 'Waypoint 1',
        }
        waypoint = GeoCoordinates(**waypoint_kwargs)
        line_kwargs = {
            'policy': country_policy,
            'color': '#000000',
            'width': 1.5,
            'waypoints': [waypoint],
        }
        CountryPolicyLine.objects.create(**line_kwargs)

    def test_get_noauth(self):
        response_list = self.client.get(reverse('policies_list'))
        response = self.client.get(reverse(
            'policy_details', kwargs={'slug': 'sample-policy'}))
        self.assertEqual(response_list.status_code, 403)
        self.assertEqual(response.status_code, 403)

    def test_get(self):
        policies = CountryPolicy.objects.filter(is_hidden=False)
        country_policy = CountryPolicy.objects.get(
                slug='sample-policy', is_hidden=False)
        response_list = self.client.get(
                reverse('policies_list'), **self.auth_headers)
        response = self.client.get(
                reverse('policy_details', kwargs={'slug': 'sample-policy'}),
                **self.auth_headers)
        request = response.wsgi_request
        context = {
            'request': request
        }
        all_policies_serializer = CountryPolicySerializer(
                policies, many=True, context=context)
        policies_serializer = CountryPolicySerializer(
                country_policy, context=context)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_list.status_code, 200)
        self.assertEqual(response_list.data, all_policies_serializer.data)
        self.assertEqual(response.data, policies_serializer.data)

    def test_post(self):
        data = {}
        response_list = self.client.post(
                reverse('policies_list'), data, **self.auth_headers)
        response = self.client.post(
                reverse('policy_details', kwargs={'slug': 'sample-policy'}),
                data, **self.auth_headers)
        self.assertEqual(response_list.status_code, 405)
        self.assertEqual(response.status_code, 405)

    def test_put(self):
        data = {}
        response_list = self.client.put(
                reverse('policies_list'), data, **self.auth_headers)
        response = self.client.put(
                reverse('policy_details', kwargs={'slug': 'sample-policy'}),
                data, **self.auth_headers)
        self.assertEqual(response_list.status_code, 405)
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        data = {}
        response_list = self.client.delete(
                reverse('policies_list'), data, **self.auth_headers)
        response = self.client.delete(
                reverse('policy_details', kwargs={'slug': 'sample-policy'}),
                data, **self.auth_headers)
        self.assertEqual(response_list.status_code, 405)
        self.assertEqual(response.status_code, 405)


class LeadAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        settings.TEST_RUN = True
        auth_headers = {
            'HTTP_AUTHORIZATION': '{} {}'.format(
                'Bearer',
                settings.API_AUTH_TOKEN),
        }
        cls.auth_headers = auth_headers

    def test_post_noauth(self):
        data = {}
        response = self.client.post(
                reverse('generate_lead'), data)
        self.assertEqual(response.status_code, 403)

    def test_get(self):
        response = self.client.get(
                reverse('generate_lead'), **self.auth_headers)
        self.assertEqual(response.status_code, 405)

    def test_post(self):
        data = {
            'first_name': 'Adam',
            'last_name': 'Warlock',
            'email': 'adam.warlock@marvel.com',
            'company': 'Marvel Inc.',
            'description': 'The Marvel Superhero.',
        }
        response = self.client.post(
                reverse('generate_lead'), data, **self.auth_headers)
        self.assertEqual(response.status_code, 201)

    def test_put(self):
        data = {}
        response = self.client.put(
                reverse('generate_lead'), data, **self.auth_headers)
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        data = {}
        response = self.client.delete(
                reverse('generate_lead'), data, **self.auth_headers)
        self.assertEqual(response.status_code, 405)
