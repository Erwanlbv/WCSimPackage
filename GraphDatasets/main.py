
import argparse
import yaml
import pprint


# Ajoute les import utiles depuis src/ ici

# from src.root_dataset import RootDataset
# from src.data_utils import squeeze_and_convert
# from src.transformations import Normalize
# from src.transformations import DataToWatchmalDict
from src.graph_in_memory_dataset import GraphInMemoryDataset


# --- Code --- # 

def main(config_path):

    # Load the YAML configuration file
    # config_path = '/pbs/home/c/cehrhardt/rootdataset_work/config.yaml'
    
    with open(config_path, 'r') as pre_config:
        config = yaml.safe_load(pre_config)
        
    pprint.pprint(config)
    
    dataset=GraphInMemoryDataset(**config)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Set the global configuration for the conversion")

    # Add the arguments
    parser.add_argument('-c', '--config_path', type=str, 
                        help='The path to the file to process.')

    args = parser.parse_args()

    print(f"Processing file at: {args.config_path}") 
    # print(f"Verbosity level: {args.verbosity}") #where this arguemtn comes from? 
    # print(f"Verbose mode: {'enabled' if args.verbose else 'disabled'}")
    # print(f"Verbosity level: {'enabled' if args.verbose else 'disabled'}")

    main(args.config_path)