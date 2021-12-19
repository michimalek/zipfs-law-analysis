# Script to compare Zipf's Law to country population

### Description

This Script's origin is based on an university project concerning Central Place Theory.
The purpose is to scrap population data from [DBpedia](https://www.dbpedia.org/) and to compare those to the by Zipf's Law defined Distribution.
DBpedia is a tool to querry trough available Wikipedia data with the use of their querry language SPARql.
If you wanna learn more about Zipf's Law feel free to read trough [here](https://en.wikipedia.org/wiki/Zipf%27s_law).

To compare the Zipf's distribution to the population frequency distribution of the cities of each country, we used two probability distribution comparison tools namely [Hellinger Distance](https://en.wikipedia.org/wiki/Hellinger_distance) and [Kullback-Leibler Divergence](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence). Those indicate how similar two distributions are from each other.
When the script is run it prints out some indication of what is going on and at the end prints the results of Hellinger Distance and KL Divergence.

Short summary of how to understand the resulting values:
- **Hellinger Distance** describes the degree of similarity between two different probability distribu-
tions. It is calculated as a scale between 0 and 1, where 0 being that the two distribution are identical to each other and 1 that
they are the furthest apart from each other.
- **Kullback-Leibler Divergence** focuses on information loss
between two distributions. This is indicated by first mapping the real data to
the zipf data and afterwards mapping the zipf data to the real data and compar-
ing both results with each other. If the results are close to each other, there is
almost no information loss and therefore no similarity between the distributions
and contrarily if the results are far away from each other there is significant
information loss and therefore the distributions are not similar. 

### Structure

The script consists of three .py files: 
- *query_graphql.py* prepares the queries and scraps the population data from DBpedia 
- *zipfs_script.py* prepares the DataFrames and does the statistical calculations to compare both distributions by Hellinger Distance and Kullbeck Divergence.
- *pipeline.py* combines all steps into one pipeline.

So far the script only receives data from two european countries Germany and Netherlands. Maybe I will be able to add more countries in the future, otherwise an experienced programmer should be able to expand on the code I wrote.