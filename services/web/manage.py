# -*- coding: utf-8 -*-
from flask.cli import FlaskGroup

from project.common import app
from project.models import User


cli = FlaskGroup(app)


if __name__ == "__main__":
    cli()
