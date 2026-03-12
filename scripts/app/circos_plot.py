'''
Script name: plotCircos.py
Version: 1.0
Date: 2026-03-11
Name: Maria Niki Chatzantoni

Description:
This script creates interactive circos plots for the IBD connections between individuals/populations in the database.
Users can select specific populations or individuals, adjust connection thresholds, and generate circos plots.
The script reads the database, filters data based on user input, and generates publication-quality circos plots.

User-defined functions: get_arguments(), query_database(), create_circos_plot(), main()
Non-standard modules: pycirclize, pandas, sqlite3, matplotlib

Input:
- `database_file`: The path to the input database file containing the IBD connections and group information.
  [Example: results/database/ibd_connections.db]

Output:
- Returns filtered dataframes and circos plots for display in Streamlit.

'''

from pycirclize import Circos
import pandas as pd
import sqlite3
import sys
import os

# def get_arguments():

#     script_name = sys.argv[0] # get the name of the script
#     print(f"You are using the script: {script_name}.\n"
#         "It will read the input database file containing the IBD connections and group information and generate circos plots to be displayed in Streamlit.\n")
        
#     # check if the useer gave unnecessary command line arguments
#     if len(sys.argv) != 2:
#         raise ValueError( "The script needs 1 argument for the database file. \n"
#                             "Please run the script with the database file  as an argument. Thank you!")
    
#     # set the input file
#     input_file = sys.argv[1]

#     # if a file doesn't exist raise an error
#         if not os.path.isfile(input_file):
#             raise FileNotFoundError(f"Input file {input_file} not found. Please make sure you have the correct file path.\n Thank you!")
    
#     return input_file, script_name


# function to read the database and create the matrices for individuals and populations
def parse_database(input_file, min_length):

# matrix for individuals and their connections

    # read the database file into a pandas dataframe
    conn = sqlite3.connect(input_file)
    query = "SELECT ind1, ind2, group1, group2, lengthM FROM ibd_connections"
    matrix = pd.read_sql_query(query, conn)
    conn.close()

    # make the lengthM column numeric
    matrix["lengthM"] = matrix["lengthM"].astype(float)

    # if any connection is below the minimum length we drop it from the matrix
    matrix = matrix[matrix["lengthM"] >= min_length]

# matrix for individuals and their connections

    # drop the group columns 
    matrix_ind = matrix.drop(columns=["group1", "group2"])

# matrix for populations and their connections

    # drop the individual columns 
    matrix_pop = matrix.drop(columns=["ind1", "ind2"])

    # if we have any NULL in the group columns we drop them from the matrix
    matrix_pop = matrix_pop.dropna(subset=["group1", "group2"])

    return matrix_ind, matrix_pop

def choose_specific_data(matrix_ind, matrix_pop, mode, selected_individuals, selected_populations):
    

# function to create the circos plot for individuals or populations based on the mode
def create_circos_plot(matrix_ind, matrix_pop, mode):

    # if the mode is individuals we create a circos plot for individuals
    if mode == "individuals":
        circos = Circos.chord_diagram(matrix_ind, "ind1", "ind2", "lengthM", 
        space=5, cmap="Pastel2", label_kws=dict(size=12)) 
        fig = circos.plotfig()
    
    # if the mode is populations we create a circos plot for populations
    elif mode == "populations":
        circos = Circos.chord_diagram(matrix_pop, "group1", "group2", "lengthM", 
        space=5, cmap="Pastel2", label_kws=dict(size=12))
        fig = circos.plotfig()
    
    # if the mode is not individuals or populations we raise an error
    else:
        raise ValueError("Mode must be either 'individuals' or 'populations'. Please choose one of the two options. Thank you!")
    
    return fig
            