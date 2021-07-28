import pytest
from PythonAPI.rna_interaction import (
    InteractionFile,
    RNAInteraction,
    Evidence,
    Partner,
    Site,
)
import os


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
