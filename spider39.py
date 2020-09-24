from urllib.parse import urljoin
from try39net.items import Try39NetItem
import scrapy
import copy
from scrapy.loader import ItemLoader

from sqlalchemy import create_engine

class Spider39Spider(scrapy.Spider):
    name = 'spider39'
    allowed_domains = ['ypk.39.net/']
    start_urls = (
        'http://ypk.39.net/AllCategory/',
    )

    # 爬取分类页面上的东西
    def parse(self, response):
        saved_item = Try39NetItem()
        self.logger.info('Parse function called on {}'.format(response.url))

        # 保留 “按疾病找药品”
        class_list = response.xpath('//ul[@class="classification-ul"]/li')
        class_list = class_list[0:15]

        for i in class_list:
            ## 再以疾病科的每个疾病为单位，一个疾病为一个词条
            for j in i.xpath('./p/a'):
                saved_item['name'] = j.xpath('./../../strong/a/text()').extract()[0]
                href = 'http://ypk.39.net' + j.xpath('./@href').extract()[0] ##下一页（药品列表）的url
                saved_item['disease'] = j.xpath('./text()').extract()[0]

                if (href != 'http://ypk.39.net'):#个别疾病没有药品列表，url直接指向当前页面
                    yield scrapy.Request(href, callback=self.parseNext,dont_filter=True, meta={'saved_item': copy.deepcopy(saved_item)})


    # 爬取每一个疾病页面的东西 （每一个药品）
    def parseNext(self, response):
        # saved_item = response.meta['saved_item']
        med_list = response.xpath('//div[@class="screen-sort-zh screen-sort-show"]//ul[@class="drugs-ul"]/li')
        for med in med_list:
            saved_item = response.meta['saved_item']
            # 存药名
            saved_item['medicine'] = med.xpath('./a/@title').extract()[0]
            # 存药品url
            med_url = med.xpath('./a/@href').extract()[0]
            saved_item['url'] = med_url

            if (med_url[18] == 'c'): ## 如果是中药（net/后面是‘c’）,跳过
                continue
            yield scrapy.Request(med_url, callback=self.parseMed, dont_filter=True,
                                 meta={'saved_item': copy.deepcopy(saved_item)})

    # 爬取每一个药品下面的信息
    def parseMed(self, response):

        saved_item = response.meta['saved_item']
        loader = ItemLoader(item=saved_item, response=response)

        '''
        ===适应症
        判断第一条是不是适应症，找到对应text，通过len判断
        如果是，保存，如果不是，跳过
        '''
        idx = 1 #xpath index从1开始
        checkthis = response.xpath('//ul[@class = "drug-layout-r-ul"]/li[1]/i/text()').extract()[0]
        if (len(checkthis) == 7):
            path = '//ul[@class = "drug-layout-r-ul"]/li[' + str(idx) + ']/div/p/text()'
            loader.add_xpath('primary_uses',path)
            # saved_item['primary_uses'] = response.xpath(path).extract()[0]
            idx = idx+1
        else:
            saved_item['primary_uses'] = 'Unknown'

        # 成分
        # 后期需要处理：***********
        path = '//ul[@class = "drug-layout-r-ul"]/li[' + str(idx) + ']/i/text()'
        checkthis = response.xpath(path).extract()[0]
        if (checkthis[0]!="主"):
            saved_item['ingredient'] = "Unknown"
        else:
            path = '//ul[@class = "drug-layout-r-ul"]/li[' + str(idx) + ']/div/p/a/text()'
            if (response.xpath(path).extract() == []):
                # if no superlink, change path back
                path = '//ul[@class = "drug-layout-r-ul"]/li[' + str(idx) + ']/div/p/text()'
            else:
                pass
            ing_list = response.xpath(path).extract()
            ing_str = ''
            for ing in ing_list:
                ing_str = ing_str + ing.strip('\r\n ').replace('。', '') + ' '
            saved_item['ingredient'] = ing_str
            idx = idx + 1


        # 功能主治 & 说明书URL
        # 后期需要处理：删掉list里的 '[详情]'， 然后把list变成空格分开的string
        path = '//ul[@class = "drug-layout-r-ul"]/li[' + str(idx) + ']/div/p/a/text()'
        url_path = '//ul[@class = "drug-layout-r-ul"]/li[' + str(idx) + ']/div/p//a[@class="a-details"]/@href'
        loader.add_xpath('main_function', path)
        loader.add_xpath('manual_url', url_path)
        # saved_item['main_function'] = response.xpath(path).extract()
        idx = idx + 1

        # dose
        # 后期需要处理：查null
        path = '//ul[@class = "drug-layout-r-ul"]/li[' + str(idx) + ']/i/text()'
        checkthis = response.xpath(path).extract()[0]
        if (checkthis[0] != "用"):
            saved_item['dose'] = 'Unknown'
        else:
            path = '//ul[@class = "drug-layout-r-ul"]/li[' + str(idx) + ']/div/text()'
            loader.add_xpath('dose', path)
            # saved_item['dose'] = response.xpath(path).extract()[0]
            idx = idx + 1

        # 批准文号
        # 后期需要处理：
        path = '//ul[@class = "drug-layout-r-ul"]/li[' + str(idx) + ']/div/p/text()'
        loader.add_xpath('approval_num', path)
        # saved_item['approval_num'] = response.xpath(path).extract()[0]
        idx = idx + 1

        # 生产企业
        # 后期需要处理：
        path = '//ul[@class = "drug-layout-r-ul"]/li[' + str(idx) + ']/i/text()'
        checkthis = response.xpath(path).extract()[0]
        if (checkthis[0] != "生"):
            saved_item['producer'] = 'Unknown'
        else:
            path = '//ul[@class = "drug-layout-r-ul"]/li[' + str(idx) + ']/div/p/a/text()'
            if (response.xpath(path).extract() == []):
                # if no superlink, change path back
                path = '//ul[@class = "drug-layout-r-ul"]/li[' + str(idx) + ']/div/p/text()'
            else:
                pass
            loader.add_xpath('producer', path)
            # saved_item['producer'] = response.xpath(path).extract()[0]
            idx = idx + 1

        # 价格
        # 后期需要处理：如果是‘暂无’则变成‘￥0’，接着删掉价格开头的￥，然后转换成两位的float
        path = '//ul[@class = "drug-layout-r-ul"]/li[' + str(idx) + ']/div/b/text()'
        loader.add_xpath('price', path)
        # saved_item['price'] = response.xpath(path).extract()[0]
        idx = idx + 1

        # 相关标签
        # 后期需要处理：把list变成空格分开的string
        path = '//ul[@class = "drug-layout-r-ul"]/li[' + str(idx) + ']/div/span/a/text()'
        # loader.add_xpath('tag', path)
        ing_list = response.xpath(path).extract()
        ing_str = ''
        for tag in ing_list:
            ing_str = ing_str + tag + ' '
        saved_item['tag'] = ing_str
        idx = idx + 1


        loader.load_item()


        yield saved_item
