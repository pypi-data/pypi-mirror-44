# RDF2SRL

This package exposes RDF data from sparql database engines for relational 
learning models.

It provides some convenience functions that send sparql queries in http 
requests for both public and private sparql endpoints. 

Starting from version 1.0.3, a ```SmartRDFGraphDataset``` class is added that performs
client-side optimization of the Sparql query processing. This improves the performance 
if the configuration of the public endpoint isn't tuned for a specific query.

## Installation
You cna install the requirements using 
```
pip install -r requiremtns.txt
```
You can install the RDF2SRL package from PyPI:
```
pip install RDF2SRL
```

## Getting Started
### Collecting Statistics about the data
We can use this package to get some statistics about the DBpedia dataset.
Let's use the [DBpedia public endpoint](http://dbpedia.org/sparql) provided 
by [OpenLink Virtuoso](http://dbpedia.org/page/Virtuoso_Universal_Server)

First, import the ```RDFGraphDataset``` class from the python package ```rdf2srl```
and initialize the ```RDFGraphDataset``` class with the endpoint URI and the graph URI

```python
from rdf2srl import RDFGraphDataset
loader = RDFGraphDataset(sparql_endpoint="http://dbpedia.org/sparql", graph_name='http://dbpedia.org/')
```
Now, Let's find the number of (subject, predicate, object) triples in the DBpedia graph:
```python
num_triples = loader.num_triples()
```
To find the number of (subject, predicate, object) triples where the object is another entity,
find the number of entity to entity triples.
```python
num_e2e_triples = loader.num_entity2entity_triples()
```
To find the number of (subject, predicate, object) triples where the object is a literal value,
find the number of entity to entity triples.
```python
num_e2l_triples = loader.num_entity2literal_triples()
```
### Loading the dataset into a dataframe

We can also use the package to access the entities in the graph. A useful format for
relational learning models is a dictionary that maps each entity to an index that starts
from 0 to n_entities-1. Other available formats are pandas dataframes and python lists.
```python
entity2idx = loader.entities('dict')
```
Similarly, we can get all the entity-to-entity predicates in the graph. A useful format for
relational learning models is a dictionary that maps each predicate to an index that starts
from 0 to n_relations-1. Other available formats are pandas dataframes and python lists.
```python
relation2idx = loader.relations('dict')
```
Now, we can get the triples in the dataset in a dataframe of three columns: [subject, object, predicate]
where the values inside the tuples represent the indices in ```entity2idx``` and ```relation2idx```.
The other available format is python list.
The dataframe can be saved in ```csv``` file if output_dir is passed.
```python
triples = loader.triples('list')
```

## list of the convenience functions available:
```python
RDFGraphDataset.num_entities()  
RDFGraphDataset.num_predicates()  
RDFGraphDataset.num_relations()  
RDFGraphDataset.num_attributes()  
RDFGraphDataset.num_attr_literal_pairs()  
RDFGraphDataset.num_triples()  
RDFGraphDataset.num_entity2literal_triples()  
RDFGraphDataset.num_entity2entity_triples()  
RDFGraphDataset.num_rdf_type_triples()  
RDFGraphDataset.predicates(format) # where format is one of ['dict', 'df', 'list']  
RDFGraphDataset.relations(format) # where format is one of ['dict', 'df', 'list']  
RDFGraphDataset.attributes(format) # where format is one of ['dict', 'df', 'list']  
RDFGraphDataset.entities(format) # where format is one of ['dict', 'df', 'list']  
RDFGraphDataset.attr_literal_pairs()  
RDFGraphDataset.triples(format) # where format is one of ['df', 'list']  
RDFGraphDataset.entity2entity_triples(format) # where format is one of ['df', 'list']  
RDFGraphDataset.entity2literal_triples(format) # where format is one of ['df', 'list']  
RDFGraphDataset.subjects(predicate)  
RDFGraphDataset.objects(predicate)  
RDFGraphDataset.predicates_freq()
```

