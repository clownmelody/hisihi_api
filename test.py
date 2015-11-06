__author__ = 'bliss'

import sys
from herovii import create_app
from herovii.models import db
from enum import Enum


class games(Enum):
    hero = 1
    msg = 2
    tlou = 3

print(games.g)
