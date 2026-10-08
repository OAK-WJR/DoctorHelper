#!/usr/local/bin/python3
from transformers import T5ForConditionalGeneration, T5Tokenizer
import re
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

def run(input_text):
    def initialize_model_and_tokenizer():
        MODEL_NAME = 't5-small'
        tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME, model_max_length=512, legacy=False)
        model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)
        return model, tokenizer

    model, tokenizer = initialize_model_and_tokenizer()

    def split_into_sentences(text, max_chunk_size=400):
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = ""
        current_length = 0

        for sentence in sentences:
            if current_length + len(sentence) <= max_chunk_size:
                current_chunk += " " + sentence
                current_length += len(sentence)
            else:
                chunks.append(current_chunk)
                current_chunk = sentence
                current_length = len(sentence)

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

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

    def generate_summary(input_text, max_chunk_size=480):
        target_length = len(input_text) // 3
        while len(input_text) > target_length:
            input_text_chunks = split_into_sentences(input_text, max_chunk_size)

            combined_output = ''
            for chunk in input_text_chunks:
                input_ids = tokenizer.encode('summarize: ' + chunk, return_tensors='pt', truncation=True, max_length=512)
                output_ids = model.generate(input_ids, max_length=150, num_beams=5, length_penalty=1.3)
                chunk_output = tokenizer.decode(output_ids[0], skip_special_tokens=True)
                combined_output += chunk_output + ' '

            input_text = combined_output

        return remove_redundant_sentences(input_text.strip())

    result = generate_summary("medical summary:" + input_text)
    print(result)
    return result
