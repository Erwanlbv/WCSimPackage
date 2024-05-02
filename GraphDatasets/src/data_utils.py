
import numpy as np
import torch

def squeeze_and_convert(data_dict, keys, index, to_tensor, to_type=torch.float32):
    
    feature_list = []
    for key in keys:
        feature = data_dict[key][index]
        feature_list.append(feature)
            
    features = np.transpose(np.squeeze(np.array(feature_list)))
    if to_tensor:
        features = torch.from_numpy(features) if len(features.shape) >= 1 else torch.tensor(features)
        features = features.to(to_type)

    return features

    #fct with data vector and the actual config extremal_config_vlaue
    #take the extremal.dict and replace if min 