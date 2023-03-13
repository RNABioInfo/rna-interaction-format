import pytest
from RIF.RNAInteractionFormat import (
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
    testfile = InteractionFile.load(path)
    for interaction in testfile:
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
            "single_tmp.json",
        ),
        (
            "multi_test_json",
            "multi_tmp.json",
        ),
    ],
)
def test_json_export(path: str, testfile, tmpdir, request):
    path = request.getfixturevalue(path)
    infile = InteractionFile.load(path)
    testfile = os.path.join(tmpdir, testfile)
    infile.export_json(testfile)
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


def test_bed_export(expected_bed, tmpdir, multi_test_json):
    interaction_file = InteractionFile.load(multi_test_json)

    file_path = os.path.join(tmpdir, "bed_export_test.bed")
    interaction_file.export_bed(file_path)
    with open(file_path, "r") as handle, open(expected_bed, "r") as expected_handle:
        expected = expected_handle.read().split("\n")
        result = handle.read()
        for line in result.split(("\n")):
            if line not in expected:
                print(line)
            assert line in expected


def interaction_from_scratch():
    evidence = Evidence(
        evidence_type="prediction",
        method="RNAProt",
        command="RNAProt predict --mode 2 --thr 2",
        data={"significance": {"p-value": 0.001}},
    )
    mrna_partner = Partner(
        name="Tumor protein P53",
        symbol="TP53",
        partner_type="mRNA",
        organism_name="Homo sapiens",
        genomic_coordinates=GenomicCoordinates(
            chromosome="chr17",
            strand="-",
            start=7687490,
            end=7668421,
        ),
        local_sites={
            "ELAVL1": [LocalSite(start=2125, end=2160), LocalSite(start=2452, end=2472)]
        },
        custom={
            "organism_acc": "9606",
        },
    )
    rbp_partner = Partner(
        name="ELAV-like protein 1",
        symbol="ELAVL1",
        partner_type="Protein",
        organism_name="Homo sapiens",
        genomic_coordinates=GenomicCoordinates(
            chromosome="chr19",
            strand="-",
            start=8005641,
            end=7958573,
        ),
        local_sites={
            "Tumor protein P53": [
                LocalSite(start=2125, end=2160),
                LocalSite(start=2452, end=2472),
            ]
        },
        custom={
            "organism_acc": "9606",
        },
    )
    interaction = RNAInteraction(
        interaction_id=1,
        evidence=[evidence],
        interaction_class="RNA-Protein",
        interaction_type="RNA binding",
        partners=[mrna_partner, rbp_partner],
    )
    return interaction


def test_interaction_from_scratch():
    interaction = interaction_from_scratch()
    assert isinstance(interaction, RNAInteraction)
    _ = InteractionFile([interaction])


@pytest.fixture()
def fixt_interaction_from_scratch():
    return interaction_from_scratch()


def test_add_interaction(fixt_interaction_from_scratch, multi_test_json):
    interaction_file = InteractionFile.load(multi_test_json)

    interaction_file.add(fixt_interaction_from_scratch)
    assert fixt_interaction_from_scratch in interaction_file.interactions


def test_rm_interaction(multi_test_json):
    interaction_file = InteractionFile.load(multi_test_json)
    interaction_file.rm(1)
    ids = [interaction.interaction_id for interaction in interaction_file]
    assert 1 not in ids
