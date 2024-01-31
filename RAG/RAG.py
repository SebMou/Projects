import torch
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import DocArrayInMemorySearch
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.document_loaders import ConfluenceLoader

directory = 'sagemaker_documentation'
#If possible set device to gpu
device = torch.device("cpu")
model = "lmsys/fastchat-t5-3b-v1.0"

def load_docs(directory):
  loader = DirectoryLoader(directory)
  documents = loader.load()

  # An alternate loader would look something like this
  # loader = ConfluenceLoader(
  #     url="https://yoursite.atlassian.com/wiki", username="me", api_key="12345"
  # )
  # documents = loader.load(space_key="SPACE", include_attachments=True, limit=50)

  return documents

def split_docs(documents, chunk_size=512, chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

def create_retriever(split_documents):
  embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

  vector_db = DocArrayInMemorySearch.from_documents(split_documents, embedding=embedding, serializer="parquet")
  return vector_db.as_retriever(search_kwargs={"k": 3})

def create_tokenizer(model):
  return AutoTokenizer.from_pretrained(model)

def create_LM_model(model):
  # If possible to run in GPU, set load_in_8bit to True
  return AutoModelForSeq2SeqLM.from_pretrained(model, trust_remote_code=True, load_in_8bit=False)

def create_answerer(LMModel, tokenizer, retriever, max_new_tokens=100, repetition_penalty=1.1):
  pipe = pipeline(task="text2text-generation", model=LMModel, tokenizer=tokenizer, trust_remote_code=True, max_new_tokens=max_new_tokens, repetition_penalty=repetition_penalty, model_kwargs={"device_map": "auto", "max_length": 1200, "temperature": 0.01, "torch_dtype":torch.bfloat16})

  HFPipe = HuggingFacePipeline(pipeline=pipe)
  return RetrievalQA.from_chain_type(llm=HFPipe, chain_type="stuff", retriever=retriever, return_source_documents=True)

def Question(Answerer, question):
  result = Answerer({"query": question})

  print(result["query"] + "\n")

  answer = " ".join(result["result"].split()).replace("<pad>", "")

  print(answer + "\n")
  print("Suggested reading: ")
  for doc in result["source_documents"]:
    print(doc.metadata["source"] + "\n")
  return

documents = load_docs(directory)
split_documents = split_docs(documents)
retriever = create_retriever(split_documents)
tokenizer = create_tokenizer(model)
LMModel = create_LM_model(model)
Answerer = create_answerer(LMModel, tokenizer, retriever)

Question(Answerer, "What is SageMaker?")
Question(Answerer, "What are all AWS regions where SageMaker is available?")
Question(Answerer, "How to check if an endpoint is KMS encrypted?")
Question(Answerer, "What are SageMaker Geospatial capabilities?")
Question(Answerer, "Blahblabla Aquaman")