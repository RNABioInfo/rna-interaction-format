#include<iostream>
#include<vector>
#include <string>
#include "update.h"

using namespace std;

int isin(int e, std::vector<int> lst)
{
	int s=lst.size();
	int c=0;
	int i=0;
	while(c==0 && i<s)
	{
		if(lst[i]==e)
		{
			c=1;
		}
		i++;
	}
	return i*c-1;
}

std::vector<std::vector<std::string>> read_query(std::string q)
{
	std::vector<std::vector<std::string>> res(0);
	std::vector<std::string> tmp(0);
	std::string s="";
	int i=0;
	int t=0;
	while(i<q.size())
	{
		if(q[i]=='=' || q[i]==':')
		{
			tmp.push_back(s);
			res.push_back(tmp);
			tmp.clear();
			s="";
		}
		else if(q[i]==',')
		{
			(res[t]).push_back(s);
			s="";
		}
		else if(q[i]==';')
		{
			(res[t]).push_back(s);
			s="";
			t++;
		}
		else if(q[i] !=' ')
		{
			s+=q[i];
		}
		i++;
	}
	(res[t]).push_back(s);
	return res;
}

//to use one of the methods below, better make sure first that the json document given as input is valid with regard to the schema (with schema_validator()). Things will probably not work otherwise.


int find_interaction(rapidjson::Document *doc, int ref)
//searches an interaction from its ID, returns its position in the list of partners (or -1 if the partner is not found).
{
	int s=(*doc).Size();
	int i=0;
	int c=0;
	while(c==0 && i<s)
	{
		if(((*doc)[i]["ID"]).GetInt()==ref)
		{
			c=1;
		}
		i++;
	}
	return i*c-1;
}

std::vector<int> subset_interaction(rapidjson::Document *doc, std::string q)
//returns position of all interactions whose ID/class/type/partner matches the query.
//queries are single string of the form "key1: val1, val2; key2: val; key3: val1, val2".
//spaces are ignored.
//example of a valid query: "partner=Hfq,Bbh,micF; type=basepairing"
{	
	std::vector<int> res;
	int s=(*doc).Size();
	std::vector<std::vector<std::string>> qr=read_query(q);
	int sq=qr.size();
	std::string nm;
	std::string val;
	int ref=0;
	std::vector<int> c (s);
	for(int j=0; j<qr.size(); j++)
	{
		nm=qr[j][0];
		if (std::string(nm)=="ID")
		{
			for(int k=1; k<(qr[j]).size(); k++)
			{
				int ref=stoi(qr[j][k]);
				for(int i=0; i<s; i++)
				{
					if(((*doc)[i]["ID"]).GetInt()==ref)
					{
						c[i]++;
					}
				}
			}
		}
		else if (std::string(nm)=="class" || std::string(nm)=="type")
		{
			for(int k=1; k<(qr[j]).size(); k++)
			{
				val=qr[j][k];
				for(int i=0; i<s; i++)
				{
					if(((*doc)[i][nm.c_str()]).GetString()==val)
					{
						c[i]++;
					}
				}
			}
		}
		else if(std::string(nm)=="partner")
		{
			int p=0;
			int ch=0;
			int ib=0;
			int k=0;
			for(int i=0; i<s; i++)
			{
				ch=0;
				p=((*doc)[i]["partners"]).Size();
				k=1;
				while(k<(qr[j]).size() && ch==0)
				{
					ib=0;
					val=qr[j][k];
					while(ib<p && ch==0)
					{
						if(((*doc)[i]["partners"][ib]["name"]).GetString()==val || ((*doc)[i]["partners"][ib]["symbol"]).GetString()==val )
						{
							ch=1;
						}
						ib++;
					}
					k++;
				}
				if(ch==1)
				{
					c[i]++;
				}
			}
		}
		else
		{
			cout << "interactions have no field " << nm << endl;
		}
	}
	for(int i=0; i<s;i++)
	{
		if(c[i]==sq)
		{
			res.push_back(i);
		}
	}
	return res;
}

rapidjson::Document get_interaction(rapidjson::Document *doc, std::string q)
//creates a new json Document containing all interactions whose ID/class/type/partner matches the query.
//queries are single string of the form "key1: val1, val2; key2: val; key3: val1, val2". spaces are ignored.
//example of a valid query: "partner=Hfq,Bbh,micF; type=basepairing"
{
	std::vector<int> loc=subset_interaction(doc,q);
	rapidjson::Document res;
	res.SetArray();
	rapidjson::Value tmp;
	int s=(*doc).Size();
	for(int i=0; i<s; i++)
	{
		if(isin(i,loc)>-1)
		{
			tmp.CopyFrom((*doc)[i], res.GetAllocator());
			(res.GetArray()).PushBack(tmp, res.GetAllocator());
		}
	}
		return res;
}

void add_interaction(rapidjson::Document *doc, rapidjson::Value v)
//adds a new interaction, but first checks that there is not already an interaction with same ID. Does not add the new interaction if this is the case. And does not check that the updated document remains valid with regards to the schema
{
	int ref=(v["ID"]).GetInt();
	int i=find_interaction(doc, ref);
	if(i==-1)
	{
		((*doc).GetArray()).PushBack(v, (*doc).GetAllocator());
		cout << "added interaction " << ref << endl;
	}
	else
	{
		cout << "an interaction with ID " << ref << " already exists" << endl;
	}
}

void remove_interaction(rapidjson::Document *doc, int ref)
//as name says
{
	int i=find_interaction(doc, ref);
	if(i==-1)
	{
		cout << "no interaction " << ref << endl;
	}
	else
	{
		((*doc).GetArray()).Erase(((*doc).GetArray()).Begin()+i);
		cout << "interaction " << ref << " removed" << endl;
	}
}



