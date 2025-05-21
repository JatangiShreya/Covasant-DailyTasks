from transformers import pipeline
from langchain.llms import HuggingFacePipeline


hf_pipeline = pipeline(
    task="text2text-generation",
    model="google/flan-t5-base",
    tokenizer="google/flan-t5-base",
    max_length=256
)

llm = HuggingFacePipeline(pipeline=hf_pipeline)


response = llm("Translate English to French: I love programming.")
print(response)
