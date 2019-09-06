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


class DoctorRatingSpider(scrapy.Spider):
    name = "doctorrating"

    def __init__(self):
        self.DOCTORS_HREF = '#doctors'
        self.FLOAT_DECIMALS = 3

        with open('facilityfilter.json') as json_file:
            facility_filter_json = json.load(json_file)
        self.FACILITY_FILTER = set(facility_filter_json.get('Valid_Facility'))

    def start_requests(self):
        urls = [
            # Use 'https://www.ratemds.com/facilities/?country=us' to scrape ratings nation wide
            # 'https://www.ratemds.com/facilities/wa/seattle/',
            'https://www.ratemds.com/facilities/ny/ithaca/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_facilities)

    def parse_facilities(self, response):

        for facility in response.css('div.search-item'):
            facility_name = facility.css('h2.search-item-location-name::text').get()
            facility_href = facility.css('a.search-item-location-link::attr(href)').get() + self.DOCTORS_HREF
            if facility_name in self.FACILITY_FILTER:
                yield response.follow(facility_href, self.parse_facility_doctors,
                                      cb_kwargs=dict(facility_name=facility_name))

        next_page_href = self.get_next_page_href(response)
        if next_page_href is not None:
            yield response.follow(next_page_href, callback=self.parse_facilities)

    def parse_facility_doctors(self, response, facility_name):
        for doctor in response.css('div.doctor-profile h2.search-item-doctor-name a'):
            doctor_name = doctor.css('::text').get()
            cb_kwargs = dict(facility_name=facility_name, doctor_name=doctor_name, rating_matrix=list())
            yield response.follow(doctor.attrib['href'], self.parse_doctor_ratings, cb_kwargs=cb_kwargs)

        next_page_href = self.get_next_page_href(response)
        if next_page_href is not None:
            yield response.follow(self.__get_doctor_next_page_href(next_page_href), self.parse_facility_doctors,
                                  cb_kwargs=dict(facility_name=facility_name))

    def parse_doctor_ratings(self, response, facility_name, doctor_name, rating_matrix):
        rating = [0, 0, 0, 0]
        for rating in response.css('div.rating-numbers-compact'):
            rating_strings = rating.css('div.rating-number span.value::text').getall()
            rating_matrix.append(self.__get_valid_rating_numbers(rating_strings))

        next_page_href = self.get_next_page_href(response)
        if next_page_href is not None:
            cb_kwargs = dict(facility_name=facility_name, doctor_name=doctor_name, rating_matrix=rating_matrix)
            yield response.follow(next_page_href, callback=self.parse_doctor_ratings, cb_kwargs=cb_kwargs)
        else:
            if self.__has_rating(rating_matrix):
                rating = np.array(rating_matrix).mean(axis=0).round(self.FLOAT_DECIMALS)
            yield DoctorRatingItem(
                Facility_Name=facility_name,
                Doctor_Name=doctor_name,
                Staff_Rating=rating[0],
                Punctuality_Rating=rating[1],
                Helpfulness_Rating=rating[2],
                Knowledge_Rating=rating[3]
            )

    def get_next_page_href(self, response):
        next_page_href = None
        pagination = response.css('ul.pagination li a')
        if self.__has_pagination(pagination):
            next_page_href = pagination[-1].attrib['href']
        if self.__has_next_page(response.url, next_page_href):
            return next_page_href
        return None

    def __get_valid_rating_numbers(self, rating_strings):
        rating_numbers = [float(rating_string) for rating_string in rating_strings]
        if (len(rating_numbers) is 3):
            rating_numbers.insert(0, 5.0)
        return rating_numbers

    def __has_rating(self, rating_matrix):
        return len(rating_matrix) is not 0

    def __has_next_page(self, url, next_page_href):
        return next_page_href is not None and url.split('?')[-1] != next_page_href.split('?')[-1]

    def __has_pagination(self, pagination):
        return len(pagination) != 0

    def __get_doctor_next_page_href(self, next_page_href):
        return next_page_href + self.DOCTORS_HREF
