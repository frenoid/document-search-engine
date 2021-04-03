from rest_framework.serializers import (
        ModelSerializer, SerializerMethodField)
from .constants import AdditionalFieldsType
from .models import (
        Country, CountryDetailsGeneral,
        CountryDetailsEconomy, CountryDetailsDemographicsAge,
        CountryDetailsBusinessExport, CountryDetailsBusinessFDI,
        CountryDetailsBusinessFTA, CountryDetailsBusinessInvestmentReasons,
        CountryDetailsBusinessInvestmentSectors, CountryDetailsMobileUsage,
        CountryDetailsServiceUsage, CountryPolicy, CountryPolicyLine, Lead,
        Goods, Service, Language, Religion, GenericImage, CountryPolicyRegion,
        CountryDetailsBusinessImport)


def get_values_list(data, key):
    return_data = []
    for item in data:
        value = item.get(key)
        if value is not None:
            return_data.append(value)

    return return_data


def append_additional_data(
        data, additional_fields_type, request=None):
    fields_type_map = {
        AdditionalFieldsType.COUNTRY: {
            'slug_proxy': 'country',
            'iso_proxy': 'iso_code',
            'model': Country
        },
        AdditionalFieldsType.LANGUAGE: {
            'slug_proxy': 'title',
            'model': Language
        },
        AdditionalFieldsType.RELIGION: {
            'slug_proxy': 'title',
            'model': Religion
        },
        AdditionalFieldsType.GOODS: {
            'slug_proxy': 'product',
            'image_proxy': 'logo',
            'model': Goods
        },
        AdditionalFieldsType.SERVICE: {
            'slug_proxy': 'product',
            'image_proxy': 'logo',
            'color_proxy': 'color',
            'model': Service
        },
        AdditionalFieldsType.GENERIC_IMAGE: {
            'slug_proxy': 'logo',
            'image_proxy': 'logo',
            'model': GenericImage
        }
    }

    slug_list = []
    slug_proxy = fields_type_map[additional_fields_type].get('slug_proxy')
    iso_proxy = fields_type_map[additional_fields_type].get('iso_proxy')
    image_proxy = fields_type_map[additional_fields_type].get('image_proxy')
    color_proxy = fields_type_map[additional_fields_type].get('color_proxy')
    Model = fields_type_map[additional_fields_type].get('model')

    if type(data) == list:
        for entry in data:
            slug = entry.get(slug_proxy)
            if slug is not None:
                slug_list.append(slug)
    else:
        slug = data.get(slug_proxy)
        if slug is not None:
            slug_list.append(slug)

    model_objects = Model.objects.filter(slug__in=slug_list)
    objects_dict = {}
    for model_object in model_objects:
        object_name = model_object.name
        object_image = ''
        object_color = ''
        object_iso = ''
        if image_proxy is not None:
            object_image = getattr(model_object, image_proxy, None)
        if color_proxy is not None:
            object_color = getattr(model_object, color_proxy, '')
        if iso_proxy is not None:
            object_iso = getattr(model_object, iso_proxy, '')
        objects_dict[model_object.slug] = (
                object_name,
                (request.build_absolute_uri(
                    object_image.url) if object_image and request else ''),
                object_color, object_iso)

    if type(data) == list:
        for count, entry in enumerate(data):
            slug = entry.get(slug_proxy)
            if slug in objects_dict:
                data[count][slug_proxy] = objects_dict.get(slug)[0]
                if image_proxy is not None:
                    data[count][image_proxy] = objects_dict.get(slug)[1]
                if color_proxy is not None:
                    data[count][color_proxy] = objects_dict.get(slug)[2]
                if iso_proxy is not None:
                    data[count][iso_proxy] = objects_dict.get(slug)[3]
    else:
        slug = data.get(slug_proxy)
        if slug in objects_dict:
            data[slug_proxy] = objects_dict.get(slug)[0]
            if image_proxy is not None:
                data[image_proxy] = objects_dict.get(slug)[1]
            if color_proxy is not None:
                data[color_proxy] = objects_dict.get(slug)[2]
            if iso_proxy is not None:
                data[iso_proxy] = objects_dict.get(slug)[3]

    return data


