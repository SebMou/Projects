import sys
from langchain.document_loaders import DirectoryLoader

directory = 'test_dir/'

loader = DirectoryLoader(directory)
documents = loader.load()