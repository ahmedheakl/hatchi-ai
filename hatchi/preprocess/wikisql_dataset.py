"""Implementation of WikiSQL dataset preprocessors"""
from typing import Dict, Set, List, TypeVar, NamedTuple
import logging
import re

from datasets.dataset_dict import DatasetDict

_LOG = logging.getLogger(__name__)
WikiTokenizer = TypeVar("WikiTokenizer", bound="WikiSQLTokenizer")


class Accessors(NamedTuple):
    """Accessor names for the database"""

    table: str = "table"
    table_cols: str = "headers"
    table_name: str = "name"
    sql: str = "sql"
    sql_readable: str = "human_readable"
    question: str = "question"


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
            " ": 4,
        }
        self._vocab_size = 5

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
            split_words = re.sub(puncs_pattern, " ", word)
            split_words = re.sub(pattern, " ", split_words).split(" ")

            for clean_word in split_words:
                if clean_word.isdigit() and not clean_word.isalpha():
                    processed_words.add(clean_word[0])

                else:
                    processed_words.add(re.sub(pattern, "", clean_word))

            for punc in punc_marks:
                processed_words.add(punc)

        if "" in processed_words:
            processed_words.remove("")

        return processed_words

    def add_to_vocab(self, word: str) -> None:
        """Add word to tokenizer vocabulary"""
        if self._vocab.get(word, -1) != -1:
            return

        self._vocab[word] = self._vocab_size
        self._vocab_size += 1

    def vocab_extractor(self: WikiTokenizer, dataset: DatasetDict) -> WikiTokenizer:
        """Load the dataset to extract vocabulary

        Args:
            dataset (DatasetDict): Dataset to extract vocabulary from
        """
        # Add table column names
        for split in dataset:
            for entry in split:
                for words in entry[self._opt.table][self._opt.table_cols]:
                    for word in self.process_text(words):
                        self.add_to_vocab(word)

                # Adding table name, sql query, and the given
                self.add_to_vocab(
                    self.process_text(
                        entry[self._opt.table][self._opt.table_name],
                    )
                )
                self.add_to_vocab(
                    self.process_text(
                        entry[self._opt.sql][self._opt.sql_readable],
                    )
                )
                self.add_to_vocab(
                    self.process_text(
                        entry[self._opt.question],
                    )
                )

        return self
