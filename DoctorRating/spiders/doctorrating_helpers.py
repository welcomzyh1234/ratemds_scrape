from DoctorRating.spiders.doctorrating_constants import DOCTORS_HREF


def get_next_page_href(response):
    next_page_href = None
    pagination = response.css('ul.pagination li a')
    if has_pagination(pagination):
        next_page_href = pagination[-1].attrib['href']
    if has_next_page(response.url, next_page_href):
        return next_page_href
    return None


def get_valid_rating_numbers(rating_strings):
    rating_numbers = [float(rating_string) for rating_string in rating_strings]
    if (len(rating_numbers) is 3):
        rating_numbers.insert(0, 5.0)
    return rating_numbers


def has_rating(rating_matrix):
    return len(rating_matrix) is not 0


def has_next_page(url, next_page_href):
    return next_page_href is not None and url.split('?')[-1] != next_page_href.split('?')[-1]


def has_pagination(pagination):
    return len(pagination) != 0


def get_doctor_next_page_href(next_page_href):
    return next_page_href + DOCTORS_HREF
