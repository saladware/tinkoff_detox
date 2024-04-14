import nltk
import polars as pl
import torch
from transformers import AutoTokenizer, T5ForConditionalGeneration

nltk.download("punkt")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


tokenizer = AutoTokenizer.from_pretrained("sberbank-ai/ruT5-base")
model = T5ForConditionalGeneration.from_pretrained(
    "SkolkovoInstitute/ruT5-base-detox"
).to(device)

toxic_words = (
    pl.read_csv("toxic_vocab_extended.csv")
    .to_pandas()
    .apply(lambda x: x.strip() if isinstance(x, str) else x)["vocab"]
    .to_list()
)


def detoxify(
    text: str,
    max_tokens: int = 50,
    temperature: float = 0.7,
    top_k: int = 50,
    top_p: float = 0.95,
    penalty: float = 1.0,
    n: int = 1,
):
    # Токенизация текста и перенос на GPU
    inputs = tokenizer.encode_plus(
        text,
        return_tensors="pt",
        add_special_tokens=True,
        max_length=max_tokens,
        padding="max_length",
        truncation=True,
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Генерация ответов моделью
    outputs = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=max_tokens,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        repetition_penalty=penalty,
        num_return_sequences=n,
        do_sample=True,
    )

    detoxified_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return detoxified_text
