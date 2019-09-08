import numpy as np

from DoctorRating.items import DoctorRatingItem
from DoctorRating.spiders.doctorrating_constants import FLOAT_DECIMALS, FACILITY_FILTER, DOCTORS_HREF
from DoctorRating.spiders.doctorrating_helpers import get_next_page_href, get_valid_rating_numbers, has_rating, \
    get_doctor_next_page_href


def parse_facilities(response):
    for facility in response.css('div.search-item'):
        facility_name = facility.css('h2.search-item-location-name::text').get().upper()
        facility_href = facility.css('a.search-item-location-link::attr(href)').get() + DOCTORS_HREF

        if facility_name in FACILITY_FILTER:
            yield response.follow(facility_href, parse_facility_doctors,
                                  cb_kwargs=dict(facility_name=facility_name))


def parse_facility_doctors(response, facility_name):
    doctors = response.css('div.doctor-profile h2.search-item-doctor-name a')
    for doctor in doctors:
        doctor_name = doctor.css('::text').get()
        cb_kwargs = dict(facility_name=facility_name, doctor_name=doctor_name, rating_matrix=list())
        yield response.follow(doctor.attrib['href'], parse_doctor_ratings, cb_kwargs=cb_kwargs)

    if len(doctors) != 0:
        next_page_href = get_next_page_href(response)
        if next_page_href is not None:
            yield response.follow(get_doctor_next_page_href(next_page_href), parse_facility_doctors,
                                  cb_kwargs=dict(facility_name=facility_name))


def parse_doctor_ratings(response, facility_name, doctor_name, rating_matrix):
    rating = np.array([0, 0, 0, 0])
    for rating in response.css('div.rating-numbers-compact'):
        rating_strings = rating.css('div.rating-number span.value::text').getall()
        rating_matrix.append(get_valid_rating_numbers(rating_strings))

    next_page_href = get_next_page_href(response)
    if next_page_href is not None:
        cb_kwargs = dict(facility_name=facility_name, doctor_name=doctor_name, rating_matrix=rating_matrix)
        yield response.follow(next_page_href, callback=parse_doctor_ratings, cb_kwargs=cb_kwargs)
    else:
        if has_rating(rating_matrix):
            rating = np.array(rating_matrix).mean(axis=0).round(FLOAT_DECIMALS)
        yield DoctorRatingItem(
            Facility_Name=facility_name,
            Doctor_Name=doctor_name,
            Staff_Rating=rating[0],
            Punctuality_Rating=rating[1],
            Helpfulness_Rating=rating[2],
            Knowledge_Rating=rating[3],
            Average_Rating=rating.mean().round(FLOAT_DECIMALS)
        )
