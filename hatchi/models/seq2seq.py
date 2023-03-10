"""Implementation for the Seq2Seq model using LSTM"""
from typing import Tuple
from random import random
import os
import torch
from torch import nn

_DEVICE = os.environ["TRAIN_DEVICE"]


class Encoder(nn.Module):
    """Implementation for Seq2Seq decoder"""

    def __init__(
        self,
        hidden_size: int,
        embedding_dim: int,
        vocab_size: int,
        num_layers: int,
        dropout_ratio: float = 0.5,
    ) -> None:
        super().__init__()
        self.embedding = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=embedding_dim,
        )
        self.dropout = nn.Dropout(dropout_ratio)
        self.lstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout_ratio,
        )

    def forward(self, input_query: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Forward pass through the decoder network

        Input query dim = [seq_len, batch_size]

        Note that the input tensors are assumed to be set to the desired device.

        Args:
            input_query (torch.Tensor): Natural language of the query as a tensor of words
            represented as indices.
            database_schema (torch.Tensor): Schema structure written in SQL for the database
            to be queried.

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: Hidden and cell gate vectors representing the latent
            dim. Both have the same dimension [num_layers, batch_size, hidden_size]
        """
        # Embedding shape = [seq_len, batch_size, embedding_dim]
        embedding = self.dropout(self.embedding(input_query))

        _, (hidden, cell) = self.lstm(embedding)

        return hidden, cell


class Decoder(nn.Module):
    """Implementation for Seq2Seq Decoder"""

    def __init__(
        self,
        vocab_size: int,
        hidden_size: int,
        embedding_size: int,
        num_layers: int,
        dropout_ratio: float = 0.5,
    ) -> None:
        super().__init__()
        self.dropout = nn.Dropout(dropout_ratio)
        self.embedding = nn.Embedding(vocab_size, embedding_size)
        self.lstm = nn.LSTM(
            embedding_size,
            hidden_size,
            num_layers=num_layers,
            dropout=dropout_ratio,
        )
        self.out = nn.Linear(hidden_size, vocab_size)

    def forward(
        self,
        input_tensor: torch.Tensor,
        hidden: torch.Tensor,
        cell: torch.Tensor,
    ) -> Tuple[torch.Tensor, ...]:
        """Forward pass through the decoder network

        Args:
            input_tensor (torch.Tensor): Input text as a tensor with dimension [N,]
            hidden (torch.Tensor): Hidden tensor
            cell (torch.Tensor): Cell gate tensor

        Returns:
            Tuple[torch.Tensor, ...]: (prediction scores for the output word, hidden tensor,
            cell gate tensor)
        """
        # Conver the dimension from [N, ] to [1, N] meaning a seq_len=1
        input_tensor = input_tensor.unsqueeze(0)

        # Embedding dim = [1, N, embedding_dim]
        embedding = self.dropout(self.embedding(input_tensor))

        # Output dim = [1, N, hidden_size]
        output, (hidden, cell) = self.lstm(embedding, (hidden, cell))

        # Predictions dim = [1, N, vocab_size]
        predictions: torch.Tensor = self.out(output)

        # We need to remove the seq_len dimension -> [N, vocab_size]
        predictions = predictions.squeeze(0)

        return predictions, hidden, cell


class Seq2Seq(nn.Module):
    """Implementation for the Seq2Seq model"""

    def __init__(self, encoder: Encoder, decoder: Decoder, vocab_size: int) -> None:
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.vocab_size = vocab_size

    def forward(
        self,
        source: torch.Tensor,
        target: torch.Tensor,
        teacher_forcing_ratio: float = 0.5,
    ) -> torch.Tensor:
        """Forward pass through the Seq2Seq model

        Args:
            source (torch.Tensor): Source text which is the natural language query
            concatenated with the database schema
            target (torch.Tensor): Target text which is the SQL query
            teacher_forcing_ratio (float, optional): Ratio of picking the last output as an input
            for the next stage for decoding. Defaults to 0.5.

        Returns:
            torch.Tensor: Word outputs with dim [target_len, N, vocab_size]
        """
        batch_size = source.size(1)
        target_len = target.size(0)

        outputs = torch.zeros(target_len, batch_size, self.vocab_size).to(_DEVICE)

        hidden, cell = self.encoder(source)

        # Since the source starts with <SOS> token, we are setting the first token
        # input to decoder to <SOS>. Output dim = [N,]
        output: torch.Tensor = target[0]

        for word_t in range(1, target_len):
            # Output dim = [N, vocab_size]
            output, hidden, cell = self.decoder(output, hidden, cell)
            outputs[word_t] = output

            # Best word dim = [N, ]
            best_word = output.argmax(1)

            # With probability of teacher_force_ratio we take the actual next word
            # otherwise we take the word that the Decoder predicted
            output = target[word_t] if random() < teacher_forcing_ratio else best_word

        return outputs
