# backend/app/ml/annotation.py
import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_name = "dmis-lab/biobert-base-cased-v1.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name).to(device).eval()

options_df = pd.read_excel("backend/app/ml/data/unique_values.xlsx")
column_options = {
    col: options_df[col].dropna().astype(str).unique().tolist()
    for col in options_df.columns
}

def get_embeddings_batch(text_list):
    tokens = tokenizer(text_list, return_tensors="pt", truncation=True,
                       padding=True, max_length=512).to(device)
    with torch.no_grad():
        outputs = model(**tokens)
        embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings

column_embeddings = {
    col: get_embeddings_batch(opts)
    for col, opts in column_options.items()
}

default_fields = {
    "Name": "",
    "Genome Location": "",
    "Tier": 1,
    "Hallmark": "no",
    "Chr Band": "",
    "Somatic": "no",
    "Germline": "no",
    "Tissue Type": "Epithelial",
    "Molecular Genetics": "Dominant",
    "Mutation Types": "D",
    "Other Germline Mut": "no",
    "Synonyms": ""
}

def get_embedding(text):
    tokens = tokenizer(text, return_tensors="pt", truncation=True,
                       padding=True, max_length=512).to(device)
    with torch.no_grad():
        embedding = model(**tokens).last_hidden_state.mean(dim=1)
    return embedding

def get_best_match(paragraph_embedding, option_embs, options):
    similarities = torch.nn.functional.cosine_similarity(
        paragraph_embedding, option_embs, dim=1)
    best_idx = similarities.argmax().item()
    return options[best_idx]

def extract_semantic_fields(input_json: dict) -> list:
    paragraphs = input_json.get("biology_paragraphs", [])
    if not paragraphs:
        return [default_fields.copy()]

    results = []
    for paragraph in paragraphs:
        paragraph_embedding = get_embedding(paragraph)
        entry = default_fields.copy()
        entry["Name"] = input_json.get("Name", "")
        entry["Synonyms"] = input_json.get("Synonyms", "")
        for column, options in column_options.items():
            if column in default_fields and options:
                best_match = get_best_match(paragraph_embedding, column_embeddings[column], options)
                entry[column] = best_match
        results.append(entry)
    return results


