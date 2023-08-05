from random import randint

import pytest
from faker import Faker

from synapse_p2p.messages import Intro
from synapse_p2p.server import Server
from synapse_p2p.types import Node
from synapse_p2p.utils import random_hash

f = Faker()


@pytest.fixture
def identifier():
    return random_hash()


@pytest.fixture
def ipv4():
    return f.ipv4_public()


@pytest.fixture
def port():
    return randint(2000, 10000)


@pytest.fixture
def node(identifier, ipv4, port):
    return {
        "identifier": identifier,
        "ip": ipv4,
        "port": port,
    }


@pytest.fixture
def intro(node, identifier):
    return Intro(
        identifier=identifier,
        nodes=[Node(**node) for _ in range(randint(0, 20))],
    )


@pytest.fixture
def server():
    return Server("123", "127.0.0.1", 9999)
