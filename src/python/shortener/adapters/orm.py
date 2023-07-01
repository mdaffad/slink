import logging

from shortener.domains.models import ShortLink, User
from sqlalchemy import Boolean, Column, ForeignKey, String, Table
from sqlalchemy.orm import registry, relationship

logger = logging.getLogger(__name__)

mapper_registry = registry()
metadata = mapper_registry.metadata

short_links = Table(
    "short_links",
    metadata,
    Column("source", String(32), primary_key=True),
    Column("destination", String(255)),
    Column("user_id", ForeignKey("users.id")),
    Column("is_private", Boolean),
)

users = Table(
    "users",
    metadata,
    Column("id", String(32), primary_key=True),
)


def start_mappers():
    logger.info("Starting mappers")
    short_links_mapper = mapper_registry.map_imperatively(ShortLink, short_links)
    mapper_registry.map_imperatively(
        User,
        users,
        properties={
            "_short_links": relationship(
                short_links_mapper,
                collection_class=set,
            )
        },
    )
