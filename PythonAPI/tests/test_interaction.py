import pytest
from PythonAPI.RNAInteractions import (
    InteractionFile,
    RNAInteraction,
    Evidence,
    Partner,
    GenomicCoordinates,
    LocalSite,
)
import os
import json
from tempfile import TemporaryDirectory, NamedTemporaryFile

TESTDIR = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = TemporaryDirectory()
TMP_TEST_DIR = TMP_DIR.name


@pytest.mark.parametrize(
    "path",
    [
        os.path.join(TESTDIR, "test.json"),
        os.path.join(TESTDIR, "multi_test.json"),
    ],
)
def test_file_load(path: str):
    file = InteractionFile.load(path)
    for interaction in file:
        assert type(interaction) == RNAInteraction
        for evidence in interaction.evidence:
            assert type(evidence) == Evidence
        for partner in interaction.partners:
            assert type(partner) == Partner
            assert type(partner.genomic_coordinates) == GenomicCoordinates
            for site in partner.local_sites:
                assert type(site) == LocalSite


@pytest.mark.parametrize(
    "path,testfile",
    [
        (
            os.path.join(TESTDIR, "test.json"),
            os.path.join(TMP_TEST_DIR, "single_tmp.json"),
        ),
        (
            os.path.join(TESTDIR, "multi_test.json"),
            os.path.join(TMP_TEST_DIR, "multi_tmp.json"),
        ),
    ],
)
def test_json_export(path: str, testfile):
    file = InteractionFile.load(path)
    file.export_json(testfile)
    with open(path) as handle, open(testfile) as handle2:
        json1 = json.load(handle)
        json2 = json.load(handle2)
    assert json1 == json2


@pytest.mark.parametrize(
    "path",
    [
        os.path.join(TESTDIR, "multi_test.json"),
        os.path.join(TESTDIR, "test.json"),
    ],
)
def test_file_parsing(path: str):
    i = 0
    for element in InteractionFile.parse(path):
        assert type(element) == RNAInteraction
        i += 1
    assert i != 0, "Parsing File yielded zero Interactions"
