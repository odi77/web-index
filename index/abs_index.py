import string
import requests
import re
import logging
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import nltk
nltk.download('stopwords')


# Define a dictionary mapping types to their corresponding values
TYPES = {
    "title": 'title',
    "header": [f'h{i}' for i in range(1, 7)],
    "paragraph": 'p'
}


class AbstractIndex(ABC):
    """
    An abstract base class for implementing document indexing.

    This class serves as a blueprint for specific indexing implementations. It defines common attributes
    and methods that can be utilized by subclasses to manage document indexing. Subclasses are expected to
    implement specific logic for creating indexes based on the provided URLs and type.

    Parameters
    ----------
    index : dict, optional
        Initial index to start with (default is an empty dictionary).
    urls : list, optional
        List of URLs to process (default is None).
    type : str, optional
        Type of indexing to perform (default is 'title').
    print_logs : bool, optional
        Whether to print logging information (default is False).
    print_metadata : bool, optional
        Whether to print metadata information (default is False).
    delete_stopwords : bool, optional
        Whether to delete French stopwords during tokenization (default is False).
    use_stemmer : bool, optional
        Whether to use French stemming during tokenization (default is False).

    Attributes
    ----------
    __index : dict
        The current index.
    urls : list
        List of URLs to be processed.
    tokens : list
        List of tokens generated during the indexing process.
    nb_tokens : int
        Total number of tokens.
    nb_documents : int
        Total number of documents in the provided URLs.
    visited_urls : list
        List of URLs successfully processed during indexing.
    nb_visited_urls : int
        Total number of visited URLs.
    failed_urls : list
        List of URLs that failed during processing.
    nb_failed_urls : int
        Total number of failed URLs.
    type : str
        Type of indexing to perform.
    print_logs : bool
        Flag indicating whether to print logging information.
    print_metadata : bool
        Flag indicating whether to print metadata information.
    stopwords : list or None
        List of French stopwords if delete_stopwords is True, otherwise None.
    use_stemmer : bool
        Flag indicating whether stemming is used during tokenization.
    stemmer : SnowballStemmer or None
        SnowballStemmer for French if use_stemmer is True, otherwise None.

    Methods
    -------
    abstractmethod create_index():
        Abstract method to be implemented by subclasses for creating the specific index logic.

    abstractmethod run():
        Abstract method to be implemented by subclasses for running the indexing process.
    """
    def __init__(
            self,
            index={},
            urls=None,
            type: str = "title",
            print_logs=False,
            print_metadata=False,
            delete_stopwords=False,
            use_stemmer=False
    ) -> None:
    # Initialize instance variables with default values or provided values
        self.__index = index
        self.urls = urls
        self.tokens = []
        self.nb_tokens = 0
        self.nb_documents = len(self.urls)
        self.visited_urls = []
        self.nb_visited_urls = 0
        self.failed_urls = []
        self.nb_failed_urls = 0
        self.type = type
        self.print_logs = print_logs
        self.print_metadata = print_metadata
    # Initialize stopwords and stemmer based on user preferences
        self.stopwords = stopwords.words(
            'french') if delete_stopwords else None
        self.use_stemmer = use_stemmer
        self.stemmer = SnowballStemmer('french') if use_stemmer else None

    def __download_url(self, url):
        """
        Gets the text of the web page for a given URL.

        Parameters
        ----------
        url : str
            URL from which to download the HTML text page.
        
        Returns
        -------
        str or None
            Text contained in the web page if successful, otherwise None.
            
        """
        try:
            req = requests.get(url)
            if req.status_code == 200:
                if self.print_logs:
                    logging.info(f'Getting URL {url}')
                return req.text
            else:
                return None
        except Exception:
            if self.print_logs:
                logging.warning(f'Failed to reach {url}')

    def get_text_from_url(self, url):
        """
        Gets the text of the web page for a given URL

        Parameters
        ----------
        url:str
            URL from which we fetch the info

        Returns
        -------
        str
            titles, headers or paragraphs depending on the type of user query 
            as raw string (all glued together)
        """
        html = self.__download_url(url=url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            raw_text = ''
            for paragraph in soup.find_all(TYPES[self.type]):
                raw_text += " " + paragraph.text
            return raw_text

    def tokenize(self, text):
        """
        Tokenizes the given text by performing the following steps:
            1. Remove all characters that are not letters, numbers, or punctuation.
            2. Convert the text to lowercase, remove leading and trailing whitespace, and split the string.
            3. Optionally, remove French stopwords and stem the tokens.

        Parameters
        ----------
        text : str
            The text to be tokenized

        Returns
        -------
        list
            List of tokens derived from the input text.
        """
        # keep all letters (accents included)
        text = re.sub(r"(?i)^(?:(?![×Þß÷þø])[-'0-9a-zÀ-ÿ])+$", "", text)
        # replace anormal punctuation by a whitespace
        text = re.sub(r"’|…", " ", text)
        # delete punctuation and numbers then lowercase and delete trailing whitespaces then split string
        tokens = ''.join(
            ' ' if char in string.punctuation or char.isdigit() else char for char in text
        ).lower().strip('').split()
        # compute some statistics
        for token in tokens:
            if token not in self.tokens:
                self.tokens.append(token)
                self.nb_tokens += 1
        # delete stopwords
        if self.stopwords:
            tokens = [token for token in tokens if token.lower()
                      not in self.stopwords]
        # stem tokens
        if self.stemmer is not None:
            tokens = [self.stemmer.stem(token) for token in tokens]
        return tokens

    @abstractmethod
    def create_index(self):
        """
        Build the index by browsing the tokens
        """
        pass

    def get_index(self):
        """
        Getter method for retrieving the index.

        Returns
        -------
        dict
            The current index
        """
        return self.__index

    def get_statistics(self):
        """
        Print statistics including the number of documents, the number of distinct tokens,
        and the mean number of tokens per document.

        Returns
        -------
        str
            A formatted string containing the statistics.
        """
        return (
            f"------ Statistics ------\n"
            f"Number of documents: {self.nb_documents}\n"
            f"Number of tokens: {self.nb_tokens}\n"
            f"Mean number of tokens per document: {round(self.nb_tokens/self.nb_documents)}\n"
        )

    def get_metadata(self):
        """
        Print metadata including the number of URLs visited, the number of URLs that failed to download,
        and the total number of URLs.

        Returns
        -------
        str
            A formatted string containing the metadata.
        """
        return (
            f"------- Metadata -------\n"
            f"Number of URLs visited: {self.nb_visited_urls}\n"
            f"Number of failed URLs: {self.nb_failed_urls}\n"
            f"Total number of  URLs: {self.nb_visited_urls + self.nb_failed_urls}"
        )

    def export_metadata(self):
        """
        Export the metadata.

        Returns
        -------
        dict
            Dictionary containing all the metadata.
        """
        metadata = {
            "nb_documents": self.nb_documents,
            "nb_tokens": self.nb_tokens,
            "mean_nb_tokens_per_document": round(self.nb_tokens/self.nb_documents),
            "nb_visited_urls": self.nb_visited_urls,
            "nb_failed_urls": self.nb_failed_urls,
            "nb_total_urls": self.nb_visited_urls + self.nb_failed_urls
        }
        return metadata

    @abstractmethod
    def run(self):
        """
        Process the indexing
        """
        pass
