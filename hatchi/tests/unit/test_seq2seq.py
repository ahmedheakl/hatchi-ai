"""Testing implementation for seq2seq model"""
import os
import pytest
import torch

from hatchi.models.seq2seq import Encoder, Decoder, Seq2Seq


@pytest.fixture
def setup_train_device():
    """Setting up training device"""
    os.environ["DEVICE"] = "cpu"


@pytest.mark.parametrize("dropout_ratio", [-1.2, 20.0])
@pytest.mark.parametrize("model", [Encoder, Decoder])
def test_dropout_ratio_bigger_out_of_range(dropout_ratio, model):
    """Testing if the model throws an assertion error if the value of dropout
    parameter is less than zero or bigger than one
    """
    hidden_size, vocab_size, embedding_size, num_layers = 256, 2000, 128, 2
    with pytest.raises(AssertionError):
        model(vocab_size, hidden_size, embedding_size, num_layers, dropout_ratio)


@pytest.mark.parametrize("model", [Encoder, Decoder])
def test_encoder_layers_is_positive(model):
    """Testing if the model throws an assertion error if the value of `num_layers`
    parameter is less than zero or bigger than one
    """
    hidden_size, vocab_size, embedding_size, dropout_ratio = 256, 2000, 128, 0.2
    with pytest.raises(AssertionError):
        model(vocab_size, hidden_size, embedding_size, 0, dropout_ratio)


def test_encoder_input_type():
    """Testing if the model throws a type error if the input query is not a tensor"""
    hidden_size, vocab_size, embedding_size, num_layers = 256, 2000, 128, 2
    input_query = [1, 2, 3]
    encoder = Encoder(vocab_size, hidden_size, embedding_size, num_layers)
    with pytest.raises(TypeError):
        encoder(input_query)


def test_encoder_output_dim():
    """Testing a correct output shape from the encoder"""
    hidden_size, vocab_size, embedding_size, num_layers = 256, 2000, 128, 2
    batch_size, seq_len = 14, 4
    input_query = torch.zeros(seq_len, batch_size, dtype=torch.int32)
    encoder = Encoder(vocab_size, hidden_size, embedding_size, num_layers)
    hidden, cell = encoder(input_query)
    assert hidden.shape == torch.Size([num_layers, batch_size, hidden_size])
    assert cell.shape == torch.Size([num_layers, batch_size, hidden_size])


@pytest.mark.parametrize(
    "query, hidden, cell",
    [
        ([1, 2], torch.zeros(1), torch.zeros(1)),
        (torch.zeros(1), [1, 2], torch.zeros(1)),
        (torch.zeros(1), torch.zeros(1), [1, 2]),
    ],
)
def test_decoder_input_type(query, hidden, cell):
    """Testing if the model throws a type error if the inputs is not
    of a tensor type"""
    hidden_size, vocab_size, embedding_size, num_layers = 256, 2000, 128, 2
    decoder = Decoder(hidden_size, embedding_size, vocab_size, num_layers)
    with pytest.raises(TypeError):
        decoder(query, hidden, cell)


def test_decoder_output_dim():
    """Testing the output dimension of the decoder model"""
    hidden_size, vocab_size, embedding_size, num_layers = 256, 2000, 128, 2
    batch_size = 14
    input_tensor = torch.zeros(batch_size, dtype=torch.int32)
    hidden = torch.zeros(num_layers, batch_size, hidden_size)
    cell = torch.zeros(num_layers, batch_size, hidden_size)
    decoder = Decoder(vocab_size, hidden_size, embedding_size, num_layers)
    preds, hidden, cell = decoder(input_tensor, hidden, cell)
    assert preds.shape == torch.Size([batch_size, vocab_size])
    assert hidden.shape == torch.Size([num_layers, batch_size, hidden_size])
    assert cell.shape == torch.Size([num_layers, batch_size, hidden_size])


@pytest.mark.parametrize("teacher_forcing_ratio", [-2, 5.0])
def test_teacher_forcing_range(teacher_forcing_ratio):
    """Testing wether the model will throw an assertion error if the value of
    the teacher forcing ratio is bigger than one or low than zero"""
    hidden_size, vocab_size, embedding_size, num_layers = 256, 2000, 128, 2
    batch_size, seq_len = 14, 4
    source = torch.zeros(seq_len, batch_size, dtype=torch.int32)
    target = torch.zeros(seq_len, batch_size, dtype=torch.int32)
    encoder = Encoder(vocab_size, hidden_size, embedding_size, num_layers)
    decoder = Decoder(vocab_size, hidden_size, embedding_size, num_layers)
    seq2seq_model = Seq2Seq(encoder, decoder, vocab_size)
    with pytest.raises(AssertionError):
        seq2seq_model(source, target, teacher_forcing_ratio)


def test_seq2seq_output_dim(setup_train_device):
    """Testing the output dimension of the Seq2Seq Model"""
    hidden_size, vocab_size, embedding_size, num_layers = 256, 2000, 128, 2
    batch_size, seq_len = 14, 4
    source = torch.zeros(seq_len, batch_size, dtype=torch.int32)
    target = torch.zeros(seq_len, batch_size, dtype=torch.int32)
    encoder = Encoder(vocab_size, hidden_size, embedding_size, num_layers)
    decoder = Decoder(vocab_size, hidden_size, embedding_size, num_layers)
    seq2seq_model = Seq2Seq(encoder, decoder, vocab_size)
    outputs = seq2seq_model(source, target)

    assert outputs.shape == torch.Size([seq_len, batch_size, vocab_size])
