#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telegram
import logging

from flask import Flask, request

from bot.handlers.create import create, demo, delete, add_platform, exit, CREATE_FLOW_NAME  # noqa
from bot.handlers.start import start
from bot.handlers.help_page import help_page, ping, pong, whoareyou
from bot.handlers.rating import rating
from bot.handlers.review import review_fdde, review_pde, review_lhde
from bot.handlers.summary import summary
from bot.handlers.restaurants_list import restaurants_list
from bot.extensions import db, migrate
from bot.admin.api import downgrade
from bot.admin.api import drop_table
from bot.admin.api import upgrade

from .model import Flow
from .settings import config


class App(Flask):
    def make_shell_context(self):
        ctx = super(App, self).make_shell_context()
        ctx['db'] = db
        return ctx


def create_app(config_object=None, test=False):
    app = App(__name__)
    add_urls(app)
    app.config.from_object(config_object)
    app.config['SQLALCHEMY_DATABASE_URI'] = config_object.sql_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    register_extensions(app)
    # register_error_handlers(app)
    return app


def register_extensions(app, test=False):
    db.init_app(app)
    migrate.init_app(app, db=db)


def add_urls(app):
    app.add_url_rule(
        '/_admin/upgrade', view_func=upgrade, methods=["POST"])
    app.add_url_rule(
        '/_admin/downgrade', view_func=downgrade, methods=["POST"])
    app.add_url_rule(
        '/_admin/drop-table', view_func=drop_table, methods=["POST"])


app = create_app(config)
db.init_app(app)


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

global bot
bot = telegram.Bot(token='')


@app.route('/HOOK', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        body = request.get_json()
        logger.debug(body)
        if body.get("callback_query"):
            logger.debug("CALLBACK")
            logger.debug(body["callback_query"]["data"])
            data = body["callback_query"]["data"]

            if data.startswith("/delete"):
                logger.debug("CALL DELETE IN")
                delete(bot, update, data)
            if data.startswith("/rating"):
                logger.debug("CALL RATING IN")
                rating(bot, update, data)
            if data.startswith("/summary"):
                logger.debug("CALL SUMMARY IN")
                summary(bot, update, data)
            if data.startswith("/review_fdde"):
                logger.debug("CALL REVIEW FDDE IN")
                review_fdde(bot, update, data)
            if data.startswith("/review_pde"):
                logger.debug("CALL REVIEW PDE IN")
                review_pde(bot, update, data)
            if data.startswith("/review_lhde"):
                logger.debug("CALL REVIEW LHDE IN")
                review_lhde(bot, update, data)
            return 'ok'

        # retrieve the message in JSON and then transform it to Telegram object
        if not update.message:
            return 'err'
        if not update.message.text:
            return 'err'
        chat_id = update.message.chat.id
        # Telegram understands UTF-8, so encode text for unicode compatibility
        text = update.message.text.encode('utf-8')

        active_flow = Flow.check_flow_name(chat_id)
        if active_flow:
            flow = Flow.get_by_name(chat_id, active_flow)
            logger.debug("ACTIVE NAME " + active_flow)

            if text.startswith('/exit'):
                exit(bot, update, text, flow)
            else:
                if str(active_flow) == str(CREATE_FLOW_NAME):
                    logger.debug("ADD PLATFORM")
                    add_platform(bot, update, text, flow)
        else:
            if text.startswith('/'):
                if text == '/start':
                    start(bot, update, text)
                if text.startswith('/create'):
                    create(bot, update, text)
                if text.startswith('/rating'):
                    rating(bot, update, text)
                if text.startswith('/list'):
                    restaurants_list(bot, update, text)
                if text.startswith('/help'):
                    help_page(bot, update, text)
                if text.startswith('/exit'):
                    exit(bot, update, text)
                if text.startswith('/ping'):
                    ping(bot, update, text)
                if text.startswith('/demo'):
                    demo(bot, update, text)
                if text.startswith('/pong'):
                    pong(bot, update, text)
                if text.startswith('/whoareyou'):
                    whoareyou(bot, update, text)

        # repeat the same message back (echo)
        # bot.sendMessage(chat_id=chat_id, text="ECHO " + text)
        logger.debug(text)

    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('https://bot-dot-marvin-staging.appspot.com/HOOK')
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return 'ok'
