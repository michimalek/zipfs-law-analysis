# Script to compare Zipf's Law to country population

### Description

This Script's origin is based on an university project concerning Central Place Theory.
The purpose is to scrap population data from [DBpedia](https://www.dbpedia.org/) and to compare those to the by Zipf's Law defined Distribution.
DBpedia is a tool to querry trough available Wikipedia data with the use of their querry language SPARql.
If you wanna learn more about Zipf's Law feel free to read trough [here](https://en.wikipedia.org/wiki/Zipf%27s_law).

### How to use

The script consists of three .py files: 
- query_graphql.py prepares the queries and scraps the population data from DBpedia 
- zipfs_script.py prepares the DataFrames and does the statistical calculations to compare both distributions by Hellinger Distance and Kullbeck Divergence
- pipeline.py combines all steps into one pipeline

So far the script only receives data from two european countries Germany and Netherlands. 