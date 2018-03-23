#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telegram
import logging

from flask import Flask, request  # noqa

from bot.model import Restaurant


logger = logging.getLogger(__name__)


def summary(bot, update, text):
    logger.debug("SUMMARY")
    data = text.split()
    restaurant_id = data[1]
    chat_id = data[2]
    logger.debug(chat_id)

    r = Restaurant.get_by_id(restaurant_id)
    if not r:
        reply = "This Restaurant doesn't exists in my mind anymore 🤔"
        bot.sendMessage(chat_id=chat_id, text=reply)
        return

    reviews_pde_action = "/review_pde " + str(r.id) + " " + str(chat_id)
    reviews_lhde_action = "/review_lhde " + str(r.id) + " " + str(chat_id)
    reviews_fdde_action = "/review_fdde " + str(r.id) + " " + str(chat_id)

    reply = "👉 {0} Summary Menu".format(r.name)
    bot.sendMessage(chat_id=chat_id, text=reply)

    if r.pde:
        web_btn = telegram.InlineKeyboardButton(
            "Open Website",
            callback_data=0,
            url="https://pizza.de/lieferservice/berlin/restaurant-sushi-for-you10/" + r.pde + "/"  # noqa
        )
        rew_btn = telegram.InlineKeyboardButton(
            "Show Reviews",
            callback_data=reviews_pde_action,
        )

        reply = "Pizza DE"
        reply_markup = telegram.InlineKeyboardMarkup([[web_btn], [rew_btn]])
        bot.send_message(
            chat_id=chat_id,
            text=reply,
            reply_markup=reply_markup
        )
    if r.lhde:
        web_btn = telegram.InlineKeyboardButton(
            "Open Website",
            callback_data=0,
            url="https://www.lieferheld.de/lieferservices-berlin/restaurant-habba-habba/" + r.lhde + "/"  # noqa
        )
        rew_btn = telegram.InlineKeyboardButton(
            "Show Reviews",
            callback_data=reviews_lhde_action,
        )

        reply = "Lieferheld DE"
        reply_markup = telegram.InlineKeyboardMarkup([[web_btn], [rew_btn]])
        bot.send_message(
            chat_id=chat_id,
            text=reply,
            reply_markup=reply_markup
        )
    if r.fdde:
        web_btn = telegram.InlineKeyboardButton(
            "Open Website",
            callback_data=0,
            url="https://www.foodora.de/restaurant/" + r.fdde + "/"  # noqa
        )
        rew_btn = telegram.InlineKeyboardButton(
            "Show Reviews",
            callback_data=reviews_fdde_action,
        )

        reply = "Foodora DE"
        reply_markup = telegram.InlineKeyboardMarkup([[web_btn], [rew_btn]])
        bot.send_message(
            chat_id=chat_id,
            text=reply,
            reply_markup=reply_markup
        )

    if not r.pde and not r.lhde and not r.fdde:
        reply = "Restaurant is not assigned to any platform, please delete it"
        bot.sendMessage(chat_id=chat_id, text=reply)
    return
