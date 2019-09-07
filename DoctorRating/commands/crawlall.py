from scrapy.commands import ScrapyCommand
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

from DoctorRating.spiders.doctorrating_spider import DoctorRatingSpider1, DoctorRatingSpider2, \
    DoctorRatingSpider3, DoctorRatingSpider4, DoctorRatingSpider5, DoctorRatingSpider6, DoctorRatingSpider7, \
    DoctorRatingSpider8, DoctorRatingSpider9


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)

    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)

    def run(self, args, opts):
        settings = get_project_settings()
        process = CrawlerProcess(settings)
        process.crawl(DoctorRatingSpider1)
        process.crawl(DoctorRatingSpider2)
        process.crawl(DoctorRatingSpider3)
        process.crawl(DoctorRatingSpider4)
        process.crawl(DoctorRatingSpider5)
        process.crawl(DoctorRatingSpider6)
        process.crawl(DoctorRatingSpider7)
        process.crawl(DoctorRatingSpider8)
        process.crawl(DoctorRatingSpider9)
        process.start()
