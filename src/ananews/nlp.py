import os
import re
from typing import Union

import joblib
import numpy as np
from sklearn.decomposition import PCA
import torch
from transformers import AutoModel, AutoModelForSeq2SeqLM, AutoTokenizer


class BertWrapper:
    """
    Враппер для модели Bert для получения эмбеддингов
    """

    def __init__(self, multitask: bool = True, pca=Union[PCA, Union[os.PathLike, str]]):
        """
        :param multitask bool: if True, use multilingual model, else standard model
        The type of the pre-trained model:
        If True, then sberbank-ai/sbert_large_mt_nlu_ru downloaded
        If False, then sberbank-ai/sbert_large_nlu_ru downloaded
        """
        self.multitask = multitask
        self.model_name: str
        if self.multitask:
            self.model_name = "sberbank-ai/sbert_large_mt_nlu_ru"
        else:
            self.model_name = "sberbank-ai/sbert_large_nlu_ru"
        super().__init__()
        if isinstance(pca, str) or isinstance(pca, os.PathLike):
            self.pca = joblib.load(pca)
        else:
            self.pca = pca
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Load AutoModel from huggingface model repository
        # https://huggingface.co/sberbank-ai/sbert_large_mt_nlu_ru
        # https://huggingface.co/sberbank-ai/sbert_large_nlu_ru
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name).to(self.device)

    def _get_model_output(self, encoded_input):
        """
        Compute token embeddings

        :param encoded_input: tokenized data
        :return: embeddings (last_hidden_state, pooler_output)
        """
        encoded_input = encoded_input.to(self.device)
        with torch.no_grad():
            model_output = self.model(**encoded_input)
            return model_output

    def _mean_pooling(self, model_output, attention_mask: torch.Tensor):
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask

    def get_embedding(self, text: str) -> np.ndarray:

        encoded_input = self.tokenizer(text, padding=True, truncation=True, max_length=64, return_tensors="pt")
        model_output = self._get_model_output(encoded_input)
        sentence_embeddings = self._mean_pooling(model_output, encoded_input["attention_mask"])

        result_embedding = self.pca.transform(sentence_embeddings.detach().cpu().numpy())

        return result_embedding


class SummarizationWrapper:
    """
    NLP Model for text summarization
    """

    def __init__(
        self,
        model_name: str = "csebuetnlp/mT5_multilingual_XLSum",
    ):
        """
        :param model_name: name of model from huggingface.co
        """
        self.model_name = model_name

        # Whitespace handler taken from tutorial
        self.whitespace_handler = lambda k: re.sub(r"\s+", " ", re.sub(r"\n+", " ", k.strip()))

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Load AutoModelForSeq2SeqLM from huggingface model repository
        # https://huggingface.co/csebuetnlp/mT5_multilingual_XLSum
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name).to(self.device)

    def get_summary(self, text: str) -> str:
        """
        Get summary for text
        :param text: text for summarization
        :return: summary
        """
        input_ids = self.tokenizer(
            [self.whitespace_handler(text)], return_tensors="pt", padding="max_length", truncation=True, max_length=512
        )["input_ids"]

        input_ids = input_ids.to(self.device)

        with torch.no_grad():
            output_ids = self.model.generate(input_ids=input_ids, max_length=128, no_repeat_ngram_size=2, num_beams=4)[
                0
            ]

        output_ids = output_ids.detach().cpu().numpy()  # to numpy array

        summary = self.tokenizer.decode(output_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)

        return summary
