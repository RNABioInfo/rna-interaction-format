import pytest
from PythonAPI.rna_interaction import (
    InteractionFile,
    RNAInteraction,
    Evidence,
    Partner,
    Site,
)
import os
import json


TESTDIR = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize("path", [os.path.join(TESTDIR, "test.json")])
def test_file_load(path: str):
    file = InteractionFile.load(path)
    for interaction in file:
        assert type(interaction) == RNAInteraction
        for evidence in interaction.evidence:
            assert type(evidence) == Evidence
        for partner in interaction.partners:
            assert type(partner) == Partner
            for site in partner.sites:
                assert type(site) == Site


@pytest.mark.parametrize("path", [os.path.join(TESTDIR, "test.json")])
def test_json_export(path: str):
    file = InteractionFile.load(path)
    file.export_json("./testfile.json")
    with open(path) as handle, open("./testfile.json") as handle2:
        json1 = json.load(handle)
        json2 = json.load(handle2)
    assert json1 == json2
    p = 0
