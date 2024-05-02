import numpy as np
import torch
import pprint


class ExtremaFinder:
    r"""

    Class for finding the extrema values of a set of tensors
    The keywords used at initialization must be the same ones called in compute_extrema. 

    Args:
        **kwargs: Arbitrary keyword arguments representing keys and corresponding tensors.
    """
    
    def __init__(
            self,
            **kwargs
    ):

        self.keys = kwargs #dictionary of all keys
        self.all_extrema_keys={key: {} for key in kwargs} #dictionary for final extrema values

    def compare_extrema(self, data_torch, keys_list, extrema_key_value):
        r"""
        Compares extrema values of features between the previous events and the current one.

        Args:
            data_torch (torch.Tensor or np.ndarray): tensor or array.
            keys_list (list): List of keys representing features.
            extrema_key_value (dict): Dictionary containing extrema values for the keys.

        Returns:
            dict: Updated dictionary containing extrema values for the keys.
        """
        for column, key in enumerate(keys_list):
                if isinstance(data_torch, torch.Tensor):
                    if data_torch.dim() == 0:
                        # Handle scalar tensor
                        x_min = data_torch.item()
                        x_max = data_torch.item() 
                    elif data_torch.dim() == 2:
                        # Handle 2-dimensional tensor (example tensor[hits, features])
                        x_min = torch.min(data_torch[:,column]).item()
                        x_max = torch.max(data_torch[:,column]).item()
                    else:
                        print(f"Input tensor {data_torch} of incorrect dimension, ") 
                        print(f'input dimension {data_torch.dim()} for expected dimension 0 or 2') 

                # elif isinstance(data_torch, np.ndarray):
                #     x_min = np.min(data_torch[:,column])
                #     x_max = np.max(data_torch[:,column])
                # We consider that everything will be tensor for now,
                # but we keep the ndarray support for future
                
                else:
                     print('The given object is not a torch tensor')

                if key not in extrema_key_value:
                    extrema_key_value[key] = {'min': x_min, 'max': x_max}
                    
                if x_min < extrema_key_value[key]['min']:
                    extrema_key_value[key]['min'] = x_min
                if x_max > extrema_key_value[key]['max']:
                    extrema_key_value[key]['max'] = x_max

        return extrema_key_value

    def compute_extrema(self, **data_torch):
        r"""
        Computes extrema values for the set of tensors.

        Args:
            **data_torch: Same keywords arguments than in initialization representing the tensors.

        Returns:
            dict: A dictionary containing extrema values for each key.
        """

        if len(data_torch) != len(self.keys):
                    print("Error: Number of arguments to monitor is not the same than in the init.")
                    print(f"Error: Given argument {data_torch} against \n{self.keys}.")
                    return
    
        for key_name, key_type in self.keys.items():  
            self.all_extrema_keys[key_name] = self.compare_extrema(data_torch[key_name], key_type, self.all_extrema_keys[key_name])
            
        return self.all_extrema_keys

    def print_extrema(self):
        """
        Prints extrema values for the keys.
        """
        for key_name, type_key in self.all_extrema_keys.items():
            print(f'{key_name.upper()} KEYS EXTREMA:')
            for key, value in type_key.items():
                print(f"\t{key}:")
                print(f"\t \tMinimum: {value['min']:.2f}")
                print(f"\t \tMaximum: {value['max']:.2f}")