

from torch_geometric.data import InMemoryDataset, Data

# import the RootInterface
from src.RootInterface import RootInterface_v2

# fonctions to manage the data
import src.data_utils as du
from src.data_utils import ExtremaFinder


"""
The purpose of this class is to create one big InMemoryDataset
class from multiple InMemoryDataset already processed and store 
somewhere.
"""

class MultipleInMemoryDataset(RootInterface_v2, InMemoryDataset):
    r"""" Last update of this documentation : //2024    
    Args:
            root_file_path: str
                path to the existing .root file
            save_graph_path: str 
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
            save_graph_path : str,
            graph_file_names : list=['aaa.pt'],
            nb_datapoints = None,
            root_folder_path : str='',
            root_file_names: list=['hey.root'],
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


        # if init_from_processed:
            
        #     self.nb_datapoints = 
        #     graph_save_path = ''

        #     self.init_from_processed()
    
        # else :
        #     self.init_from_root_file()


        # General variables
        self.nb_datapoints = nb_datapoints    
        
        self.verbose = verbose

        # Variables to get the root file
        self.root_file_path  = root_folder_path
        self.root_file_names = root_file_names 
        self.tree_name       = tree_name

        self.graph_folder_path = save_graph_path
        self.graph_file_names  = graph_file_names

        # Variable to create the graphs
        self.graph_init = False

        self.train_keys, self.train_types = train_data_info['keys'], train_data_info['types']
        self.label_keys, self.label_types = label_data_info['keys'], label_data_info['types']
        self.edge_keys, self.edge_types   = edge_data_info['keys'], edge_data_info['types']

        self.to_torch_tensor  = to_torch_tensor
        #self.graph_init       = True # Deprecated variable. Not used anymore

        # Check how many events to store
        if nb_datapoints is not None  : 
            self.nb_datapoints = nb_datapoints
        else :
            self.nb_datapoints = 100_000_000 # Number of events never reached

        ### --- Not the most clean way to call the __init__ of parents classes, but 
        ### --- still it seems the most comprehensible way for everyone to me

        # Instantiate the RootDataset class (to read the .root file)
        RootInterface.__init__(
            self,
            root_file_path=self.root__path,
            tree_name=self.tree_name,
            verbose=self.verbose,
            nb_datapoints=self.nb_datapoints
        )

        # Instantiate the PyG Dataset class
        # MUST BE AT THE END OF THE __INIT__ (JUST BEFORE THE self.load)
        InMemoryDataset.__init__(
            self,
            root=self.save_graph_path, 
            pre_filter=pre_filter,
            pre_transform=pre_transform, # Pre transform is applied to the data only once, before creating the grah
            transform=transform # composition of transforms argument should go there. (Équivalent to torchvision "transformCompose class")
        )

        # Check if there is data in save_graph_path
        print(f"Processed_path: {self.processed_paths}")

        self.load(self.processed_paths[0])


    def init_from_processed(self, save_graph_path, transform, force_reload=False, nb_datapoints=None):

        self.root_file_path  = '' # for self.raw_file_name() compatibility
        self.save_graph_path = save_graph_path

        InMemoryDataset.__init__(
            self,
            root=self.save_graph_path, 
            transform=transform, # composition of transforms argument should go there. (Équivalent to torchvision "transformCompose class")
            force_reload=force_reload
        )

    @property
    def raw_file_names(self):
        return self.root_file_path

    @property
    def processed_file_names(self):
        return self.graph_names

    def process(self):

        # If process() is called it means that path_to_gnn_dataset is empty
        print(f"No graphs found in the path : {self.save_graph_path}.")
        print(f"Creating a dataset from the .root file : {self.root_file_path}")

        data_list = [] 

        if self.pre_filter is not None:
            pass 
            # Exemple : data_list = [data for data in data_list if self.pre_filter(data)]

        # Get the data from the .root file
        all_keys = self.train_keys + self.label_keys + self.edge_keys
        num_entries, data_dict = self.extract_data(all_keys) # returns (number_of_events, a dict with all the data)
        
        # Class to monitor extrema of the data
        extrema_monitor = ExtremaFinder(*all_keys)

        # Akward array format makes complex the use of
        # np.min directly on data_dict (even flattening is not trivial)
        # so we chose to compute the maxs / mins while iterating below 
        for i in range(num_entries):

            # Monitor extrema while they are numpy arrays
            for key in all_keys:
                extrema_monitor.update(key, data_dict[key][i])
        
            # Extract train, label and edge data and convert to torch.Tensor
            x   = du.convert_from_keys(data_dict, index=i, keys=self.train_keys, to_types=self.train_types, to_tensor=self.to_torch_tensor)
            y   = du.convert_from_keys(data_dict, index=i, keys=self.label_keys, to_types=self.label_types, to_tensor=self.to_torch_tensor)
            pos = du.convert_from_keys(data_dict, index=i, keys=self.edge_keys, to_types=self.edge_types, to_tensor=self.to_torch_tensor)
            
            graph = Data(x=x, y=y, pos=pos) # for .pos see torch_geometric.transforms.KNNGraph 
            data_list.append(graph)

            # --- Display --- #
            if self.verbose >= 1:
                if i % int(num_entries / 2) == 0 :
                    print(f"\nÉvènement numéro {i}")
                    print(graph)

        extrema_monitor.print_extrema()

        if self.pre_transform is not None:
            data_list = [self.pre_transform(data) for data in data_list]

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

