import argparse
import wandb
from pathlib import Path
from language_model.NER.dataset import TokenClassificationDataset
from language_model.NER.malfong import Malfong
from language_model.NER.XLM_RoBERTa import XLMRoBERTa
from language_model.lib.log import get_logger
from transformers import AutoTokenizer

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--data_dir", type=str, help="Data directory for storing the expirement", default="./data")
parser.add_argument(
    "--run_name", type=str, help="Name the model run . Defaults to icelandic-model", default="icelandic-model"
)
parser.add_argument(
    "--local_rank", type=int, help="Local rank. Necessary for using the torch.distributed.launch utility.", default=-1
)

argv = parser.parse_args()

data_dir = argv.data_dir
run_name = argv.run_name
local_rank = argv.local_rank

logger = get_logger(__file__)

logger.info(f"Starting run: {run_name}")


wandb.login()

data_dir = Path(f"{data_dir}") / run_name
data_dir.mkdir(parents=True, exist_ok=True)
dataset_filename = "malfong_ner.txt"

malfong = Malfong(data_dir)
malfong.download()

max_seq_length = 128
tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")
dataset = TokenClassificationDataset(data_dir / dataset_filename, tokenizer, max_seq_length)
model = XLMRoBERTa(data_dir, dataset=dataset)


model.train()
