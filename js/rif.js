const fs = require('fs');
const lr = require('line-reader')

//
const Ajv2020 = require("ajv/dist/2020")
const ajv = new Ajv2020()

// checks if 
function isObject(objValue) {
  return objValue && typeof objValue === 'object' && objValue.constructor === Object;
}

function toArray(object) {
	var query = []	
	if(isObject(object)) {
		query.push(object);
	} else {
			if(Array.isArray(object)) {
				query = object;
			}
		}
	return query;
}

class RIF {
	content = []
	validate = {}
	parse = {}
	schema = {}
	maxID = 0

	constructor() {
		this.changeSchema('../rna-interaction-schema_v1.json');
	}

	// getter & setter
	changeSchema(schemaFile) { 
		// load & parse RIF schema
		var schemaData = fs.readFileSync(schemaFile, 'utf8');
		var schema = JSON.parse(schemaData);
		this.validate = ajv.compile(schema);
	}


	set content(value) { this.content = value; }
	get schema() { return this.schema; }
	get content() { return this.content }

	import(filename) {
		var data = fs.readFileSync(filename, 'utf8');
		const parsed = JSON.parse(data); // parse data
		//const valid = ajv.validate(this.schema, parsed);
		
		var valid = this.validateSchema(parsed);

		if(valid) {
			// iterate through keys 
			var keys = Object.keys(parsed);
			for (var i = 0; i < keys.length; i++) {
				if(this.maxID < parsed[i].ID) {
					this.maxID = parsed[i].ID
				}
				this.content.push(parsed[i])
			}
		}
	}

	// validate object with 
	validateSchema(data) {
		//const valid = ajv.validate(this.schema, data)
		const valid = this.validate(data)
		if(!valid) {
			console.log("Invalid")
			console.log(this.validate.errors)
			return false
		} 
		return true
	}

	// return interaction 
	get(attr) {
		// init 
		var [query, queryKeys, queryValues, subset] = [[],[],[],[]];
		query = toArray(attr);

		var keys, values;
		for(var i=0;i<this.content.length;i++) { 
			for(var j=0;j<query.length;j++) {
				queryKeys = Object.keys(query[j]);
				queryValues = Object.values(query[j]);

				var l = queryKeys.length
				for(var k=0;k<l;k++) {
					if(this.content[i][queryKeys[k]] == queryValues[k]) {
						if(k==l-1) {
							subset.push(this.content[i])
						}
					} else {
						break;
					}
				}
			}
		}		
		return subset;
	}

	rm(attr) {
		// init 
		var [query, queryKeys, queryValues] = [[],[],[]];
		query = toArray(attr);

		for(var i=0;i<this.content.length;i++) {
			for(var j=0;j<query.length;j++) {
				queryKeys = Object.keys(query[j]);
				queryValues = Object.values(query[j]);

				var l = queryKeys.length
				for(var k=0;k<l;k++) {
					if(this.content[i][queryKeys[k]] == queryValues[k]) {
						if(k==l-1) {
							this.content.splice(i,1)
						}
					} else {
						break;
					}
				}
			}
		}
		return this.content;
	}

	add(attr) {
		for(var i=0;i<this.content.length;i++) {
			// check if new element already exists
			if(attr == this.content[i]) {
				console.log('identical element already exists');
				return -1; // cancel operation
			}
		}
		// add to data
		var obj = {
			"ID": this.maxID+1,
			"class": "",
			"type": "",
			"evidence": [],
			"partners": []
		};

		if(obj["ID"] > this.maxID) {
			this.maxID = obj["ID"];
		}

		var keys = Object.keys(attr);
		var values = Object.values(attr);
		for(var j=0;j<attr.length;j++) {
			if(keys[j] == "ID") {
				if(values[j] > this.maxID) {
					this.maxID = values[j];
				}
			}
			obj[keys[j]] = values[j]; 
		}
		this.content.push(obj);
		return this.content;
	} 

	mod(id, attr) {
		var key = Object.keys(attr);
		var value = Object.values(attr);
		if (key.length != 1) {
			console.log("ERROR: multiple key/value pairs have been specified")
			return -1;
		} else {
			var tmp = JSON.parse(JSON.stringify(this.content));
			for(var i=0;i<tmp.length;i++) {
				if(tmp[i].ID == id) {
					tmp[i][key[0]] = value[0];
				}
			}
		}
		var valid = this.validateSchema(tmp);
		if(valid) {
			this.content = JSON.parse(JSON.stringify(tmp));
		} else {
			console.log("ERROR: modification renders the data as invalid")
		}
	}

