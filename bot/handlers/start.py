#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telegram  # noqa
import logging  # noqa

from flask import Flask, request  # noqa

from ..settings import Config

logger = logging.getLogger(__name__)


def start(bot, update, text):
    chat_id = update.message.chat.id
    logger.debug("START")

    # reply = "Please use /create restaurant_name"
    # bot.sendMessage(chat_id=chat_id, text=reply)

    reply = """
👉 Welcome! I am 'Delivery Tech Reviews Bot' 🤖

- Use /create "restaurant name" to add a restaurant.
- Use /help to see a help message.
- Use /list to see a list of added restaurants.

DM 📩 @TestingCatalog with feedback.

        """

    test_keyboard = telegram.KeyboardButton(
        text="/ping the bot", value=1)
    custom_keyboard = [
            ['/list my restaurants'],
            [test_keyboard, '/help me'],
        ]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.send_photo(
        chat_id=chat_id, photo=open(Config.bot_static + '/logo2.png', 'rb'))
    bot.send_message(
        chat_id=chat_id,
        text=reply,
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )
