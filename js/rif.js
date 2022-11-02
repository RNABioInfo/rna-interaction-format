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
	content = []; // contains the RIF JSON object
	validate = {}; // stores ajv validate object using this.schema 
	//parse = {}
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

	readRIF(filename) {
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

	writeRIF(filename) {
		console.log(this.content);

		// convert JSON object to string
		const data = JSON.stringify(this.content, null, 4);

		fs.writeFile(filename, data, err => {
			if(err) {
				throw err
			}
			console.log('RIF has been saved to' + filename);
		});
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

	writeBED(filePath) {
		var bed = [];
		var file = fs.createWriteStream(filePath);

		for(var i=0;i<this.content.length;i++) {
			var name = "";			
			var object = this.content[i];
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
						line[6] = line[1];
						line[7] = line[2]; // thickStart & thickEnd equal chromStart

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


