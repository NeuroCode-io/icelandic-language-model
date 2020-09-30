import os
from pathlib import Path


class Tokenizer:
    def __init__(self, tokenizer, data_dir=""):
        if data_dir:
            self.data_dir = data_dir
        else:
            self.data_dir = f"{os.getcwd()}/data"

        print(self.data_dir)
        self.tokenizer = tokenizer

    def is_local_store(self):
        return os.path.exists(f"{self.data_dir}/icelandic/vocab.json")

    def train(self):
        if self.is_local_store():
            return

        paths = [str(x) for x in Path(self.data_dir).glob("*.txt")]

        self.tokenizer.train(
            files=paths,
            vocab_size=52_000,
            min_frequency=2,
            special_tokens=[
                "<s>",
                "<pad>",
                "</s>",
                "<unk>",
                "<mask>",
            ],
        )

        Path(f"{self.data_dir}/icelandic").mkdir(parents=True, exist_ok=True)

        self.tokenizer.save_model(f"{self.data_dir}/icelandic")