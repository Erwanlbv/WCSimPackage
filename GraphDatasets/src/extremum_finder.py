import numpy as np
import torch
import pprint


class ExtremumFinder:
    r"""

    Class for finding and comparing extremum values of features in a dataset. 
    The names used at initialization must be the same ones called in compute_extremum. 

    Args:
        **kwargs: Arbitrary keyword arguments representing keys and corresponding data types.
        """
    
    def __init__(
            self,
            **kwargs
    ):

        self.keys = kwargs #dictionary of all keys
        self.all_extremum_keys={key: {} for key in kwargs} #dictionary for final extrema values

    def compare_extremum(self, data_torch, keys_list, extremum_key_value):
        r"""
        Compares extremum values of features between the previous events and the current one.

        Args:
            data_torch (torch.Tensor or np.ndarray): tensor or array.
            keys_list (list): List of keys representing features.
            extremum_key_value (dict): Dictionary containing extremum values for the keys.

        Returns:
            dict: Updated dictionary containing extremum values for the keys.
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
                #We consider that everything will be tensor for now,
                #but we keep the ndarray support for futur
                
                else:
                     print('The given object is not a torch tensor')

                if key not in extremum_key_value:
                    extremum_key_value[key] = {'min': x_min, 'max': x_max}
                    
                if x_min < extremum_key_value[key]['min']:
                    extremum_key_value[key]['min'] = x_min
                if x_max > extremum_key_value[key]['max']:
                    extremum_key_value[key]['max'] = x_max

        return extremum_key_value

    def compute_extremum(self, **data_torch):
        r"""
        Computes extremum values for the dataset.

        Args:
            **data_torch: Arbitrary keyword arguments representing data tensors.

        Returns:
            dict: A dictionary containing extremum values for each key.
        """

        if len(data_torch) != len(self.keys):
                    print("Error: Number of arguments to monitor is not the same than in the init.")
                    print(f"Error: Given argument {data_torch} against \n{self.keys}.")
                    return
    
        for key_name, key_type in self.keys.items():  
            self.all_extremum_keys[key_name] = self.compare_extremum(data_torch[key_name], key_type, self.all_extremum_keys[key_name])
            
        return self.all_extremum_keys

    def print_extremum(self):
        """
        Prints extremum values for the keys.
        """
        for key_name, type_key in self.all_extremum_keys.items():
            print(f'{key_name.upper()} KEYS EXTREMUM:')
            for key, value in type_key.items():
                print(f"\t{key}:")
                print(f"\t \tMinimum: {value['min']:.2f}")
                print(f"\t \tMaximum: {value['max']:.2f}")