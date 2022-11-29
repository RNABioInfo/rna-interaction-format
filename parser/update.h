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

int find_interaction(rapidjson::Document *doc, int ref);

std::vector<int> subset_interaction(rapidjson::Document *doc, std::string q);

rapidjson::Document get_interaction(rapidjson::Document *doc, std::string q);

void add_interaction(rapidjson::Document *doc, rapidjson::Value v);

void remove_interaction(rapidjson::Document *doc, int ref);

#endif /* UPDATE_H_ */
