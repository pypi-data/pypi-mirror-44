# FOntCell

Ontology Fusion proyect

# User Manual:
After download and installing FOntCell using pip you have to create the 
following directories:

-output_folder: named has you want and put them where you want.

-input_folder: named has you want and put them where you want.

Output_folder will be the directory where FOntCell put the differents results
(the fused ontolgy, a html doc, figures, etc)

At input_folder the user has to put the Configurations file, both ontologies,
and the ontology_edit documents.

# Documents required at Input directory

- Configuration file

The configuration file has to be the next arguments (a default configuration
will add at the end of the document). This file will be in .txt format.

_Most arguments will be for ontology 1 (A) and ontology 2 (B)_

| Arguments | Description |
| ------ | ------ |
| input_folder | _str_ path to input directory |
| output_folder | _str_ path to output directory | 
| parallelization | _bool_ perform if true, a paralellization*| 
| proc | _int_ number of processors¹*|
| parse_ontology | _bool_ perform if true, the ontology parsing|
| file | _str_ name of the ontology (at .owl format)² ³| 
| take_synonyms | _bool_ take the also the synonyms from ontology classes ³|
| ontologyName | _str_ name of the ontology ³|
| synonym_type | _str_ _one or more_ ontology arguments where take the synonyms³|
| label_type | _str_ _one or more_ ontology arguments where take the label³|
| relative_type |  _str_ _one or more_ ontology arguments where take the ascendants³|
| file_clean_ontology | _str_ name of the file for edit the ontology² ³|
| ontology_file | _str_ name to ontology parsed² ⁴|
| ontology_name | _str_  name of the ontology⁴|
| del_old_trials_files | _bool_ delete the internal files generated for other trials|
| onto_fuse_classes | _bool_ fuse the classes in a ontology if they have the same label|
| onto_restriction | _bool_ fuse the classes in a ontology if they have the same ID (or secondary info) and the same label|
| onto_list_clear | _str_ _one or more_ delete the introduced words from labels⁵|
| synonyms | _bool_ perform if true the synonyms sequential test|
| text_process | _bool_ perform if true, a test processing |
| split_from | _str_ split and take the labels from the introduced word to end⁵|
| split_since | _str_ split and take the labels from the beigining since the word introduced⁵|
| windowsize | _int_ Size (in edges) of the convolutional windows|
| globalthreshold | _float_ threshold between 0.0-1.0 for sequential similarity|
| localthreshold | _float_ threshold between 0.0-1.0 for local sequential similarity (used at topological similarity)|
| constriction_threshold | _float_ threshold between 0.0-1.0 for constriction similarity*|
| topological_treshold | _float_ threshold between 0.0-1.0 for topological similarity*|
| topological_similarity| _str_ topological similarity test: 'blondel', 'cosine', 'euclidiean', 'pearson' or 'constriction'|

_* Argument can be blank if your analysis does not require those arguments_

_¹ only if parallelization is True_

_² files must be at input directory_

_³ only if parse ontology is True_

_⁴ only if parse ontology is False_

_⁵ if text_process is True_

_Every argument at configuration.txt need a '>' character forward to be parsed. The user do not have to introduce a threshold for a test that it has not been selected_

- Ontology Edit File

This documents allows the user to edit the ontology after parse in order to direct the ontology fusion.

The document must be in .txt file with the different orders for an authomatic processing. 

|Order name | order |  order example | explanation |
| ------ | ------ | ------ | ------ |
| delete class | ' ... ' | 'ontology label x' | deletes the nodes/classes that contais the label  |
| concatenate classes | [[...], [...]]   | [[[ontology_class_synonyms]1, ID:0], [[ontology_class_synonyms2], ID:1]] | concatenate two classes, allows introduce new classes |
| delete class from ID | ID: ' ... '| ID:'xxxxx' | delete the class that has the ID introduced|
| fuse classes | f[[...], [...]] | f[[ontology_synonyms1], [ontology_synonyms2]] | fuse two classes. The resultant class conserve the ID from the first and both descendant-ascendant relations)|

- Ontologies

The ontologies that we want to fuse. The ontologies can be at .owl format (that requires a parse) or in a .ods format if we want to save the parse step.

The .ods format will two column file. The format will be a edges-like format:

|  |  |
| ------ | ------ |
| [[class synonyms 1], ID class 1] | [[class synonyms 2], ID class 2] |
| [[class synonyms 1], ID class 1] | [[class synonyms 3], ID class 3] |
| [[class synonyms 2], ID class 2] | [[class synonyms 4], ID class 4] | 

_note Attending that the first column correspond to 'father' and the second column 'his descendant'. If a class don not have descendant will be recognized if it is at father column (with no descendant) or only as a child of another class_


# Documents found at output directory after fusion

- A .owl document

This document is the resultant ontology of fusing both ontologies. The structure is the same as the ontology 1 (A) with the new classes added from ontology two at the top of ontology class section. 

- FOntCell_OntolgyA_OntologyB.html file

This file shows information about the fusion. First we can see three interactive circular graph of ontology A, ontology B and the merged ontology. Also shows other information such: the different thresholds values and statistics about fusion. 
This file also shows a direct link to the OBO formated merged ontology, and a representative image of type of node asignation between ontology A and B (a donut graph) and a image of an Euler-Venn diagram (using squares) about how the fusion has work.

- Other .html and -png files

These files are the incrusted at the FOntCell_OntologyA_OntologyB.html file. The .html files are all the different interactive circular graphs, and the .png are the Euler-Venn diagram and the donut graph.

- Additional .txt files

If one 'raw' ontology (start as .owl file) has more than one plausible roots (a node in a digraph without ascendant), two .txt file will be created:

*ontology_plausibles_roots.txt:* The list of nodes (in the digraph, classes at ontology) without ascendant nodes. In the example of fusing cell development ontologies, only one root will be allowed (zyogote). The others has to be reconected using the edit-ontologies tools in FOntCell.

*ontology_with_various_roots.txt:* In order to facilitate the task of search the correct node label for concatenate nodes to 'false root nodes', FOntCell creates this file with all the relations in a parent-son (graph edge) format.


# How to run FOntCell

Once we have the input and output directories, FOntCell and the configuration.txt file correctly configured (and the ontologies edit .txt files configures or not depending on our analysis) we have to go to python (At bash for example) and write:

`import fontcell`

And now we get:

_configuration.txt path:_

Finally, we only have to put the path to our configuration.txt file and FOntCell will run our ontology fusion. After a while we get the results of our fusion (and the fused result) at the out_put directory

