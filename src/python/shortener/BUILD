python_sources(
    name="shortener",
    dependencies=[
        "3rdparty/python:default#psycopg2-binary",
        "3rdparty/python:default#asyncpg",
    ],
)
pex_binary(
    name="fastapi_app",
    entry_point="entrypoints/fastapi_app.py",
    restartable=True,
)

pex_binary(
    name="migrate_app",
    entry_point="entrypoints/migrate.py",
)
