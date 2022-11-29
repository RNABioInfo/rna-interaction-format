# Python API

## Usage

### Loading and Parsing

Main functions are provided via the `InteractionFile` class.
Using this it is possible to load a whole file of Interactions like:

```python
from RNAInteraction.RNAInteractions import InteractionFile

interaction_file = InteractionFile.load("/path/to/file")
```

It is then possible to iterate over the Interactions within this file

```python
for interaction in interaction_file:
    print(interaction.interaction_id)
```

For large files it might be beneficial to not load them into memory at once.
Thus, it is possible to parse entries in Interaction Files one after another using
and Generator returned by the `parse()` function.
This can be used  for example to filter the file and construct an `InteractionFile` object
only from a subset as shown below.

```python
from RNAInteraction.RNAInteractions import InteractionFile

filtered_interactions = []
for interaction in InteractionFile.parse("/path/to/file"):
    if interaction.interaction_class == "RNA-RNA":
        filtered_interactions.append(interaction)

interaction_file = InteractionFile(filtered_interactions)
```

### Export

InteractionFile objects can be exported to the RNAinteraction Format using the 
``export_json()`` function as follows:

```python
from RNAInteraction.RNAInteractions import InteractionFile

interaction_file = InteractionFile.load("/path/to/file")
interaction_file.export_json("/new/file/path")
```

### Creating a File within Python

You can also create an InteractionFile object in pure python and export it to 
the json format. Using this approach it is easy to include the API into your python tool
and write an export function. Keep in mind that json object are converted to classes in the
python api. In contrast, Lists will stay Lists (except for the local and genomic coordinates).

However, lets start from the bottom and create an InteractionFile with
a single hypothetical entry of an RNA-Protein interaction which was predicted using 
the tool [RNAProt](https://github.com/BackofenLab/RNAProt).

First we will import all necessary classes


```python
from RNAInteraction.RNAInteractions import (
    Evidence,
    EvidenceData,
    Partner,
    GenomicCoordinates,
    LocalSite,
    RNAInteraction,
    InteractionFile
)
```

Afterwards, we will construct the Evidence objects and the evidence data.
```python
data = {"significance": EvidenceData(unit="p-value", value=0.001)}
evidence = Evidence(
    evidence_type="prediction",
    method="RNAProt",
    command="RNAProt predict --mode 2 --thr 2",
    data=data,
)
```

The next step is the creation of Partner entries.
```python
mRNA_partner = Partner(
    name="Tumor protein P53",
    symbol="TP53",
    parnter_type="mRNA",
    organism_acc="9606",
    organism_name="Homo sapiens",
    genomic_coordinates=GenomicCoordinates(
        chromosome="chr17",
        strand="-",
        start=7687490,
        end=7668421,
    ),
    local_sites=[
        LocalSite(
            start=2125,
            end=2160
        ),
        LocalSite(
            start=2452,
            end=2472
        )
    ]  
)

rbp_partner = Partner(
    name="ELAV-like protein 1",
    symbol="ELAVL1",
    parnter_type="Protein",
    organism_acc="9606",
    organism_name="Homo sapiens",
    genomic_coordinates=GenomicCoordinates(
        chromosome="chr19",
        strand="-",
        start=8005641,
        end=7958573,
    ),
    local_sites=[
        LocalSite(
            start=2125,
            end=2160
        ),
        LocalSite(
            start=2452,
            end=2472
        )
    ]  
)
```

The last step is quite simple as it only includes packing all together in an RNAInteraction
and building the InteractionFile, which you can easily export.

```python
interaction = RNAInteraction(
    interaction_id = 1,
    evidence=evidence,
    interaction_class="RNA-Protein",
    interaction_type="RNA binding",
    partners=[mrna_partner, rbp_partner]
)
interaction_file = InteractionFile([interaction])
interaction_file.export_json("testfile.json")
```



