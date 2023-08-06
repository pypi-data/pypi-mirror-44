import asyncio
import logging
from argparse import ArgumentParser
from logging.config import dictConfig

from aiohttp import web

from mem_usage_ui.routes import setup_routes
from mem_usage_ui.snapshot import SnapshotProcessor


async def init_app(loop):
    app = web.Application()
    app["websockets"] = set()
    app["snapshot_processor"] = SnapshotProcessor(loop)

    app.on_cleanup.append(shutdown)
    setup_routes(app)
    return app


async def shutdown(app):
    for ws in app["websockets"]:
        await ws.close()

    app["websockets"].clear()


def configure_logging(debug=False):
    level = logging.DEBUG if debug else logging.INFO

    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': level,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'mem_usage_ui': {
                'handlers': ['default'],
                'level': level,
                'propagate': True
            },
        }
    })


def open_browser(url):
    import webbrowser
    webbrowser.open(url)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--debug", required=False, default=False)
    parser.add_argument("--host", required=False, default="localhost")
    parser.add_argument("--port", required=False, default=8080)

    return parser.parse_args()


def main():
    options = parse_args()
    configure_logging(options.debug)
    loop = asyncio.get_event_loop()
    loop.set_debug(options.debug)
    app = init_app(loop)
    loop.call_later(1, open_browser, "http://{host}:{port}".format(host=options.host, port=options.port))
    web.run_app(app, host=options.host, port=options.port)


if __name__ == "__main__":
    main()
