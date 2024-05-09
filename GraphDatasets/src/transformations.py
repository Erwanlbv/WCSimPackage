
import numpy as np
import torch

import omegaconf
from omegaconf import OmegaConf

import torch_geometric
from torch_geometric.data import Data
from torch_geometric.data.datapipes import functional_transform
from torch_geometric.transforms import BaseTransform
from torch_geometric.utils import to_undirected


"""
This file should contain all the callables (i.e python functions or class with a __call__ attribut) 
used for creating graph datasets.

"""

# À FAIRE : 
# 14/02 :  - Mettre à jour la doc de Normalize

class Normalize(torch.nn.Module):
    """Normalize a torch_geometric Data object with mean and standard deviation.
    Given mean: ``(mean[1],...,mean[n])`` and std: ``(std[1],..,std[n])`` for ``n``
    channels, this transform will normalize each channel of the input
    ``torch.*Tensor`` i.e.,
    ``output[channel] = (input[channel] - mean[channel]) / std[channel]``

    .. note::
        This transform acts out of place, i.e., it does not mutate the input tensor.

    Args:
        mean (sequence): Sequence of means for each channel.
        std (sequence): Sequence of standard deviations for each channel.
        inplace(bool,optional): Bool to make this operation in-place.

    """

    def __init__(
            self, 
            feat_norm,
            label_norm=None, 
            eps=1e-12, 
            inplace=False        
    ):
        
        super().__init__()
        
        self.feat_norm  = feat_norm
        self.label_norm = label_norm
        self.eps        = eps
        self.inplace    = inplace
        
        # For hydra compatibility
        if isinstance(self.feat_norm, omegaconf.listconfig.ListConfig):
            self.feat_norm = OmegaConf.to_container(self.feat_norm)
            if self.label_norm is not None:
                self.label_norm = OmegaConf.to_container(self.label_norm)

        # Need to convert list to torch tensor to perform addition & subtraction
        self.feat_norm = torch.tensor(self.feat_norm)
        if self.label_norm is not None:
            self.label_norm = torch.tensor(self.label_norm)


    def forward(self, data):
        """
        self.feat_norm and self.label_norm must contain Tensor object
        """
        
        data.x = (data.x - self.feat_norm[1]) / (self.feat_norm[0] - self.feat_norm[1] + self.eps)
        
        if self.label_norm is not None:
            data.y = (data.y - self.label_norm[1]) / (self.label_norm[0] - self.label_norm[1] + self.eps)

        return data


# In the futur : Standardize ?