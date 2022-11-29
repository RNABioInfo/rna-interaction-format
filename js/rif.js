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
	data = []; // contains the RIF JSON object
	validate = {}; // stores ajv validate object using this.schema 
	schema = {}
	maxID = 0

	constructor() {
		this.changeSchema('../rna-interaction-schema_v1.json');
	}

	// changes the underlying schema (e.g, to older versions) and compiles it
	changeSchema(schemaFile) { 
		// load & parse RIF schema
		var schemaData = fs.readFileSync(schemaFile, 'utf8');
		this.schema = JSON.parse(schemaData);
		this.validate = ajv.compile(this.schema);
	}

	// changes interaction data (provided that it follows the schema)
	changeData(data) {
		if(this.validateData(data)) {
			this.data = data;
		} else {
			console.log("Provided data does not follow the RIF schema")
		}
	}
	
	// getter
	get getData() { return this.data; }
	get getMaxID() { return this.maxID; }

	// imports any given (valid) RIF file - interactions are added to existing data
	readRIF(filename) {
		var data = fs.readFileSync(filename, 'utf8');
		const parsed = JSON.parse(data); // parse data
		//const valid = ajv.validate(this.schema, parsed);
		
		var valid = this.validateData(parsed);

		if(valid) {
			// iterate through keys 
			var keys = Object.keys(parsed);
			for (var i = 0; i < keys.length; i++) {
				if(this.maxID < parsed[i].ID) {
					this.maxID = parsed[i].ID
				}
				this.data.push(parsed[i])
			}
		}
	}

	// writes the RIF to file
	writeRIF(filename) {
		// convert JSON object to string
		const data = JSON.stringify(this.data, null, 4);

		// write back to filename
		fs.writeFile(filename, data, err => {
			if(err) {
				throw err
			}
			console.log("Data has been saved to: " + filename);
		});
	}

	// validate data object with the current schema
	validateData(data) {
		const valid = this.validate(data);
		if(!valid) {
			console.log("Data does not uphold ")
			console.log(this.validate.errors)
			return false
		} 
		return true
	}

	// return interaction given single or multiple queries
	get(attr) {
		// bring (single or) multiple queries into same array format    
		var [query, queryKeys, queryValues, subset] = [[],[],[],[]];
		query = toArray(attr);

		// retrieve interactions 
		var keys, values;
		for(var i=0;i<this.data.length;i++) { 
			for(var j=0;j<query.length;j++) {
				queryKeys = Object.keys(query[j]);
				queryValues = Object.values(query[j]);

				var l = queryKeys.length
				for(var k=0;k<l;k++) {
					if(this.data[i][queryKeys[k]] == queryValues[k]) {
						if(k==l-1) {
							subset.push(this.data[i]); // select element
						}
					} else {
						break;
					}
				}
			}
		}		
		return subset;
	}

	// return interactions excluding the query
	rm(attr) {
		// bring (single or) multiple queries into same array format
		var [query, queryKeys, queryValues] = [[],[],[]];
		query = toArray(attr);

		// iterate through elements and match with query
		for(var i=0;i<this.data.length;i++) {
			for(var j=0;j<query.length;j++) {
				queryKeys = Object.keys(query[j]);
				queryValues = Object.values(query[j]);

				var l = queryKeys.length
				for(var k=0;k<l;k++) {
					if(this.data[i][queryKeys[k]] == queryValues[k]) {
						if(k==l-1) {
							this.data.splice(i,1); // remove element
						}
					} else {
						break;
					}
				}
			}
		}
		return this.data;
	}

	// add interaction to the data
	add(attr) {
		for(var i=0;i<this.data.length;i++) {
			// check if new element already exists
			if(attr == this.data[i]) {
				console.log('identical element already exists');
				return -1; // cancel operation
			}
		}
		// empty interaction object
		var obj = {
			"ID": this.maxID+1,
			"class": "",
			"type": "",
			"evidence": [],
			"partners": []
		};

		// determine next ID
		if(obj["ID"] > this.maxID) {
			this.maxID = obj["ID"];
		}

		// substitute name/values pairs in attr
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
		this.data.push(obj);
		return this.data;
	} 

	// modify name/value pair of interaction
	mod(id, attr) {
		var key = Object.keys(attr);
		var value = Object.values(attr);
		if (key.length != 1) {
			console.log("ERROR: multiple key/value pairs have been specified")
			return -1;
		} else {
			var tmp = JSON.parse(JSON.stringify(this.data));
			for(var i=0;i<tmp.length;i++) {
				if(tmp[i].ID == id) {
					tmp[i][key[0]] = value[0];
				}
			}
		}
		var valid = this.validateData(tmp);
		if(valid) {
			this.data = JSON.parse(JSON.stringify(tmp));
		} else {
			console.log("ERROR: modification renders the data as invalid")
		}
	}

	// export RIF to BED12 format
	writeBED(filePath) {
		var bed = [];
		var file = fs.createWriteStream(filePath);

		for(var i=0;i<this.data.length;i++) {
			var name = "";			
			var object = this.data[i];
			for(var j=0;j<object.partners.length;j++) {
				for(var k=0;k<object.partners.length;k++) {
					if(j != k) {
						var line = ["","","","","0","","","","(0,0,0)","","",""];
						var coord = object.partners[j].genomic_coordinates.split(":");
						var chrom = coord[2].split("-");

						// 
						line[0] = coord[0]; // chrom
						line[1] = chrom[0]-1; // chromStart
						line[2] = chrom[1]; // chromEnd
						line[3] = object.partners[j].symbol + "-" + object.partners[k].symbol// name
						line[5] = coord[1]; // strand
						line[6] = line[1]; // thickStart = chromStart
						line[7] = line[2]; // thickEnd = chromEnd

						// determine RGB codes
						if(object.partners.length == 2) {
							line[8] = "(0,255,0)"; // green
							if(line[8].split("-").includes("polypetide")) {
								line[8] = "(0,0,255)"; // blue
							} 
						} else {
							if(object.partners.length > 2) {
								line[8] = "(255,0,0)"; // red
							}
						}
						
						var sites = object.partners[j].local_sites[object.partners[k].symbol];
						line[9] = sites.length; // blockCount
						for(var l=0;l<sites.length;l++) {
							var size = (sites[l][1]+1)-sites[l][0];
							line[10] += line[10].length == 0 ? size : "," + size; // blockSizes
							line[11] += line[11].length == 0 ? sites[l][0] : ","+ sites[l][0];
						}
						file.write(line.join("\t") + "\n");
					}
				}
			}
		}
		file.close();
	}
}

module.exports = RIF;


