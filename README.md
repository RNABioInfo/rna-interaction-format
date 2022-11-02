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
*coming soon...*


### JavaScript 

At first, the required packages for RIF module need to be installed.
```javascript
cd ./js 
npm install
```
The RIF module can be included in node.js using the `require` function by referencing to the `rif.js` file. 

```javascript
const rif = require('./rif.js');
var r = new rif();
```
For the basic functionality of reading and writing RIF files, the functions `readRif(RIFfile)` and `writeRif(RIFfile)` are provided. In addition, `validate(data)` validates the data against the current schema. This is also called when importing RIFfiles using `readRif`.

```javascript
r.readRif('./examples/RNA-RNA.json'); // import a RIF file 
r.writeRif('./RNA-RNA.json'); // write the RIF file 
r.validate();
```

For the retrieval of specific interactions, `get` allows different queries of the data.   

```javascript
r.get({"ID": 1}); // single query
r.get([{"class": "RNA-RNA", "type": "basepairing"}]); // single query, multiple properties
r.get([{"class": "RNA-RNA"}]); // single query, returns multiple values 
r.get([{"ID": 1}, {"ID": 2}]); // multiple queries
```

Other data manipulation is done with `add` and `rm` which add an interaction to the data and removes it, respectively.

```javascript
r.add({"class": "RNA-RNA", 
    "type": "basepairing"})
```

In addition, specific properties can be modified using the `mod` routine which accepts the id of the interaction and the key/value pair. 

```javascript
r.mod(1,{"type": 123})
```

Finally, the import and export to BED format is provided

```javascript
r.writeBED("./examples/RNA-RNA.bed12");
```

### Python


















