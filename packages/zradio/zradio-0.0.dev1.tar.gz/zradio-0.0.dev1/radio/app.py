from radio.log import logger

from radio.tui import application


def main():
    logger.info("init app")
    application.run()
