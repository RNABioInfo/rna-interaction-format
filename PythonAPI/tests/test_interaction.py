import pytest
from PythonAPI.RNAInteraction.RNAInteractions import (
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
import jsonschema

TESTDIR = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = TemporaryDirectory()
TMP_TEST_DIR = TMP_DIR.name


@pytest.fixture()
def test_json():
    return os.path.join(TESTDIR, "test.json")


@pytest.fixture()
def multi_test_json():
    return os.path.join(TESTDIR, "multi_test.json")


@pytest.mark.parametrize(
    "path",
    [
        "test_json",
        "multi_test_json",
    ],
)
def test_file_load(path, request):
    path = request.getfixturevalue(path)
    file = InteractionFile.load(path)
    for interaction in file:
        assert type(interaction) == RNAInteraction
        for evidence in interaction.evidence:
            assert type(evidence) == Evidence
        for partner in interaction.partners:
            assert type(partner) == Partner
            assert type(partner.genomic_coordinates) == GenomicCoordinates
            for key, site_list in partner.local_sites.items():
                for site in site_list:
                    assert type(site) == LocalSite


@pytest.mark.parametrize(
    "path,testfile",
    [
        (
            "test_json",
            os.path.join(TMP_TEST_DIR, "single_tmp.json"),
        ),
        (
            "multi_test_json",
            os.path.join(TMP_TEST_DIR, "multi_tmp.json"),
        ),
    ],
)
def test_json_export(path: str, testfile, request):
    path = request.getfixturevalue(path)
    file = InteractionFile.load(path)
    file.export_json(testfile)
    with open(path) as handle, open(testfile) as handle2:
        json1 = json.load(handle)
        json2 = json.load(handle2)
    assert json1 == json2


@pytest.mark.parametrize(
    "path",
    [
        "multi_test_json",
        "test_json",
    ],
)
def test_file_parsing(path, request):
    path = request.getfixturevalue(path)
    i = 0
    for element in InteractionFile.parse(path):
        assert type(element) == RNAInteraction
        i += 1
    assert i != 0, "Parsing File yielded zero Interactions"


@pytest.fixture()
def evidence():
    return Evidence("prediction", "CopraRNA", "CopraRNA -h")


@pytest.fixture()
def evidence_list():
    return [Evidence("prediction", "CopraRNA", "CopraRNA -h")]


@pytest.fixture()
def none_fixture():
    return None


@pytest.mark.parametrize(
    "interaction_id,interaction_class,interaction_type,evidence",
    [(1, "RNA-RNA", "basepairing", "evidence_list")],
)
def test_rna_interaction_init(
    interaction_id, interaction_class, interaction_type, evidence, request
):
    evidence = request.getfixturevalue(evidence)
    rna_interaction = RNAInteraction(
        interaction_id, interaction_class, interaction_type, evidence
    )


@pytest.mark.parametrize(
    "interaction_id,interaction_class,interaction_type,evidence",
    [
        (1, "Foo", "basepairing", "evidence_list"),
        ("foo", "RNA-RNA", "basepairing", "evidence_list"),
        (1, "RNA-RNA", "foo", "none_fixture"),
    ],
)
def test_wrong_schema_rna_interaction(
    interaction_id, interaction_class, interaction_type, evidence, request
):
    with pytest.raises(jsonschema.ValidationError):
        evidence = request.getfixturevalue(evidence)
        interaction = RNAInteraction(
            interaction_id, interaction_class, interaction_type, evidence
        )
        InteractionFile([interaction])


def test_printing_interaction(test_json, capsys):
    interaction_file = InteractionFile.load(test_json)
    print(interaction_file)
    stdout = capsys.readouterr().out
    printed_json = json.loads(stdout)
    with open(test_json) as handle:
        expected_json = json.load(handle)
    assert printed_json == expected_json


@pytest.fixture()
def expected_bed():
    return os.path.join(TESTDIR, "expected_bed_export.bed")


def test_bed_export(expected_bed, tmpdir, test_json):
    interaction_file = InteractionFile.load(test_json)

    file_path = os.path.join(tmpdir, "bed_export_test.bed")
    interaction_file.export_bed(file_path)
    with open(file_path, "r") as handle, open(expected_bed, "r") as expected_handle:
        expected = expected_handle.read().split("\n")
        result = handle.read()
        for line in result.split(("\n")):
            assert line in expected

