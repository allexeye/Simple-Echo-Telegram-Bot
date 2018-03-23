#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging


from bot.model import Restaurant, Flow

logger = logging.getLogger(__name__)

CREATE_FLOW_NAME = 'CREATE_RESTAURANT'

# EXIT Flow
# restrict /commands
# max 3
# make ping
# make summary
# FIXME set proper keyboard???


def delete(bot, update, text):
    logger.debug("DELETE")
    data = text.split()
    restaurant_id = data[1]
    chat_id = data[2]
    logger.debug(chat_id)

    r = Restaurant.get_by_id(restaurant_id)
    if not r:
        reply = "This Restaurant doesn't exists in my mind anymore 🤔"
        bot.sendMessage(chat_id=chat_id, text=reply)
        return

    try:
        r.delete()
    except Exception as e:
        logger.error(e)

    reply = "Restaurant '{0}' was deleted from your list 💀".format(r.name)
    bot.sendMessage(chat_id=int(chat_id), text=reply)
    return


def demo(bot, update, text):
    logger.debug("DEMO")
    chat_id = update.message.chat.id
    name = "habahaba"

    total_restaurants = len(Restaurant.get_all(chat_id))
    if total_restaurants > 2:
        reply = "You have 3 restaurants already - this is a maximum for now"  # noqa
        bot.sendMessage(chat_id=chat_id, text=reply)
        return

    r = create_demo_restaurant(name, chat_id)

    reply = "Demo Restaurant Name: {0}".format(r.name)
    bot.sendMessage(chat_id=chat_id, text=reply)
    reply_next = "👌 All set! Use /list to check your restaurants list"
    bot.sendMessage(chat_id=chat_id, text=reply_next)


def create(bot, update, text):
    logger.debug("CREATE")
    chat_id = update.message.chat.id
    name = text.split("/create", 1)[1]
    if str(name) == "":
        reply = "Restaurant Name shouldn't be empty, please use '/create restaurant_name' query"  # noqa
        bot.sendMessage(chat_id=chat_id, text=reply)
        return

    total_restaurants = len(Restaurant.get_all(chat_id))
    if total_restaurants > 2:
        reply = "You have 3 restaurants already - this is a maximum for now"  # noqa
        bot.sendMessage(chat_id=chat_id, text=reply)
        return

    r = create_restaurant(name, chat_id)
    set_flow(1, chat_id, restaurant_id=r.id)

    reply = "New Restaurant Name: {0}".format(r.name)
    bot.sendMessage(chat_id=chat_id, text=reply)
    reply_next = "Please Enter Pizza.de ID 🍕 to assign it to the Restaurant"
    bot.sendMessage(chat_id=chat_id, text=reply_next)
    reply_next = "Use /skip if it is not listed on Pizza.de or /exit to stop configuration"  # noqa
    bot.sendMessage(chat_id=chat_id, text=reply_next)


def exit(bot, update, text, flow):
    logger.debug("EXIT FLOW")
    chat_id = update.message.chat.id
    set_flow(0, chat_id, flow.restaurant_id)
    reply = "Restaurant configuration flow was cancelled..."
    bot.sendMessage(chat_id=chat_id, text=reply)


