#include<iostream>
#include<vector>
#include <string>
#include "parse.h"

using namespace std;

std::string read_jfile(std::string add)
//creates string from text file.
{
	std::string res="";
	ifstream flux(add);
	if(flux)
	{
		std::string line="";
		while(getline(flux,line))
		{
			res+=line;
		}
	}
	else
	{
		cout << "No file there :(" << endl;
		cout << add << endl;
	}
	return res;
}

std::string folder(std::string add)
//defines the working directory
{
	std::string res=add;
	while(res[res.size()-1] !='/')
	{
		res.pop_back();
	}
	return res;
}

void write_json(rapidjson::Document *doc, std::string add, std::string name)
//creates a string from a json object and exports as a .json file. 
{
	ofstream flux(add+name);
	if(flux)
	{
		rapidjson::StringBuffer buffer;
		rapidjson::PrettyWriter<rapidjson::StringBuffer> writer(buffer);
		(*doc).Accept(writer);
		flux << buffer.GetString();
	}
}

int json_check(rapidjson::Document *doc)
//checks whether a json object is a valid json.
{
	int res=1;
	if((*doc).HasParseError())
	{
		cout << "Your input is not a valid json document" << endl;
		cout << "Useful tips:" << endl;
		cout << "-Check for misplaced commas" << endl;
		cout << "-Integers starting with '0' (other than 0 itself) are not supported" << endl;
		res=0;
	}
	return res;
}

int schema_validator(rapidjson::Document *doc, rapidjson::Document *s)
//checks whether a json object is valid with regards to a given schema.
{
	int res=1;
	cout << "Comparing json input with schema..." << endl;
	rapidjson::SchemaDocument schema(*s);
	rapidjson::SchemaValidator val(schema);
	if((*doc).Accept(val))
	{
		cout << "Your input is valid :)" << endl;
	}
	else
	{
		cout << "Your input is not valid with regard to the schema; Here is your problem:" << endl;
		rapidjson::StringBuffer sb;
		rapidjson::PrettyWriter<rapidjson::StringBuffer> w(sb);
        	val.GetError().Accept(w);
		cout << sb.GetString() << endl;
		sb.Clear();
	res=0;
	}
	return res;
}

