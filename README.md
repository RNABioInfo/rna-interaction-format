# RNA Interaction Format (RIF)

The **RNA Interaction Format (RIF)** is focused on capturing RNA interactions in a convenient to use format. It has been developed on the basis of [JSON](https://www.json.org) to store RNA-RNA, Protein-RNA or multi Protein/RNA complexes. 

RIF uses the [JSON schema](https://json-schema.org/) draft [2020-12](https://json-schema.org/draft/2020-12/release-notes.html) for validation of correctly formatted RIF files. 

## Overview

The top-level **interaction object** represents a single RNA-centric interaction object consisting of the name/value pairs **ID**, **class**, **type**, **evidence** and **partners**.

| element | value | description |
| ------- | ----- | ----------- |
| ID | number | unique identifier of the interaction used as reference |
| class | keyword | class of the interaction: RNA-RNA, Protein-RNA or Protein-RNA-RNA |
| type | string | chemical nature of the interaction |
| evidence | list | data supporting the interaction | 
| partners | list | transcript interaction |

### ID, class and type

The name/value pairs **ID**, **class** and **type** describe general information about the interaction and are mandatory. 

### evidence

An *interaction object* should contain at least one *evidence object*. Therefore, the name/value pair **evidence** is an ordered list of the evidence objects. This consists of the mandatory name/value pairs **type**, **method**, **data** that provide supporting evidence for the interaction. The **type** name/value pair describes the broad type of evidence. It should be a distinct term, like the type of experiment (e.g., prediction, pull-down assay, overexpression). In that regard, **method** declares the technique by which the supporting evidence for the interaction has been detected. This can either be computational tools (e.g., RNAcofold, RNAnue, IntaRNA) or laboratory techniques (e.g., qPCR). In the former, the optional name/value pair **command** specifies the command line call. Moreover, the name/value pair **data** specifies the actual evidence and can be arbitrary name/value pairs (e.g., values, DOI).

### partners

The name/value pair partners is a list of elements that correspond to the RNAs/Proteins involved in an interaction. These contains the mandatory name/value pairs **name**, **symbol**, **type**, **local_sites**. Other pairs include **sequence_type**, **genomic_coordinates**, **organism_name** and **organism_acc** and **local_sites**. The **name** name/value pair corresponds to the principal name of the gene/transcript and the **symbol** corresponds to its scientific name. However, this may include unannotated transcript with arbitrary naming. In that regard, **type** depicts the type of the interaction partner. These are terms that are specified in the [sequence ontology](http://www.sequenceontology.org/) and may match the entries in the corresponding annotations (.gff/gtf) file. The **genomic_coordinates** name/value pair depicts the coordinates of the transcript on the genome in the format *chromosome:strand:start-end*. In the **organism_name** name/value pair, the scientific organisms name is stated with **organism_acc** being the corresponding accession number. The **local_sites** name/value pair is specified as an object with keys corresponding to the symbols of the interacting transcripts. The values are lists of 2-element lists specifying start and end of the interaction site. 

| name | value | mandatory | description |
| ---  | ----  | --------  | ----------  |
| name | string | yes | Name of the gene/transcript/protein |
| symbol | string | yes | (Scientific) Naming of the gene/transcript/protein |
| type | string | yes | Type of the interaction partner, terms as defined in sequence ontology |
| genomic_coordinates | string | yes | Coordinates on the genome in the form chromosome:strand:start-end |
| organism_name | string | yes | Name of the organism the gene/transcript/protein belongs to |
| organism_acc | string | yes | Corresponding accession number of the organism (e,g., DDBJ/EMBL/GenBank, RefSeq, UniProt) |
| local_sites | list of list | yes | Interaction sites between the partners |

Moreover, **other** is a nested name/value pair that determines optional properties of the interaction partner. These include the name/value pairs **description**, **sequence** and **structure**. Arbirtrary name-value pairs can be specified as well. 

| name | value | mandatory | description |
| ---  | ----  | --------  | ----------  |
| description | string | no | Details on the function of the gene/transcript/protein |
| sequence | string | no | Sequence of the gene/transcript/protein as specified in *genomic_coordinates* |
| structure | string | no | Representation of the RNA secondary structure |

In addition, the **custom** name/value pair allows to specify user-defined name/value pairs. 

## Functionality

### BED Export

Data in RIF can be exported to [BED format](https://samtools.github.io/hts-specs/BEDv1.pdf). For that, the columns of the BED file are specified as follows:

| column | title | description |
| ------ | ----- | ----------- |
| 1 | chrom | chromosome name, any valid sequence region name can be used |
| 2 | chromStart | start coordinate of the feature |
| 3 | chromEnd | end coordinate of the feature |
| 4 | name | symbols of the interacting elements, linked using '-' |
| 5 | score | unused, set to 0 |
| 6 | strand | Strand orientation of the feature |
| 7 | thickStart | unused, set to chromStart |  
| 8 | thickEnd | unused, set to chromEnd |
| 9 | itemRgb | class of the interaction |
| 10 | blockCount | number of interaction sites |
| 11 | blockSizes | sizes of the interaction sites |
| 12 | blockStarts | starts of the interaction sites |


It is to be noted that #9 describes the class of interaction in which RNA-RNA corresponds to `(0,255,0)` (green), Protein-RNA to `(0,0,255)` (blue), and a multi RNA/Protein complex corresponds to `(255,0,0)` (red)


An interaction in RIF format (see [minimal example](#minimal)) then corresponds to the following BED file

```
NC_000913.3 4400287 4400596 Hfq-dsrA    0   +   4400287 4400596 (255,0,0)   2   19,11   60,45
NC_000913.3 4400287 4400596 Hfq-rpoS    0   +   4400287 4400596 (255,0,0)   1   31  10
NC_000913.3 2025222 2025313 dsrA-Hfq    0   -   2025222 2025313 (255,0,0)   2   19,11   12,80
NC_000913.3 2025222 2025313 dsrA-rpoS   0   -   2025222 2025313 (255,0,0)   1   21  50
NC_000913.3 2866558 2867551 rpoS-Hfq    0   -   2866558 2867551 (255,0,0)   1   31  200
NC_000913.3 2866558 2867551 rpoS-dsrA   0   -   2866558 2867551 (255,0,0)   1   21  587
NC_000913.3 2313083 2313176 micF-lrp    0   +   2313083 2313176 (0,255,0)   2   8,10    25,55
NC_000913.3 932594  933089  lrp-micF    0   +   932594  933089  (0,255,0)   2   8,10    100,158
```

## Examples

[Additional Examples](./examples/) 

### <a id="minimal"></a>Minimal Example

```json
[{
    "ID": 1,
    "class": "RNA-RNA-Protein",
    "type": "basepairing", 
    
    "evidence": [
        {
            "type": "experimental",
            "method": "gel shift assay",
            "data": {
                "URI": "https://journals.asm.org/doi/full/10.1128/JB.183.6.1997-2005.2001",
                "note": "Hfq and DsrA interact in vivo"
            }
        },
        {
            "type": "experimental",
            "method": "protein binding assay",
            "data": {
                "URI": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1370368/"
            }
        }
    ],

    "partners": [ 
        {
            "name": "Hfq",
            "symbol": "Hfq",
            "type": "polypeptide",
            "sequence_type": "protein",
            "genomic_coordinates": "NC_000913.3:+:4400288-4400596",
            "organism_name": "Escherichia coli K-12 MG1655",
            "organism_acc": "NC_000913.3",
            "local_sites": {
                "dsrA": [[60,78],[45,55]],
                "rpoS": [[10,40]]
            },
            "other": {
                "description": "RNA chaperone that binds small regulatory RNA (sRNAs) and mRNAs to facilitate mRNA translational regulation in response to envelope stress, environmental stress and changes in metabolite concentrations.",
                "sequence": "MAKGQSLQDPFLNALRRERVPVSIYLVNGIKLQGQIESFDQFVILLKNTVSQMVYKHAISTVVPSRPVSHHSNNAGGGTSSNYHHGSSAQNTSAQQDSEETE",
                "structure": "https://www.ebi.ac.uk/pdbe/entry/pdb/5I21"
            }
        },
        {
            "name": "dsrA",
            "symbol": "dsrA", 
            "type": "small_regulatory_ncRNA", 
            "sequence_type": "rna",
            "genomic_coordinates": "NC_000913.3:-:2025223-2025313",
            "organism_name": "Escherichia coli K-12 MG1655",
            "organism_acc": "NC_000913.3",
            "local_sites": {
                "Hfq": [[12,30],[80,90]],
                "rpoS": [[50,70]]
            },
            "other": {                
                "description": "DsrA small regulatory RNA; riboregulator of RpoS and H-NS production",
                "sequence": "AACGCATCGGATTTCCCGGTGTAACGAATTTTCAAGTGCTTCTTGCATTAGCAAGTTTGATCCCGACTCCTGCGAGTCGGGATTT", 
                "structure": "...(((((((.....)))))))..(((((((...(((((.....)))))...)))))))((((((((((....)))))))))).."
            },

            "custom": {}
        },
        {
            "name": "rpoS",
            "symbol": "rpoS",
            "type": "mRNA",
            "sequence_type": "rna",
            "genomic_coordinates": "NC_000913.3:-:2866559-2867551",
            "organism_name": "Escherichia coli K-12 MG1655",
            "organism_acc": "NC_000913.3",
            "local_sites": { 
                "Hfq": [[200,230]],
                "dsrA": [[587,607]]
            },
            "other": {
                "description": "RNA polymerase, sigma S (sigma 38) factor",
                "sequence": "TGAGTCAGAATACGCTGAAAGTTCATGATTTAAATGAAGATGCGGAATTTGATGAGAACGGAGTTGAGGTTTTTGACGAAAAGGCCTTAGTAGAACAGGAACCCAGTGATAACGATTTGGCCGAAGAGGAACTGTTATCGCAGGGAGCCACACAGCGTGTGTTGGACGCGACTCAGCTTTACCTTGGTGAGATTGGTTATTCACCACTGTTAACGGCCGAAGAAGAAGTTTATTTTGCGCGTCGCGCACTGCGTGGAGATGTCGCCTCTCGCCGCCGGATGATCGAGAGTAACTTGCGTCTGGTGGTAAAAATTGCCCGCCGTTATGGCAATCGTGGTCTGGCGTTGCTGGACCTTATCGAAGAGGGCAACCTGGGGCTGATCCGCGCGGTAGAGAAGTTTGACCCGGAACGTGGTTTCCGCTTCTCAACATACGCAACCTGGTGGATTCGCCAGACGATTGAACGGGCGATTATGAACCAAACCCGTACTATTCGTTTGCCGATTCACATCGTAAAGGAGCTGAACGTTTACCTGCGAACCGCACGTGAGTTGTCCCATAAGCTGGACCATGAACCAAGTGCGGAAGAGATCGCAGAGCAACTGGATAAGCCAGTTGATGACGTCAGCCGTATGCTTCGTCTTAACGAGCGCATACCTCGGTAGACACCCCGCTGGGTGGTGATTCCGAAAAAGCGTTGCTGGACATCCTGGCCGATGAAAAAGAGAACGGTCCGGAAGATACCACGCAAGATGACGATATGAAGCAGAGCATCGTCAAATGGCTGTTCGAGCTGAACGCCAAACAGCGTGAAGTGCTGGCACGTCGATTCGGTTTGCTGGGGTACGAAGCGGCAACACTGGAAGATGTAGGTCGTGAAATTGGCCTCACCCGTGAACGTGTTCGCCAGATTCAGGTTGAAGGCCTGCGCCGTTTGCGCGAAATCCTGCAAACGCAGGGGCTGAATATCGAAGCGCTGTTCCGCGAGTAA", 
                "structure": "(((((((((((.........)))).))))))).........(((((((..((((.((((((..(((((((((((.....))))))))))).......((..(((.(((((((((......((.....))...))))))))).)))..)).....(((((((((.((((((....((((((..((((((..(((((((.....))))..)))....))).)))..)))))).......))))))....((((((((((....(((((((..(((((((((((..((((.....))))))))))))))).....(((((((((.....)))..(((.((((((((...))))))))....)))...))))))...))))).)))))))))))).(((((((..((((((...)).))))...))))))))))))))))...((((((....))))))((((....(((((...............))))).....))))...))).))).))))........(((((.((((...((((((.((((((.((.(((((((........))))....))))).))))))......))))))..(((((((....)))))))..))))))))).(((((((((((....))))).)))))).((((....((((((....)).))))...))))...(((((((((((...(((.(((((.............))))).))).....))).)))......((((((..(((......((((((((((((.((((.....))))(((...((((.((((...((((((((((..((((((((((((..........)))))).)))))).)))))((((((......))))))(((........)))...))))).)))).))))..)))....)))))))).))))..((((((....)))))))))..))))))..))))))))))))......"
            },

            "custom": {}
        }
    ]
}]
```

## Implementation


### C/C++

The implementation uses the RapidJSON library (https://rapidjson.org/). RapidJSON parses a json string into a 'Document', which makes it easy to manipulate.

Header:

~~~~~~~~~~cpp
#include "parser/parse.h" //parser; import/export
#include "parser/update.h" // updating documents
using namespace rapidjson;
~~~~~~~~~~

Read a .json file:

~~~~~~~~~~cpp
std::string json=(read_jfile(path_to_your_json));
Document doc;
doc.Parse(json);
~~~~~~~~~~

Validator:

~~~~~~~~~~cpp
json_check(*doc); // the object 'doc' is a valid json document.

Document schema;
schema.Parse(read_jfile(path_to_your_schema));
schema_validator(*doc, *schema); // the object 'doc' is valid for the given schema.
~~~~~~~~~~

Write a document into a .json file:

~~~~~~~~~~cpp
write_json(&doc, path_to_directory, file_name);
~~~~~~~~~~

Export a document to a .bed file:

~~~~~~~~~~cpp
export_bed(&doc, path_to_directory, file_name);
~~~~~~~~~~

Basic file manipulations are handled by RapidJSON (see RapidJSON documentation:  https://rapidjson.org/):

~~~~~~~~~~cpp
(doc[i]).HasMember("ID"); //checks that the i-th interaction of 'doc' has a member "ID".
int id=(document[i]["ID"]).GetInt(); // retrieves the ID of the i-th interaction.
doc[i]["ID"]=12; // sets the ID of the i-th interaction to 1.
std::string nm=(doc[i]["partners"][j]["name"]).GetString(); // retrieves the name of the j-th partner of the i-th interaction.
doc[i]["partners"][j]["name"]="Bbh"; // sets the name of the j-th partner of the i-th interaction to "Bbh".
~~~~~~~~~~

Since an interaction is called by its position in 'doc', 'find_interaction' allows to retrieve the position of an interaction from its ID. To avoid problems, IDs within a single document are assumed to be unique:

~~~~~~~~~~cpp
int i=find_interaction(3);
std::string cl=(document[i]["class"]).GetString(); // retrieves the class of the interaction with "ID": 3.
~~~~~~~~~~

A specific interaction can be removed:
~~~~~~~~~~cpp
int i=find_interaction(3);
remove_interaction(&doc, i); // removes from 'doc' the interaction with "ID": 3.
~~~~~~~~~~

Or added:
~~~~~~~~~~cpp
Document otherdoc;
add_interaction(&doc, &((otherdoc[i])).GetValue()); // add to 'doc' the i-th interaction of 'otherdoc'
~~~~~~~~~~


Specific interactions can be retrieved using 'get_interaction', via a string query:

~~~~~~~~~~cpp
Document sub1=get_interaction(&doc, "class=RNA-RNA") // New rapidjson document containing all interaction of 'doc' with "class": "RNA-RNA".
Document sub2=get_interaction(&doc, "class=RNA-RNA, RNA-Protein") // New rapidjson document containing all interaction of 'doc' with "class": "RNA-RNA" or "class": "RNA-Protein".
Document sub3=get_interaction(&doc, "class=RNA-RNA; partner=dsrA") // New rapidjson document containing all interaction of 'doc' with "class": "RNA-RNA" and "dsrA" as one of the partner.
~~~~~~~~~~


### JavaScript 

At first, the required packages for the RIF module need to be installed.
```
cd ./js 
npm install
```
The RIF module can be included in node.js using the `require` function by referencing to the `rif.js` file. 

```javascript
const rif = require('./rif.js');
var r = new rif();
```
For the basic functionality of reading and writing RIF files, the functions `readRIF(RIFfile)` and `writeRIF(RIFfile)` are provided. In addition, `validateData(data)` validates a `data` object against the schema, which is also called when importing RIF files using `readRIF`. Moreover, `changeData(data)` and `changeSchema(schemaFile)` allow to change the data and the schema, respectively. Direct access to the interaction data is provided using `getData()`. 

```javascript
r.readRif('./examples/RNA-RNA.json'); // import a RIF file 
r.writeRif('./RNA-RNA.json'); // write the RIF file 
r.validateData(data); // validates `data` against the schema

```
For the retrieval of specific interactions, `get` allows different queries of the data. This includes queries in which single or multiple properties are defined. In doing so, this returns the interactions which match all provided properties.

```javascript
r.get({"ID": 1}); // unique query, returns a single interaction that matches the ID
r.get({"class": "RNA-RNA"}); // returns all interactions matching the class property
r.get({"class": "RNA-RNA", "type": "basepairing"}); // returns all interactions matching the class and type property
```

In a similar manner, RIF can be queried for multiple interactions. 

```javascript
r.get([{"ID": 1}, {"ID": 2}]); // multiple queries
```

Other data manipulation is done with `add` and `rm` which add an interaction to the data and removes it, respectively. In the of adding an interaction, this requires an interaction data which suffices the schema, e.g., 

```javascript
r.add({
    "class": "RNA-RNA",
    "type": "basepairing",
    "evidence": [
        {
            "type": "experimental",
            "method": "gel shift assay",
            "data": {
                "URI": "https://journals.asm.org/doi/full/10.1128/JB.183.6.1997-2005.2001",
                "note": "Hfq and DsrA interact in vivo"
            }
        }
    ],
    "partners": [
        {
            "name": "micF",
            "symbol": "micF",
            "type": "small_regulatory_ncRNA",
            "local_sites": {
                "lrp": [[25,32],[55,64]]
            }
        }, 
        {
            "name": "lrp",
            "symbol": "lrp",
            "type": "mRNA",
            "local_sites": {
                "micF": [[100,107],[158,167]]
            }
        }
    ]
})
```

It is to be noted that `ID` is determined automatically, but can also be set manually. However, this should be unique. Similarly, an interaction can be removed by querying for certain name/value pairs, e.g.,

```javascript
r.rm({"ID": 1}); // removes interaction with ID=1
r.rm({"class": "RNA-RNA"}); // removes all interactions of class: RNA-RNA
```
In addition, specific properties can be modified using the `mod` routine which accepts the id of the interaction and the key/value pair. 

```javascript
r.mod(1,{"type": "Protein-RNA"}); // changes the type to "Protein-RNA" on interaction with ID=1
```

Finally, the interaction can exported to BED format using `writeBED(filename)`


### Python

#### Get it

The python API can be installed from source via cloning the repository and:

```shell
pip install PythonAPI
```

You can test if the module was installed correctly using `pytest`:

```shell
pip install pytest
pytest --pyargs RIF
```

#### Loading and Parsing

Main functions are provided via the `InteractionFile` class.
Using this it is possible to load a whole file of Interactions like:

```python
from RIF.pRIF import InteractionFile

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
from RIF.pRIF  import InteractionFile

filtered_interactions = []
for interaction in InteractionFile.parse("/path/to/file"):
    if interaction.interaction_class == "RNA-RNA":
        filtered_interactions.append(interaction)

interaction_file = InteractionFile(filtered_interactions)
```

#### Validation

The validation happens automatically during actions like File creation, loading, or adding. It is possible to 
disable this via setting the corresponding validate flags to False. 
However, a user can also validate the object manually via:

```python
interaction_file.validate()
```

#### Export

##### JSON

InteractionFile objects can be exported to the RNAinteraction Format using the 
``export_json()`` function as follows:

```python
from RIF.pRIF  import InteractionFile

interaction_file = InteractionFile.load("/path/to/file")
interaction_file.export_json("/new/file/path")
```

##### BED

It is also possible to export In Bed format using `InteractionFile.export_bed()` function in a similar way.


```python
from RIF.pRIF  import InteractionFile

interaction_file = InteractionFile.load("/path/to/file")
interaction_file.export_bed("/new/file/path.bed")
```


#### Creating a File within Python

You can also create an InteractionFile object in pure python and export it to 
the json format. Using this approach it is easy to include the API into your python tool
and write an export function. Keep in mind that json object are converted to classes in the
python api. In contrast, Lists will stay Lists (except for the local and genomic coordinates).

However, lets start from the bottom and create an InteractionFile with
a single hypothetical entry of an RNA-Protein interaction which was predicted using 
the tool [RNAProt](https://github.com/BackofenLab/RNAProt).

First we will import all necessary classes


```python
from RIF.pRIF  import (
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
evidence = Evidence(
        evidence_type="prediction",
        method="RNAProt",
        command="RNAProt predict --mode 2 --thr 2",
        data={
            "significance": {"p-value": 0.001}
        }
    )
```

The next step is the creation of Partner entries.

```python
mrna_partner = Partner(
        name="Tumor protein P53",
        symbol="TP53",
        partner_type="mRNA",
        organism_acc="9606",
        organism_name="Homo sapiens",
        genomic_coordinates=GenomicCoordinates(
            chromosome="chr17",
            strand="-",
            start=7687490,
            end=7668421,
        ),
        local_sites={
            "ELAVL1": [
                LocalSite(
                    start=2125,
                    end=2160
                ),
                LocalSite(
                    start=2452,
                    end=2472
                )
            ]
        }
    )
    rbp_partner = Partner(
        name="ELAV-like protein 1",
        symbol="ELAVL1",
        partner_type="Protein",
        organism_acc="9606",
        organism_name="Homo sapiens",
        genomic_coordinates=GenomicCoordinates(
            chromosome="chr19",
            strand="-",
            start=8005641,
            end=7958573,
        ),
        local_sites={
            "Tumor protein P53": [
                LocalSite(
                    start=2125,
                    end=2160
                ),
                LocalSite(
                    start=2452,
                    end=2472
                )
            ]
        }
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

It is also possible to add or remove interactions. Adding is done via the `add()` method and removing via `rm()`. 
adding takes a single object of type `RNAInteraction` or an Iterable object of them as argument. Further, it always 
validates the file after adding the entries. You can disable this behavior via setting `validate=False`. In contrast,
`rm` takes a single Interaction ID or a List of ids and removed them from the file. 

```python
interaction_file.add(interaction, validate=True)
interaction_file.rm(1)
```





