	exportBED(filePath) {
		console.log('ExportBED')
		//console.log(this.content)
		var bed = [];
		var file = fs.createWriteStream(filePath);
		
		for(var i=0;i<this.content.length;i++) {
			var name = "";
			
			var object = this.content[i];
			for(var j=0;j<object.partners.length;j++) {
				var line = ["","","","","0","","","","(0,0,0)","","",""];
				var coord = object.partners[j].genomic_coordinates.split(":");
				var chrom = coord[2].split("-");

				line[0] = coord[0]; // chrom
				line[1] = chrom[0]-1; // chromStart
				line[2] = chrom[1]-1; // chromEnd
				line[5] = coord[1]; // strand
				line[6] = line[7] = line[1] // thickStart & thickEnd equal chromStart
				//line[9] = object.partners[j].local_sites.length; // blockCount

				name += j==0 ? object.partners[j].name : "-" + object.partners[j].name;

				var sites = object.partners[j].local_sites;
				for(var k=0;k<sites.length;k++) {
					if(sites[k].length != 0) {
						for(var l=0;l<sites[k].length;l++) {
							var size = sites[k][l][1]+1-sites[k][l][0];
							line[9]++; // blockCounts
							line[10] += line[10].length == 0 ? size : "," + size; // blockSizes
							line[11] += line[11].length == 0 ? sites[k][l][0] : "," + sites[k][l][0]; // blockStarts
						}
					}
				}
				bed.push(line);
			}

			// write name back to bed entry
			for(var j=0;j<bed.length;j++) {
				bed[j][3] = name; // name
			}
			console.log(bed); 
			// write to file
			
			bed.forEach(function(v) { 
				file.write(v.join('\t') + '\n'); 
			});
			
			bed = [];
		}
		file.end();
	}

	// import BED file
	importBED(filePath) {
		console.log("importBED")

		var cols = "";
		var name = "";
		var int = []; // buffer interaction partners
		lr.eachLine(filePath, (line,last) => {
			cols = line.split("\t");
			if(name == "" || name == cols[3]) {
				int.push(cols);
			} else {
				console.log(int)
				
				var partners = [];
				// do something
				for(var i=0;i<int.length;i++) {
					var el = int[i];



					var p = {
						"name": el[3].split("-")[i],
						"type": "region",
						"local_sites": []
					}


					// convert blockStarts and blockSizes to local_sites
					for(var j=0;j<int.length;j++) {
						 if(i != j) {
						 	// determine intersecting sites
						 	var sitesA = int[i][10].split(",");
						 	var sitesB = int[j][10].split(",");
						 	var intersection = sitesA.filter(
						 		value=>sitesB.includes(value));

						 	console.log(intersection);
						 	for(var k=0;)


						 	p["local_sites"]
						 } else {
						 	p["local_sites"].push([]);
						 }
					}



					console.log(p)

					console.log("add")
					this.add({});

					console.log(this.content)

				}

				int = [];
				int.push(cols)
			}
			name = cols[3];
			if(last) {
				console.log(int)
			}
		});

	}
}


module.exports = RIF;


/*
console.log('new RIF instance')
var r = new RIF();
//r.import('../examples/RNA-RNA.json')
//r.mod(1,{"type": 123})
//r.exportBED("output.bed12")
r.importBED("output.bed12");

console.log("asda")
console.log(r.content)

*/




// return single element
/*
as = r.get({"ID": 1}) // single query
console.log(as) 
as = r.get([{"class": "RNA-RNA", "type": "basepairing"}]) // single query, multiple properties
console.log(as)
as = r.get([{"class": "RNA-RNA"}]) // single query, returns multiple values 
console.log(as)
as = r.get([{"ID": 1}, {"ID": 2}])
console.log(as)*/

//console.log(r.content)
//as = r.rm({"ID":1});
//console.log(r.content)

//r.add({})


/*
schema = '../rna-interaction-schema_v1.json'
f = '../examples/testJSON.json'
s = '../examples/RNA-RNA.json'
schematest = 'testschema.json'
*/



