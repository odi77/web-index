# main.py

from index.non_pos_index import NonPositionalIndex
from index.utils import get_docs_from_json
from index.pos_index import PositionalIndex
import argparse


def main():
    parser = argparse.ArgumentParser(description='Create positional or non-positional index (default).')
    parser.add_argument('--pos_idx', action='store_true', help='Use positional index')
    args = parser.parse_args()

    file_path = 'data/crawled_urls.json'
    documents = get_docs_from_json(file_path)

    # Utilisation de l'index non positionnel par défaut
    if args.pos_idx:
        index_builder = PositionalIndex()
    else:
        index_builder = NonPositionalIndex()

    index_builder.build_index(documents)
    index_builder.calculate_statistics(documents)

    if args.pos_idx:
        index_builder.write_index_to_file('title.pos_index.json')
    else:
        index_builder.write_index_to_file('title.non_pos_index.json')
        # Création d'un nouvel index avec le stemming
        index_builder.stem_index()

    index_builder.write_statistics_to_file('metadata.json')

if __name__ == "__main__":
    main()