def get_embedded_data(field):
    return_data = None
    if type(field) == list:
        embedded_list = []
        for item in field:
            embedded_dict = item.__dict__
            for key in list(embedded_dict.keys()):
                if key.startswith('_'):
                    embedded_dict.pop(key)
            embedded_list.append(embedded_dict)
        return_data = embedded_list
    elif field is not None:
        embedded_dict = field.__dict__
        for key in list(embedded_dict.keys()):
            if key.startswith('_'):
                embedded_dict.pop(key)
        return_data = embedded_dict
    return return_data


def get_hierarchical_trade_data(data, request):
    trade_items_data = []
    goods_slug_list = []
    goods_parent_map = {}
    goods_parent_data = {}
    trade_items = []
    for item in data:
        goods_slug_list.append(item['product'])
        item['slug'] = item['product']
        trade_items_data.append(item)
    all_goods = Goods.objects.filter(slug__in=goods_slug_list)
    for item in all_goods:
        if item.parent_id:
            goods_parent_map[item.slug] = item.parent.slug
    trade_items_data = append_additional_data(
            trade_items_data, AdditionalFieldsType.GOODS, request=request)
    for item in trade_items_data:
        if item['slug'] in goods_parent_map:
            parent = goods_parent_map[item['slug']]
            if parent in goods_parent_data:
                goods_parent_data[parent].append(item)
            else:
                goods_parent_data[parent] = [item]
    for item in trade_items_data:
        if item['slug'] in goods_parent_data:
            item['sub_products'] = goods_parent_data[item['slug']]
            trade_items.append(item)

    return trade_items


class CountrySerializer(ModelSerializer):
    currency = SerializerMethodField()

    class Meta:
        model = Country
        fields = (
                'name', 'slug', 'calling_code', 'iso_code', 'capital',
                'marker_latitude', 'marker_longitude', 'currency')

    def __init__(self, *args, **kwargs):
        include_fields = kwargs.pop('include_fields', None)
        super().__init__(*args, **kwargs)
        if include_fields is not None:
            for field in list(self.fields):
                if field not in include_fields:
                    self.fields.pop(field)

    def get_currency(self, obj):
        return get_embedded_data(obj.currency)


class CountryDetailsGeneralSerializer(ModelSerializer):
    languages = SerializerMethodField()
    religions = SerializerMethodField()
    highlights = SerializerMethodField()

    class Meta:
        model = CountryDetailsGeneral
        fields = ('area', 'population', 'languages', 'religions', 'highlights')

    def get_languages(self, obj):
        data = get_embedded_data(obj.languages)
        updated_data = append_additional_data(
                data, AdditionalFieldsType.LANGUAGE)
        return get_values_list(updated_data, 'title')

    def get_religions(self, obj):
        data = get_embedded_data(obj.religions)
        updated_data = append_additional_data(
                data, AdditionalFieldsType.RELIGION)
        return get_values_list(updated_data, 'title')

    def get_highlights(self, obj):
        return get_embedded_data(obj.highlights)


class CountryDetailsEconomySerializer(ModelSerializer):
    political_stability_index = SerializerMethodField()
    highlights = SerializerMethodField()

    class Meta:
        model = CountryDetailsEconomy
        fields = (
                'gdp_total', 'gdp_per_capita', 'unemployment_rate',
                'political_stability_index', 'highlights')

    def get_highlights(self, obj):
        return get_embedded_data(obj.highlights)

    def get_political_stability_index(self, obj):
        return get_embedded_data(obj.political_stability_index)


class CountryDetailsDemographicsAgeSerializer(ModelSerializer):
    distribution = SerializerMethodField()
    highlights = SerializerMethodField()

    class Meta:
        model = CountryDetailsDemographicsAge
        fields = (
                'median', 'distribution', 'distribution_indicator',
                'distribution_year', 'distribution_value_type', 'highlights')

    def get_highlights(self, obj):
        return get_embedded_data(obj.highlights)

    def get_distribution(self, obj):
        request = self._context.get('request')
        data = get_embedded_data(obj.distribution)
        return append_additional_data(
                data, AdditionalFieldsType.GENERIC_IMAGE, request=request)


