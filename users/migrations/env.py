import os, sys

from database.env import run_migrations

from core.database import Base
from users.models import *

metadata = Base.metadata
schema = ["User"]

run_migrations(metadata, schema)