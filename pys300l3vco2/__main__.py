# -*- coding: utf-8 -*-

from argparse import ArgumentParser

from . server import gen_app

parser = ArgumentParser(description='run S-300L-3V CO2 sensor server')


args = parser.parse_args()

app = gen_app()

app.run(host=app.config['HOST'])
