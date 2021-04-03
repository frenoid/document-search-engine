from django.conf import settings
from .email_html import HTML


class ServiceType(object):
    SOCIAL_MEDIA = 'social-media'
    E_COMMERCE = 'e-commerce'
    DIGITAL_PAYMENTS = 'digital-payments'
    CHOICES = (
            (SOCIAL_MEDIA, 'Social Media'),
            (E_COMMERCE, 'E-Commerce'),
            (DIGITAL_PAYMENTS, 'Digital Payments'),
    )


class ValueType(object):
    PERCENTAGE = 'percentage'
    ABSOLUTE = 'absolute'
    CHOICES = (
            (PERCENTAGE, 'Percentage'),
            (ABSOLUTE, 'Absolute'),
    )


class RouteType(object):
    LAND = 'land'
    SEA = 'sea'
    COMBINED = 'combined'
    CHOICES = (
            (LAND, 'Land Route'),
            (SEA, 'Sea Route'),
            (COMBINED, 'Land & Sea Route'),
    )


class AdditionalFieldsType(object):
    COUNTRY = 'country'
    GOODS = 'goods'
    SERVICE = 'service'
    GENERIC_IMAGE = 'generic_image'
    LANGUAGE = 'language'
    RELIGION = 'religion'


class ZohoAPI(object):
    CLIENT_ID = '1000.FDUAIFKAZG8H07096JWYNC0EIOI71P'
    CLIENT_SECRET = '60cb2328508b6fc363ac82f602964374f0d9cff9f7'
    REFRESH_TOKEN = (
            '1000.434e1cda3cf2d65256f63cb2bf97e90f'
            '.8dca4e194d88699a459a7bd9b549667b')
    REDIRECT_URI = 'https://www.goldenequatorconsulting.com/insight-leads'
    API_BASE_URL = 'https://www.zohoapis.com/crm/v2/'
    OAUTH_BASE_URL = 'https://accounts.zoho.com/oauth/v2/'
    ACCESS_TOKEN_URL = (
            '{}token?refresh_token={}&client_id={}&client_secret={}'
            '&grant_type=refresh_token').format(
                    OAUTH_BASE_URL, REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET)
    LEAD_INSERT_URL = '{}Leads'.format(API_BASE_URL)
    CACHE_KEY = 'zoho_access_token_v1'
    LEAD_OWNER_EMAIL_TO_ID_MAP = {
            'weiliang.ho@goldenequator.com': '2932222000000154155'
    }

    @staticmethod
    def get_auth_headers(access_token):
        auth_headers = {
            'Authorization': 'Zoho-oauthtoken {}'.format(access_token)
        }

        return auth_headers

    @classmethod
    def generate_payload(
            cls, first_name, last_name, email, company,
            description, lead_owner, lead_source):
        payload = {
            'data': [
                {
                    'First_Name': first_name,
                    'Last_Name': last_name,
                    'Email': email,
                    'Company': company,
                    'Description': description,
                    'Owner': cls.LEAD_OWNER_EMAIL_TO_ID_MAP[lead_owner],
                    'Lead_Source': lead_source,
                    'Lead_Status': 'To Contact'
                },
            ],
            "trigger": []
        }

        return payload


class LeadGenerationEmail(object):
    TO_EMAIL = (
            'arindammani.das@goldenequator.com'
            if settings.DEV else
            'insights@goldenequator.com')
    FROM_EMAIL = 'insights@goldenequator.com'
    FROM_NAME = 'Insights'
    EMAIL_SUBJECT = 'New lead on Insights'
    SENDGRID_API_BASE_URL = 'https://api.sendgrid.com/v3/'
    SENDGRID_SEND_MAIL_URL = '{}mail/send'.format(SENDGRID_API_BASE_URL)
    SENDGRID_API_KEY = (
            'SG.w5rGZZDKSOCte1c89AxRfQ'
            '.6k_r6vNj-I9VWJ2wJCoo1z71SCu1xmJpnbNxQgSI3K8')
    AUTH_HEADERS = {
        'authorization': 'Bearer {}'.format(SENDGRID_API_KEY),
        'content-type': 'application/json'
    }
    EMAIL_BODY = '''A new lead has been generated on Insights.

                    First Name: {}
                    Last Name: {}
                    Email: {}
                    Company: {}
                    Query: {}

                    Please check the leads on Zoho for more details.'''

    @classmethod
    def generate_payload(
            cls, first_name, last_name, email, company, description):
        payload = {
            'personalizations': [
                {
                    'to': [
                        {
                            'email': cls.TO_EMAIL
                        }
                    ],
                    'subject': cls.EMAIL_SUBJECT
                }
            ],
            'from': {
                'email': cls.FROM_EMAIL,
                'name': cls.FROM_NAME
            },
            'reply_to': {
                'email': cls.FROM_EMAIL,
                'name': cls.FROM_NAME
            },
            'content': [
                {
                    'type': 'text/plain',
                    'value': cls.EMAIL_BODY.format(
                                first_name, last_name, email,
                                company, description)
                }
            ]
        }

        return payload


