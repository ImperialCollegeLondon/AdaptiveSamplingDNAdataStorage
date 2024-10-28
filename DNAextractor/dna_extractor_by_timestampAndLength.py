import argparse
import glob
import os


import re
from datetime import datetime
#import pytz

def check_timestamp(line, target_time, mode):
    # Define the pattern to match the timestamp
    timestamp_pattern = r"start_time=(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)"
	
    print("target_time_before", target_time)
    
    target_time = str(target_time)
    
    target_time = datetime.fromisoformat(target_time.replace("Z", "+00:00"))

    print("target_time_after", target_time)
    
    # Search for the timestamp pattern in the line
    match = re.search(timestamp_pattern, line)
   

    # If timestamp pattern is found, extract and parse the timestamp
    if match:
        timestamp_str = match.group(1)
        #timestamp = datetime.fromisoformat(timestamp_str).replace(tzinfo=pytz.UTC)
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        print("timestamp", timestamp, "target_time", target_time)

        # Check the mode and perform the comparison accordingly
        if mode == "before_or_equal":
            return timestamp <= target_time
        elif mode == "equal_or_after":
            return timestamp >= target_time
        elif mode == "equal":
            return timestamp == target_time
        elif mode == "before":
            return timestamp < target_time
        elif mode == "after":
            return timestamp > target_time
        elif mode == "any":
            return True            
        else:
            raise ValueError("Invalid mode. Please choose 'before_or_equal' or 'equal_or_after'.")
    else:
        return False  # If timestamp pattern is not found in the line


def read_dna_sequences(file_paths, target_time, mode, min_length):
    sequences = [] 
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            current_sequence = ""
            in_sequence = False
            for line in file:
                line = line.strip()
                print("Line:", line)
                print("Timestamp Check Result:", check_timestamp(line, target_time, mode))
                if "@v4.1.0" in line and check_timestamp(line,target_time, mode) is True:
                    in_sequence = True
                    continue
                elif "+" in line:
                    in_sequence = False
                    if current_sequence:
                    	if int(len(current_sequence)) > int(min_length):
                    		sequences.append(current_sequence)
                    	current_sequence = ""
                    continue
                if in_sequence:
                    current_sequence += line
    print("current sequence:", current_sequence)
    print("FINAL SEQ:",sequences)   
    return sequences

def write_fasta_file(sequences, output_file):
    with open(output_file, 'w') as file:
        for i, seq in enumerate(sequences, start=1):
            file.write(f">Sequence_{i}\n")
            file.write(f"{seq}\n")

def main():
    parser = argparse.ArgumentParser(description="Extract DNA sequences from text files in a folder and save them in fasta format.")
    parser.add_argument("input_folder", help="Path to the input folder containing text files with DNA sequences.")
    parser.add_argument("output_file", help="Path to the output fasta file.")
    parser.add_argument("--mode", choices=["before", "after", "before_or_equal", "equal_or_after", "equal", "any"], default="any", help="Timestamp comparison mode.")
    parser.add_argument("--target_time", help="Target time for comparison in the format 'YYYY-MM-DDTHH:MM:SSZ'.", default="1990-07-15T13:30:22Z")
    #parser.add_argument("--target_time", required=True, help="Target time for comparison in the format 'YYYY-MM-DDTHH:MM:SSZ'.")
    parser.add_argument("--min_length", default=0, help="Target cut-off minimum length of the sequences")


    args = parser.parse_args()

    input_folder = args.input_folder
    output_file = args.output_file

    # List all text files in the input folder
    file_paths = glob.glob(os.path.join(input_folder, "*.fastq"))

    dna_sequences = read_dna_sequences(file_paths, args.target_time, args.mode, args.min_length)
    write_fasta_file(dna_sequences, output_file)
    print("Fasta file has been created successfully!")

if __name__ == "__main__":
    main()

