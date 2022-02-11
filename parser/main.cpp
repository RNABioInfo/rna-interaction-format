//============================================================================
// Name        : main.cpp
// Author      : gs
// Version     :
// Copyright   :
// Description : @_y
//============================================================================


#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <unistd.h>
#include <time.h>
#include "parse.h"
#include "update.h"

using namespace std;

int main(int argc, char** argv) {
	int dflag=0;
	int sflag=0;
	int arg=0;
	std::string json="";
	std::string sch="";
	std::string wfolder="";
	cout << endl << "RNA-interaction-specification; json and schema validator" << endl;
	cout << "More informations at https://github.com/Ibvt/rna-interaction-specification" << endl << endl;
	while (-1 != (arg = getopt(argc, argv, "s:d:")))
	{
		switch(arg)
		{
			//mandatory parameters
			case 's':
				// path to schema
				sflag=1;
				sch=read_jfile(optarg);
				break;
			case 'd':
				// path to json
				dflag=1;
				wfolder=folder(optarg);
				json=read_jfile(optarg);
				break;
			default:
        			abort ();
		}
	}
	if(sflag==0)
	{
		cout << "Please provide a path to the json schema (using option -s)" << endl;
		return 1;
	}
	if(dflag==0)
	{
		cout << "Please provide a path to your json file (using option -d)" << endl;
	}
	rapidjson::Document d;
	d.Parse(json.c_str());
	if(json_check(&d)==1)
	{
		rapidjson::Document s;
		s.Parse(sch.c_str());
		schema_validator(&d, &s);
	}
	cout << endl << "The End !" << endl;
	return 0;
}
