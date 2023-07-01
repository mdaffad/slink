python_sources(
    name="shortener",
    dependencies=[
        "3rdparty/python:reqs#psycopg2-binary",
        "3rdparty/python:reqs#asyncpg",
    ],
)
pex_binary(
    name="fastapi_app",
    entry_point="entrypoints/fastapi_app.py",
    restartable=True,
)

pex_binary(
    name="migrate",
    entry_point="entrypoints/migrate.py",
)