class LeadGenerationEmailConfirm(LeadGenerationEmail):
    EMAIL_SUBJECT = 'We\'ll be in touch'
    EMAIL_BODY = HTML

    @classmethod
    def generate_payload(cls, first_name, email):
        payload = {
            'personalizations': [
                {
                    'to': [
                        {
                            'email': email
                        }
                    ],
                    'subject': cls.EMAIL_SUBJECT
                }
            ],
            'from': {
                'email': cls.FROM_EMAIL,
                'name': cls.FROM_NAME
            },
            'reply_to': {
                'email': cls.FROM_EMAIL,
                'name': cls.FROM_NAME
            },
            'content': [
                {
                    'type': 'text/html',
                    'value': cls.EMAIL_BODY.replace(
                        '{#FIRST_NAME#}', first_name)
                }
            ]
        }

        return payload


class RecaptchaDetails(object):
    VERIFICATION_URL = 'https://www.google.com/recaptcha/api/siteverify'
    SECRET = '6Lf61l8UAAAAAIisodL5qoY4lrKfiQ-xZLyDTvsK'


class MITApi(object):
    BASE_URL = (
        'https://atlas.media.mit.edu/hs92/{}/{}/{}/all/show/'
        '?output_depth=hs92_id_len.6')

    @classmethod
    def get_url(cls, year, country, trade_type):
        return cls.BASE_URL.format(trade_type, year, country)


class TradeType(object):
    EXPORT = 'export'
    IMPORT = 'import'
    CHOICES = (
        (EXPORT, 'Export'),
        (IMPORT, 'Import'),
    )
    OPTIONS = [EXPORT, IMPORT]


class FTACoverageType(object):
    GOODS = 'goods'
    SERVICES = 'services'
    GOODS_N_SERVICES = 'goods-and-services'
    CHOICES = (
        (GOODS, 'Goods'),
        (SERVICES, 'Services'),
        (GOODS_N_SERVICES, 'Goods & Services'),
    )


class TradeDescriptionType(object):
    GOODS = 'goods'
    SERVICES = 'services'
    INVESTMENTS = 'investments'
    CHOICES = (
        (GOODS, 'Trade in Goods'),
        (SERVICES, 'Trade in Services'),
        (INVESTMENTS, 'Investments'),
    )


class TradeLinksType(object):
    FULL_TEXT = 'full-text'
    GOVT_WEBSITE = 'govt-website'
    RSM_BUSINESS_GUIDE = 'rsm-business-guide'
    CHOICES = (
        (FULL_TEXT, 'Full-text Link'),
        (GOVT_WEBSITE, 'Government Website Link'),
        (RSM_BUSINESS_GUIDE, 'RSM Business Guide'),
    )


class AppStoreType(object):
    GOOGLE = 'google-play-store'
    APPLE = 'apple-app-store'
    CHOICES = (
        (GOOGLE, 'Google Play Store'),
        (APPLE, 'Apple App Store'),
    )


class GenderType(object):
    MALE = 'male'
    FEMALE = 'female'
    OTHERS = 'others'
    CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHERS, 'Others'),
    )


HS92SectionToProductMapping = {
    '01': 'S1',
    '02': 'S1',
    '03': 'S1',
    '04': 'S1',
    '05': 'S1',
    '06': 'S2',
    '07': 'S2',
    '08': 'S2',
    '09': 'S2',
    '10': 'S2',
    '11': 'S2',
    '12': 'S2',
    '13': 'S2',
    '14': 'S2',
    '15': 'S3',
    '16': 'S4',
    '17': 'S4',
    '18': 'S4',
    '19': 'S4',
    '20': 'S4',
    '21': 'S4',
    '22': 'S4',
    '23': 'S4',
    '24': 'S4',
    '25': 'S5',
    '26': 'S5',
    '27': 'S5',
    '28': 'S6',
    '29': 'S6',
    '30': 'S6',
    '31': 'S6',
    '32': 'S6',
    '33': 'S6',
    '34': 'S6',
    '35': 'S6',
    '36': 'S6',
    '37': 'S6',
    '38': 'S6',
    '39': 'S7',
    '40': 'S7',
    '41': 'S8',
    '42': 'S8',
    '43': 'S8',
    '44': 'S9',
    '45': 'S9',
    '46': 'S9',
    '47': 'S10',
    '48': 'S10',
    '49': 'S10',
    '50': 'S11',
    '51': 'S11',
    '52': 'S11',
    '53': 'S11',
    '54': 'S11',
    '55': 'S11',
    '56': 'S11',
    '57': 'S11',
    '58': 'S11',
    '59': 'S11',
    '60': 'S11',
    '61': 'S11',
    '62': 'S11',
    '63': 'S11',
    '64': 'S12',
    '65': 'S12',
    '66': 'S12',
    '67': 'S12',
    '68': 'S13',
    '69': 'S13',
    '70': 'S13',
    '71': 'S14',
    '72': 'S15',
    '73': 'S15',
    '74': 'S15',
    '75': 'S15',
    '76': 'S15',
    '77': 'S15',
    '78': 'S15',
    '79': 'S15',
    '80': 'S15',
    '81': 'S15',
    '82': 'S15',
    '83': 'S15',
    '84': 'S16',
    '85': 'S16',
    '86': 'S17',
    '87': 'S17',
    '88': 'S17',
    '89': 'S17',
    '90': 'S18',
    '91': 'S18',
    '92': 'S18',
    '93': 'S19',
    '94': 'S20',
    '95': 'S20',
    '96': 'S20',
    '97': 'S21',
}
