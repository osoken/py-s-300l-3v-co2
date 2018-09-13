# -*- coding: utf-8 -*-

import os
import time
import json
from logging.config import dictConfig


from flask import Flask, jsonify

from . sensor import S300L3VSensor


def gen_app(config_object=None, logsetting_file=None):
    if logsetting_file is not None:
        with open(logsetting_file, 'r') as fin:
            dictConfig(json.load(fin))
    elif os.getenv('PYS300L3VCO2_LOGGER') is not None:
        with open(os.getenv('PYS300L3VCO2_LOGGER'), 'r') as fin:
            dictConfig(json.load(fin))
    app = Flask(__name__)
    app.config.from_object('pys300l3vco2.config')
    if os.getenv('PYS300L3VCO2') is not None:
        app.config.from_envvar('PYS300L3VCO2')
    if config_object is not None:
        app.config.update(**config_object)

    sensor = S300L3VSensor(
        app.config['DEVICE'],
        baudrate=app.config['BAUDRATE'],
        timeout=app.config['TIMEOUT'],
        hook=lambda v: app.logger.info('sensor value.', extra=v)
    )

    @app.route('/api/co2')
    def api_co2():
        return jsonify({
            'co2': sensor.co2,
            'timestamp': time.time()
        })

    return app
