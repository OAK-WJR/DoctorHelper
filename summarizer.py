#!/usr/bin/env python3
"""Summarize English text with the t5-small model, a few sentences at a time."""
import re
import nltk
from nltk.tokenize import sent_tokenize
from transformers import T5ForConditionalGeneration, T5Tokenizer

MODEL_NAME = 't5-small'
PREFIX = 'medical summary:'
MAX_ROUNDS = 5

try:
    sent_tokenize("Test.")
except LookupError:
    for resource in ('punkt', 'punkt_tab'):  # older and newer NLTK use different names
        nltk.download(resource, quiet=True)

tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME, model_max_length=512, legacy=False)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

def split_into_sentences(text, max_chunk_size=400):
    """Group whole sentences into chunks of about max_chunk_size characters; a longer sentence is a chunk of its own."""
    chunks = []
    current_chunk = ""
    for sentence in sent_tokenize(text):
        if current_chunk and len(current_chunk) + len(sentence) > max_chunk_size:
            chunks.append(current_chunk)
            current_chunk = sentence
        else:
            current_chunk = (current_chunk + " " + sentence).strip()
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def summarize_chunk(chunk):
    input_ids = tokenizer.encode('summarize: ' + chunk, return_tensors='pt', truncation=True, max_length=512)
    output_ids = model.generate(input_ids, max_length=150, num_beams=5, length_penalty=1.3)
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

def remove_redundant_sentences(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    unique_tokens = set()
    unique_sentences = []

    for sentence in sentences:
        tokens = frozenset(sentence.split())
        if tokens not in unique_tokens:
            unique_tokens.add(tokens)
            unique_sentences.append(sentence)

    return " ".join(unique_sentences)

def run(input_text, max_chunk_size=480):
    """Summarize round after round until the text is a third of its length: at most MAX_ROUNDS rounds,
    stopping early when a round makes it no shorter."""
    if not input_text.strip():
        return ""
    text = PREFIX + input_text
    target_length = len(text) // 3
    for _ in range(MAX_ROUNDS):
        if len(text) <= target_length:
            break
        shorter = " ".join(summarize_chunk(chunk) for chunk in split_into_sentences(text, max_chunk_size))
        if len(shorter) >= len(text):  # the model cannot make it any shorter
            break
        text = shorter
    if text.startswith(PREFIX):
        text = text[len(PREFIX):]
    return remove_redundant_sentences(text.strip())
