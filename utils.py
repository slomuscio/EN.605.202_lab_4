import os 
import random
import numpy as np
import glob
import pandas as pd

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
    timing_data = pd.DataFrame()
    timing_data['filenames'] = filenames
    timing_data['sort_type'] = sort_type
    timing_data['elapsed_time_s'] = elapsed_times_s
    timing_data['n'] = n_data
    timing_data['file_type'] = file_types
    return timing_data


def time_stats(timing_data:dict):
    """
    - Stats per file
        - Which was fastest 
        - Average
    - Stats per file_type 
    - Stats per file length 
    """
    # Per file 
    def per_file(timing_data, filename):
        # Extract timing and meta data for a specific file. 
        file_data = timing_data[timing_data.filenames == filename]

        # Get shell sort and heap sort timing info. 
        average_shell_sort = file_data[file_data['sort_type'].str.contains('shell')].elapsed_time_s.mean()
        heap_sort = file_data[file_data['sort_type'] == 'heap'].elapsed_time_s

        # Get ratio of heap sort to average of all shell sorts.
        ratio_heap_to_shell = heap_sort / average_shell_sort

        # Get algos that took the longest and shortest times. 
        max_elapsed_time = file_data[file_data.elapsed_time_s == file_data.elapsed_time_s.max()]
        min_elapsed_time = file_data[file_data.elapsed_time_s == file_data.elapsed_time_s.min()] 

        # Write these stats to the output file. 
        print(f"\tAverage shell sort execution time: {average_shell_sort} seconds.")
        print(f"\tHeap sort execution time: {heap_sort.to_string(index=False)} seconds.")
        print(f"\n\tHeap sort takes {ratio_heap_to_shell.to_string(index=False)} times longer than shell sort.")
        print(f"\n\t{min_elapsed_time.sort_type.to_string(index=False)} algorithm took the minimum time to run; {min_elapsed_time.elapsed_time_s.to_string(index=False)} seconds.")
        print(f"\t{max_elapsed_time.sort_type.to_string(index=False)} algorithm took the maximum time to run; {max_elapsed_time.elapsed_time_s.to_string(index=False)} seconds.")
    
    def per_type(timing_data, file_type):
        # Extract timing and meta data for a file type (rev, asc, dup, ran). 
        type_data = timing_data[timing_data.file_type == file_type]
        
        # Get shell sort and heap sort timing info. 
        average_shell_sort = type_data[type_data['sort_type'].str.contains('shell')].elapsed_time_s.mean()
        average_heap_sort = type_data[type_data['sort_type'] == 'heap'].elapsed_time_s.mean()

        # Get ratio of heap sort to average of all shell sorts. 
        ratio_heap_to_shell = average_heap_sort / average_shell_sort 

        # Get algos that took the longest and shortest times. 
        max_elapsed_time = type_data[type_data.elapsed_time_s == type_data.elapsed_time_s.max()]
        min_elapsed_time = type_data[type_data.elapsed_time_s == type_data.elapsed_time_s.min()]

        # Write these stats to the output file. 
        print(f"\tAverage shell sort execution time: {average_shell_sort} seconds.")
        print(f"\tAverage heap sort execution time: {average_heap_sort} seconds.")
        print(f"\n\tHeap sort takes {ratio_heap_to_shell} times longer than shell sort.")
        print(f"\n\t{min_elapsed_time.sort_type.to_string(index=False)} algorithm took the minimum time to run; {min_elapsed_time.elapsed_time_s.to_string(index=False)} seconds.")
        print(f"\t{max_elapsed_time.sort_type.to_string(index=False)} algorithm took the maximum time to run; {max_elapsed_time.elapsed_time_s.to_string(index=False)} seconds.")
        # return max_elapsed_time, min_elapsed_time, average_shell_sort, ratio_heap_to_shell 
        
    def per_n(timing_data, n):
        # Extract timing and meta data for all files with same number of items to sort. 
        n_data = timing_data[timing_data.n == n]

        # Get shell sort and heap sort timing info. 
        average_shell_sort = n_data[n_data['sort_type'].str.contains('shell')].elapsed_time_s.mean()
        average_heap_sort = n_data[n_data['sort_type'] == 'heap'].elapsed_time_s.mean()

        # Get ratio of heap sort to average of all shell sorts. 
        ratio_heap_to_shell = average_heap_sort / average_shell_sort 

        # Get algos that took the longest and shortest times. 
        max_elapsed_time = n_data[n_data.elapsed_time_s == n_data.elapsed_time_s.max()].iloc[0]
        min_elapsed_time = n_data[n_data.elapsed_time_s == n_data.elapsed_time_s.min()].iloc[0]

        # Write these stats to the output file. 
        print(f"\tAverage shell sort execution time: {average_shell_sort} seconds.")
        print(f"\tAverage heap sort execution time: {average_heap_sort} seconds.")
        print(f"\n\tHeap sort takes {ratio_heap_to_shell} times longer than shell sort.")
        print(f"\n\t{min_elapsed_time.sort_type} algorithm took the minimum time to run; {min_elapsed_time.elapsed_time_s} seconds.")
        print(f"\t{max_elapsed_time.sort_type} algorithm took the maximum time to run; {max_elapsed_time.elapsed_time_s} seconds.")
        # return max_elapsed_time, min_elapsed_time, average_shell_sort, ratio_heap_to_shell 

    unique_filenames = timing_data.filenames.unique()  # Unique list of all filenames
    unique_filetypes = timing_data.file_type.str.lower().unique()  # Unique list of all file types (asc, dup, ran, rev)
    unique_filetypes.sort()
    unique_n = timing_data.n.unique()  # Unique list of all n
    unique_n.sort()

    print("\n\n========================== STATISTICS PER FILE ==========================")
    for fname in unique_filenames:
        print(f"\t------- {fname} ------------------------------------------")
        per_file(timing_data, fname)
        print(f"\t------------------------------------------------------------\n")
    print("=========================================================================\n")

    print("\n\n========================== STATISTICS PER TYPE ==========================")
    for ftype in unique_filetypes:
        print(f"\t------- {ftype} ------------------------------------------")
        per_type(timing_data, ftype)
        print(f"\t------------------------------------------------------------\n")
    print("=========================================================================\n")

    print("\n\n========================== STATISTICS PER n ==========================")
    for f_n in unique_n:
        print(f"\t------- n = {f_n} ------------------------------------------")
        per_n(timing_data, f_n)
        print(f"\t------------------------------------------------------------\n")
    print("=========================================================================\n")
