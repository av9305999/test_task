import click
import uvicorn

from api.app import init_app
from config import settings

app = init_app()


@click.command(name='run_server')
def runserver():
    """Start API server."""
    server_config = dict(
        port=4000,
        host='0.0.0.0',
        lifespan='on'
    )
    if settings.DEBUG:
        server_config['reload'] = True
        server_config['log_level'] = 'info'

    uvicorn.run("main:app", **server_config)


@click.group()
def cli():
    """Initialize CLI."""


cli.add_command(runserver)


if __name__ == '__main__':
    cli()