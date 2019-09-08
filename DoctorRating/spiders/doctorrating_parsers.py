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
        cb_kwargs = dict(facility_name=facility_name, doctor_name=doctor_name)
        yield response.follow(doctor.attrib['href'], parse_doctor_ratings, cb_kwargs=cb_kwargs)

    if len(doctors) != 0:
        next_page_href = get_next_page_href(response)
        if next_page_href is not None:
            yield response.follow(get_doctor_next_page_href(next_page_href), parse_facility_doctors,
                                  cb_kwargs=dict(facility_name=facility_name))


def parse_doctor_ratings(response, facility_name, doctor_name):
    ratings = response.css('div.rating')
    if has_rating(ratings):
        for rating in ratings:
            for rating_values in rating.css('div.rating-numbers-compact'):
                rating_value_strings = rating_values.css('div.rating-number span.value::text').getall()
                rating_value_numbers = get_valid_rating_numbers(rating_value_strings)
            rating_comment = rating.css('div.rating-comment')
            yield DoctorRatingItem(
                Facility_Name=facility_name,
                Doctor_Name=doctor_name,
                Has_Rating=1,
                Staff_Rating=rating_value_numbers[0],
                Punctuality_Rating=rating_value_numbers[1],
                Helpfulness_Rating=rating_value_numbers[2],
                Knowledge_Rating=rating_value_numbers[3],
                Average_Rating=rating_value_numbers.mean().round(FLOAT_DECIMALS),
                Comment_Text=rating_comment.css('p.rating-comment-body span::text').get(),
                Comment_Votes=rating_comment.css('p.rating-comment-votes span::text').getall()[-2],
                Comment_Date=rating_comment.css('p.rating-comment-created a span::text').getall()[-1]
            )
        next_page_href = get_next_page_href(response)
        if next_page_href is not None:
            cb_kwargs = dict(facility_name=facility_name, doctor_name=doctor_name)
            yield response.follow(next_page_href, callback=parse_doctor_ratings, cb_kwargs=cb_kwargs)
    else:
        yield DoctorRatingItem(
            Facility_Name=facility_name,
            Doctor_Name=doctor_name,
            Has_Rating=0,
            Staff_Rating=None,
            Punctuality_Rating=None,
            Helpfulness_Rating=None,
            Knowledge_Rating=None,
            Average_Rating=None,
            Comment_Text=None,
            Comment_Votes=None,
            Comment_Date=None
        )
