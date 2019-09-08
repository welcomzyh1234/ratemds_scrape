# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoctorRatingItem(scrapy.Item):
    Facility_Name = scrapy.Field()
    Doctor_Name = scrapy.Field()
    Staff_Rating = scrapy.Field()
    Punctuality_Rating = scrapy.Field()
    Helpfulness_Rating = scrapy.Field()
    Knowledge_Rating = scrapy.Field()
    Average_Rating = scrapy.Field()
