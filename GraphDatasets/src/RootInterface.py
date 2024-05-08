
import numpy as np
import uproot


"""
Note for future :
If memory becomes a problem when loading, look at .iterate(step_size) 
events = uproot.open("https://scikit-hep.org/uproot3/examples/Zmumu.root:events")
for batch in events.iterate(step_size=500):
    print(repr(batch))

"""


class RootInterface:

    def __init__(
            self,
            nb_datapoints,
            verbose=0,
            entry_start=None, # not used, but kept for future if needed
            entry_stop=None,  # same
        ):

        self.verbose        = verbose
        self.nb_datapoints  = nb_datapoints


    def extract_data(
            self, 
            file_path,
            tree_name,
            keys: list[str],
            ):
        r"""
        keys: (list) Contains all the keys (train, label, edge..) to lookup into the .root file 
        """
        with uproot.open(file_path) as root_file:

            root_tree   = root_file[tree_name]
            num_entries = min(root_tree.num_entries, self.nb_datapoints)
            data_dict   = root_tree.arrays(
                keys, 
                library='np', 
                entry_stop=num_entries
            )

            print("")
            print(f"Keys is the root file : \n{root_tree.keys()}\n")
            print(f"Type of each key : \n{root_tree.typenames()}\n")

        # --- Display additionnal informations --- #
        if self.verbose >= 1:
            
            for key, value in data_dict.items():
                print(f"\n[RootInterface] Key : {key}")
                #print(f"   Value (shape) : {value.shape}")
                
                if isinstance(value, np.ndarray):
                    print(f"   Value is a np.ndarray.\n   Value[0].shape : {value[0].shape}")

        print("")
        return num_entries, data_dict
    