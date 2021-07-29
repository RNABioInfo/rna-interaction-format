from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import List, Union, Dict
from collections import defaultdict, OrderedDict
from Bio import Seq


class InteractionFile:
    def __init__(self, interactions: List[RNAInteraction]):
        self.interactions = interactions

    @classmethod
    def load(cls, file: Union[str, os.PathLike]):
        interaction = []
        with open(file) as handle:
            json_repr = json.load(handle)
        for entry in json_repr:
            interaction.append(RNAInteraction.from_dict(entry))
        return InteractionFile(interaction)

    def export_json(self, path: Union[str, os.PathLike]):
        with open(path, "w") as handle:
            json.dump(self, handle, cls=CustomEncoder, indent=2)

    def __iter__(self):
        for interaction in self.interactions:
            yield interaction

    def __repr__(self):
        return str(self.__dict__)

    def json_repr(self):
        json_repr = self.interactions
        return json_repr


class RNAInteraction:
    def __init__(
        self,
        interaction_id: int,
        classname: str,
        interaction_type: str,
        evidence: List[Evidence],
        organism: str = None,
        refseqid: str = None,
        partners: List[Partner] = None,
    ):
        self.interaction_id = interaction_id
        self.classname = classname
        self.interaction_type = interaction_type
        self.evidence = evidence
        self.organism = organism
        self.refseqid = refseqid
        self.partners = partners

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def json_repr(self):
        json_repr = dict()
        for key, value in self.__dict__.items():
            if value is not None:
                key = "ID" if key == "interaction_id" else key
                key = "class" if key == "classname" else key
                key = "type" if key == "interaction_type" else key
                key = "refSeqID" if key == "refseqid" else key
                json_repr[key] = value
        return json_repr

    @classmethod
    def from_dict(cls, dict_repr: Dict):
        interaction_id = dict_repr["ID"]
        classname = dict_repr["class"]
        interaction_type = dict_repr["type"]
        evidence = [Evidence.from_dict(x) for x in dict_repr["evidence"]]
        dict_repr = defaultdict(lambda: None, dict_repr)
        organism = dict_repr["organism"]
        refseqid = dict_repr["refSeqID"]

        partners = dict_repr["partners"]
        if partners is not None:
            partners = [Partner.from_dict(x) for x in partners]
        return RNAInteraction(
            interaction_id,
            classname,
            interaction_type,
            evidence,
            organism,
            refseqid,
            partners,
        )


class Evidence:
    def __init__(
        self,
        evidence_type: str,
        complementarity: List = None,
        hybridisation: List = None,
        p_value: List = None,
        reads: int = None,
    ):
        self.evidence_type = evidence_type
        self.complementarity = complementarity
        self.hybridisation = hybridisation
        self.p_value = p_value
        self.reads = reads

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def json_repr(self):
        json_repr = dict()
        for key, value in self.__dict__.items():
            if value is not None:
                key = "type" if key == "evidence_type" else key
                key = "p-value" if key == "p_value" else key
                json_repr[key] = value
        return json_repr

    @classmethod
    def from_dict(cls, dict_repr: Dict):
        evidence_type = dict_repr["type"]
        dict_repr = defaultdict(lambda: None, dict_repr)
        complementarity = dict_repr["complementarity"]
        hybridisation = dict_repr["hybridisation"]
        p_value = dict_repr["p-value"]
        reads = dict_repr["reads"]
        return Evidence(
            evidence_type, complementarity, hybridisation, p_value, reads
        )


class Partner:
    def __init__(
        self,
        name: str,
        partner_type: str,
        sites: List[List[Site]],
        symbol: str = None,
        coordinates: List = None,
        description: str = None,
        sequence: Seq.Seq = None,
        structure: str = None,
        **kwargs,
    ):
        self.name = name
        self.partner_type = partner_type
        self.sites = sites
        self.symbol = symbol
        self.coordinates = coordinates
        self.description = description
        self.sequence = sequence
        self.structure = structure
        self.__dict__.update(kwargs)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def json_repr(self):
        json_repr = dict()
        for key, value in self.__dict__.items():
            if value is not None:
                key = "type" if key == "partner_type" else key
                json_repr[key] = value
        return json_repr

    @classmethod
    def from_dict(cls, dict_repr):
        name = dict_repr.pop("name")
        partner_type = dict_repr.pop("type")
        # TODO: ask whether list in list is necessary
        sites = [[Site.from_string(x) for x in dict_repr.pop("sites")[0]]]
        return Partner(name, partner_type, sites, **dict_repr)


@dataclass
class Site:
    chromosome: str
    strand: str
    start: int
    end: int

    def __str__(self):
        return f"{self.chromosome}:{self.strand}:{self.start}-{self.end}"

    def __repr__(self):
        return str(self.__dict__)

    def json_repr(self):
        return str(self)

    @classmethod
    def from_string(cls, str_repr: str):
        chromosome, strand, coordinates = str_repr.split(":")
        start, end = (int(x) for x in coordinates.split("-"))
        return Site(chromosome, strand, start, end)


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "json_repr"):
            return obj.json_repr()
        else:
            return json.JSONEncoder.default(self, obj)
