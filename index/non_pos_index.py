# non_pos_index.py

import json
import re
from collections import defaultdict
from nltk.stem import SnowballStemmer

class NonPositionalIndex:
    def __init__(self):
        self.index = defaultdict(list)
        self.statistics = {}
        self.stemmer = SnowballStemmer("french")

    def tokenize(self, text):
        # Utilise une expression régulière pour tokenizer le texte
        tokens = re.findall(r'\w+', text.lower())
        return tokens

    def build_index(self, documents):
        for idx, doc in enumerate(documents):
            # Tokenize le titre
            title_tokens = self.tokenize(doc['title'])
            for token in title_tokens:
                # Ajoute l'index du document à la liste des documents associés au token
                self.index[token].append(idx)

    def calculate_statistics(self, documents):
        num_documents = len(documents)
        total_tokens = 0
        tokens_per_field = defaultdict(int)

        for doc in documents:
            # Tokenize le titre
            title_tokens = self.tokenize(doc['title'])
            total_tokens += len(title_tokens)

            # Calcule le nombre de tokens par champ
            for field, value in doc.items():
                if field != 'url':
                    tokens_per_field[field] += len(self.tokenize(value))

        # Calcule la moyenne des tokens par document
        avg_tokens_per_doc = total_tokens / num_documents

        self.statistics = {
            'num_documents': num_documents,
            'total_tokens': total_tokens,
            'tokens_per_field': tokens_per_field,
            'avg_tokens_per_doc': avg_tokens_per_doc
        }
        
    def stem_index(self):
        stemmed_index = defaultdict(list)
        for term, postings in self.index.items():
            stemmed_term = self.stemmer.stem(term)
            stemmed_index[stemmed_term] = postings
        with open('mon_stemmer.title.non_pos_index.json', 'w', encoding='utf-8') as file:
            json.dump(stemmed_index, file, ensure_ascii=False, indent=4)

    def write_index_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.index, file, ensure_ascii=False, indent=4)

    def write_statistics_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.statistics, file, ensure_ascii=False, indent=4)
