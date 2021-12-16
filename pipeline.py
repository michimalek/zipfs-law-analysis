from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON, N3
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint
import csv
import pprint
import os


import query_graphql
from zipfs_script import calc_freq_prob, compare_hel_dist, compare_kl_divergence, convert_to_rank_table, plot_zipf


def remove_folder(path: str):
    try:
        os.rmdir(path)
    except:
        None


def make_folder(path: str):
    try:
        os.mkdir(path)
    except:
        None


def fetch_countries_data(countries_data: dict):
    # try to remove folders where the computed data will end up in
    for (country_name, paths) in countries_data.items():
        remove_folder(paths["input"])

    # try to create folders where the computed data will end up in
    for (country_name, paths) in countries_data.items():
        make_folder(paths["input"])

    # fetch data from dbpedia
    for (country_name, paths) in countries_data.items():
        csv_path = paths["input"] + paths["file"]

        # make sure that the possibly existing dataset with the same name is removed
        try:
            os.remove(csv_path)
        except:
            None

        # download new dataset
        query_graphql.query_country(country_name, csv_path)


def research_question(countries_data: dict):
    print("----------- research_question - BEGIN -----------")
    # Choose country to get data from (Format: country = "Country")
    # So far there are only Netherlands and Poland
    country = "Poland"

    # Read querried .CSV from DBPedia
    df = pd.read_csv(countries_data[country]["input"] + countries_data[country]["file"])

    # Sort cities by population, add rank column
    sorted_df = convert_to_rank_table(df)
    plot_zipf(sorted_df)

    # Calculate frequency probability of all cities
    freq_prob_df = calc_freq_prob(sorted_df)

    # Print the head of the current Dataframe
    print("\nHead of table")
    print(freq_prob_df.head())

    # Calculate and comapre both Hellinger Distance and Kullback-Leiber Divergence for each data set
    compare_hel_dist(freq_prob_df)
    compare_kl_divergence(freq_prob_df)

    
    print("----------- research_question - DONE -----------")

if __name__ == '__main__':
    countries_to_query = {
        'Poland': {
            "input": os.getcwd() + "/data/",
            "file": "poland_data.csv",
            "output": os.getcwd() + "/data/poland/"
        },
        'Netherlands': {
            "input": os.getcwd() + "/data/",
            "file": "netherlands_data.csv",
            "output": os.getcwd() + "/data/netherlands/"
        }  # ,
        # 'United_Kingdom': {
        #     "input": os.getcwd() + "/data/",
        #     "file": "united_kingdom_data.csv",
        #     "output": os.getcwd() + "/data/united_kingdom/"
        # }
    }

    fetch_countries_data(countries_to_query)

    research_question(countries_to_query)
