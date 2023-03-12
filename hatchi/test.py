from preprocess.wikisql_dataset import WikiSQLTokenizer
from datasets import load_dataset

# wiki = load_dataset("wikisql")
w = WikiSQLTokenizer()

# w.vocab_extractor(wiki).save_vocab()

print(w.process_text("Race Report"))
