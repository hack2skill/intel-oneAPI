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
  "llm_method": "azure_gpt3", #options: azure_gpt3, hf_pipeline, hf_peft

  "azure_gpt3":{
    "deployment_name": "text-davinci-003-prod",
    "llm_kwargs": {
        "temperature": 0.3,
        "max_tokens": 300,
        "n": 1,
        "top_p": 1.0,
        "frequency_penalty": 1.1
    }      
  },
  "hf_pipeline":{
      "model_name": "tiiuae/falcon-7b-instruct",
      "task": "text-generation",
      "device": -1,
      "llm_kwargs":{
         "torch_dtype": "float16",  #bfloat16, float16, float32
         "device_map": "auto",
         "load_in_4bit": True,
         "max_memory": "24000MB",
         "trust_remote_code": True
      },
      "pipeline_kwargs": {
          "max_new_tokens": 300,
          "top_p": 0.15,
          "top_k": 0,
          "temperature": 0.3,
          "repetition_penalty": 1.1,
          "num_return_sequences": 1,
          "do_sample": True,
          "stop_sequence": []
      },
      "quantization_kwargs": {
        "load_in_4bit": True, # do 4 bit quantization
        "load_in_8bit": False,
        "bnb_4bit_compute_dtype": "float16", #bfloat16, float16, float32
        "bnb_4bit_use_double_quant": True,
        "bnb_4bit_quant_type": "nf4"
      }
  },
  "hf_peft":{
      "model_name": "huggyllama/llama-7b",
      "adapter_name": "timdettmers/qlora-alpaca-7b",
      "task": "text-generation",
      "device": -1,
      "llm_kwargs":{
         "torch_dtype": "float16",  #bfloat16, float16, float32
         "device_map": "auto",
         "load_in_4bit": True,
         "max_memory": "32000MB",
         "trust_remote_code": True
      },
      "generation_kwargs": {
          "max_new_tokens": 300,
          "top_p": 0.15,
          "top_k": 0,
          "temperature": 0.3,
          "repetition_penalty": 1.1,
          "num_return_sequences": 1,
          "do_sample": True,
          "early_stopping": True,
          "stop_sequence": []
      },
      "quantization_kwargs": {
        "load_in_4bit": True, # do 4 bit quantization
        "load_in_8bit": False,
        "bnb_4bit_compute_dtype": "float16", #bfloat16, float16, float32
        "bnb_4bit_use_double_quant": True,
        "bnb_4bit_quant_type": "nf4"
      }
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
