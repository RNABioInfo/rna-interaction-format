from __future__ import annotations
import ijson
import json
import os
from dataclasses import dataclass
from typing import List, Union, Dict, Generator, Iterable
from collections import defaultdict, OrderedDict
from Bio import Seq
import jsonschema


class InteractionFile:
    def __init__(self, interactions: List[RNAInteraction], validate: bool = True):
        """
        Args:
            interactions: list of interactions within the file
            validate (bool): whether to use the json schema to validate the file
        """
        self.interactions = interactions
        if validate:
            self.validate()

    def validate(self):
        """Validates itself using the provided schema

        """
        self.__json_validate(
            json.loads(json.dumps(self, cls=CustomEncoder))
        )

    @classmethod
    def parse(cls, file: Union[str, os.PathLike]) -> Generator[RNAInteraction]:
        """Iterates over RIF files without loading it completetly into memory

        Args:
            file: Path to a RIF file

        Yields:
            :class:`RIF.RNAInteractions.InteractionFile`: The next Interaction within the file
        """
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
        """

        Args:
            file: Path to a RIF file
            validate: whether to use the json schema to validate the file

        Returns:
            :class:`RIF.RNAInteractions.InteractionFile`

        """
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
        """ Exports the Interaction File in the original format

        Args:
            path: Path where the file should be stored

        """
        with open(path, "w") as handle:
            json.dump(
                self.interactions, handle, cls=CustomEncoder, indent=2
            )

    def export_bed(self, path: Union[str, os.PathLike]):
        """ Exports bed file

        Args:
            path: Path to the output bed file
        """
        with open(path, "w") as handle:
            for interaction in self.interactions:
                bed_repr = interaction.bed_repr()
                handle.write(f"{bed_repr}\n")

    def json_repr(self):
        """

        Returns: representation used for json serialization

        """
        return self.interactions

    def add(self, other: Union[RNAInteraction, Iterable[RNAInteraction]], validate: bool = True):
        """adds RNAInteractions to the InteractionFile

        Args:
            other Union(RNAInteraction, Iterable(RNAInteraction): The RNAInteraction elements to add
            validate (bool): whether to validate the File after adding new Instances
        Raises:
            TypeError if the elements to add are not of type RNAInteraction

        """
        if isinstance(other, RNAInteraction):
            other = [other]
        try:
            add_interactions = list(other)
            for element in add_interactions:
                if not isinstance(element, RNAInteraction):
                    raise TypeError("Can only add Lists or single items of type RNAInteraction")
                else:
                    self.interactions.append(element)
            if validate:
                self.validate()
        except TypeError:
            raise TypeError("Can only add Lists or single items of type RNAInteraction")

    def rm(self, item: Union[int, Iterable[int]]):
        """Removes Interaction specified via its ID

        This function does not care whether the element is actually in the File. It will not raise an error.
        """
        if isinstance(item, int):
            item = [item]
        self.interactions = [interaction for interaction in self.interactions if interaction.interaction_id not in item]

    def __iter__(self):
        for interaction in self.interactions:
            yield interaction

    def __str__(self):
        return json.dumps(self, cls=CustomEncoder, indent=1)


class RNAInteraction:
    """ Interaction of different Molecules

     Attributes:
        rgb_map Dict[str]: Maps from the interaction class to an rgb value.
    """
    rgb_map = {
        "RNA-RNA": "(0,255,0)",
        "RNA-Protein": "(0,0,255)",
        "RNA-RNA-Protein": "(255,0,0)"
    }

    def __init__(
        self,
        interaction_id: int,
        version: str,
        interaction_class: str,
        interaction_type: str,
        evidence: List[Evidence],
        organism_name: str = None,
        refseqid: str = None,
        partners: List[Partner] = None,
    ):
        """

        Args:
            interaction_id (int): ID of the interaction
            interaction_class (str): one of ['RNA-RNA', 'RNA-Protein', 'RNA-RNA-protein']
            interaction_type (str): chemical nature of the interaction
            evidence List[Evidence]: data supporting the interaction
            organism_name (str): Name of the organism
            refseqid (str): Refseqid
            partners List[Partner]: transcript interaction
        """
        self.interaction_id = interaction_id
        self.version = version
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
        version = dict_repr["version"]
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
            version,
            interaction_class,
            interaction_type,
            evidence,
            organism_name,
            refseqid,
            partners,
        )

        return rna_interaction

    def bed_repr(self):
        """Bed string representation of all pairwise interactions in this Interaction

        Returns (str): Bed string

        """
        bed_lines = []
        for first_partner in self.partners:
            to_col_three = first_partner.bed_repr()
            rgb = self.rgb_map[self.interaction_class]
            ph = first_partner.genomic_coordinates.start-1
            ph2 = first_partner.genomic_coordinates.end
            for second_partner in self.partners:
                if second_partner != first_partner and second_partner.symbol in first_partner.local_sites:
                    lsssizes = ",".join([str(ls.end - ls.start + 1) for ls in first_partner.local_sites[second_partner.symbol]])
                    lsstarts = ",".join([str(ls.start) for ls in first_partner.local_sites[second_partner.symbol]])

                    s = f"{to_col_three}\t{first_partner.symbol}-{second_partner.symbol}\t0\t" \
                        f"{first_partner.genomic_coordinates.strand}\t{ph}\t" \
                        f"{ph2}\t{rgb}\t{len(first_partner.local_sites[second_partner.symbol])}\t" \
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
        local_sites: Dict[str, List[LocalSite]],
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
        string = f"{self.genomic_coordinates.chromosome}\t{self.genomic_coordinates.start-1}\t{self.genomic_coordinates.end}"
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
