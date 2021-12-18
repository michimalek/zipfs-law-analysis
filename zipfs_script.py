import pandas as pd
import plotly.express as px
import numpy as np

def convert_to_rank_table(df):

    #Sort by countries population and adds 'rank' column and remove rows with value 0
    sorted_df = df[df['total_pop'] != 0]
    sorted_df = df.sort_values(by=["total_pop"], ascending=False)
    sorted_df['rank'] = range(1, len(sorted_df) + 1)

    # Add Zipf's Law comparison data
    highest_pop = sorted_df.loc[sorted_df['rank'] == 1, 'total_pop'].iloc[0]
    sorted_df['zipf_tot_pop'] = highest_pop // sorted_df['rank']
    final_df = sorted_df[['city_name', 'latitude', 'longitude', 'rank', 'total_pop', 'zipf_tot_pop']]

    # Export DataFrame to CSV (In case file want to be safed)
    # sorted_df.to_csv('data/poland_sorted.csv', index=False)
    print("CSV converted")

    # print(pd.DataFrame(sorted_df))
    return final_df

def plot_zipf(sorted_df,country_name):
    fig = px.line(sorted_df, x = 'rank', y = 'total_pop', 
        title='Cities in {} based on their Rank'.format(country_name), log_x=True,log_y=True,)
    fig.update_traces(name='{}\'s Cities'.format(country_name), showlegend = True)
    fig.add_scatter(x = sorted_df['rank'], y = sorted_df['zipf_tot_pop'])
    fig.update_xaxes(title_text='Rank of City')
    fig.update_yaxes(title_text='Population of City')
    
    fig.show()
    print("Graph comparison should be opened in your browser")

def calc_freq_prob(sorted_df):
    clasf_df = sorted_df
    clasf_df['prob_pop'] = clasf_df['total_pop'] / np.sum(clasf_df['total_pop'])
    clasf_df['prob_zip'] = clasf_df['zipf_tot_pop'] / np.sum(clasf_df['zipf_tot_pop'])
    
    #Check if both probability columns add to a total of 1 (100%)
    print("\nCheck if probability columns add up to 1")
    print("SUCCESS: Population probability adds up to 1") if np.sum(clasf_df['prob_pop']) else print("FAILED: Population probability does not add up to one")
    print("SUCCESS: Zipf probability adds up to 1") if np.sum(clasf_df['prob_zip']) else print("FAILED: Zipfs probability does not add up to one")
    
    return clasf_df

# Function for Hellinger Distance
def hel_dist(true, pred):
    return np.sqrt(0.5 * np.sum((np.sqrt(true) - np.sqrt(pred)) ** 2))

# Function for Kullback-Leiber Divergence
def kul_lei(true, pred):
    return -(np.sum(true * (np.log10(pred / true))))

# Calculate and compare Hellinger Distance for each data set#
def compare_hel_dist(freq_prob_df):
    print('\nHellinger Distance:', hel_dist(freq_prob_df['prob_pop'], freq_prob_df['prob_zip']))

# Calculate and compare Kullback-Leiber Divergence
def compare_kl_divergence(freq_prob_df):
    print('\nKullback-Leiber Divergence')
    print('(P = Data || Q = Zipf) :', kul_lei(freq_prob_df['prob_pop'], freq_prob_df['prob_zip']))
    print('(Q = Zipf || P = Data) :', kul_lei(freq_prob_df['prob_zip'], freq_prob_df['prob_pop']))