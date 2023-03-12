"""Implementation of WikiSQL dataset preprocessors"""
from typing import Dict, Set, List, TypeVar, NamedTuple, Union
from pathlib import Path
import logging
import json
import re
from datasets.dataset_dict import DatasetDict

_LOG = logging.getLogger(__name__)
WikiTokenizer = TypeVar("WikiTokenizer", bound="WikiSQLTokenizer")


class Accessors(NamedTuple):
    """Accessor names for the database"""

    table: str = "table"
    table_cols: str = "header"
    table_name: str = "name"
    sql: str = "sql"
    sql_readable: str = "human_readable"
    question: str = "question"
    folder_path: Path = Path(__file__).parent.resolve()


class WikiSQLTokenizer:
    """
    Wikisql dataset tokenizer
    """

    sos_token = "<sos>"
    eos_token = "<eos>"
    pad_token = "<pad>"
    unk_token = "<unk>"
    scheme_start_token = "<sch>"
    scheme_end_token = "</sch>"

    def __init__(self) -> None:
        self._opt = Accessors()
        self._vocab: Dict[str, int] = {
            self.sos_token: 0,
            self.eos_token: 1,
            self.pad_token: 2,
            self.unk_token: 3,
            self.scheme_start_token: 4,
            self.scheme_end_token: 5,
            " ": 6,
        }
        self._vocab_size = 7

    @property
    def vocab_size(self) -> int:
        """Retrieve vocab size"""
        return self._vocab_size

    @vocab_size.setter
    def vocab_size(self, _) -> None:
        raise AttributeError("Vocab size cannot be modified")

    def get_sos_index(self) -> int:
        """Getter for index of SOS token"""
        return self._vocab[self.sos_token]

    def get_eos_index(self) -> int:
        """Getter for index of EOS token"""
        return self._vocab[self.eos_token]

    def get_pad_index(self) -> int:
        """Getter for index of PAD token"""
        return self._vocab[self.pad_token]

    def get_unk_index(self) -> int:
        """Getter for index of UNK token"""
        return self._vocab[self.unk_token]

    def get_index(self, word: str) -> int:
        """Retrieve index of the word"""
        return self._vocab[word]

    def process_text(self, words: List[str]) -> Set[str]:
        """Process text by:
        1. Lowercasing
        2. Removing punctuation and special characters (except '?', '.' , ',', '"', "'",
        and mathmatical operations)
        3. Splitting words which are concatnated with punctuation marks/mathematical
        operations

        Returns:
            Set[str]: Set of processed words
        """
        try:
            assert isinstance(words, list)

        except AssertionError as exc:
            _LOG.error("Input must be list")
            raise TypeError() from exc

        # Match all special chars except space
        pattern = r"(?!([a-z]|[0-9]|(\ )))."

        # Pattern to match all mentioned punctuation marks
        puncs_pattern = (
            r"[(\,)|(\.)|(\?)|(\")|(\')|(\=)|(\*)|(\+)|(\/)|(\-)|(\ )|(\;)|(\))|(\())]"
        )
        processed_words = set()

        for word in words:
            word = word.lower()
            punc_marks = re.findall(puncs_pattern, word)
            unsplitted_words = re.sub(puncs_pattern, " ", word)
            split_words = re.sub(pattern, " ", unsplitted_words).split(" ")

            for clean_word in split_words:
                if clean_word.isdigit() and not clean_word.isalpha():
                    nums = list(clean_word)
                    for num in nums:
                        processed_words.add(num)

                else:
                    processed_words.add(re.sub(pattern, "", clean_word))

            for punc in punc_marks:
                processed_words.add(punc)

        if "" in processed_words:
            processed_words.remove("")

        return processed_words

    def add_to_vocab(self, words: Union[List[str], Set[str]]) -> None:
        """Add word to tokenizer vocabulary"""
        if isinstance(words, str):
            if self._vocab.get(words, -1) != -1:
                return

            self._vocab[words] = self._vocab_size
            self._vocab_size += 1

        for word in words:
            self._vocab[word] = self._vocab_size
            self._vocab_size += 1

    def vocab_extractor(self: WikiTokenizer, dataset: DatasetDict) -> WikiTokenizer:
        """Load the dataset to extract vocabulary

        Args:
            dataset (DatasetDict): Dataset to extract vocabulary from
        """
        # Add table column names
        for split in dataset:
            for entry in dataset[split]:
                processed_columns_names = self.process_text(
                    entry[self._opt.table][self._opt.table_cols]
                )

                self.add_to_vocab(processed_columns_names)

                self.add_to_vocab(
                    self.process_text(
                        [entry[self._opt.table][self._opt.table_name]],
                    )
                )
                self.add_to_vocab(
                    self.process_text(
                        [entry[self._opt.sql][self._opt.sql_readable]],
                    )
                )
                self.add_to_vocab(
                    self.process_text(
                        [entry[self._opt.question]],
                    )
                )

        return self

    def save_vocab(self) -> None:
        """Save WikiSQL tokenizer vocab as a json file in the same directory."""
        with open(
            self._opt.folder_path / "wikisql_vocab.json", "w", encoding="utf-8"
        ) as file:
            json.dump(self._vocab, file)
            _LOG.debug("Vocab saved in %s", self._opt.folder_path.absolute())

    def load_vocab(self, vocab_dir: Path) -> None:
        """Load WikiSQL tokenizer vocab from provided directory"""

        try:
            with open(vocab_dir, encoding="utf-8") as file:
                _LOG.debug("Loaded vocab from %s", vocab_dir)
                self._vocab = json.load(file)

        except FileNotFoundError as exc:
            raise FileNotFoundError(f"File {vocab_dir} doesn't exist!") from exc

    def wikisql_parser(self, data_row: str) -> List[int]:
        """Parses input soruce/target data into vector of mapped tokens
        indicies from the tokenizer's vocab with a constant
        output size of 512 tokens for the source query and 64 for SQL query.

        Args:
            data_row (str): input row of data

        Returns:
            List[int]: list of parsed tokens mapped from the tokenizer's vocab
        """
        _ = data_row
        return []
