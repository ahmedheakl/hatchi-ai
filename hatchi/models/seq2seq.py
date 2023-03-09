"""Implementation for the Seq2Seq model using LSTM"""
from typing import TypeVar
import os
import torch
from torch import nn

WikiData = TypeVar("WikiData", bound="WikiSQLDatasetFactory")
_DEVICE = os.environ["TRAIN_DEVICE"]


class WikiSQLDatasetFactory:
    """Dataset factory for WikiSQL.

    It implements a pipeline for preprocessing and transforming
    WikiSQL to the desired format.
    """

    def __init__(self, dataset) -> None:
        self.dataset = dataset

    def preprocess(self: WikiData) -> WikiData:
        """Preprocess WikiSQL dataset from training"""
        return self


class Encoder(nn.Module):
    """Implementation for Seq2Seq decoder"""

    def __init__(self, input_size: int, hidden_size: int, num_layers: int) -> None:
        super().__init__()

    def forward(self, input_query: torch.Tensor) -> torch.Tensor:
        """Forward pass through the decoder network"""
        return input_query
