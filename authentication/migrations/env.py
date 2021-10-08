import os, sys

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

from database.env import run_migrations

from authentication.models import Base

def combine_metadata():
    from sqlalchemy import MetaData
    import authentication.models as models  # models file into which all models are imported

    model_classes = []
    for model_name in models.__all__:
        model_classes.append(getattr(models, model_name))

    m = MetaData()
    for model in model_classes:
        for t in model.metadata.tables.values():
            t.tometadata(m)

    return m

metadata = combine_metadata()
schema = [""]

print(metadata)
run_migrations(metadata, schema)