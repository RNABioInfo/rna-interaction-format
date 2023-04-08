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
	ofstream flux(add+name+".json");
	if(flux)
	{
		rapidjson::StringBuffer buffer;
		rapidjson::PrettyWriter<rapidjson::StringBuffer> writer(buffer);
		(*doc).Accept(writer);
		flux << buffer.GetString();
	}
	else
	{
		cout << "Export location not valid" << endl;
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

std::vector<std::string> extract_gc(std::string gc)
//extracts information from a string given in field "genomic_coordinates" in a table of strings
{
	std::vector<std::string> res(0);
	std::string tmp="";
	for(int i=0;i<gc.length(); i++)
	{
		if(gc[i]!=':' && (gc[i]!='-' || tmp==""))
		{
			tmp.push_back(gc[i]);
		}
		else
		{
			res.push_back(tmp);
			tmp="";
		}
	}
	res.push_back(tmp);
	return res;
}

void export_bed(rapidjson::Document *doc, std::string add, std::string name)
//extracts interactions from a json object and exports it as a .bed file.
{
	ofstream flux(add+name+".bed");
	if(flux)
	{
		rapidjson::Value par;
		rapidjson::Value ls;
		rapidjson::Value lss;
		std::vector<std::string> gc(0);
		for(int k=0; k< ((*doc).GetArray()).Size(); k++)
		{
			par=((*doc)[k]["partners"]).GetArray();
			for (int i=0;i<par.Size(); i++)
			{
				gc=extract_gc((par[i]["genomic_coordinates"]).GetString());
				ls=(par[i]["local_sites"]).GetArray();
				for (int l=0; l<ls.Size(); l++)
				{
					lss=(ls[l]).GetArray();
					if(lss.Size()>0)
					{
						flux << gc[0] << " ";
						flux << gc[2] << " ";
						flux << gc[3] << " ";
						flux << (par[i]["name"]).GetString() << "-" << (par[l]["name"]).GetString() << " ";
						flux << 1 << " ";
						flux << gc[1] << " ";
						flux << gc[2] << " ";
						flux << gc[3] << " ";
						flux << "255,0,0" << " ";
						flux << lss.Size() << " ";
						for(int j=0;j<lss.Size(); j++)
							{
							flux << (lss[j][1]).GetInt()-lss[j][0].GetInt()+1;
							if(j<lss.Size()-1)
							{
							flux << ",";
							}
						else
							{
								flux << " ";
							}
						}
						for(int j=0;j<lss.Size(); j++)
						{
							flux << lss[j][0].GetInt();
							if(j<lss.Size()-1)
							{
								flux << ",";
							}
						}
						flux << endl;
					}
				}
			}
		}
		
	}
	else
	{
		cout << "Export location not valid" << endl;
	}
}

