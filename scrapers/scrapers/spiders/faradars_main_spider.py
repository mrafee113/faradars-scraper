import bs4

from lxml import html
from django.conf import settings
from scrapy.spiders import Spider
from scrapy.http.request import Request
from scrapy.http.response import Response
from playwright.async_api._generated import Page

from utils import fa_to_en
from .items import MainItem, MainLoader


class FaradarsMainSpider(Spider):
    """
    Uses one urls, which needs page number.
    - Uses one request per url.
    Output: list[dict]
    Dictionary Keys: todo
    """

    name = 'faradars_main_spider'
    allowed_domains = ['faradars.org']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapers.pipelines.FaradarsMainPipeline': 300},
        'CONCURRENT_REQUESTS': 10,
        'DOWNLOAD_HANDLERS': {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 120000,
        # 'PLAYWRIGHT_LAUNCH_OPTIONS': {'slow_mo': 50,
        #                               'headless': False}  # todo: remove
    }

    URL = settings.FARADARS_URL

    @classmethod
    def format_url(cls, page: int):
        return cls.URL.format(page=page)

    def start_requests(self):
        url = self.format_url(1)
        yield Request(url=url, callback=self.parse,
                      meta={'playwright': True, 'playwright_include_page': True},
                      errback=self.errback_close_page)

    @classmethod
    async def errback_close_page(cls, failure):
        await failure.requst.meta('playwright_page')

    @classmethod
    async def wait_for(cls, page: Page):
        loader_xpath = '//body//div[@id="faradars-main"]//div/nav[@aria-label="Pagination"]'
        loader = page.locator(f'xpath={loader_xpath}')
        await loader.wait_for()

    @classmethod
    async def get_html(cls, page: Page) -> html.HtmlElement:
        inner_html = await page.inner_html('//body')
        inner_html = f'<html><body>{inner_html}</body></html>'
        soup = bs4.BeautifulSoup(inner_html, 'html.parser')
        doc: html.HtmlElement = html.document_fromstring(str(soup))
        return doc

    @classmethod
    def parse_items(cls, doc: html.HtmlElement) -> list[MainItem]:
        rows_xpath = '//body/div/div/div/main/div/div/div/div[2]/div/div[2]/div[3]/div'
        rows = doc.xpath(rows_xpath)
        items: list[MainItem] = list()
        for row in rows:
            loader = MainLoader()
            row = row.xpath('./div/div[2]')[0]

            title = row.xpath('./a')
            if title and isinstance(title[0], html.HtmlElement):
                loader.add_value('title', title[0].text_content())
                if 'href' in title[0].attrib:
                    loader.add_value('link', title[0].attrib['href'])

            nou = row.xpath('./div[1]/div[1]')
            if nou and isinstance(nou[0], html.HtmlElement):
                loader.add_value('number_of_students', nou[0].text_content())

            tutor = row.xpath('./div[1]/div[2]')
            if tutor and isinstance(tutor[0], html.HtmlElement):
                loader.add_value('tutor', tutor[0].text_content())

            duration = row.xpath('./div[1]/div[3]')
            if duration and isinstance(duration[0], html.HtmlElement):
                print('here', duration[0].text_content())
                loader.add_value('duration', duration[0].text_content())

            items.append(loader.load_item())

        return items

    async def parse(self, response: Response, **kwargs):
        page: Page = response.meta['playwright_page']
        await self.wait_for(page)
        doc = await self.get_html(page)
        await page.close()

        for item in self.parse_items(doc):
            yield item
        print('-' * 100 + ' ' + 'done ' + '1')

        max_page_number = int(fa_to_en(doc.xpath('//body//nav[@aria-label="Pagination"]/a')[-2].text))
        for page_number in range(2, max_page_number + 1):
            url = self.format_url(page_number)
            yield Request(url=url, callback=self.parse_page,
                          meta={'playwright': True, 'playwright_include_page': True},
                          errback=self.errback_close_page, cb_kwargs={'page_number': page_number})

    async def parse_page(self, response: Response, **kw):
        page: Page = response.meta['playwright_page']
        await self.wait_for(page)
        doc = await self.get_html(page)
        items = self.parse_items(doc)
        await page.close()
        print('-' * 100 + ' ' + 'done ' + str(response.cb_kwargs['page_number']))
        return items
