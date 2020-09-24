# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy.item
from scrapy.loader.processors import MapCompose, TakeFirst

def getPrice(price):
    if( len(price) == 2):
        return 0
    else:
        return float(price.strip('￥'))

def getProducer(input):
    if (input.strip('\r\n ') == ''):
        return 'Unknown'
    else:
        return input.strip('\r\n ')

def getTag(input):
    return input + ' '
def getDose(input):
    return input.replace('\n', '')
def getUses(input):
    return input.replace('  ', ' ')[0:255]


class Try39NetItem(scrapy.Item):
    name = scrapy.Field(
        output_processor=TakeFirst()
    )
    disease = scrapy.Field(
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        # input_processor=MapCompose(complete_url),
        output_processor=TakeFirst()
    )
    medicine = scrapy.Field(
        output_processor=TakeFirst()
    )
    # 第三层页面信息
    # 适应症
    primary_uses = scrapy.Field(
        input_processor=MapCompose(getUses),
        output_processor=TakeFirst()
    )
    # 主要成分
    ingredient = scrapy.Field(
        # input_processor=MapCompose(getIng)
    )
    # 功能主治
    main_function = scrapy.Field(
        output_processor=TakeFirst()
    )
    # 用法用量
    dose = scrapy.Field(
        input_processor=MapCompose(getDose),
        output_processor=TakeFirst()
    )
    approval_num = scrapy.Field(
        output_processor=TakeFirst()
    )
    producer = scrapy.Field(
        input_processor=MapCompose(getProducer),
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        input_processor = MapCompose(getPrice),
        output_processor=TakeFirst()
    )
    tag = scrapy.Field(
        # input_processor=MapCompose(getTag)
    )
    manual_url = scrapy.Field(
        output_processor=TakeFirst()
    )


