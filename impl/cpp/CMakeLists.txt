cmake_minimum_required(VERSION 3.10)
project(rna-interaction-specification)

add_executable(
	RNA_INT_SPEC
        main.cpp
	parse.cpp
	parse.h
	update.cpp
	update.h
)
