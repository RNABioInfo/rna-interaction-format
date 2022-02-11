# rna-interaction-specification

**C++ Parser and Validator**

# Installation and test

**Source compilation prerequisites:**

* Your GCC compiler must support C++17
* CMake >= 3.10 installed
* rapidjson: https://github.com/Tencent/rapidjson/

**Rapid test:**

#Compilation:

```shell
mkdir release-build && cd release-build
cmake..
make
```

# Execution

```shell
./RNA_INT_SPEC [options] 
```

# Mandatory options

**-d** : Path to the .json file to parse

**-s** : Path to a .json schema file

# Output

If the .json file is not a valid json document, an error message is printed in the console, with some tips on frequent mistakes.

If the .json file is not valid with regards the schema, an error message is printed in the console, with indications on the missing/invalid field.

If the .json file is valid with regards to the schema, a success message is printed.
