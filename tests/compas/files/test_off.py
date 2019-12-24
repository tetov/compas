import os

import pytest

import compas
from compas.files.off import OFF, OFFReader

REPO_ROOT = os.path.join(os.path.dirname(compas.__file__), '../..')
BASE_FOLDER = os.path.dirname(__file__)


@pytest.fixture
def cube_off():
    return os.path.join(REPO_ROOT, 'data', 'cube.off')


@pytest.fixture
def cube_off_w_continuing_lines():
    return os.path.join(BASE_FOLDER, 'fixtures', 'cube_w_continuing_lines.off')


@pytest.fixture
def sphere_off():
    return os.path.join(BASE_FOLDER, 'fixtures', 'sphere.off')


def test_OFFReader(cube_off):
    off = OFFReader(cube_off)

    assert len(off.vertices) == 8


def test_off_continuing_lines(cube_off_w_continuing_lines):
    off = OFFReader(cube_off_w_continuing_lines)

    assert len(off.faces) == 6


def test_OFF(sphere_off):
    off = OFF(sphere_off)

    assert off.reader.number_of_faces == 180
