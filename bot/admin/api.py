from flask import jsonify
from flask_migrate import upgrade as _upgrade
from flask_migrate import downgrade as _downgrade

from bot.settings import config
from bot.extensions import db


def upgrade():
    try:
        _upgrade(directory=config.bot_migrations)
    except Exception as e:
        return jsonify({"error": e}), 500
    return jsonify({'status': 'ok'})


def downgrade():
    try:
        _downgrade(directory=config.bot_migrations)
    except Exception as e:
        return jsonify({"error": e}), 500
    return jsonify({'status': 'ok'})


def drop_table():
    try:
        db.session.execute("DROP TABLE restaurants")
    except Exception as e:
        return jsonify({"error": e}), 500
    return jsonify({'status': 'ok'})
