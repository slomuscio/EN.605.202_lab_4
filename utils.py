import os 
import sys
import random
import numpy as np
import glob
import pandas as pd

np.set_printoptions(threshold=sys.maxsize)

def set_working_directory() -> str:
    """Sets the working directory to be the root of this repo. 

    Returns:
        str: Absolute path to working directory. 
    """
    current_working_directory = os.path.dirname(os.path.abspath(__file__))  # Find the path to this file.
    os.chdir(current_working_directory)  # cd to the directory containing this file.
    return current_working_directory


def set_output_file_path(current_working_directory:str) -> str:
    """Sets output filename and path.

    Args:
        current_working_directory (str): Current working directory (output of set_working_directory()). 

    Returns:
        str: Absolute path to the output.txt file. 
    """
    return os.path.join(current_working_directory, "output", "output.txt") 


def generate_input_files(directory:str):
    """Generates input file containing either 25,50, 200, 500 integers that are either in random, ascending, or descending order. 

    Args:
        directory (str): Path to directory containing input files. 
    """
    def write_list(filename:str, values:list):
        """Nested function to write a list to a text file. 

        Args:
            filename (str): Name of output file to write list to. 
            values (list): Values to write to output file. 
        """
        with open(filename, 'w') as f:
            f.write(' '.join(map(str, values)))

    sizes = [25, 50, 200, 500]

    for size in sizes: 
        # Ascending order.
        ascending = list(range(1, size+1))

        # Randomly ordered dataset. 
        random_order = ascending[:]
        random.shuffle(random_order)

        # Descending order. 
        descending = ascending[::-1]

        # Set up filenames for each random, reverse, and ascending order. 
        random_filename = f'{directory}/random_{size}_sam_generated.txt'
        descending_filename = f'{directory}/reverse_{size}_sam_generated.txt'
        ascending_filename = f'{directory}/ascending_{size}_sam_generated.txt'

        # Write lists to files. 
        write_list(random_filename, random_order)
        write_list(descending_filename, descending)
        write_list(ascending_filename, ascending) 


def list_input_files(directory:str) -> list:
    """Generates a list of input files to iterate over. 

    Args:
        directory (str): Path to directory containing input files.  

    Returns:
        list: List of input files to iterate over. 
    """
    input_filenames = glob.glob(f'{directory}/*')
    input_filenames.sort(key=str.lower)
    return input_filenames


def format_input_filename_section_header(filename:str):
    """Formats the header that will be written to output file that will denote which input file is being sorted. 

    Args:
        filename (str): Relative path to input file being sorted. 
    """
    print(f"\n================================================================================")
    print(f"==================== NOW SORTING DATA IN {filename} =====================")
    print(f"================================================================================\n")


def format_shell_sort_output(input_filename:str, gap_values:list, shell_sort_output:np.ndarray, shell_sort_elapsed_time_s:float):
    """Formats the shell sort output in the output text file. 

    Args:
        input_filename (str): Input filename that was just sorted. 
        gap_values (list): Gap values used in the shell sort. 
        shell_sort_output (np.ndarray): Output of the shell sort (should be a sorted array). 
        shell_sort_elapsed_time_s (float): Time taken in SECONDS to perform the sort. 
    """
    print("\t-----------------------------------------------------------------------")
    print(f"\tSorting data in {input_filename}")
    print(f"\tGap Values: {gap_values}")
    print(f"\n\tSorted List: \n{shell_sort_output}")
    print(f"\n\tElapsed Time for Shell Sort: {shell_sort_elapsed_time_s} seconds.")
    print("\t-----------------------------------------------------------------------\n")


def format_heap_sort_output(input_filename:str, heap_sort_output:np.ndarray, heap_sort_elapsed_time_s:float):
    """Formats the heap sort output in the output text file. 

    Args:
        input_filename (str):  Input filename that was just sorted. 
        heap_sort_output (np.ndarray): Output of the heap sort (should be a sorted array). 
        heap_sort_elapsed_time_s (float): Time taken in SECONDS to perform the sort.
    """
    print("\t-----------------------------------------------------------------------")
    print(f"\tSorting data in {input_filename}")
    print(f"\n\tSorted List: \n{heap_sort_output}")
    print(f"\n\tElapsed Time for Heap Sort: {heap_sort_elapsed_time_s} seconds.")
    print("\t-----------------------------------------------------------------------\n")


