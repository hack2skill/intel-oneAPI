
# lang chain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain.llms import AzureOpenAI
from langchain import HuggingFacePipeline


def get_llm(llm_name="azure_gpt3",
            azure_deployment_name="text-davinci-003-prod",
            hf_model_name="TheBloke/falcon-7b-instruct-GPTQ",
            **kwargs):

    llm = None
    if llm_name == "azure_gpt3":
        llm = AzureOpenAI(streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()],
            deployment_name=azure_deployment_name,
            temperature=kwargs["llm_kwargs"].get("temperature", 0.5),
            max_tokens=kwargs["llm_kwargs"].get("max_new_tokens", 300),
            n=kwargs["llm_kwargs"].get("num_return_sequences", 1),
            top_p=kwargs["llm_kwargs"].get("top_p", 1.0),
            frequency_penalty=kwargs["llm_kwargs"].get("repetition_penalty", 0)
        )
    elif llm_name == "hf_pipeline":
        llm = HuggingFacePipeline.from_model_id(
            model_id=hf_model_name, 
            task="text-generation",
            device=kwargs.get("device", -1),
            stop_sequence=kwargs["llm_kwargs"].get("stop_sequence", "<|endoftext|>"),
            model_kwargs=kwargs.get("llm_kwargs")
        )
    else:
        raise ValueError("Please use a valid llm_name. Supported options are [azure_gpt3, hf_pipeline] only.")
    
    return llm
