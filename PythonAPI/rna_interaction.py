from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import List, Union, Dict
from collections import defaultdict
from Bio import Seq


class InteractionFile:
    def __init__(self, interactions: List[RNAInteraction]):
        self.interactions = interactions

    @classmethod
    def load(cls, file: Union[str, os.PathLike]):
        with open(file) as handle:
            json_repr = json.load(handle)
        interaction = RNAInteraction.from_dict(json_repr)
        return InteractionFile([interaction])

    def __iter__(self):
        for interaction in self.interactions:
            yield interaction


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
        complementary: List = None,
        hybridisation: List = None,
        p_value: List = None,
        reads: int = None,
    ):
        self.evidence_type = evidence_type
        self.complementary = complementary
        self.hybridisation = hybridisation
        self.p_value = p_value
        self.reads = reads

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
        sites: List[Site],
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

    @classmethod
    def from_dict(cls, dict_repr):
        name = dict_repr.pop("name")
        partner_type = dict_repr.pop("type")
        # TODO: ask whether list in list is necessary
        sites = [Site.from_string(x) for x in dict_repr.pop("sites")[0]]
        return Partner(name, partner_type, sites, kwargs=dict_repr)


@dataclass
class Site:
    chromosome: str
    strand: str
    start: int
    end: int

    def __str__(self):
        return f"{self.chromosome}:{self.strand}:{self.start}-{self.end}"

    @classmethod
    def from_string(cls, str_repr: str):
        chromosome, strand, coordinates = str_repr.split(":")
        start, end = (int(x) for x in coordinates.split("-"))
        return Site(chromosome, strand, start, end)
