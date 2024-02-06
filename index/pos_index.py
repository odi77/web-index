# pos_index.py

import json
import re
from collections import defaultdict

class PositionalIndex:
    def __init__(self):
        self.index = defaultdict(dict)

    def tokenize(self, text):
        # Utilise une expression régulière pour tokenizer le texte
        tokens = re.findall(r'\w+', text.lower())
        return tokens

    def build_index(self, documents):
        for idx, doc in enumerate(documents):
            # Tokenize le titre
            title_tokens = self.tokenize(doc['title'])
            for position, token in enumerate(title_tokens):
                # Ajoute la position du token dans le document à l'index
                if token not in self.index:
                    self.index[token] = {}
                if idx not in self.index[token]:
                    self.index[token][idx] = []
                self.index[token][idx].append(position)
                
    def calculate_statistics(self, documents):
        num_documents = len(documents)
        total_tokens = 0
        tokens_per_field = defaultdict(int)

        for doc in documents:
            title_tokens = self.tokenize(doc['title'])
            total_tokens += len(title_tokens)

            for field, value in doc.items():
                if field != 'url':
                    tokens_per_field[field] += len(self.tokenize(value))

        avg_tokens_per_doc = total_tokens / num_documents

        self.statistics = {
            'num_documents': num_documents,
            'total_tokens': total_tokens,
            'tokens_per_field': tokens_per_field,
            'avg_tokens_per_doc': avg_tokens_per_doc
        }


    def write_index_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.index, file, ensure_ascii=False, indent=4)


    def write_statistics_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.statistics, file, ensure_ascii=False, indent=4)
