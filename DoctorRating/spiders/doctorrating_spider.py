import json
import logging
import scrapy
import numpy as np

from DoctorRating.items import DoctorRatingItem

logging.basicConfig(
    filename='DoctorRatingSpider.log',
    format='%(levelname)s: %(message)s',
    level=logging.DEBUG
)

DOCTORS_HREF = '#doctors'
FLOAT_DECIMALS = 3

with open('facilityfilter.json') as json_file:
    facility_filter_json = json.load(json_file)
FACILITY_FILTER = set(facility_filter_json.get('Valid_Facility'))


def parse_facilities(response):
    for facility in response.css('div.search-item'):
        facility_name = facility.css('h2.search-item-location-name::text').get()
        facility_href = facility.css('a.search-item-location-link::attr(href)').get() + DOCTORS_HREF

        if facility_name in FACILITY_FILTER:
            yield response.follow(facility_href, parse_facility_doctors,
                                  cb_kwargs=dict(facility_name=facility_name))


def parse_facility_doctors(response, facility_name):
    for doctor in response.css('div.doctor-profile h2.search-item-doctor-name a'):
        doctor_name = doctor.css('::text').get()
        cb_kwargs = dict(facility_name=facility_name, doctor_name=doctor_name, rating_matrix=list())
        yield response.follow(doctor.attrib['href'], parse_doctor_ratings, cb_kwargs=cb_kwargs)

    next_page_href = get_next_page_href(response)
    if next_page_href is not None:
        yield response.follow(__get_doctor_next_page_href(next_page_href), parse_facility_doctors,
                              cb_kwargs=dict(facility_name=facility_name))


def parse_doctor_ratings(response, facility_name, doctor_name, rating_matrix):
    rating = [0, 0, 0, 0]
    for rating in response.css('div.rating-numbers-compact'):
        rating_strings = rating.css('div.rating-number span.value::text').getall()
        rating_matrix.append(__get_valid_rating_numbers(rating_strings))

    next_page_href = get_next_page_href(response)
    if next_page_href is not None:
        cb_kwargs = dict(facility_name=facility_name, doctor_name=doctor_name, rating_matrix=rating_matrix)
        yield response.follow(next_page_href, callback=parse_doctor_ratings, cb_kwargs=cb_kwargs)
    else:
        if __has_rating(rating_matrix):
            rating = np.array(rating_matrix).mean(axis=0).round(FLOAT_DECIMALS)
        yield DoctorRatingItem(
            Facility_Name=facility_name,
            Doctor_Name=doctor_name,
            Staff_Rating=rating[0],
            Punctuality_Rating=rating[1],
            Helpfulness_Rating=rating[2],
            Knowledge_Rating=rating[3]
        )


def get_next_page_href(response):
    next_page_href = None
    pagination = response.css('ul.pagination li a')
    if __has_pagination(pagination):
        next_page_href = pagination[-1].attrib['href']
    if __has_next_page(response.url, next_page_href):
        return next_page_href
    return None


def __get_valid_rating_numbers(rating_strings):
    rating_numbers = [float(rating_string) for rating_string in rating_strings]
    if (len(rating_numbers) is 3):
        rating_numbers.insert(0, 5.0)
    return rating_numbers


def __has_rating(rating_matrix):
    return len(rating_matrix) is not 0


def __has_next_page(url, next_page_href):
    return next_page_href is not None and url.split('?')[-1] != next_page_href.split('?')[-1]


def __has_pagination(pagination):
    return len(pagination) != 0


def __get_doctor_next_page_href(next_page_href):
    return next_page_href + DOCTORS_HREF


class DoctorRatingSpider1(scrapy.Spider):
    name = "doctorrating-1"

    def start_requests(self):
        urls = ['https://www.ratemds.com/facilities/?country=us&page={}'.format(page_num) for page_num in
                range(1, 1000)]
        for url in urls:
            yield scrapy.Request(url=url, callback=parse_facilities)


class DoctorRatingSpider2(scrapy.Spider):
    name = "doctorrating-2"

    def start_requests(self):
        urls = ['https://www.ratemds.com/facilities/?country=us&page={}'.format(page_num) for page_num in
                range(1000, 2000)]
        for url in urls:
            yield scrapy.Request(url=url, callback=parse_facilities)


class DoctorRatingSpider3(scrapy.Spider):
    name = "doctorrating-3"

    def start_requests(self):
        urls = ['https://www.ratemds.com/facilities/?country=us&page={}'.format(page_num) for page_num in
                range(2000, 3000)]
        for url in urls:
            yield scrapy.Request(url=url, callback=parse_facilities)


class DoctorRatingSpider4(scrapy.Spider):
    name = "doctorrating-4"

    def start_requests(self):
        urls = ['https://www.ratemds.com/facilities/?country=us&page={}'.format(page_num) for page_num in
                range(3000, 4000)]
        for url in urls:
            yield scrapy.Request(url=url, callback=parse_facilities)


class DoctorRatingSpider5(scrapy.Spider):
    name = "doctorrating-5"

    def start_requests(self):
        urls = ['https://www.ratemds.com/facilities/?country=us&page={}'.format(page_num) for page_num in
                range(4000, 5000)]
        for url in urls:
            yield scrapy.Request(url=url, callback=parse_facilities)


class DoctorRatingSpider6(scrapy.Spider):
    name = "doctorrating-6"

    def start_requests(self):
        urls = ['https://www.ratemds.com/facilities/?country=us&page={}'.format(page_num) for page_num in
                range(5000, 6000)]
        for url in urls:
            yield scrapy.Request(url=url, callback=parse_facilities)


class DoctorRatingSpider7(scrapy.Spider):
    name = "doctorrating-7"

    def start_requests(self):
        urls = ['https://www.ratemds.com/facilities/?country=us&page={}'.format(page_num) for page_num in
                range(6000, 7000)]
        for url in urls:
            yield scrapy.Request(url=url, callback=parse_facilities)


class DoctorRatingSpider8(scrapy.Spider):
    name = "doctorrating-8"

    def start_requests(self):
        urls = ['https://www.ratemds.com/facilities/?country=us&page={}'.format(page_num) for page_num in
                range(7000, 8000)]
        for url in urls:
            yield scrapy.Request(url=url, callback=parse_facilities)


class DoctorRatingSpider9(scrapy.Spider):
    name = "doctorrating-9"

    def start_requests(self):
        urls = ['https://www.ratemds.com/facilities/?country=us&page={}'.format(page_num) for page_num in
                range(8000, 9000)]
        for url in urls:
            yield scrapy.Request(url=url, callback=parse_facilities)
