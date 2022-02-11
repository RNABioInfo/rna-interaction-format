#ifndef PARSE_H_
#define PARSE_H_
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "include/rapidjson/document.h"
#include "include/rapidjson/schema.h"
#include "include/rapidjson/stringbuffer.h"
#include "include/rapidjson/prettywriter.h"


std::string read_jfile(std::string add);

std::string folder(std::string add);

void write_json(rapidjson::Document *doc, std::string add, std::string name);

int json_check(rapidjson::Document *doc);

int schema_validator(rapidjson::Document *doc, rapidjson::Document *s);

#endif /* PARSE_H_ */
