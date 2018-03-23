#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import requests
import json

from flask import Flask, request  # noqa

from bot.model import Restaurant

logger = logging.getLogger(__name__)
BASE_URL = "https://marvin-eu.appspot.com/api/v1/"
PDE_NS = "pizza.de"
LHDE_NS = "lieferheld.de"
FDDE_NS = "fd-de"


def rating(bot, update, text):
    logger.debug("RATING")
    data = text.split()
    restaurant_id = data[1]
    chat_id = data[2]
    logger.debug(chat_id)

    r = Restaurant.get_by_id(restaurant_id)
    if not r:
        reply = "This Restaurant doesn't exists in my mind anymore 🤔"
        bot.sendMessage(chat_id=chat_id, text=reply)
        return

    rating_pde = None
    rating_lhde = None
    rating_fdde = None
    if r.pde:
        rating_pde = get_rating(r.pde, PDE_NS)
    if r.lhde:
        rating_lhde = get_rating(r.lhde, LHDE_NS)
    if r.fdde:
        rating_fdde = get_rating(r.fdde, FDDE_NS)

    reply = """
👉 """ + str(r.name) + """ Ratings by Platform
-----------
- Pizza de Rating: """ + str(rating_pde) + """
- Lieferheld de Rating: """ + str(rating_lhde) + """
- Foodora de Rating: """ + str(rating_fdde) + """
-----------
    """
    bot.sendMessage(chat_id=chat_id, text=reply)
    return


def get_rating(business_id, namespace):
    logger.debug(BASE_URL + "ratings/?businessId=" + business_id)
    response = requests.get(
        BASE_URL + "ratings/?businessId=" + business_id,
        headers={"X-MRV-Namespace": namespace}
    )
    data = json.loads(response.text)
    if len(data["data"]) > 0:
        average = data["data"][0]["average"]
    else:
        average = 0
    return average