def add_platform(bot, update, text, flow):
    logger.debug("ADD PLATFORM")
    chat_id = update.message.chat.id

    if text == "/skip":
        reply = "Skipped..."
        bot.sendMessage(chat_id=chat_id, text=reply)

        if flow.state_id == 1:
            set_flow(2, chat_id, flow.restaurant_id)
            reply_next = "Please Enter Lieferheld.de ID 🥝 to assign it to the Restaurant"  # noqa
            bot.sendMessage(chat_id=chat_id, text=reply_next)
            reply_next = "Use /skip if it is not listed on Lieferheld.de or /exit to stop configuration"  # noqa
            bot.sendMessage(chat_id=chat_id, text=reply_next)
            return
        if flow.state_id == 2:
            set_flow(3, chat_id, flow.restaurant_id)
            reply_next = "Please Enter Foodora.de ID 🍣 to assign it to the Restaurant"  # noqa
            bot.sendMessage(chat_id=chat_id, text=reply_next)
            reply_next = "Use /skip if it is not listed on Foodora.de or /exit to stop configuration"  # noqa
            bot.sendMessage(chat_id=chat_id, text=reply_next)
            return
        if flow.state_id == 3:
            set_flow(0, chat_id, flow.restaurant_id)
            reply_next = "All set! Use /list to check your restaurants list"
            bot.sendMessage(chat_id=chat_id, text=reply_next)
            return
        return

    if text.startswith('/'):
        reply = "Restaurant ID shouldn't start with '/', please try again"
        bot.sendMessage(chat_id=chat_id, text=reply)
        return

    if len(text.split(" ", 1)) > 1:
        reply = "Wrong Input - Restaurant ID shouldn't have Spaces. Please try again"  # noqa
        bot.sendMessage(chat_id=chat_id, text=reply)
        return

    if flow.state_id == 1:
        r = Restaurant.get_by_id(flow.restaurant_id)
        r.pde = text
        r.update()
        set_flow(2, chat_id, flow.restaurant_id)

        reply = "🔥 Pizza.de Restaurant ID was set"
        bot.sendMessage(chat_id=chat_id, text=reply)
        reply_next = "Please Enter Lieferheld.de ID 🥝 to assign it to the Restaurant"  # noqa
        bot.sendMessage(chat_id=chat_id, text=reply_next)
        reply_next = "Use /skip if it is not listed on Lieferheld.de or /exit to stop configuration"  # noqa
        bot.sendMessage(chat_id=chat_id, text=reply_next)
        return

    if flow.state_id == 2:
        r = Restaurant.get_by_id(flow.restaurant_id)
        r.lhde = text
        r.update
        set_flow(3, chat_id, flow.restaurant_id)

        reply = "🔥 Lieferheld.de Restaurant ID was set"
        bot.sendMessage(chat_id=chat_id, text=reply)
        reply_next = "Please Enter Foodora.de ID 🍣 to assign it to the Restaurant"  # noqa
        bot.sendMessage(chat_id=chat_id, text=reply_next)
        reply_next = "Use /skip if it is not listed on Foodora.de or /exit to stop configuration"  # noqa
        bot.sendMessage(chat_id=chat_id, text=reply_next)
        return

    if flow.state_id == 3:
        r = Restaurant.get_by_id(flow.restaurant_id)
        r.fdde = text
        r.update()
        set_flow(0, chat_id, flow.restaurant_id)

        reply = "🔥 Foodora.de Restaurant ID was set"
        bot.sendMessage(chat_id=chat_id, text=reply)
        reply_next = "👌 All set! Use /list to check your restaurants list"
        bot.sendMessage(chat_id=chat_id, text=reply_next)
        return


def create_restaurant(name, chat_id):
    r = Restaurant(
        chat_id=chat_id,
        name=name,
    )
    r.save()
    return r


def create_demo_restaurant(name, chat_id):
    r = Restaurant(
        chat_id=chat_id,
        name=name,
    )
    r.lhde = "15454"
    r.fdde = "s4ft"
    r.save()
    return r


def set_flow(state, chat_id, restaurant_id=None):
    if Flow.check_flow_exists(chat_id, CREATE_FLOW_NAME):
        logger.debug("FLOW UPDATE")
        f = Flow.get_by_name(chat_id, CREATE_FLOW_NAME)
        f.state_id = state
        f.restaurant_id = restaurant_id
        f.update()
    else:
        logger.debug("FLOW SAVE")
        f = Flow(
            chat_id=chat_id,
            flow_name=CREATE_FLOW_NAME,
            state_id=state,
            restaurant_id=restaurant_id,
        )
        f.save()
    return f