class CountryDetailsBusinessExportSerializer(ModelSerializer):
    partner_countries = SerializerMethodField()
    exported_items = SerializerMethodField()
    highlights = SerializerMethodField()

    class Meta:
        model = CountryDetailsBusinessExport
        fields = (
                'partner_countries', 'partner_countries_indicator',
                'partner_countries_year', 'partner_countries_value_type',
                'exported_items', 'exported_items_indicator',
                'exported_items_year', 'exported_items_value_type',
                'highlights')

    def get_highlights(self, obj):
        return get_embedded_data(obj.highlights)

    def get_partner_countries(self, obj):
        data = get_embedded_data(obj.partner_countries)
        return append_additional_data(data, AdditionalFieldsType.COUNTRY)

    def get_exported_items(self, obj):
        request = self._context.get('request')
        data = get_embedded_data(obj.exported_items)
        return get_hierarchical_trade_data(data, request)


class CountryDetailsBusinessImportSerializer(ModelSerializer):
    partner_countries = SerializerMethodField()
    imported_items = SerializerMethodField()
    highlights = SerializerMethodField()

    class Meta:
        model = CountryDetailsBusinessImport
        fields = (
                'partner_countries', 'partner_countries_indicator',
                'partner_countries_year', 'partner_countries_value_type',
                'imported_items', 'imported_items_indicator',
                'imported_items_year', 'imported_items_value_type',
                'highlights')

    def get_highlights(self, obj):
        return get_embedded_data(obj.highlights)

    def get_partner_countries(self, obj):
        data = get_embedded_data(obj.partner_countries)
        return append_additional_data(data, AdditionalFieldsType.COUNTRY)

    def get_imported_items(self, obj):
        request = self._context.get('request')
        data = get_embedded_data(obj.imported_items)
        return get_hierarchical_trade_data(data, request)


class CountryDetailsBusinessFDISerializer(ModelSerializer):
    investor_countries = SerializerMethodField()
    net_inflow = SerializerMethodField()
    highlights = SerializerMethodField()

    class Meta:
        model = CountryDetailsBusinessFDI
        fields = (
                'net_inflow', 'net_inflow_indicator', 'net_inflow_year',
                'net_inflow_value_type', 'investor_countries',
                'investor_countries_indicator', 'investor_countries_year',
                'investor_countries_value_type', 'highlights')

    def get_highlights(self, obj):
        return get_embedded_data(obj.highlights)

    def get_investor_countries(self, obj):
        data = get_embedded_data(obj.investor_countries)
        return append_additional_data(data, AdditionalFieldsType.COUNTRY)

    def get_net_inflow(self, obj):
        return get_embedded_data(obj.yearly_net_inflow)


class CountryDetailsBusinessFTASerializer(ModelSerializer):
    associated_countries = SerializerMethodField()
    highlights = SerializerMethodField()

    class Meta:
        model = CountryDetailsBusinessFTA
        fields = ('associated_countries', 'highlights')

    def get_associated_countries(self, obj):
        queryset = obj.associated_countries.all().order_by('name')
        country_kwargs = {
            'include_fields': ['name', 'iso_code']
        }
        return CountrySerializer(queryset, many=True, **country_kwargs).data

    def get_highlights(self, obj):
        return get_embedded_data(obj.highlights)


class CountryDetailsBusinessInvestmentReasonsSerializer(ModelSerializer):
    reasons = SerializerMethodField()
    highlights = SerializerMethodField()

    class Meta:
        model = CountryDetailsBusinessInvestmentReasons
        fields = ('reasons', 'highlights')

    def get_reasons(self, obj):
        return get_embedded_data(obj.reasons)

    def get_highlights(self, obj):
        return get_embedded_data(obj.highlights)


