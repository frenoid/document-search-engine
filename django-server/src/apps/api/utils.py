import csv
import requests
import time
from operator import itemgetter
from .constants import HS92SectionToProductMapping, MITApi, TradeType
from .models import (
        Country, CountryDetailsGeneral,
        CountryDetailsEconomy, CountryDetailsDemographicsAge,
        CountryDetailsBusinessExport, CountryDetailsBusinessFDI,
        CountryDetailsBusinessFTA, CountryDetailsBusinessInvestmentReasons,
        CountryDetailsBusinessInvestmentSectors, CountryDetailsMobileUsage,
        CountryDetailsServiceUsage, CountryPolicy, CountryPolicyLine,
        Goods, GoodsDistribution, CountryDetailsBusinessImport, IndustrySector,
        YearDistribution)


def create_initial_model_history():
    model_list = [
            Country, CountryDetailsGeneral,
            CountryDetailsEconomy, CountryDetailsDemographicsAge,
            CountryDetailsBusinessExport, CountryDetailsBusinessFDI,
            CountryDetailsBusinessFTA,
            CountryDetailsBusinessInvestmentReasons,
            CountryDetailsBusinessInvestmentSectors,
            CountryDetailsMobileUsage, CountryDetailsServiceUsage,
            CountryPolicy, CountryPolicyLine
    ]

    for model in model_list:
        model_name = model._meta.verbose_name
        records = model.objects.all()
        print('Creating initial model history for {}...'.format(model_name))
        record_count = 0
        for record in records:
            print('....')
            record_count += 1
            record.save()
            time.sleep(1)

        print('Processed {} records for {}'.format(record_count, model_name))
        print('\n')


def populate_hs92_data():
    print('Populating HS92 section data...')
    with open('hs92_sections.csv', encoding='utf-8') as csvfile_section:
        reader = csv.reader(csvfile_section, delimiter=',')
        for row in reader:
            name = row[1]
            hs92_id = row[0]
            Goods.objects.create(name=name, hs92_id=hs92_id)
    print('HS92 section data population DONE.')
    print('Populating HS92 products data...')
    with open('hs92_products.csv', encoding='utf-8') as csvfile_product:
        reader = csv.reader(csvfile_product, delimiter=',')
        sections_list = list(set(HS92SectionToProductMapping.values()))
        sections = Goods.objects.filter(hs92_id__in=sections_list)
        sections_map = {}
        for section in sections:
            sections_map[section.hs92_id] = section
        for row in reader:
            name = row[2]
            hs92_id = row[1]
            parent = sections_map.get(
                HS92SectionToProductMapping.get(hs92_id[:2]))
            Goods.objects.create(name=name, hs92_id=hs92_id, parent=parent)
    print('HS92 products data population DONE.')


def populate_industry_sector_data():
    print('Populating industry sector data...')
    with open('industry_sectors.csv', encoding='utf-8') as csvfile_section:
        reader = csv.reader(csvfile_section, delimiter=',')
        previous_sector = None
        for row in reader:
            sector = row[0]
            subsector = row[1]
            if previous_sector and sector == previous_sector.name:
                IndustrySector.objects.create(
                    name=subsector, parent=previous_sector)
            else:
                sector_obj = IndustrySector.objects.create(name=sector)
                IndustrySector.objects.create(
                    name=subsector, parent=sector_obj)
                previous_sector = sector_obj
    print('Industry sector data population DONE.')


