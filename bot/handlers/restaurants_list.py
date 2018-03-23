#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telegram
import logging

from flask import Flask, request  # noqa

from bot.model import Restaurant


logger = logging.getLogger(__name__)


def restaurants_list(bot, update, text):
    chat_id = update.message.chat.id
    logger.debug("LIST")
    logger.debug(str(chat_id))

    restaurants = Restaurant.get_all(chat_id)

    icons = ["🏪", "🏦", "🏣"]

    for i, r in enumerate(restaurants):
        # reply = "Restaurant {0}".format(r)
        reply = """
""" + icons[i] + """ Restaurant Name: """ + str(r.name) + """
-----------
Pizza de ID: """ + str(r.pde) + """
Lieferheld de ID: """ + str(r.lhde) + """
Foodora de ID: """ + str(r.fdde) + """
-----------
        """
        delete_action = "/delete " + str(r.id) + " " + str(chat_id)
        rating_action = "/rating " + str(r.id) + " " + str(chat_id)
        summary_action = "/summary " + str(r.id) + " " + str(chat_id)

        button_list = [
            [
                telegram.InlineKeyboardButton(
                    "Detete 🗑", callback_data=delete_action),
                telegram.InlineKeyboardButton(
                    "Ratings 🤩", callback_data=rating_action)
            ],
            [telegram.InlineKeyboardButton(
                "Summary 📋",
                callback_data=summary_action,
            )],
        ]
        reply_markup = telegram.InlineKeyboardMarkup(button_list)
        bot.send_message(
            chat_id=chat_id,
            text=reply,
            reply_markup=reply_markup
        )
    if len(restaurants) == 0:
        reply = "Restaurants list is empty"
        bot.sendMessage(chat_id=chat_id, text=reply)
