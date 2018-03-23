#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import requests
import json
import telegram  # noqa

from datetime import datetime
from flask import Flask, request  # noqa

from bot.model import Restaurant

logger = logging.getLogger(__name__)
BASE_URL = "https://marvin-eu.appspot.com/api/v1/"
PDE_NS = "pizza.de"
LHDE_NS = "lieferheld.de"
FDDE_NS = "fd-de"


def review_fdde(bot, update, text):
    logger.debug("REVIEW FDDE")
    data = text.split()
    restaurant_id = data[1]
    chat_id = data[2]
    logger.debug(chat_id)

    r = Restaurant.get_by_id(restaurant_id)
    reviews_fdde = get_reviews(r.fdde, FDDE_NS)

    reply = """
    👉 Latest 5 reviews from Foodora.de
    """
    bot.sendMessage(chat_id=chat_id, text=reply)
    if reviews_fdde:
        for i, r in enumerate(reviews_fdde):
            if i < 6:
                ratings = reviews_fdde[i]["ratings"]
                text = reviews_fdde[i]["text"].encode('utf-8')
                d = reviews_fdde[i]["createdAt"]
                date = datetime.strptime(d[:19], '%Y-%m-%dT%H:%M:%S')
                date = date.strftime('%Y-%m-%d')
                food = (item for item in ratings if item["name"] == "restaurant_food").next()  # noqa
                stars = ""
                for s in range(int(food["value"])):
                    stars = stars + "⭐️"

                message = """
Date: """ + str(date) + """
Rating: """ + str(stars) + """
Review: """ + str(text) + """
                """
                bot.sendMessage(
                    chat_id=chat_id,
                    text=message,
                    parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        reply = "There are no reviews with text so far 🤔"
        bot.sendMessage(chat_id=chat_id, text=reply)
    return


def review_pde(bot, update, text):
    logger.debug("REVIEW PDE")
    data = text.split()
    restaurant_id = data[1]
    chat_id = data[2]
    logger.debug(chat_id)

    r = Restaurant.get_by_id(restaurant_id)
    reviews_pde = get_reviews(r.pde, PDE_NS)

    reply = """
    👉 Latest 5 reviews from Pizza.de
    """
    bot.sendMessage(chat_id=chat_id, text=reply)
    if reviews_pde:
        for i, r in enumerate(reviews_pde):
            if i < 6:
                ratings = reviews_pde[i]["ratings"]
                text = reviews_pde[i]["text"].encode('utf-8')
                d = reviews_pde[i]["createdAt"]
                date = datetime.strptime(d[:19], '%Y-%m-%dT%H:%M:%S')
                date = date.strftime('%Y-%m-%d')
                food = (item for item in ratings if item["name"] == "restaurant_food").next()  # noqa
                stars = ""
                for s in range(int(food["value"])):
                    stars = stars + "⭐️"

                message = """
Date: """ + str(date) + """
Rating: """ + str(stars) + """
Review: """ + str(text) + """
                """
                bot.sendMessage(
                    chat_id=chat_id,
                    text=message,
                    parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        reply = "There are no reviews with text so far 🤔"
        bot.sendMessage(chat_id=chat_id, text=reply)
    return


def review_lhde(bot, update, text):
    logger.debug("REVIEW LHDE")
    data = text.split()
    restaurant_id = data[1]
    chat_id = data[2]
    logger.debug(chat_id)

    r = Restaurant.get_by_id(restaurant_id)
    reviews_lhde = get_reviews(r.lhde, LHDE_NS)

    reply = """
    👉 Latest 5 reviews from Lieferheld.de
    """
    bot.sendMessage(chat_id=chat_id, text=reply)
    if reviews_lhde:
        for i, r in enumerate(reviews_lhde):
            if i < 6:
                ratings = reviews_lhde[i]["ratings"]
                text = reviews_lhde[i]["text"].encode('utf-8')
                d = reviews_lhde[i]["createdAt"]
                date = datetime.strptime(d[:19], '%Y-%m-%dT%H:%M:%S')
                date = date.strftime('%Y-%m-%d')
                food = (item for item in ratings if item["name"] == "restaurant_food").next()  # noqa
                stars = ""
                for s in range(int(food["value"])):
                    stars = stars + "⭐️"

                message = """
Date: """ + str(date) + """
Rating: """ + str(stars) + """
Review: """ + str(text) + """
                """
                bot.sendMessage(
                    chat_id=chat_id,
                    text=message,
                    parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        reply = "There are no reviews with text so far 🤔"
        bot.sendMessage(chat_id=chat_id, text=reply)
    return


def get_reviews(business_id, namespace):
    logger.debug(BASE_URL + "reviews/?businessId=" + business_id)
    response = requests.get(
        BASE_URL + "reviews/?businessId=" + business_id + "&hasText=true",
        headers={"X-MRV-Namespace": namespace}
    )
    data = json.loads(response.text)
    if len(data["data"]) > 0:
        reviews = data["data"]
    else:
        reviews = None
    return reviews
