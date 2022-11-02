from __future__ import annotations
import ijson
import json
import os
from dataclasses import dataclass
from typing import List, Union, Dict, Generator
from collections import defaultdict, OrderedDict
from Bio import Seq
import jsonschema


class InteractionFile:
    def __init__(self, interactions: List[RNAInteraction], validate: bool = True):
        self.interactions = interactions
        if validate:
            self.__json_validate(
                json.loads(json.dumps(self, cls=CustomEncoder))
            )

    @classmethod
    def parse(cls, file: Union[str, os.PathLike]) -> Generator[RNAInteraction]:
        i = 0
        with open(file, "rb") as handle:
            parser = ijson.parse(handle)
            for element in ijson.items(parser, "item"):
                i += 1
                yield RNAInteraction.from_dict(element)
            if i == 0:
                handle.seek(0)
                json_repr = json.load(handle)
                yield RNAInteraction.from_dict(json_repr)

    @staticmethod
    def __json_validate(json_repr):
        with open(
                os.path.join(
                    os.path.dirname(__file__), "rna-interaction-schema_v1.json"
                )
        ) as handle:
            schema = json.load(handle)
        jsonschema.validate(instance=json_repr, schema=schema)

    @classmethod
    def load(cls, file: Union[str, os.PathLike], validate: bool = True) -> InteractionFile:
        interaction = []
        with open(file) as handle:
            json_repr = json.load(handle)
        if validate:
            cls.__json_validate(json_repr)
        if type(json_repr) == list:
            for entry in json_repr:
                interaction.append(RNAInteraction.from_dict(entry))
        else:
            interaction.append(RNAInteraction.from_dict(json_repr))
        return cls(interaction, validate=False)

    def export_json(self, path: Union[str, os.PathLike]):
        with open(path, "w") as handle:
            json.dump(
                self.interactions, handle, cls=CustomEncoder, indent=2
            )

    def export_bed(self, path: Union[str, os.PathLike]):
        with open(path, "w") as handle:
            for interaction in self.interactions:
                bed_repr = interaction.bed_repr()
                handle.write(f"{bed_repr}\n")

    def json_repr(self):
        return self.interactions

    def __iter__(self):
        for interaction in self.interactions:
            yield interaction

    def __str__(self):
        return json.dumps(self, cls=CustomEncoder, indent=1)


class RNAInteraction:
    rgb_map = {
        "RNA-RNA": "(0,255,0)",
        "RNA-Protein": "(0, 0, 255)",
        "RNA-RNA-Protein": "(255, 0, 0)"
    }

    def __init__(
        self,
        interaction_id: int,
        interaction_class: str,
        interaction_type: str,
        evidence: List[Evidence],
        organism_name: str = None,
        refseqid: str = None,
        partners: List[Partner] = None,
    ):
        self.interaction_id = interaction_id
        self.interaction_class = interaction_class
        self.interaction_type = interaction_type
        self.evidence = evidence
        self.organism_name = organism_name
        self.refseqid = refseqid
        self.partners = partners


    def __str__(self):
        return json.dumps(self, cls=CustomEncoder, indent=1)

    def __repr__(self):
        return str(self.__dict__)

    def json_repr(self):
        json_repr = dict()
        for key, value in self.__dict__.items():
            if value is not None:
                key = "ID" if key == "interaction_id" else key
                key = "class" if key == "interaction_class" else key
                key = "type" if key == "interaction_type" else key
                key = "refSeqID" if key == "refseqid" else key
                json_repr[key] = value
        return json_repr

    @classmethod
    def from_dict(cls, dict_repr: Dict) -> RNAInteraction:
        interaction_id = dict_repr["ID"]
        interaction_class = dict_repr["class"]
        interaction_type = dict_repr["type"]
        evidence = [Evidence.from_dict(x) for x in dict_repr["evidence"]]
        dict_repr = defaultdict(lambda: None, dict_repr)
        organism_name = dict_repr["organism_name"]
        refseqid = dict_repr["refSeqID"]

        partners = dict_repr["partners"]
        if partners is not None:
            partners = [Partner.from_dict(x) for x in partners]

        rna_interaction = RNAInteraction(
            interaction_id,
            interaction_class,
            interaction_type,
            evidence,
            organism_name,
            refseqid,
            partners,
        )

        return rna_interaction

    def bed_repr(self):
        bed_lines = []
        for first_partner in self.partners:
            to_col_three = first_partner.bed_repr()
            rgb = self.rgb_map[self.interaction_class]
            for idx, second_partner in enumerate(self.partners):
                lsssizes = ",".join([ls.end - ls.start for ls in first_partner.local_sites[idx]])
                lsstarts = ",".join([ls.start for ls in first_partner.local_sites[idx]])

                s = f"{to_col_three}\t{first_partner.name}-{second_partner.name}\t0\t" \
                    f"{first_partner.genomic_coordinates.strand}\t{first_partner.genomic_coordinates.start}\t" \
                    f"{first_partner.genomic_coordinates.end}\t{rgb}\t{len(first_partner.local_sites[idx])}\t" \
                    f"{lsssizes}\t{lsstarts}"
                bed_lines.append(s)
        string = "\n".join(bed_lines)
        return string