def make_dataframe(filenames:list, sort_type:list, elapsed_times_s:list, n_data:list, file_types:list) -> pd.DataFrame:
    """Constructs DataFrame containing timing data and sort metadata for analysis. 

    Args:
        filenames (list): Input files that were sorted. 
        sort_type (list): Types of sort performed. 
        elapsed_times_s (list): Times taken to run each sort. 
        n_data (list): Number of items sorted (contained in the input file). 
        file_types (list): Type of input data organizaiton. 

    Returns:
        pd.DataFrame: DataFrame containing timing data and sort metadata for analysis. 
    """
    timing_data = pd.DataFrame()
    timing_data['filenames'] = filenames
    timing_data['sort_type'] = sort_type
    timing_data['elapsed_time_s'] = elapsed_times_s
    timing_data['n'] = n_data
    timing_data['file_type'] = file_types
    return timing_data


def format_timing_df(timing_data:pd.DataFrame):
    """Formats timing data DataFrame in output file. 

    Args:
        timing_data (pd.DataFrame): DataFrame containing timing data and sort metadata for analysis. Output of make_dataframe().
    """
    print("\n\n================ Timing Data ====================================")
    print(timing_data.to_string())
    print("=========================================================================\n")


def get_stats(timing_data:pd.DataFrame):
    """Calculates average runtimes for each sorting algroithm across all files, and files grouped by n and initial data organization type. 

    Args:
        timing_data (pd.DataFrame): DataFrame containing timing data and sort metadata for analysis. Output of make_dataframe().
    """
    print("\n\n================ Stats Across All Files ====================================")
    # Overall stats by gap 
    knuth_shell = timing_data[timing_data.sort_type == 'shell_knuth']
    second_shell = timing_data[timing_data.sort_type == 'shell_second']
    third_shell = timing_data[timing_data.sort_type == 'shell_third']
    sedgewich_shell = timing_data[timing_data.sort_type == 'shell_sedgewick']
    heap = timing_data[timing_data.sort_type == 'heap']
    # Mean across all n input 
    knuth_mean = knuth_shell.elapsed_time_s.mean()
    second_mean = second_shell.elapsed_time_s.mean()
    third_mean = third_shell.elapsed_time_s.mean()
    sedgewich_mean = sedgewich_shell.elapsed_time_s.mean()
    heap_mean = heap.elapsed_time_s.mean()

    for sort_algo, mean_val in zip(['shell_knuth', 'shell_second', 'shell_third', 'shell_sedgewich', 'shell_heap'], [knuth_mean, second_mean, third_mean, sedgewich_mean, heap_mean]):
        print(f"{sort_algo} mean: {mean_val} seconds.")
    print("=========================================================================\n")

    # Stats by n 
    print("\n================ Stats by n  ====================================")
    unique_n = sorted(timing_data.n.unique())
    for n in unique_n: 
        data_n = timing_data[timing_data.n == n]
        print(f"n value = {n}.\n")
        for sort_type in data_n.sort_type.unique(): 
            data_n_sort_type = data_n[data_n.sort_type == sort_type]
            print(f"{sort_type} mean: {data_n_sort_type.elapsed_time_s.mean()} seconds.")  # Prints the mean execution time for each sorting algorithm 
        print("=========================================================================")
    print("=========================================================================\n")

    # Stats by data order 
    print("\n================ Stats by data order  ====================================")
    asc = timing_data[timing_data.file_type == 'asc']
    dup = timing_data[timing_data.file_type == 'dup']
    ran = timing_data[timing_data.file_type == 'ran']
    rev = timing_data[timing_data.file_type == 'rev']
    for data_order, order_label in zip([asc, dup, ran, rev], ['asc', 'dup', 'ran', 'rev']):
        print(f"data order: {order_label}\n")
        for sort_type in data_order.sort_type.unique(): 
            data_order_sort_type = data_order[data_order.sort_type == sort_type]
            print(f"{sort_type} mean: {data_order_sort_type.elapsed_time_s.mean()} seconds.")  # Prints the mean execution time for each sorting algorithm 
        print("=========================================================================")
    print("=========================================================================\n")


def log_error(e):
    """Logs error to output file. 

    Args:
        e (Exception): Exception to be logged. 
    """
    print(f"\tERROR:\n\t\t{e}")
