
# generic imports
import numpy as np
import torch

# pyg imports
from torch_geometric.data import InMemoryDataset, Data
from torch_geometric.transforms import KNNGraph

# WCSimPackage imports
import src.data_utils as du

from src.RootInterface import RootInterface
from src.data_utils import ExtremaFinder


"""
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


class GraphInMemoryDataset(RootInterface, InMemoryDataset):
    r"""" Last update of this documentation : //2024    
    Args:
            root_folder_path: str
                path to the existing .root file
            graph_folder_path: str 
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
                Will be used to compute the edges of the graph
            transform (Optional): function
                transform argument from torch_geometric InMemoryDataset class
    """

    def __init__(
            self, 
            graph_folder_path : str,
            graph_file_names : list=[''],
            nb_datapoints : int=None,
            root_folder_path : str='',
            root_file_names: list=[''],
            tree_name : str='',
            train_data_info: dict=None,
            label_data_info: dict=None,
            edge_data_info: dict=None,
            init_from_processed : bool=False,
            to_torch_tensor : bool = True,
            verbose : int = 0,
            pre_filter = None,
            pre_transform = None,
            transform= None , 
            transforms= None  # Do not use. Only for compatibility with watchmal. In discussion with Nick to solve this redundancy.
    ):

        # Variables to get the root file
        self.root_folder_path  = root_folder_path
        self.root_file_names   = root_file_names 
        self.tree_name         = tree_name

        # Where to look for / save the data
        self.graph_folder_path = graph_folder_path
        self.graph_file_names  = graph_file_names
        
        # What to apply to the data
        self.pre_filter    = pre_filter
        self.pre_transform = pre_transform
        self.transform     = transform

        # Other
        self.verbose = verbose
        
        # All the variables in the if below are used only by self.process()
        # thus only necessary if we want to create graphs from .root files
        if not init_from_processed:
            # self.process() will be called

            self.nb_datapoints = nb_datapoints    

            # Check how many events to store
            if nb_datapoints is not None  : 
                self.nb_datapoints = nb_datapoints
            else :
                self.nb_datapoints = 100_000_000 # Number of events never reached

            self.train_keys, self.train_types = train_data_info['keys'], train_data_info['types']
            self.label_keys, self.label_types = label_data_info['keys'], label_data_info['types']
            self.edge_keys, self.edge_types   = edge_data_info['keys'], edge_data_info['types']

            if self.pre_transform is not None:
                self.pre_transform = KNNGraph(**self.pre_transform['kNN']) # If one day we need more pre_transform, we'll use the TransformCompose from torch_geometric (see CAVERNS)
            self.to_torch_tensor  = to_torch_tensor

        # Est-ce que cette classe est vraiment utile ? 
        # ou une méthode / une simple instantiation 
        # self.root_interface = RootInterface()
        # sans héritage est suffisant ?    
                    
        RootInterface.__init__(
            self,
            verbose=self.verbose,
        )

        # Instantiate the PyG Dataset class
        # MUST BE AT THE END OF THE __INIT__ (JUST BEFORE THE self.load)
        InMemoryDataset.__init__(
            self,
            root=self.graph_folder_path, 
            pre_filter=self.pre_filter,
            pre_transform=self.pre_transform, # Pre transform is applied to the data only once, before creating the grah
            transform=self.transform # composition of transforms argument should go there. (Équivalent to torchvision "transformCompose class")
        )

        # Load everything onto the RAM
        self.load(self.processed_paths[0])
        
        # --- Display info --- #
        print(f"\nProcessed path     : {self.processed_paths}")
        print(f"Len of the dataset : {self.len()}")
        if root_folder_path:
            print(f"From .root files   : {self.raw_file_names}")            


    @property
    def raw_file_names(self):
        # A list of files which must be found to skip download()
        # The fact that it points to existing file doesn't matter for torch_geometric
        #[self.root_folder_path + '/' + root_file_name for root_file_name in self.root_file_names]
        return self.root_file_names

    @property
    def processed_file_names(self):
        # A list of files which must be found to skip process()
        # Where the graph data will be looked at
        return self.graph_file_names

    def process(self):

        data_list = [] 
        all_keys = self.train_keys + self.label_keys + self.edge_keys
       
        # Class to monitor extrema of the data
        extrema_monitor = ExtremaFinder(*all_keys)

        for i, root_file_name in enumerate(self.root_file_names):

            if self.verbose >= 1:
                print(f"\nFichier root : {i}")
                print(f"From : {self.root_folder_path + '/' + root_file_name}")

            # Get the data from the current .root file
            num_entries, data_dict = self.extract_data(
                file_path=self.root_folder_path + '/' + root_file_name,
                tree_name=self.tree_name,
                keys=all_keys,
                nb_datapoints=self.nb_datapoints
                ) # returns (number_of_events, dictionnary)
            
            # Awkward array format makes complex the use of
            # np.min directly on data_dict (even flattening is not trivial)
            # so we chose to compute the maxs / mins while iterating below 
            for j in range(num_entries):

                # Monitor extrema while they are numpy arrays
                for key in all_keys:
                    extrema_monitor.update(key, data_dict[key][j])
            
                # Extract train, label and edge data and convert to torch.Tensor
                x   = du.convert_from_keys(data_dict, index=j, keys=self.train_keys, to_types=self.train_types, to_tensor=self.to_torch_tensor)
                y   = du.convert_from_keys(data_dict, index=j, keys=self.label_keys, to_types=self.label_types, to_tensor=self.to_torch_tensor)
                pos = du.convert_from_keys(data_dict, index=j, keys=self.edge_keys, to_types=self.edge_types, to_tensor=self.to_torch_tensor)
                
                graph = Data(x=x, y=y, pos=pos) # for .pos see torch_geometric.transforms.KNNGraph 
                data_list.append(graph)

                # --- Display --- #
                if self.verbose >= 1:
                    if j % int(num_entries / 2) == 0 :
                        print(f"Évènement numéro {j}")
                        print(graph)

        if self.pre_filter is not None:
            # data_list = [data for data in data_list if self.pre_filter(data)]
            pass 
        
        if self.pre_transform is not None:
            data_list = [self.pre_transform(data) for data in data_list]

        # --- Display --- #
        extrema_monitor.print_extrema()
        print(f"\nLen of data_list : {len(data_list)}")
        
        # --- Saving --- #
        self.save(data_list, self.processed_paths[0])

    def get(self, idx):
        """
        Linear layers need torch tensor as input, not ndarray

        This overcharge of the get method convert numpy arrays (the type of .x, .edge_index and .y) to torchTensors if they are not already torch tensors
        Note : Most of the loss of torch expect a float format, so even if the labels are stored as int, they will be converted to float when called.
        """

        # Caution : If transform functions are given in __init__(),
        # this data object will NOT have already be transformed.
        # See torch_geometric.Data.Dataset.__getitem__() l.292 - 293
        # Where you can notice it is transformed AFTER self.get(..)
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
