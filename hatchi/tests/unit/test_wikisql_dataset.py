"""Testing tokenizer for WikiSQL"""
from typing import Any, Set, Union, List
import pytest

from hatchi.preprocess.wikisql_dataset import WikiSQLTokenizer


@pytest.fixture
def setup_tokenizer() -> WikiSQLTokenizer:
    """Setting up the tokenizer object"""
    return WikiSQLTokenizer()


@pytest.mark.parametrize(
    "words, expected",
    [
        (["Born in 2002"], {"born", "0", "2", "in", " "}),
    ],
)
def test_text_preprocessor(
    setup_tokenizer: WikiSQLTokenizer, words: Union[List[str], str], expected: Set[str]
):
    """Test WikiSQL tokenizer text processor.

    Args:
        setup_tokenizer (WikiSQLTokenizer): Tokenizer object
        expected (Set[str]): Expected output
    """
    tokenizer: WikiSQLTokenizer = setup_tokenizer
    output = tokenizer.process_text(words)
    assert output == expected


@pytest.mark.parametrize(
    "words",
    [2000, 2.22, "I am glad"],
)
def test_type_preprocessor(setup_tokenizer: WikiSQLTokenizer, words: Any):
    """Test WikiSQL tokenizer text processor with invalid input types.

    Args:
        setup_tokenizer (WikiSQLTokenizer): Tokenizer object
    """
    tokenizer: WikiSQLTokenizer = setup_tokenizer
    with pytest.raises(TypeError):
        tokenizer.process_text(words)
