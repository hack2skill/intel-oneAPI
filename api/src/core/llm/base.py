
# lang chain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import AzureOpenAI

from core.llm.huggingface_pipeline import HuggingFacePipeline
from core.llm.huggingface_peft import HuggingFacePEFT


def get_llm(llm_method="azure_gpt3", 
            callback_manager=None, 
            **kwargs):
    
    llm = None
    if callback_manager is None:
        callback_manager = CallbackManager(
            [StreamingStdOutCallbackHandler()])
    if llm_method == "azure_gpt3":
        """
          Wrapper around Azure OpenAI
          https://azure.microsoft.com/en-in/products/cognitive-services/openai-service
        """
        llm_kwargs = kwargs.get("llm_kwargs", {})
        llm = AzureOpenAI(
            callback_manager=callback_manager,
            deployment_name=kwargs.get(
               "deployment_name", "text-davinci-003-prod"),
            **llm_kwargs
        )
    elif llm_method == "hf_pipeline":
        """
         Wrapper around HuggingFace Pipeline API.
         https://huggingface.co/models
        """

        llm = HuggingFacePipeline.from_model_id(
            model_id=kwargs.get("model_name", "bigscience/bloom-1b7"),
            task=kwargs.get("task", "text-generation"),
            device=kwargs.get("device", -1),
            model_kwargs=kwargs.get("llm_kwargs", {}),
            pipeline_kwargs=kwargs.get("pipeline_kwargs", {}),
            quantization_kwargs=kwargs.get("quantization_kwargs", {})
        )
    elif llm_method == "hf_peft":
        """
         Wrapper around HuggingFace Peft API.
         https://huggingface.co/models
        """
        llm = HuggingFacePEFT.from_model_id(
            model_id=kwargs.get("model_name", "huggyllama/llama-7b"),
            adapter_id=kwargs.get("adapter_name", "timdettmers/qlora-flan-7b"),
            task=kwargs.get("task", "text-generation"),
            device=kwargs.get("device", -1),
            model_kwargs=kwargs.get("llm_kwargs", {}),
            generation_kwargs=kwargs.get("generation_kwargs", {}),
            quantization_kwargs=kwargs.get("quantization_kwargs", {})
        )
    else:
        raise ValueError(
            "Please use a valid llm_name. Supported options are"
            "[azure-gpt3, hf_pipeline, hf_peft] only."
        )
    
    return llm
