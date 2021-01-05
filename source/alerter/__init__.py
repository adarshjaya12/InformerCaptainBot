import source.alerter.discord

from source.alerter.common import AlerterFactory


def init_alerters(args):
    return AlerterFactory.create(args)
