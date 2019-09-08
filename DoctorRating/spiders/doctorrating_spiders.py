import logging

import scrapy

from DoctorRating.spiders.doctorrating_parsers import parse_facilities
from scrapy.utils.log import configure_logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='DoctorRatingSpider.log',
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    level=logging.INFO
)


class DoctorRatingSpider1(scrapy.Spider):
    name = "doctorrating-1"

    def start_requests(self):
        urls = ['https://www.ratemds.com/facilities/?country=us&page={}'.format(page_num) for page_num in
                range(1, 20000)]
        for url in urls:
            yield scrapy.Request(url=url, callback=parse_facilities)


class DoctorRatingSpider2(scrapy.Spider):
    name = "doctorrating-2"

    def start_requests(self):
        urls = ['https://www.ratemds.com/facilities/?country=us&page={}'.format(page_num) for page_num in
                range(20000, 40000)]
        for url in urls:
            yield scrapy.Request(url=url, callback=parse_facilities)


class DoctorRatingSpider3(scrapy.Spider):
    name = "doctorrating-3"

    def start_requests(self):
        urls = ['https://www.ratemds.com/facilities/?country=us&page={}'.format(page_num) for page_num in
                range(40000, 60000)]
        for url in urls:
            yield scrapy.Request(url=url, callback=parse_facilities)


class DoctorRatingSpider4(scrapy.Spider):
    name = "doctorrating-4"

    def start_requests(self):
        urls = ['https://www.ratemds.com/facilities/?country=us&page={}'.format(page_num) for page_num in
                range(60000, 80000)]
        for url in urls:
            yield scrapy.Request(url=url, callback=parse_facilities)


class DoctorRatingSpider5(scrapy.Spider):
    name = "doctorrating-5"

    def start_requests(self):
        urls = ['https://www.ratemds.com/facilities/?country=us&page={}'.format(page_num) for page_num in
                range(80000, 100000)]
        for url in urls:
            yield scrapy.Request(url=url, callback=parse_facilities)


class DoctorRatingSpider6(scrapy.Spider):
    name = "doctorrating-6"

    def start_requests(self):
        urls = ['https://www.ratemds.com/facilities/?country=us&page={}'.format(page_num) for page_num in
                range(100000, 120000)]
        for url in urls:
            yield scrapy.Request(url=url, callback=parse_facilities)


class DoctorRatingSpider7(scrapy.Spider):
    name = "doctorrating-7"

    def start_requests(self):
        urls = ['https://www.ratemds.com/facilities/?country=us&page={}'.format(page_num) for page_num in
                range(120000, 140000)]
        for url in urls:
            yield scrapy.Request(url=url, callback=parse_facilities)


class DoctorRatingSpider8(scrapy.Spider):
    name = "doctorrating-8"

    def start_requests(self):
        urls = ['https://www.ratemds.com/facilities/?country=us&page={}'.format(page_num) for page_num in
                range(140000, 160000)]
        for url in urls:
            yield scrapy.Request(url=url, callback=parse_facilities)


class DoctorRatingSpider9(scrapy.Spider):
    name = "doctorrating-9"

    def start_requests(self):
        urls = ['https://www.ratemds.com/facilities/?country=us&page={}'.format(page_num) for page_num in
                range(160000, 172631)]
        for url in urls:
            yield scrapy.Request(url=url, callback=parse_facilities)
