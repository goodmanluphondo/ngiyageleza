import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def init_database():
    database = get_database()

    with current_app.open_resource('schema.sql') as f:
        database.executescript(f.read().decode('utf-8'))

@click.command('init-db')
@with_appcontext
def init_database_command():
    init_database()
    click.echo('Initialised the database')

def init_application(app):
    app.teardown_appcontext(close_database)
    app.cli.add_command(init_database_command)

def get_database():
    if 'database' not in g:
        g.database = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.database.row_factory = sqlite3.Row
    
    return g.database

def close_database(self):
    database = g.pop('database', None)

    if database is not None:
        database.close()
