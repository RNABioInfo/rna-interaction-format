# rna-interaction-specification
A proposal for describing RNA-centric interaction data 


## Design Principles
* RNA-centric Document Interaction Structure in valid JSON format


## Structure Overview

The top-level **interaction object** represents a single RNA-centric interaction object consisting of the name/value pairs **ID**, **class**, **type**, **evidence** and **partners**.

### ID, class and type

The name/value pairs **ID**, **class** and **type** describe general information about the interaction and are mandatory. 

| name | value | mandatory | description |
| ---- | ----- | --------- | ----------- |
|  ID  | number | yes | ID of the interaction within the interaction file |
| class | string | yes | Class of the interaction: RNA-RNA, RNA-Protein, RNA-RNA-Protein |
| type | string | yes | Type of the interaction: basepairing, hydrophobic, H-bonds, electrostatic,... |


### evidence

An *interaction object* should contain at least one *evidence object*. Therefore, the name/value pair **evidence** is an ordered list of the evidence objects. This consists of the mandatory name/value pairs **type**, **method**, **data** that provide supporting evidence for the interaction. The **type** name/value pair describes the broad type of evidence, that can be arbitrary notes. It should be a distinct term, like the type of experiment (e.g., prediction, pull-down assay, overexpression). In that regard, **method** declares the technique by which the supporting evidence for the interaction has been detected. This can either be computational tools (e.g., RNAcofold, RNAnue, IntaRNA) or laboratory techniques (e.g., qPCR). In the former, the optional name/value pair **command** specifies the command line call. Moreover, the name/value pair **data** contains the measurements as nested name/value pairs for each measurement. The names are user-defined with the value being an object in turn contains name/values pairs **unit** and **value**.

| name | value | mandatory | description |
| ---  | ----  | --------  | :---------  |
| type | string | yes | Type of evidence (e.g., prediction, pull-down assay, overexpression) |
| method | string | yes | Tools or techniques used |
| command | string | no | command line call or other information used with the method |
| data | nested | yes | contains measurement |

Note: 

e.g., 

```json
{
    "type": "Prediction", 
    "method": "<method>", 
    "command": "<command> <parameters>",
    "data": {}
}
```

### partners

The name/value pair partners is a list of elements that correspond to the RNAs/Proteins involved in an interaction. These contains the mandatory name/value pairs **name**, **symbol**, **type**, **genomic_coordinates**, **organism_name**, **organism_acc** and **local_sites**. The **name** name/value pair corresponds to the principal name of the gene/transcript and the **symbol** corresponds to its scientific name. However, this may include unannotated transcript with arbitrary naming. In that regard, **type** depicts the type of the interaction partner. These are terms that are specified in the [sequence ontology](http://www.sequenceontology.org/) and may match the entries in the corresponding annotations (.gff/gtf) file. The **genomic_coordinates** name/value pair depicts the coordinates of the transcript on the genome in the format *chromosome:strand:start-end*. In the **organism_name** name/value pair, the scientific organisms name is stated with **organism_acc** being the corresponding accession number. The **local_sites** name/value pair is specified as list of ordered interaction sites that interact between multiple partner objects. This means that the first interaction sites of the first partner interacts with the first interaction site of the second partner and so on. Each interaction site element in turn is a 2-element list specifying start and end of the site. 

| name | value | mandatory | description |
| ---  | ----  | --------  | ----------  |
| name | string | yes | Name of the gene/transcript/protein |
| symbol | string | yes | (Scientific) Naming of the gene/transcript/protein |
| type | string | yes | Type of the interaction partner, terms as defined in sequence ontology |
| genomic_coordinates | string | yes | Coordinates on the genome in the form chromosome:strand:start-end |
| organism_name | string | yes | Name of the organism the gene/transcript/protein belongs to |
| organism_acc | string | yes | Corresponding accession number of the organism (e,g., DDBJ/EMBL/GenBank, RefSeq, UniProt) |
| local_sites | list of list | yes | Interaction sites between the partners |

Moreover, **other** is a nested name/value pair that determines optional properties of the interaction partner. These include the name/value pairs **description**, **sequence** and **structure**. 

| name | value | mandatory | description |
| ---  | ----  | --------  | ----------  |
| description | string | no | Details on the function of the gene/transcript/protein |
| sequence | string | no | Sequence of the gene/transcript/protein as specified in *genomic_coordinates* |
| structure | string | no | Representation of the RNA secondary structure |

In addition, the **custom** name/value pair allows to specify user-defined name/value pairs. 

## Examples

[Additional Examples](./examples/) 

### Minimal Example

```json
{
    "ID": 1,
    "class": "RNA-RNA",
    "type": "basepairing", 
    "evidence": [{
            "type": "Direct Duplex Detection", 
            "method": "RANnue", 
            "command": "RNAnue -minfraglen 18 -minlen 36 -sitelenratio 0.3",
            "data": {
                "complementarity": {
                    "unit": "gcs",
                    "value": 0.8
                }
            }
    }],
    "partners": [ 
        {
            "name": "dsrA",
            "symbol": "dsrA", 
            "type": "small_regulatory_ncRNA", 
            "genomic_coordinates": "chr1:+:2025223-2025313",
            "organism_name": "Escherichia coli K-12 MG1655",
            "organism_acc": "NC_000913",
            "local_sites": [ 
                [25,32],[10,17]
            ],
        },
        {
            "name": "rpoS",
            "symbol": "rpoS",
            "type": "mRNA",
            "genomic_coordinates": "chr1:-:2866559-2867551",
            "organism_name": "Escherichia coli K-12 MG1655",
            "organisms_acc": "NC_000913",
            "local_sites": [ 
                [70,83],[19,32]
            ],
        }
    ]
}
```

## C/C++


## JavaScript 

### Getting Started

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
r.readBED("RNA-RNA.bed12");
```

##Python


















