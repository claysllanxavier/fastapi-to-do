import os, sys

from database.env import run_migrations

from core.database import Base

from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
from authentication.models import *

metadata = Base.metadata
schema = [""]

run_migrations(metadata, schema)