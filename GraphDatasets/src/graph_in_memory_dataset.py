import numpy as np
import uproot
import pprint

import torch
from torch_geometric.data import InMemoryDataset, Data


# Watchmal imports
from src.root_dataset import RootDataset
import src.data_utils as du
from src import transformations
from src.extremum_finder import ExtremumFinder


# Remarque : Si on souhaite transformer les données il faut créer une fonction transform
# et la passer en paramètre au début
# (Ou surcharger la fonction get de InMemoryDataset)


class GraphInMemoryDataset(RootDataset, InMemoryDataset):
    r"""" Last update of this documentation : //2024    
    Args:
            root_file_path: str
                path to the existing .root file
            graph_dataset_path: str 
                Root directory where the dataset should be saved.
            tree_name: str
                name of the tree to convert in the .root file
            nb_datapoints : int
                number of datapoint, if none define to 5 000 000 
            train_keys : list
                variables in the dataset that will be used as features during training
            label_keys : list
                variables in the dataset that will be used as labels during training
            edge_keys : list
                variables in the dataset that will be used to compute edges in the graph representation of the data
            to_torch_tensor : bool
               Specifies whether to convert data to PyTorch tensors (True) or not (False)
            verbose: int  [0 ou 1]
                Degree of information printed during the traitement of the .root
            pre_filter (Optional) : (list of) function 
                Apply filters to the data before doing any pre_processing
            pre_transform (Optional) : (list of) function
                pre_transform argument from torch_geometric InMemoryDataset class
            transform: function
                transform argument from torch_geometric InMemoryDataset class

    Notes :
        About the graph creation from an event : decision NOT TO USE the pre_transform
        parameter existing in the InMemoryDataset class of torch_geometric because 
            1. The name would not be explicit
            2. Is it supposed to be a list of functions to apply to the data points 
                before turning them into a graph. So it should not changes the nature 
                of the data. Or creating a graph changes the nature of the data.
            3. There should be only one function to call to create a graph, so a list
                of function is not adapted.
    """

    def __init__(
            self, 
            root_file_path : str,
            tree_name : str,
            graph_dataset_path : str,
            train_keys : list,
            label_keys : list,
            edge_keys : list,
            to_torch_tensor : bool ,
            verbose : int,
            nb_datapoints=None,
            pre_filter=None,
            pre_transform=None,
            transform=None, 
            transforms=None # Do not use. Only for compatibility with watchmal. In discussion with Nick to solve this redundancy.
    ):
        # General variables
        self.nb_datapoints = nb_datapoints    
        
        self.verbose = verbose

        # Variables to get the root file
        self.root_file_path = root_file_path
        self.tree_name = tree_name
        self.graph_dataset_path = graph_dataset_path

        # Variable to create the graphs
        self.graph_init = False

        self.train_keys   = train_keys
        self.label_keys   = label_keys
        self.edge_keys    = edge_keys

        self.to_torch_tensor     = to_torch_tensor
        self.graph_init = True

        if nb_datapoints is not None  : 
            self.nb_datapoints = nb_datapoints
        else :
            self.nb_datapoints = 5_000_000 # Number of events never reached

        ### --- Not the most clean way to call the __init__ of parents classes, but 
        ### --- still it seems the most comprehensible way for everyone to me

        # Instantiate the RootDataset class (to read the .root file)
        RootDataset.__init__(
            self,
            root_file_path=self.root_file_path,
            tree_name=self.tree_name,
            verbose=verbose
        )

        # Instantiate the PyG Dataset class
        # MUST BE AT THE END OF THE __INIT__ (JUST BEFORE THE self.load)
        InMemoryDataset.__init__(
            self,
            root=self.graph_dataset_path, 
            pre_filter=pre_filter,
            pre_transform=pre_transform, # Pre transform is applied to the data only once, before creating the grah
            transform=transform # composition of transforms argument should go there. (Équivalent to torchvision "transformCompose class")
        )

        # Check if there is data in graph_dataset_path
        self.load(self.processed_paths[0])


    @property
    def raw_file_names(self):
        return self.root_file_path

    @property
    def processed_file_names(self):
        return ['data.pt']


    def graph_initialize(self, train_keys, label_keys, edge_keys, to_torch_tensor):
        """
        Method to initialize variables associated to the creation of a graph given a .root file.
        I. e. the values uproot is going to look for.
        """
        self.train_keys   = train_keys
        self.label_keys   = label_keys
        self.edge_keys    = edge_keys

        self.to_torch_tensor     = to_torch_tensor
        self.graph_init = True


    def process(self):
        # If process() is called it means that path_to_gnn_dataset is empty
        print(f"No graphs found in the path : {self.graph_dataset_path}.")
        print(f"Creating a dataset from the .root file : {self.root_file_path}")
        
        if not self.graph_init:
            self.graph_initialize(self.train_keys, self.label_keys, self.edge_keys, self.to_torch_tensor)
    
        if self.pre_filter is not None:
            pass 
            # Exemple : data_list = [data for data in data_list if self.pre_filter(data)]

        # Get the data from the .root file
        all_keys = self.train_keys + self.label_keys + self.edge_keys
        num_entries, data_dict = self.extract_data(all_keys) # returns (number_of_events, a dict with all the data)
        
        data_list = [] 

        #ExtremumFinder is a class to find the extrema of each given argument (here train, edge and y)
        extremum=ExtremumFinder(train=self.train_keys, edge=self.edge_keys, y=self.label_keys)

        for i in range(num_entries):
            x   = du.squeeze_and_convert(data_dict, self.train_keys, index=i, to_tensor=self.to_torch_tensor, to_type=torch.float32)
            y   = du.squeeze_and_convert(data_dict, self.label_keys, index=i, to_tensor=self.to_torch_tensor, to_type=torch.float32)
            pos = du.squeeze_and_convert(data_dict, self.edge_keys, index=i, to_tensor=self.to_torch_tensor, to_type=torch.float32)
            
            extremum.compute_extremum(train=x, edge=pos, y=y)
            
            graph = Data(x=x, y=y, pos=pos) # for .pos see torch_geometric.transforms.KNNGraph 
            data_list.append(graph)


            if self.verbose >= 1:
                if i % ( int((num_entries / 2)) - 1) == 0 :
                    print(f"\nÉvènement numéro {i}")
                    print(graph)
    
            if (i + 1) % self.nb_datapoints  == 0 :
                break

        extremum.print_extremum()

        if self.pre_transform is not None:
            data_list = [self.pre_transform(data) for data in data_list]

        self.save(data_list, self.processed_paths[0])


    def get(self, idx):
        """
        Linear layers need torch tensor as input, not ndarray

        This overcharge of the get method convert numpy arrays (the type of .x, .edge_index and .y) to torchTensors if they are not already torch tensors
        Note : Most of the loss of torch expect a float format, so even if the labels are stored as int, they will be converted to float when called.
        """

        # Caution : If transform functions are given in __init__(), this data object will NOT
        # have already be transformed. See the torch_geometric.Data.Dataset.__get_item__()
         
        data = super().get(idx)
        data.idx = idx

        return data

    def map_labels(in_label, label_set):
        """
        Maps the labels of the dataset into a range of integers from 0 up to N-1, where N is the number of unique labels
        in the provided label set.

        Parameters
        ----------
        label_set: sequence of labels
            Set of all possible labels to map onto the range of integers from 0 to N-1, where N is the number of unique
            labels.
        """
        # This method is for watchmal compatibility
        # This kind of conversion is not currently supported
        # But it will need ot in the future
        # Conversions can be done with one line using label_set.index(PID) i think.
        # Pay attention to the compatibility with the engine

        pass 
        
        
    def add_data_information(self):
        print("Fonction to call if you want to add information on each Data object (i. e. each graph) in the data_list")
        print('You have to define this function in your child class')
        raise NotImplementedError