from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from pprint import pprint
import csv
import os
import re

def query_data(query_data: dict):

    def format_query(_query_data: dict):
        # create SELECT statement
        _result = '''SELECT DISTINCT'''
        for variable in _query_data["SELECT"]:
            _result += variable + " "
        _result += '\n'

        # create WHERE statement
        _result += "WHERE {\n"
        for union_item in _query_data["UNION"]:

            # process each UNION statement
            _result += "{\n"
            for key, value in union_item.items():
                _result += key + " " + value + " ;\n"
            _result = _result[:-2] + ".\n } UNION "

        _result = _result[:-7] + "}\n"

        # create ORDER BY statement
        _result += '''ORDER BY DESC(?total_pop) '''   # ugly hack

        # create LIMIT statement (used for testing)
        #_result += ''' LIMIT 10 '''

        return _result

    # initialize the wrapper
    sparql = SPARQLWrapper('https://dbpedia.org/sparql')

    # construct and fire the query
    query = format_query(query_data)

    sparql.setQuery(query)

    # parse the result
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()

    # digest it
    digested = []
    for result in qres['results']['bindings']:

        entry = {}
        for value in query_data["SELECT"]:
            if value[0] == '?':
                entry[value[1:]] = result[value[1:]]    # extract relevant fields
        digested.append(entry)

    return digested

def output_to_csv(data: list, file_path: str):

    # open file and prepare csv writer
    with open(file_path, 'w', encoding='UTF8') as file:
        writer = csv.writer(file)

        # output headers
        headers = []
        for key in data[0]:
            headers.append(str(key))
        writer.writerow(headers)

        # output data
        for entry in data:
            row = []
            for key, value in entry.items():
                if key != 'total_pop':
                    row.append(value["value"])
                else:
                    row.append(re.findall(r"[-+]?\d*\.\d+|\d+", value["value"])[0])

            writer.writerow(row)


def query_country(country: str, location: str):
    country_instruction = 'dbo:country  dbr:{}'.format(country)

    sparql_query = {
        "SELECT": ["?city_name", "?latitude", "?longitude", "?total_pop"],
        "UNION": [
            # {
            #     '?city  rdf:type  yago:WikicatCityCountiesOfPoland': ' ',
            #     str(country_instruction): ' ',
            #     'foaf:name': '?city_name',
            #     'geo:lat': '?latitude',
            #     'geo:long': '?longitude',
            #     'dbp:populationTotal': '?total_pop',
            # },
            {
                '?city  rdf:type  dbo:City': ' ',
                str(country_instruction): ' ',
                'foaf:name': '?city_name',
                'geo:lat': '?latitude',
                'geo:long': '?longitude',
                'dbp:populationTotal': '?total_pop',
            },
            {
                '?city  rdf:type  dbo:Town': ' ',
                str(country_instruction): ' ',
                'foaf:name': '?city_name',
                'geo:lat': '?latitude',
                'geo:long': '?longitude',
                'dbp:populationTotal': '?total_pop',
            },
            {
                '?city  rdf:type  dbo:Village': ' ',
                str(country_instruction): ' ',
                'foaf:name': '?city_name',
                'geo:lat': '?latitude',
                'geo:long': '?longitude',
                'dbp:populationTotal': '?total_pop',
            }
        ],
    }

    # fetch digested data
    data = query_data(sparql_query)

    # save to csv
    output_to_csv(data, location)
    # print(data)


if __name__ == '__main__':
    query_country('Poland', os.getcwd() + "/output.csv")