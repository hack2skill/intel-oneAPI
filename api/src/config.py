import json
import os

PORT = 8500

ASK_DOUBT_CONFIG = {
  "emb_model_name_or_path": "ai4bharat/indic-bert",
  "emb_model_type": "semantic",  #options: syntactic, semantic
  "qa_model_name_or_path": "rohitsroch/indic-mALBERT-squad-v2",
  "qa_model_type": "vanilla_fp32",  #options: vanilla_fp32, quantized_int8
  
  "intel_scikit_learn_enabled": True,
  "ipex_enabled": True,
  "keep_accents": True,
  "normalize_L2": False,
  "do_lower_case": True,
  "faiss_vector_index_path": "artifacts/index/faiss_emb_index"
}


AI_EXAMINER_CONFIG = {
  "llm_name": "azure_gpt3", #options: azure_gpt3, hf_pipeline
  "azure_deployment_name": "text-davinci-003-prod",
  "hf_model_name": "mosaicml/mpt-7b-instruct", # mosaicml/mpt-7b-instruct
  "device": 0, # cuda:0
  "llm_kwargs":{
      "do_sample": True,
      "temperature": 0.5, 
      "max_new_tokens": 300,
      "top_p": 1.0,
      "top_k": 0,
      "repetition_penalty": 1.1,
      "num_return_sequences": 1,
      "stop_sequence": "<|endoftext|>"
  }
}

os.environ["TOKENIZERS_PARALLELISM"] = "True"

# Set this to `azure`
os.environ["OPENAI_API_TYPE"]= "azure"
# The API version you want to use: set this to `2022-12-01` for the released version.
os.environ["OPENAI_API_VERSION"] = "2022-12-01"
# The base URL for your Azure OpenAI resource.  You can find this in the Azure portal under your Azure OpenAI resource.
os.environ["OPENAI_API_BASE"] = "https://c5-openai-research.openai.azure.com/"
# The API key for your Azure OpenAI resource.  You can find this in the Azure portal under your Azure OpenAI resource.
os.environ["OPENAI_API_KEY"] = "<your_key>"
