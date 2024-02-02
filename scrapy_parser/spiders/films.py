from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class FilmSpider(CrawlSpider):
    name = 'films'
    allowed_domains = ['ru.wikipedia.org']
    start_urls = ['https://ru.wikipedia.org/wiki/Категория:Фильмы_по_годам']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//div[@class="CategoryTreeItem"]/a'), follow=True),
        Rule(LinkExtractor(
            restrict_xpaths='//a[contains(text(), "Следующая страница")]'), follow=True),
        Rule(LinkExtractor(
            restrict_xpaths='//div[@id="mw-pages"]/div/div/div/ul/li/a'), callback='parse_films', follow=True)
 )

    def parse_films(self, response):
        genre_text_1 = ' '.join(response.xpath('//th[contains(.,"Жанр")]/following-sibling::td//a/text()').getall())
        genre_text_2 = response.xpath('//span[@data-wikidata-property-id="P136"]/text()').getall()
        genre_text = genre_text_1 or genre_text_2

        director_text = response.xpath('string(//span[@data-wikidata-property-id="P57"])').get()

        country_text_1 = response.xpath('//span[@data-wikidata-property-id="P495"]/span/a/span/text()').get()
        country_text_2 = response.xpath('//span[@class="country-name"]/span/a/text()').get()
        country_text = country_text_1 or country_text_2

        year_text_1 = ' '.join(response.xpath(
            '//th[contains(text(),"Год")]/following-sibling::td//a/span/text()').getall())
        year_text_2 = ' '.join(response.xpath(
            '//th[contains(text(),"Год")]/following-sibling::td//a/text()').getall())
        release_date_text = ' '.join(response.xpath(
            '//th[contains(text(),"Дата выхода") or contains(text(),"Премьера")]/following-sibling::td//text()')
                                     .getall()).strip()
        year_text = year_text_1 or year_text_2 or release_date_text

        yield {
            'title': response.xpath('//th[@class="infobox-above"]/text()').get(),
            'genre': genre_text,
            'director': director_text,
            'country': country_text,
            'year': year_text
        }
