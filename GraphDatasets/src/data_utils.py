
import numpy as np
import torch


def convert_from_keys(data_dict, keys, index, to_tensor=False, to_types=None):
    
    feature_list = []
    for key, to_type in zip(keys, to_types):
        feature = data_dict[key][index]

        if to_tensor:
            # Get the torch type
            to_type = match_type(to_type) 

            # Convert the numpy array to a torch tensor with the asked format
            if not isinstance(feature, np.ndarray): # Some ValueError raised when dealing with np.uint8 otherwise
                feature = np.array(feature)
            feature = torch.from_numpy(feature).to(to_type)
        
        feature_list.append(feature)

    # In the case of > 1 feature, transpose is needed to store as (node, features) in the Data object
    if len(feature_list) == 1:
        features = torch.stack(feature_list, dim=0)
    else:
        features = torch.transpose(torch.stack(feature_list, dim=0), 1, 0)

    return features


def match_type(to_type: str):

    match to_type:
        case 'int16':
            torch_type = torch.int16
        case 'int32':
            torch_type = torch.int32
        case 'float16':
            torch_type = torch.float16
        case 'float32':
            torch_type = torch.float32
        case _:
            print(f"Value Error, to_type {to_type} is not supported")
            print("Add the data type into the transform or change the new target type")
            raise ValueError
        
    return torch_type
