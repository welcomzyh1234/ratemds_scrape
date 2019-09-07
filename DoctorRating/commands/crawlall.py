import os

from DoctorRating.spiders.doctorrating_spiders import DoctorRatingSpider1, DoctorRatingSpider2, \
    DoctorRatingSpider3, DoctorRatingSpider4, DoctorRatingSpider5, DoctorRatingSpider6, DoctorRatingSpider7, \
    DoctorRatingSpider8, DoctorRatingSpider9
from scrapy.commands import ScrapyCommand
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import UsageError
from scrapy.utils.conf import arglist_to_dict
from scrapy.utils.project import get_project_settings
from scrapy.utils.python import without_none_values


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all spiders'

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set spider argument (may be repeated)")
        parser.add_option("-o", "--output", metavar="FILE",
                          help="dump scraped items into FILE (use - for stdout)")
        parser.add_option("-t", "--output-format", metavar="FORMAT",
                          help="format to use for dumping items with -o")

    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)
        try:
            opts.spargs = arglist_to_dict(opts.spargs)
        except ValueError:
            raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)
        if opts.output:
            if opts.output == '-':
                self.settings.set('FEED_URI', 'stdout:', priority='cmdline')
            else:
                self.settings.set('FEED_URI', opts.output, priority='cmdline')
            feed_exporters = without_none_values(
                self.settings.getwithbase('FEED_EXPORTERS'))
            valid_output_formats = feed_exporters.keys()
            if not opts.output_format:
                opts.output_format = os.path.splitext(opts.output)[1].replace(".", "")
            if opts.output_format not in valid_output_formats:
                raise UsageError("Unrecognized output format '%s', set one"
                                 " using the '-t' switch or as a file extension"
                                 " from the supported list %s" % (opts.output_format,
                                                                  tuple(valid_output_formats)))
            self.settings.set('FEED_FORMAT', opts.output_format, priority='cmdline')

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
