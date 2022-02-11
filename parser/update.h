#ifndef UPDATE_H_
#define UPDATE_H_
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "include/rapidjson/document.h"
#include "include/rapidjson/schema.h"
#include "include/rapidjson/stringbuffer.h"
#include "include/rapidjson/prettywriter.h"

std::vector<int> get_pair(std::string p);

int find_partner(rapidjson::Document *doc, std::string name);

void add_partner(rapidjson::Document *doc, rapidjson::Document *n);

void remove_partner(rapidjson::Document *doc, std::string name);

void update_partner(rapidjson::Document *doc, std::string name, std::string field, std::string nv);

#endif /* UPDATE_H_ */
