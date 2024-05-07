
# basic imports 
import argparse
import yaml
import pprint

# GraphDataset imports
from src.graph_in_memory_dataset import GraphInMemoryDataset


def main(config_path):
    
    with open(config_path, 'r') as pre_config:
        config = yaml.safe_load(pre_config)
        
    pprint.pprint(config)
    GraphInMemoryDataset(**config)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Set the global configuration for the conversion")

    # Add the arguments
    parser.add_argument('-c', '--config_path', type=str, 
                        help='The path to the file to process.')

    args = parser.parse_args()

    print(f"Processing file at: {args.config_path}") 

    main(args.config_path)