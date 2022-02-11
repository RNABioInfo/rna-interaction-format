#include<iostream>
#include<vector>
#include <string>
#include "update.h"

using namespace std;

std::vector<int> get_pair(std::string p)
//turns a string of the form "int1,int2" into a pair of coordinates; useful to update the "local_sites" field of an interaction partner.
{
	std::vector<int> res (0);
	std::string tmp="";
	for(int i=0; i<p.length(); i++)
	{
		if(p[i]==',')
		{
			res.push_back(stoi(tmp));
			tmp.clear();
		}
		else
		{
			tmp+=p[i];
		}	
	}
	res.push_back(stoi(tmp));
	return res;
}

//to use one of the methods below, better make sure first that the json document given as input is valid with regard to the schema (with schema_validator()). Specifically, things won't work if the json document has no field "partners", if "partners" is not a list, or (for method requiring searching for a partner) if an element of "partners" has no field "name" or "symbol".

int find_partner(rapidjson::Document *doc, std::string name)
//searches a partner from its name or symbol, returns its position in the list of partners (or -1 if the partner is not found).
{
	int s=(((*doc)["partners"]).GetArray()).Size();
	int i=0;
	int c=0;
	while(c==0 && i<s)
	{
		if(((((*doc)["partners"]).GetArray())[i]["name"]).GetString()==name || ((((*doc)["partners"]).GetArray())[i]["symbol"]).GetString()==name)
		{
			c=1;
		}
		i++;
	}
	return i*c-1;
}

void add_partner(rapidjson::Document *doc, rapidjson::Document *n)
//adds a new partner, but first checks that there is not already a partner of the same name. Does not add the new partner if this is the case. And does not check that the updated document remains valid with regards to the schema
{
	std::string name=((*n)["name"]).GetString();
	int i=find_partner(doc, name);
	if(i==-1)
	{
		(((*doc)["partners"]).GetArray()).PushBack(*n, (*doc).GetAllocator());
		cout << "added partner " << name << endl;
	}
	else
	{
		cout << "partner " << name << " already listed; did not add" << endl;
	}
}

void remove_partner(rapidjson::Document *doc, std::string name)
//as name says
{
	int i=find_partner(doc, name);
	if(i==-1)
	{
		cout << "partner " << name << " not found" << endl;
	}
	else
	{
		(((*doc)["partners"]).GetArray()).Erase((((*doc)["partners"]).GetArray()).Begin()+i);
		cout << "partner " << name << " removed" << endl;
	}
}

void update_partner(rapidjson::Document *doc, std::string name, std::string field, std::string nv)
//does not check that the updated document remains valid with regards to the schema
//to update "local_sites" (the only field whose value is not a string), the input should be a string recording the pair of coordinates separated with a coma, like "int1,int2".
{
	int s=(((*doc)["partners"]).GetArray()).Size();
	int i=find_partner(doc, name);
	if(i==-1)
	{
		cout << "partner " << name << " not found" << endl;
	}
	else
	{
		if((((((*doc)["partners"]).GetArray())[i]).GetObject()).HasMember(field.c_str()))
		{
			if(field=="local_sites")
			{
				int s=(((((((*doc)["partners"]).GetArray())[i]).GetObject())[field.c_str()]).GetArray()).Size();
				std::vector<int> v=get_pair(nv);
				(((((((*doc)["partners"]).GetArray())[i]).GetObject())[field.c_str()]).GetArray()).PushBack(rapidjson::Value(rapidjson::kArrayType).Move(), (*doc).GetAllocator());
				for(int j=0; j<v.size(); j++)
				{
					((((((((*doc)["partners"]).GetArray())[i]).GetObject())[field.c_str()]).GetArray())[s]).PushBack(rapidjson::Value().SetInt(v[j]), (*doc).GetAllocator());
				}
			}
			else
			{
				((((((*doc)["partners"]).GetArray())[i]).GetObject())[field.c_str()]).SetString(nv.c_str(), (*doc).GetAllocator());
			}
		}
		else
		{
			(((((*doc)["partners"]).GetArray())[i]).GetObject()).AddMember(rapidjson::Value().SetString(field.c_str(), (*doc).GetAllocator()), rapidjson::Value().SetString(nv.c_str(), (*doc).GetAllocator()), (*doc).GetAllocator());
		}
		cout << "partner " << name << " updated" << endl;
	}
}
