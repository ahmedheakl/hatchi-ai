from typing import Dict
from datasets.dataset_dict import DatasetDict

import re
import json


class WikiSQLTokenizer:
    """
    Wikisql dataset tokenizer
    """

    sos_token = "<sos>"
    eos_token = "<eos>"
    pad_token = "<pad>"
    unk_token = "<unk>"

    def __init__(self) -> None:
        self._vocab: Dict[str, int] = {
            self.sos_token: 0,
            self.eos_token: 1,
            self.pad_token: 2,
            self.unk_token: 3,
        }

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

    def vocab_extractor(self, dataset: DatasetDict) -> None:
        """Load the dataset to extract vocabulary

        Args:
            dataset (DatasetDict): Dataset to extract vocabulary from
        """
        replace_slash = r"(\/)"

        # e['table']['header'] -> list
        # e[sql][human_readable] -> split by white spaces
        for split in dataset:
            for entry in split:
                for word in entry["table"]["header"]:
                    entry["table"]["header"].extend(word.split("/"))
