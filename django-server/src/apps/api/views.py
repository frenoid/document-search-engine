import json
import requests
from django.conf import settings
from django.core.cache import cache
from ipware import get_client_ip
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from .authentication import BasicAuthentication
from .constants import (
        ServiceType, LeadGenerationEmail, ZohoAPI,
        LeadGenerationEmailConfirm, RecaptchaDetails)
from .models import (
        Country, CountryDetailsGeneral,
        CountryDetailsEconomy, CountryDetailsDemographicsAge,
        CountryDetailsBusinessExport, CountryDetailsBusinessFDI,
        CountryDetailsBusinessFTA, CountryDetailsBusinessInvestmentReasons,
        CountryDetailsBusinessInvestmentSectors, CountryDetailsMobileUsage,
        CountryDetailsServiceUsage, CountryPolicy,
        CountryDetailsBusinessImport)
from .serializers import (
        CountrySerializer,
        CountryDetailsGeneralSerializer,
        CountryDetailsEconomySerializer,
        CountryDetailsDemographicsAgeSerializer,
        CountryDetailsBusinessExportSerializer,
        CountryDetailsBusinessImportSerializer,
        CountryDetailsBusinessFDISerializer,
        CountryDetailsBusinessFTASerializer,
        CountryDetailsBusinessInvestmentReasonsSerializer,
        CountryDetailsBusinessInvestmentSectorsSerializer,
        CountryDetailsMobileUsageSerializer,
        CountryDetailsServiceUsageSerializer, CountryPolicySerializer,
        LeadSerializer)
from .throttling import BasicThrottle, StrictThrottle


class HomeView(APIView):
    throttle_classes = (BasicThrottle,)
    authentication_classes = (BasicAuthentication,)

    def get(self, request):
        return_data = {
                'message': 'Insights API'
        }
        return Response(return_data)


class CountriesListView(APIView):
    throttle_classes = (BasicThrottle,)
    authentication_classes = (BasicAuthentication,)

    def get(self, request):
        context = {
            'request': request
        }
        countries = Country.objects.filter(is_hidden=False)
        serializer = CountrySerializer(
                countries, many=True, context=context)
        return Response(serializer.data)


class CountryDetailsView(APIView):
    throttle_classes = (BasicThrottle,)
    authentication_classes = (BasicAuthentication,)

    def get(self, request, iso_code):
        try:
            country = Country.objects.get(iso_code=iso_code, is_hidden=False)
        except Country.DoesNotExist:
            raise NotFound(detail='Resource not found.', code=404)

        context = {
            'request': request
        }
        return_data = {
                'country': {},
                'general': {},
                'economy': {},
                'demographics': {
                    'age': {},
                },
                'business': {
                    'export': {},
                    'import': {},
                    'fdi': {},
                    'fta': {},
                    'reasons_to_invest': {},
                    'investment_sectors': {},
                    'demographics': {
                        'mobile_usage': {},
                        'social_media': {},
                        'ecommerce': {},
                    },
                },
        }

        return_data['country'] = CountrySerializer(
                country, context=context).data

        country_general = CountryDetailsGeneral.objects.filter(
                country=country, is_hidden=False)
        if country_general.exists():
            return_data['general'] = CountryDetailsGeneralSerializer(
                    country_general[0], context=context).data

        country_economy = CountryDetailsEconomy.objects.filter(
                country=country, is_hidden=False)
        if country_economy.exists():
            return_data['economy'] = CountryDetailsEconomySerializer(
                    country_economy[0], context=context).data

        country_age = CountryDetailsDemographicsAge.objects.filter(
                country=country, is_hidden=False)
        if country_age.exists():
            return_data['demographics']['age'] = (
                    CountryDetailsDemographicsAgeSerializer(
                        country_age[0], context=context).data)

        country_export = CountryDetailsBusinessExport.objects.filter(
                country=country, is_hidden=False)
        if country_export.exists():
            return_data['business']['export'] = (
                    CountryDetailsBusinessExportSerializer(
                        country_export[0], context=context).data)

        country_import = CountryDetailsBusinessImport.objects.filter(
                country=country, is_hidden=False)
        if country_import.exists():
            return_data['business']['import'] = (
                    CountryDetailsBusinessImportSerializer(
                        country_import[0], context=context).data)

        country_fdi = CountryDetailsBusinessFDI.objects.filter(
                country=country, is_hidden=False)
        if country_fdi.exists():
            return_data['business']['fdi'] = (
                    CountryDetailsBusinessFDISerializer(
                        country_fdi[0], context=context).data)

        country_fta = CountryDetailsBusinessFTA.objects.filter(
                country=country, is_hidden=False)
        if country_fta.exists():
            return_data['business']['fta'] = (
                    CountryDetailsBusinessFTASerializer(
                        country_fta[0], context=context).data)

        country_investment_reasons = (
                CountryDetailsBusinessInvestmentReasons.objects.filter(
                    country=country, is_hidden=False))
        if country_investment_reasons.exists():
            return_data['business']['reasons_to_invest'] = (
                    CountryDetailsBusinessInvestmentReasonsSerializer(
                        country_investment_reasons[0], context=context).data)

        country_investment_sectors = (
                CountryDetailsBusinessInvestmentSectors.objects.filter(
                    country=country, is_hidden=False))
        if country_investment_sectors.exists():
            return_data['business']['investment_sectors'] = (
                    CountryDetailsBusinessInvestmentSectorsSerializer(
                        country_investment_sectors[0], context=context).data)

        country_mobile_usage = CountryDetailsMobileUsage.objects.filter(
                country=country, is_hidden=False)
        if country_mobile_usage.exists():
            return_data['business']['demographics']['mobile_usage'] = (
                    CountryDetailsMobileUsageSerializer(
                        country_mobile_usage[0], context=context).data)

        country_social_media = CountryDetailsServiceUsage.objects.filter(
                country=country, is_hidden=False,
                service_type=ServiceType.SOCIAL_MEDIA)
        if country_social_media.exists():
            return_data['business']['demographics']['social_media'] = (
                    CountryDetailsServiceUsageSerializer(
                        country_social_media[0], context=context).data)

        country_ecommerce = CountryDetailsServiceUsage.objects.filter(
                country=country, is_hidden=False,
                service_type=ServiceType.E_COMMERCE)
        if country_ecommerce.exists():
            return_data['business']['demographics']['ecommerce'] = (
                    CountryDetailsServiceUsageSerializer(
                        country_ecommerce[0], context=context).data)

        return Response(return_data)