def populate_trade_data(year, country, trade_type, iso_code):
    if trade_type not in TradeType.OPTIONS:
        print('Invalid trade type.')
        return
    api_url = MITApi.get_url(year, country, trade_type)
    content = requests.get(api_url)
    data = content.json().get('data')
    if data:
        mit_to_hs92_map = {}
        total_trade_val = 0.00
        trade_val_key = 'export_val'
        if trade_type == TradeType.IMPORT:
            trade_val_key = 'import_val'
        with open('hs92_products.csv', encoding='utf-8') as csvfile_product:
            reader = csv.reader(csvfile_product, delimiter=',')
            for row in reader:
                mit_id = row[0]
                hs92_id = row[1]
                mit_to_hs92_map[mit_id] = hs92_id
        hs92_section_total_trade = {}
        hs92_products_trade_percentage = {}
        hs92_section_trade_percentage = []
        # get total trade value - import or export
        for item in data:
            item_id = item.get('hs92_id')
            hs92_id = mit_to_hs92_map.get(item_id)
            trade_val = item.get(trade_val_key)
            if trade_val:
                section_id = HS92SectionToProductMapping.get(hs92_id[:2])
                if section_id in hs92_section_total_trade:
                    hs92_section_total_trade[section_id] += trade_val
                else:
                    hs92_section_total_trade[section_id] = trade_val
                total_trade_val += trade_val
        # get percentage of product from total trade value
        for item in data:
            item_id = item.get('hs92_id')
            hs92_id = mit_to_hs92_map.get(item_id)
            trade_val = item.get(trade_val_key)
            if trade_val:
                section_id = HS92SectionToProductMapping.get(hs92_id[:2])
                trade_percentage = round(
                    (trade_val / total_trade_val) * 100, 2)
                if section_id in hs92_products_trade_percentage:
                    hs92_products_trade_percentage[section_id].append(
                        (hs92_id, trade_percentage))
                else:
                    hs92_products_trade_percentage[section_id] = [
                        (hs92_id, trade_percentage)]
        # get percentage of section from total trade value
        for section_id, val in hs92_section_total_trade.items():
            trade_percentage = round((val / total_trade_val) * 100, 2)
            hs92_section_trade_percentage.append(
                (section_id, trade_percentage))
        # sort sections
        top_sections = sorted(
            hs92_section_trade_percentage, key=itemgetter(1), reverse=True)[:5]
        top_sections_hs92_list = []
        section_goods_hs92_map = {}
        exported_items = []
        for section in top_sections:
            top_sections_hs92_list.append(section[0])
        section_goods = Goods.objects.filter(
            hs92_id__in=top_sections_hs92_list)
        for goods in section_goods:
            section_goods_hs92_map[goods.hs92_id] = goods.slug
        for section in top_sections:
            section_slug = section_goods_hs92_map.get(section[0])
            if section_slug:
                exported_items.append(GoodsDistribution(
                    product=section_slug, value=section[1]))
        # sort products per section
        for item in top_sections:
            unsorted_products = hs92_products_trade_percentage.get(item[0])
            top_products = sorted(
                unsorted_products, key=itemgetter(1), reverse=True)[:5]
            top_products_hs92_list = []
            product_goods_hs92_map = {}
            for product in top_products:
                top_products_hs92_list.append(product[0])
            product_goods = Goods.objects.filter(
                hs92_id__in=top_products_hs92_list)
            for goods in product_goods:
                product_goods_hs92_map[goods.hs92_id] = goods.slug
            for product in top_products:
                product_slug = product_goods_hs92_map.get(product[0])
                if product_slug:
                    exported_items.append(GoodsDistribution(
                        product=product_slug, value=product[1]))
        if trade_type == TradeType.IMPORT:
            business_import = CountryDetailsBusinessImport.objects.filter(
                country__iso_code=iso_code)
            if business_import.exists():
                business_import = business_import[0]
                business_import.imported_items = exported_items
                business_import.imported_items_year = year
                business_import.save()
                print('Import details for {} saved'.format(iso_code))
        elif trade_type == TradeType.EXPORT:
            business_export = CountryDetailsBusinessExport.objects.filter(
                country__iso_code=iso_code)
            if business_export.exists():
                business_export = business_export[0]
                business_export.exported_items = exported_items
                business_export.exported_items_year = year
                business_export.save()
                print('Export details for {} saved'.format(iso_code))


def populate_trade_volume(years, country, trade_type, iso_code):
    if trade_type not in TradeType.OPTIONS:
        print('Invalid trade type.')
        return
    yearly_trade = []
    for year in years:
        api_url = MITApi.get_url(year, country, trade_type)
        content = requests.get(api_url)
        data = content.json().get('data')
        if data:
            total_trade_val = 0.00
            trade_val_key = 'export_val'
            if trade_type == TradeType.IMPORT:
                trade_val_key = 'import_val'
            # get total trade value - import or export
            for item in data:
                trade_val = item.get(trade_val_key)
                if trade_val:
                    total_trade_val += trade_val
            total_trade_val = round(total_trade_val, 2)
            yearly_trade.append(
                YearDistribution(year=year, value=total_trade_val))
    if trade_type == TradeType.IMPORT:
        business_import = CountryDetailsBusinessImport.objects.filter(
            country__iso_code=iso_code)
        if business_import.exists():
            business_import = business_import[0]
            business_import.total_yearly_imports = yearly_trade
            business_import.save()
            print('Yearly import details for {} saved'.format(iso_code))
    elif trade_type == TradeType.EXPORT:
        business_export = CountryDetailsBusinessExport.objects.filter(
            country__iso_code=iso_code)
        if business_export.exists():
            business_export = business_export[0]
            business_export.total_yearly_exports = yearly_trade
            business_export.save()
            print('Yearly export details for {} saved'.format(iso_code))


def populate_trade_data_from_file():
    country_map = {}
    with open('trade_import_export.csv', encoding='utf-8') as csvfile_trade:
        reader = csv.reader(csvfile_trade, delimiter=',')
        for row in reader:
            iso = row[0]
            year = row[1]
            export_val = row[2]
            import_val = row[3]
            if iso in country_map:
                country_map[iso].append((year, export_val, import_val))
            else:
                country_map[iso] = [(year, export_val, import_val)]

    for iso in country_map:
        trade_data = country_map[iso]
        trade_data.sort()
        export_data = []
        import_data = []
        for data in trade_data:
            export_data.append(YearDistribution(year=data[0], value=data[1]))
            import_data.append(YearDistribution(year=data[0], value=data[2]))
        business_export = CountryDetailsBusinessExport.objects.filter(
            country__iso_code=iso)
        if business_export.exists():
            business_export = business_export[0]
            business_export.total_yearly_exports = export_data
            business_export.save()
        business_import = CountryDetailsBusinessImport.objects.filter(
            country__iso_code=iso)
        if business_import.exists():
            business_import = business_import[0]
            business_import.total_yearly_imports = import_data
            business_import.save()
        print('Yearly trade details for {} saved'.format(iso))
