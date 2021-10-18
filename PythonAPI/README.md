# Python API

## Usage

### Loading and Parsing

Main functions are provided via the `InteractionFile` class.
Using this it is possible to load a whole file of Interactions like:

```python
from RNAInteraction.RNAInteractions import InteractionFile

interaction_file = InteractionFile.load("/path/to/file")
```

It is then possible to iterate over the Interactions within this file

```python
for interaction in interaction_file:
    print(interaction.interaction_id)
```

For large files it might be beneficial to not load them into memory at once.
Thus, it is possible to parse entries in Interaction Files one after another using
and Generator returned by the `parse()` function.
This can be used  for example to filter the file and construct an `InteractionFile` object
only from a subset as shown below.

```python
from RNAInteraction.RNAInteractions import InteractionFile

filtered_interactions = []
for interaction in InteractionFile.parse("/path/to/file"):
    if interaction.interaction_class == "RNA-RNA":
        filtered_interactions.append(interaction)

interaction_file = InteractionFile(filtered_interactions)
```

### Export

InteractionFile objects can be exported to the RNAinteraction Format using the 
``export_json()`` function as follows:

```python
from RNAInteraction.RNAInteractions import InteractionFile

interaction_file = InteractionFile.load("/path/to/file")
interaction_file.export_json("/new/file/path")
```