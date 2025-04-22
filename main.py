import os 
import sys
import glob
import numpy as np  
import utils
import src
import pandas as pd 

def main():
    gaps = {
        "knuth": [29524, 9841, 3280, 1093, 364, 121, 40, 13, 4, 1],
        "second": [30341, 10111, 3371, 1123, 373, 149, 53, 17, 5, 1],
        "third": [29160, 9720, 3240,1080, 360, 120, 60, 30, 10, 1,],
        # "fourth": [],
    }

    # Set current working directory. 
    current_working_directory = utils.set_working_directory()

    # Set output file location and name. 
    output_file = utils.set_output_file_path(current_working_directory)
    o = open(output_file, 'w')
    sys.stdout = o  # Write standard output to output text file. 

    # Set location of input files containing data to be sorted. 
    input_files_directory = os.path.join(current_working_directory, "input")

    # Generate additional input files to be sorted and save them into the ./input/ directory with other input files. 
    utils.generate_input_files(input_files_directory)

    # Get list of input files. 
    input_filenames = utils.list_input_files(input_files_directory)
    # input_filenames = glob.glob(f'{input_files_directory}/*')
    # input_filenames.sort(key=str.lower)

    # Set up empty lists to append data and metadata to for timing analysis. 
    filenames = []
    sort_type = []
    elapsed_times_s = []
    n_data = []
    file_types = []

    for filename_full_path in input_filenames:  # Loop over each input file 
        # Get just the filename of the input file. 
        filename = os.path.basename(filename_full_path)

        # Read data from input file 
        data = np.genfromtxt(filename_full_path)
        n = len(data)  # Number of items to be sorted. 
        file_type = filename[:3]  # Type of data arrangement: asc, rev, dup, ran. 

        # Make a section header in output filename for this file
        utils.format_input_filename_section_header(f"./input/{filename}")  

        # Shell Sort 
        print("SHELL SORT")
        for i, gap_values in enumerate(gaps.values()):
            shell_sort_output, shell_sort_elapsed_time_s = src.shell_sort(data, gap_values)
            utils.format_shell_sort_output(f"./input/{filename}", gap_values, shell_sort_output, shell_sort_elapsed_time_s)  # Write to output file.
            
            # Collect elapsed time data and metadata for efficiency analysis. 
            filenames.append(filename)
            sort_type.append(f'shell_{i}')
            elapsed_times_s.append(shell_sort_elapsed_time_s)
            n_data.append(n)
            file_types.append(file_type)

        # Heap Sort 
        print("HEAP SORT")
        heap_sort_output, heap_sort_elapsed_time_s = src.heap_sort(data)
        utils.format_heap_sort_output(f"./input/{filename}", heap_sort_output, heap_sort_elapsed_time_s)

        # Collect elapsed time data. 
        filenames.append(filename)
        sort_type.append(f'heap')
        elapsed_times_s.append(heap_sort_elapsed_time_s)
        n_data.append(n)
        file_types.append(file_type)

    # Put elapsed time data and metadata into DataFrame for efficiency analysis. 
    timing_data = utils.make_dataframe(filenames, sort_type, elapsed_times_s, n_data, file_types)

    # Write timing data DataFrame to output file. 
    print(timing_data.to_string())

    # Timing data analysis statistics. 
    utils.time_stats(timing_data)

    o.close()

    print(data)


if __name__=="__main__":
    main()
