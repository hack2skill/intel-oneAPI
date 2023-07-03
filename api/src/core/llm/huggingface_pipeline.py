"""Wrapper around HuggingFace Pipeline APIs."""
import importlib.util
import logging
from typing import Any, List, Mapping, Optional

from pydantic import Extra

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens

DEFAULT_MODEL_ID = "gpt2"
DEFAULT_TASK = "text-generation"
VALID_TASKS = ("text2text-generation", "text-generation", "summarization")

logger = logging.getLogger(__name__)


class HuggingFacePipeline(LLM):
    """Wrapper around HuggingFace Pipeline API.

    To use, you should have the ``transformers`` python package installed.

    Only supports `text-generation`, `text2text-generation` and `summarization` for now.

    Example using from_model_id:
        .. code-block:: python

            from langchain.llms import HuggingFacePipeline
            hf = HuggingFacePipeline.from_model_id(
                model_id="gpt2",
                task="text-generation",
                pipeline_kwargs={"max_new_tokens": 10},
            )
    Example passing pipeline in directly:
        .. code-block:: python

            from langchain.llms import HuggingFacePipeline
            from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

            model_id = "gpt2"
            tokenizer = AutoTokenizer.from_pretrained(model_id)
            model = AutoModelForCausalLM.from_pretrained(model_id)
            pipe = pipeline(
                "text-generation", model=model, tokenizer=tokenizer, max_new_tokens=10
            )
            hf = HuggingFacePipeline(pipeline=pipe)
    """

    pipeline: Any  #: :meta private:
    model_id: str = DEFAULT_MODEL_ID
    """Model name to use."""
    model_kwargs: Optional[dict] = None
    """Key word arguments passed to the model."""
    pipeline_kwargs: Optional[dict] = None
    """Key word arguments passed to the pipeline."""
    quantization_kwargs: Optional[dict] = None
    """Quantization arguments passed to the quantization."""

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    @classmethod
    def from_model_id(
        cls,
        model_id: str,
        task: str,
        device: int = -1,
        model_kwargs: Optional[dict] = {},
        pipeline_kwargs: Optional[dict] = {},
        quantization_kwargs: Optional[dict] = {},
        **kwargs: Any,
    ) -> LLM:
        """Construct the pipeline object from model_id and task."""
        try:
            import torch
            from transformers import (
                AutoModelForCausalLM,
                AutoModelForSeq2SeqLM,
                AutoTokenizer,
                BitsAndBytesConfig
            )
            from transformers import pipeline as hf_pipeline
            from transformers import StoppingCriteria, StoppingCriteriaList

        except ImportError:
            raise ValueError(
                "Could not import transformers python package. "
                "Please install it with `pip install transformers`."
            )

        _model_kwargs = model_kwargs or {}
        tokenizer = AutoTokenizer.from_pretrained(model_id, **_model_kwargs)

        try:
            quantization_config = None
            if quantization_kwargs:
                bnb_4bit_compute_dtype = quantization_kwargs.get("bnb_4bit_compute_dtype", torch.float32)
                if bnb_4bit_compute_dtype == "bfloat16":
                    quantization_kwargs["bnb_4bit_compute_dtype"] = torch.bfloat16
                elif bnb_4bit_compute_dtype == "float16":
                    quantization_kwargs["bnb_4bit_compute_dtype"] = torch.float16
                elif bnb_4bit_compute_dtype == "float32":
                    quantization_kwargs["bnb_4bit_compute_dtype"] = torch.float32
                
                quantization_config = BitsAndBytesConfig(**quantization_kwargs)
            
            torch_dtype = _model_kwargs.get("torch_dtype", torch.float32)
            if torch_dtype is not None:
                if torch_dtype == "bfloat16":
                    _model_kwargs["torch_dtype"] = torch.bfloat16
                elif torch_dtype == "float16":
                    _model_kwargs["torch_dtype"] = torch.float16
                elif torch_dtype == "float32":
                    _model_kwargs["torch_dtype"] = torch.float32
            
            max_memory= {i: _model_kwargs.get(
                "max_memory", "32000MB") for i in range(torch.cuda.device_count())}
            _model_kwargs.pop("max_memory")
            if task == "text-generation":
                model = AutoModelForCausalLM.from_pretrained(
                    model_id, 
                    max_memory=max_memory,
                    quantization_config=quantization_config,
                    **_model_kwargs)
            elif task in ("text2text-generation", "summarization"):
                model = AutoModelForSeq2SeqLM.from_pretrained(
                    model_id, 
                    max_memory=max_memory,
                    quantization_config=quantization_config,
                    **_model_kwargs)
            else:
                raise ValueError(
                    f"Got invalid task {task}, "
                    f"currently only {VALID_TASKS} are supported"
                )
            _model_kwargs.pop("torch_dtype")
        except ImportError as e:
            raise ValueError(
                f"Could not load the {task} model due to missing dependencies."
            ) from e

        if importlib.util.find_spec("torch") is not None:

            cuda_device_count = torch.cuda.device_count()
            if device < -1 or (device >= cuda_device_count):
                raise ValueError(
                    f"Got device=={device}, "
                    f"device is required to be within [-1, {cuda_device_count})"
                )
            if device < 0 and cuda_device_count > 0:
                logger.warning(
                    "Device has %d GPUs available. "
                    "Provide device={deviceId} to `from_model_id` to use available"
                    "GPUs for execution. deviceId is -1 (default) for CPU and "
                    "can be a positive integer associated with CUDA device id.",
                    cuda_device_count,
                )
        if "trust_remote_code" in _model_kwargs:
            _model_kwargs = {
                k: v for k, v in _model_kwargs.items() if k != "trust_remote_code"
            }
        _pipeline_kwargs = pipeline_kwargs or {}
        
        device_id = "cpu"
        if device != -1:
            device_id = "cuda:{}".format(device)

        stopping_criteria = None
        stop_sequence = _pipeline_kwargs.get("stop_sequence", [])
        if len(stop_sequence) > 0:
            stop_token_ids = [tokenizer(
                stop_word, add_special_tokens=False, return_tensors='pt')['input_ids'].squeeze() for stop_word in stop_sequence]
            stop_token_ids = [token.to(device_id) for token in stop_token_ids]

            # define custom stopping criteria object
            class StopOnTokens(StoppingCriteria):
                def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
                    for stop_ids in stop_token_ids:
                        if torch.eq(input_ids[0][-len(stop_ids):], stop_ids).all():
                            return True
                    return False
            stopping_criteria = StoppingCriteriaList([StopOnTokens()])

            # eos_token_id = stop_token_ids[0][0].item()
            # self.generation_kwargs["pad_token_id"] = 1
            # self.generation_kwargs["eos_token_id"] = eos_token_id
        
        _pipeline_kwargs.pop("stop_sequence")
        pipeline = hf_pipeline(
            task=task,
            model=model,
            tokenizer=tokenizer,
            device=device,
            stopping_criteria=stopping_criteria,
            model_kwargs=_model_kwargs,
            **_pipeline_kwargs,
        )
        if pipeline.task not in VALID_TASKS:
            raise ValueError(
                f"Got invalid task {pipeline.task}, "
                f"currently only {VALID_TASKS} are supported"
            )
        return cls(
            pipeline=pipeline,
            model_id=model_id,
            model_kwargs=_model_kwargs,
            pipeline_kwargs=_pipeline_kwargs,
            **kwargs,
        )

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {
            "model_id": self.model_id,
            "model_kwargs": self.model_kwargs,
            "pipeline_kwargs": self.pipeline_kwargs,
        }

    @property
    def _llm_type(self) -> str:
        return "huggingface_pipeline"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        response = self.pipeline(prompt)
        if self.pipeline.task == "text-generation":
            # Text generation return includes the starter text.
            text = response[0]["generated_text"][len(prompt) :]
        elif self.pipeline.task == "text2text-generation":
            text = response[0]["generated_text"]
        elif self.pipeline.task == "summarization":
            text = response[0]["summary_text"]
        else:
            raise ValueError(
                f"Got invalid task {self.pipeline.task}, "
                f"currently only {VALID_TASKS} are supported"
            )
        if stop is not None:
            # This is a bit hacky, but I can't figure out a better way to enforce
            # stop tokens when making calls to huggingface_hub.
            text = enforce_stop_tokens(text, stop)
        return text