class PolicyView(APIView):
    throttle_classes = (BasicThrottle,)
    authentication_classes = (BasicAuthentication,)

    def get_all(self, request):
        context = {
            'request': request
        }
        policies = CountryPolicy.objects.filter(is_hidden=False)
        serializer = CountryPolicySerializer(
                policies, context=context, many=True)
        return Response(serializer.data)

    def get(self, request, slug=None):
        context = {
            'request': request
        }
        if slug is None:
            return self.get_all(request)

        try:
            country_policy = CountryPolicy.objects.get(
                    slug=slug, is_hidden=False)
        except CountryPolicy.DoesNotExist:
            raise NotFound(detail='Resource not found.', code=404)

        serializer = CountryPolicySerializer(
                country_policy, context=context)
        return Response(serializer.data)


class LeadGenerateView(APIView):
    throttle_classes = (StrictThrottle,)
    authentication_classes = (BasicAuthentication,)

    def create_zoho_lead(self, data):
        if settings.DEV or settings.TEST_RUN:
            return

        access_token = cache.get(ZohoAPI.CACHE_KEY)
        if access_token is None:
            response = requests.post(ZohoAPI.ACCESS_TOKEN_URL)
            if response.status_code == requests.codes.ok:
                access_token = response.json().get('access_token')
                cache.set(ZohoAPI.CACHE_KEY, access_token, 3600)
            else:
                return

        auth_headers = ZohoAPI.get_auth_headers(access_token)
        payload = json.dumps(ZohoAPI.generate_payload(
                data.get('first_name'), data.get('last_name'),
                data.get('email'), data.get('company'),
                data.get('description'), data.get('lead_owner'),
                data.get('lead_source')))
        response = requests.post(
                ZohoAPI.LEAD_INSERT_URL, data=payload, headers=auth_headers)
        if settings.DEV:
            print(response)

    def send_email(self, data):
        if settings.TEST_RUN:
            return

        payload = json.dumps(LeadGenerationEmail.generate_payload(
                data.get('first_name'), data.get('last_name'),
                data.get('email'), data.get('company'),
                data.get('description')))
        response = requests.post(
                LeadGenerationEmail.SENDGRID_SEND_MAIL_URL, data=payload,
                headers=LeadGenerationEmail.AUTH_HEADERS)
        if settings.DEV:
            print(response)

        payload = json.dumps(LeadGenerationEmailConfirm.generate_payload(
                data.get('first_name'), data.get('email')))
        response = requests.post(
                LeadGenerationEmailConfirm.SENDGRID_SEND_MAIL_URL,
                data=payload, headers=LeadGenerationEmailConfirm.AUTH_HEADERS)
        if settings.DEV:
            print(response)

    def is_captcha_valid(self, g_recaptcha_response):
        if settings.TEST_RUN:
            return True

        if g_recaptcha_response:
            payload = {
                'secret': RecaptchaDetails.SECRET,
                'response': g_recaptcha_response
            }
            response = requests.post(
                    RecaptchaDetails.VERIFICATION_URL, data=payload)
            if settings.DEV:
                print(response.json())
            if response.json().get('success'):
                return True
        return False

    def post(self, request):
        source_ip, is_routable = get_client_ip(request)
        source_ip = source_ip or ''
        serializer = LeadSerializer(data=request.data)
        g_recaptcha_response = request.data.get('g-recaptcha-response')
        if (serializer.is_valid() and
                self.is_captcha_valid(g_recaptcha_response)):
            serializer.save(source_ip=source_ip)
            self.send_email(serializer.data)
            self.create_zoho_lead(serializer.data)
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
