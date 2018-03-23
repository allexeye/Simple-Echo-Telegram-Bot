#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telegram  # noqa
import logging  # noqa

from flask import Flask, request  # noqa

from ..settings import Config

logger = logging.getLogger(__name__)


def help_page(bot, update, text):
    chat_id = update.message.chat.id
    logger.debug("HELP")

    # reply = "Help Message..."
    reply = """
👉 Helpful Commands

This bot can help restaurant owners to stay in touch with Delivery Hero Ratings & Reviews system.

- Use /create "restaurant name" to add a restaurant.
- Use /help to see a help message.
- Use /list to see a list of added restaurants.
- Use /whoareyou to see a gif

More to come: Reviews & Ratings Insights, Updates Notifications, Yelp/Foursquare/Google Integration...

For Demo: You can add habahaba restaurant to your list by typing /demo

DM 📩 @TestingCatalog with feedback.

        """  # noqa
    bot.send_photo(
        chat_id=chat_id, photo=open(Config.bot_static + '/logo2.png', 'rb'))
    bot.sendMessage(
        chat_id=chat_id, text=reply, parse_mode=telegram.ParseMode.MARKDOWN)


def ping(bot, update, text):
    chat_id = update.message.chat.id
    logger.debug("PING")

    reply = "/pong back to the human 🏓"
    bot.sendMessage(chat_id=chat_id, text=reply)


def pong(bot, update, text):
    chat_id = update.message.chat.id
    logger.debug("PONG")

    reply = "You lost 1-0 👻"
    bot.sendMessage(chat_id=chat_id, text=reply)


def whoareyou(bot, update, text):
    chat_id = update.message.chat.id
    logger.debug("WHOAMI")

    reply = "I am a bot 🤖, just check this vid below 👇"
    bot.sendMessage(chat_id=chat_id, text=reply)
    bot.send_document(
        chat_id=chat_id, document=open(Config.bot_static + '/movie.mp4', 'rb'))