class CountryDetailsBusinessInvestmentSectorsSerializer(ModelSerializer):
    key_sectors = SerializerMethodField()
    highlights = SerializerMethodField()

    class Meta:
        model = CountryDetailsBusinessInvestmentSectors
        fields = ('key_sectors', 'highlights')

    def get_highlights(self, obj):
        return get_embedded_data(obj.highlights)

    def get_key_sectors(self, obj):
        request = self._context.get('request')
        return_data = []
        sector_sub_sector_map = {}
        sector_order = []
        sector_image_map = {}
        for item in obj.key_sectors.all().order_by('sector__name', 'name'):
            sector = item.sector.name
            sub_sector = item.name
            if sector not in sector_order:
                sector_order.append(sector)

            if sector in sector_sub_sector_map:
                sector_sub_sector_map[sector].append(sub_sector)
            else:
                sector_sub_sector_map[sector] = [sub_sector]

            if item.sector.logo:
                sector_image_map[sector] = request.build_absolute_uri(
                        item.sector.logo.url)
        for sector in sector_order:
            sector_dict = {
                    'sector': sector,
                    'logo': sector_image_map.get(sector, ''),
                    'sub_sectors': sector_sub_sector_map.get(sector)
            }
            return_data.append(sector_dict)

        return return_data


class CountryDetailsMobileUsageSerializer(ModelSerializer):
    distribution = SerializerMethodField()
    highlights = SerializerMethodField()

    class Meta:
        model = CountryDetailsMobileUsage
        fields = (
                'total_phones', 'distribution', 'distribution_indicator',
                'distribution_year', 'distribution_value_type', 'highlights')

    def get_distribution(self, obj):
        request = self._context.get('request')
        data = get_embedded_data(obj.distribution)
        return append_additional_data(
                data, AdditionalFieldsType.GOODS, request=request)

    def get_highlights(self, obj):
        return get_embedded_data(obj.highlights)


class CountryDetailsServiceUsageSerializer(ModelSerializer):
    distribution = SerializerMethodField()
    highlights = SerializerMethodField()

    class Meta:
        model = CountryDetailsServiceUsage
        fields = (
                'service_type', 'distribution', 'distribution_indicator',
                'distribution_year', 'distribution_value_type', 'highlights')

    def get_distribution(self, obj):
        request = self._context.get('request')
        data = get_embedded_data(obj.distribution)
        return append_additional_data(
                data, AdditionalFieldsType.SERVICE, request=request)

    def get_highlights(self, obj):
        return get_embedded_data(obj.highlights)


class CountryPolicyRegionSerializer(ModelSerializer):
    countries = SerializerMethodField()

    class Meta:
        model = CountryPolicyRegion
        fields = (
                'region', 'region_latitude', 'region_longitude',
                'region_zoom', 'countries')

    def get_countries(self, obj):
        queryset = obj.countries.all().order_by('name').values_list(
                'name', flat=True)
        return list(queryset)


class CountryPolicyLineSerializer(ModelSerializer):
    waypoints = SerializerMethodField()

    class Meta:
        model = CountryPolicyLine
        fields = ('color', 'width', 'route_type', 'waypoints')

    def get_waypoints(self, obj):
        return get_embedded_data(obj.waypoints)


class CountryPolicySerializer(ModelSerializer):
    country_kwargs = {
            'include_fields': ['name', 'marker_latitude', 'marker_longitude']
    }
    lines = CountryPolicyLineSerializer(many=True)
    regions = CountryPolicyRegionSerializer(many=True)
    origin_country = CountrySerializer(**country_kwargs)
    associated_countries = SerializerMethodField()
    is_multi_region_policy = SerializerMethodField()

    class Meta:
        model = CountryPolicy
        fields = (
                'name', 'slug', 'short_description', 'description',
                'origin_country', 'associated_countries',
                'is_multi_region_policy', 'regions', 'lines',)

    def get_is_multi_region_policy(self, obj):
        return obj.regions.filter(is_hidden=False).exists()

    def get_associated_countries(self, obj):
        queryset = obj.associated_countries.all().order_by('name').values_list(
                'name', flat=True)
        return list(queryset)


class LeadSerializer(ModelSerializer):
    class Meta:
        model = Lead
        fields = (
                'first_name', 'last_name', 'email', 'company', 'description',
                'source_ip', 'lead_owner', 'lead_source')