class Evidence:
    def __init__(
        self,
        evidence_type: str,
        method: str,
        command: str = None,
        data: Dict = None,
    ):
        self.evidence_type = evidence_type
        self.method = method
        self.command = command
        self.data = data

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def json_repr(self):
        json_repr = dict()
        for key, value in self.__dict__.items():
            if value is not None:
                key = "type" if key == "evidence_type" else key
                json_repr[key] = value
        return json_repr

    @classmethod
    def from_dict(cls, dict_repr: Dict) -> Evidence:
        evidence_type = dict_repr["type"]
        method = dict_repr["method"]
        command = dict_repr["command"] if "command" in dict_repr else None
        data = dict_repr["data"] if "data" in dict_repr else None
        data = {
            key: value
            for key, value in data.items()
        }
        return cls(
            evidence_type=evidence_type,
            method=method,
            command=command,
            data=data,
        )


class Partner:
    def __init__(
        self,
        name: str,
        symbol: str,
        partner_type: str,
        genomic_coordinates: GenomicCoordinates,
        organism_name: str,
        local_sites: List[Dict[str, LocalSite]],
        description: str = None,
        sequence: Seq.Seq = None,
        structure: str = None,
        **kwargs,
    ):
        self.name = name
        self.symbol = symbol
        self.partner_type = partner_type
        self.genomic_coordinates = genomic_coordinates
        self.organism_name = organism_name
        self.local_sites = local_sites
        self.description = description
        self.sequence = sequence
        self.structure = structure
        self.__dict__.update(kwargs)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def bed_repr(self):
        string = f"{self.genomic_coordinates.chromosome}\t{self.genomic_coordinates.start}\t{self.genomic_coordinates.end}"
        return string

    def json_repr(self):
        json_repr = dict()
        for key, value in self.__dict__.items():
            if value is not None:
                key = "type" if key == "partner_type" else key
                json_repr[key] = value
        return json_repr

    @classmethod
    def from_dict(cls, dict_repr: Dict) -> Partner:
        name = dict_repr.pop("name")
        symbol = dict_repr.pop("symbol")
        partner_type = dict_repr.pop("type")
        genomic_coordinates = GenomicCoordinates.from_string(
            dict_repr.pop("genomic_coordinates")
        )
        organism_name = dict_repr.pop("organism_name")
        local_sites = {}
        for key, values in dict_repr.pop("local_sites").items():
            local_sites[key] = [LocalSite(x[0], x[1]) for x in values]
        return cls(
            name=name,
            symbol=symbol,
            partner_type=partner_type,
            genomic_coordinates=genomic_coordinates,
            organism_name=organism_name,
            local_sites=local_sites,
            **dict_repr,
        )


@dataclass
class LocalSite:
    start: int
    end: int

    def __str__(self):
        return f"{self.start}-{self.end}"

    def json_repr(self):
        return [self.start, self.end]


@dataclass
class GenomicCoordinates(LocalSite):
    chromosome: str
    strand: str

    def __str__(self):
        return f"{self.chromosome}:{self.strand}:{self.start}-{self.end}"

    def __repr__(self):
        return str(self.__dict__)

    def json_repr(self):
        return str(self)

    @classmethod
    def from_string(cls, str_repr: str) -> GenomicCoordinates:
        chromosome, strand, coordinates = str_repr.split(":")
        start, end = (int(x) for x in coordinates.split("-"))
        return cls(start=start, end=end, chromosome=chromosome, strand=strand)


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "json_repr"):
            return obj.json_repr()
        else:
            return json.JSONEncoder.default(self, obj)
