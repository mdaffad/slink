from typing import Set
from uuid import uuid4

from pytest import fixture
from shortener.domains.models import ShortLink, User


def test_source_empty():
    new_short_link = ShortLink("", "http://test.com")
    assert new_short_link.is_empty()


@fixture
def short_link_a():
    return ShortLink("short-link-a", "http://my-web-a.com")


@fixture
def short_link_a_2():
    return ShortLink("short-link-a2", "http://my-web-a.com")


@fixture
def short_link_b():
    return ShortLink("short-link-b", "http://my-web-b.com")


def test_short_link_equivalent(
    short_link_a: ShortLink,
    short_link_a_2: ShortLink,
    short_link_b: ShortLink,
):
    assert short_link_a != short_link_b
    assert short_link_a != short_link_a_2


def test_short_link_hash(short_link_a: ShortLink):
    new_set: Set[ShortLink] = set()
    short_link_c = ShortLink(short_link_a.source, "http://my-web-c.com")

    new_set.add(short_link_a)
    new_set.add(short_link_c)

    assert len(new_set) == 1


@fixture
def user_a():
    return User(id=str(uuid4()))


@fixture
def test_register_short_link(
    user_a: User, short_link_a: ShortLink, short_link_b: ShortLink
):
    user_a.register_short_link(short_link_a)
    user_a.register_short_link(short_link_b)

    assert short_link_a in user_a._short_links and short_link_b in user_a._short_links

    return user_a


def test_update_short_link(test_register_short_link: User, short_link_a: ShortLink):
    user_a = test_register_short_link
    new_short_link = ShortLink(short_link_a.source, "http://new-address.com")
    user_a.update_short_links(new_short_link)
    assert short_link_a in user_a._short_links


def test_update_on_forbidden_access_link(test_register_short_link: User):
    user_a = test_register_short_link

    new_short_link = ShortLink("unregistered-sources", "http://any-web.com")
    user_a.update_short_links(new_short_link)
    assert new_short_link not in user_a._short_links
