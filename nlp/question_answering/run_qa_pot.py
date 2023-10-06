#!/usr/bin/env python
# coding=utf-8
# Copyright 2023 C5ailabs Team (Authors: Rohit Sroch) All rights reserved.
# Copyright 2020 The HuggingFace Team All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Post Training Optimization/Quantization of a 🤗 Transformers model for question answering using 💻 IPEX (Intel® Extension for PyTorch) and 🤖 Neural Compressor.
"""
# You can also adapt this script on your own question answering task. Pointers for this are left as comments.

import logging
import os
import json
import timeit
import sys
import psutil
from dataclasses import dataclass, field
from typing import Optional

import torch
import datasets
import evaluate
from datasets import load_dataset
from trainer_qa import QuestionAnsweringTrainer
from utils_qa import postprocess_qa_predictions

import transformers
from transformers import (
    AutoConfig,
    AutoModelForQuestionAnswering,
    AutoTokenizer,
    DataCollatorWithPadding,
    EvalPrediction,
    HfArgumentParser,
    PreTrainedTokenizerFast,
    TrainingArguments,
    default_data_collator
)

from transformers.utils import check_min_version
from transformers.utils.versions import require_version

# neural compressor
from neural_compressor.config import PostTrainingQuantConfig
from neural_compressor import quantization

from neural_compressor import benchmark
from neural_compressor.config import BenchmarkConfig
from neural_compressor.utils.pytorch import load
from neural_compressor.adaptor.pytorch import get_example_inputs

try:
    import intel_extension_for_pytorch as ipex
except:
    assert False, "transformers 4.29.0 requests IPEX version higher or equal to 1.12"

os.environ["TOKENIZERS_PARALLELISM"] = "false"
# Will error if the minimal version of Transformers is not installed. Remove at your own risks.
check_min_version("4.29.0")

require_version("datasets>=1.8.0", "To fix: pip install datasets")

logger = logging.getLogger(__name__)


@dataclass
class ModelArguments:
    """
    Arguments pertaining to which model/config/tokenizer we are going to fine-tune from.
    """

    model_name_or_path: str = field(
        metadata={"help": "Path to pretrained model or model identifier from huggingface.co/models"}
    )
    config_name: Optional[str] = field(
        default=None, metadata={"help": "Pretrained config name or path if not the same as model_name"}
    )
    tokenizer_name: Optional[str] = field(
        default=None, metadata={"help": "Pretrained tokenizer name or path if not the same as model_name"}
    )
    cache_dir: Optional[str] = field(
        default=".cache",
        metadata={"help": "Path to directory to store the pretrained models downloaded from huggingface.co"},
    )
    model_revision: str = field(
        default="main",
        metadata={"help": "The specific model version to use (can be a branch name, tag name or commit id)."},
    )
    use_auth_token: bool = field(
        default=False,
        metadata={
            "help": (
                "Will use the token generated when running `huggingface-cli login` (necessary to use this script "
                "with private models)."
            )
        },
    )
    keep_accents: bool = field(
        default=False,
        metadata={
            "help": "To preserve accents (vowel matras / diacritics) while tokenization "
            
        },
    )
    do_lower_case: bool = field(
        default=False,
        metadata={
            "help": "Whether to lower case while tokenization"
            
        },
    )

    #########################################
    # Neural Compressor Arguments and IPEX
    #########################################
    tune: bool = field(
        default=False,
        metadata={"help": "Whether or not to apply quantization."},
    )
    ptq_method: str = field(
        default="dynamic_qat",
        metadata={"help": "Post Training Quantization method with choices as dynamic_int8, static_int8, static_smooth_int8"},
    )
    int8: bool = field(
        default=False, metadata={"help": "use int8 model to get accuracy or benchmark"}
    )
    backend: str = field(
        default="default",
        metadata={"help": "Post Training Quantization backend with choices as default, ipex"},
    )
    benchmark: bool = field(
        default=False, metadata={"help": "get benchmark instead of accuracy"}
    )
    accuracy_only: bool = field(
        default=False, metadata={"help": "get accuracy"}
    )
    iters: int = field(
        default=100,
        metadata={
            "help": "The inference iterations to run for benchmark."
        },
    )


@dataclass
class DataTrainingArguments:
    """
    Arguments pertaining to what data we are going to input our model for training and eval.
    """

    dataset_name: Optional[str] = field(
        default=None, metadata={"help": "The name of the dataset to use (via the datasets library)."}
    )
    dataset_config_name: Optional[str] = field(
        default=None, metadata={"help": "The configuration name of the dataset to use (via the datasets library)."}
    )
    validation_file: Optional[str] = field(
        default=None,
        metadata={"help": "An optional input evaluation data file to evaluate the perplexity on (a text file)."},
    )
    overwrite_cache: bool = field(
        default=False, metadata={"help": "Overwrite the cached training and evaluation sets"}
    )
    preprocessing_num_workers: Optional[int] = field(
        default=None,
        metadata={"help": "The number of processes to use for the preprocessing."},
    )
    max_seq_length: int = field(
        default=384,
        metadata={
            "help": (
                "The maximum total input sequence length after tokenization. Sequences longer "
                "than this will be truncated, sequences shorter will be padded."
            )
        },
    )
    pad_to_max_length: bool = field(
        default=True,
        metadata={
            "help": (
                "Whether to pad all samples to `max_seq_length`. If False, will pad the samples dynamically when"
                " batching to the maximum length in the batch (which can be faster on GPU but will be slower on TPU)."
            )
        },
    )
    max_eval_samples: Optional[int] = field(
        default=50,
        metadata={
            "help": (
                "For debugging purposes or quicker training, truncate the number of evaluation examples to this "
                "value if set."
            )
        },
    )
    version_2_with_negative: bool = field(
        default=False, metadata={"help": "If true, some of the examples do not have an answer."}
    )
    null_score_diff_threshold: float = field(
        default=0.0,
        metadata={
            "help": (
                "The threshold used to select the null answer: if the best answer has a score that is less than "
                "the score of the null answer minus this threshold, the null answer is selected for this example. "
                "Only useful when `version_2_with_negative=True`."
            )
        },
    )
    doc_stride: int = field(
        default=128,
        metadata={"help": "When splitting up a long document into chunks, how much stride to take between chunks."},
    )
    n_best_size: int = field(
        default=20,
        metadata={"help": "The total number of n-best predictions to generate when looking for an answer."},
    )
    max_answer_length: int = field(
        default=30,
        metadata={
            "help": (
                "The maximum length of an answer that can be generated. This is needed because the start "
                "and end predictions are not conditioned on one another."
            )
        },
    )

    def __post_init__(self):
        if (
            self.dataset_name is None
            and self.validation_file is None
        ):
            raise ValueError("Need either a dataset name or a training/validation file/test_file.")
        else:
            if self.validation_file is not None:
                extension = self.validation_file.split(".")[-1]
                assert extension in ["csv", "json"], "`validation_file` should be a csv or a json file."


def main():
    # See all possible arguments in src/transformers/training_args.py
    # or by passing the --help flag to this script.
    # We now keep distinct sets of args, for a cleaner separation of concerns.

    parser = HfArgumentParser((ModelArguments, DataTrainingArguments, TrainingArguments))
    if len(sys.argv) == 2 and sys.argv[1].endswith(".json"):
        # If we pass only one argument to the script and it's the path to a json file,
        # let's parse it to get our arguments.
        model_args, data_args, training_args = parser.parse_json_file(json_file=os.path.abspath(sys.argv[1]))
    else:
        model_args, data_args, training_args = parser.parse_args_into_dataclasses()

    # Setup logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
    )

    if training_args.should_log:
        # The default of training_args.log_level is passive, so we set log level at info here to have that default.
        transformers.utils.logging.set_verbosity_info()

    log_level = training_args.get_process_log_level()
    logger.setLevel(log_level)
    datasets.utils.logging.set_verbosity(log_level)
    transformers.utils.logging.set_verbosity(log_level)
    transformers.utils.logging.enable_default_handler()
    transformers.utils.logging.enable_explicit_format()

    if data_args.dataset_name is not None:
        # Downloading and loading a dataset from the hub.
        raw_datasets = load_dataset(
            data_args.dataset_name,
            data_args.dataset_config_name,
            cache_dir=model_args.cache_dir,
            use_auth_token=True if model_args.use_auth_token else None,
        )
    else:
        data_files = {}
        if data_args.validation_file is not None:
            data_files["validation"] = data_args.validation_file
            extension = data_args.validation_file.split(".")[-1]

        raw_datasets = load_dataset(
            extension,
            data_files=data_files,
            field="data",
            cache_dir=model_args.cache_dir,
            use_auth_token=True if model_args.use_auth_token else None,
        )
    # See more about loading any type of standard or custom dataset (from files, python dict, pandas DataFrame, etc) at
    # https://huggingface.co/docs/datasets/loading_datasets.html.

    # Load pretrained model and tokenizer
    #
    # Distributed training:
    # The .from_pretrained methods guarantee that only one local process can concurrently
    # download model & vocab.
    config = AutoConfig.from_pretrained(
        model_args.config_name if model_args.config_name else model_args.model_name_or_path,
        cache_dir=model_args.cache_dir,
        revision=model_args.model_revision,
        use_auth_token=True if model_args.use_auth_token else None,
    )
    tokenizer = AutoTokenizer.from_pretrained(
        model_args.tokenizer_name if model_args.tokenizer_name else model_args.model_name_or_path,
        cache_dir=model_args.cache_dir,
        use_fast=True,
        revision=model_args.model_revision,
        use_auth_token=True if model_args.use_auth_token else None,
        keep_accents=model_args.keep_accents,
        do_lower_case=model_args.do_lower_case
    )
    model = AutoModelForQuestionAnswering.from_pretrained(
        model_args.model_name_or_path,
        from_tf=bool(".ckpt" in model_args.model_name_or_path),
        config=config,
        cache_dir=model_args.cache_dir,
        revision=model_args.model_revision,
        use_auth_token=True if model_args.use_auth_token else None,
    )

    # Tokenizer check: this script requires a fast tokenizer.
    if not isinstance(tokenizer, PreTrainedTokenizerFast):
        raise ValueError(
            "This example script only works for models that have a fast tokenizer. Checkout the big table of models at"
            " https://huggingface.co/transformers/index.html#supported-frameworks to find the model types that meet"
            " this requirement"
        )

    # Preprocessing the datasets.
    # Preprocessing is slighlty different for training and evaluation.
    column_names = raw_datasets["validation"].column_names
   
    question_column_name = "question" if "question" in column_names else column_names[0]
    context_column_name = "context" if "context" in column_names else column_names[1]
    answer_column_name = "answers" if "answers" in column_names else column_names[2]

    # Padding side determines if we do (question|context) or (context|question).
    pad_on_right = tokenizer.padding_side == "right"

    if data_args.max_seq_length > tokenizer.model_max_length:
        logger.warning(
            f"The max_seq_length passed ({data_args.max_seq_length}) is larger than the maximum length for the"
            f"model ({tokenizer.model_max_length}). Using max_seq_length={tokenizer.model_max_length}."
        )
    max_seq_length = min(data_args.max_seq_length, tokenizer.model_max_length)

    # Validation preprocessing
    def prepare_validation_features(examples):
        # Some of the questions have lots of whitespace on the left, which is not useful and will make the
        # truncation of the context fail (the tokenized question will take a lots of space). So we remove that
        # left whitespace
        examples[question_column_name] = [q.lstrip() for q in examples[question_column_name]]

        # Tokenize our examples with truncation and maybe padding, but keep the overflows using a stride. This results
        # in one example possible giving several features when a context is long, each of those features having a
        # context that overlaps a bit the context of the previous feature.
        tokenized_examples = tokenizer(
            examples[question_column_name if pad_on_right else context_column_name],
            examples[context_column_name if pad_on_right else question_column_name],
            truncation="only_second" if pad_on_right else "only_first",
            max_length=max_seq_length,
            stride=data_args.doc_stride,
            return_overflowing_tokens=True,
            return_offsets_mapping=True,
            padding="max_length" if data_args.pad_to_max_length else False,
        )

        # Since one example might give us several features if it has a long context, we need a map from a feature to
        # its corresponding example. This key gives us just that.
        sample_mapping = tokenized_examples.pop("overflow_to_sample_mapping")

        # For evaluation, we will need to convert our predictions to substrings of the context, so we keep the
        # corresponding example_id and we will store the offset mappings.
        tokenized_examples["example_id"] = []

        for i in range(len(tokenized_examples["input_ids"])):
            # Grab the sequence corresponding to that example (to know what is the context and what is the question).
            sequence_ids = tokenized_examples.sequence_ids(i)
            context_index = 1 if pad_on_right else 0

            # One example can give several spans, this is the index of the example containing this span of text.
            sample_index = sample_mapping[i]
            tokenized_examples["example_id"].append(examples["id"][sample_index])

            # Set to None the offset_mapping that are not part of the context so it's easy to determine if a token
            # position is part of the context or not.
            tokenized_examples["offset_mapping"][i] = [
                (o if sequence_ids[k] == context_index else None)
                for k, o in enumerate(tokenized_examples["offset_mapping"][i])
            ]

        return tokenized_examples

    eval_examples = raw_datasets["validation"]
    if data_args.max_eval_samples is not None:
        # We will select sample from whole data
        max_eval_samples = min(len(eval_examples), data_args.max_eval_samples)
        eval_examples = eval_examples.select(range(max_eval_samples))
    # Validation Feature Creation
    with training_args.main_process_first(desc="validation dataset map pre-processing"):
        eval_dataset = eval_examples.map(
            prepare_validation_features,
            batched=True,
            num_proc=data_args.preprocessing_num_workers,
            remove_columns=column_names,
            load_from_cache_file=not data_args.overwrite_cache,
            desc="Running tokenizer on validation dataset",
        )
    if data_args.max_eval_samples is not None:
        # During Feature creation dataset samples might increase, we will select required samples again
        max_eval_samples = min(len(eval_dataset), data_args.max_eval_samples)
        eval_dataset = eval_dataset.select(range(max_eval_samples))

    
    # Data collator
    # We have already padded to max length if the corresponding flag is True, otherwise we need to pad in the data
    # collator.
    data_collator = (
        default_data_collator
        if data_args.pad_to_max_length
        else DataCollatorWithPadding(tokenizer, pad_to_multiple_of=None)
    )

    # Post-processing:
    def post_processing_function(examples, features, predictions, stage="eval"):
        # Post-processing: we match the start logits and end logits to answers in the original context.
        predictions = postprocess_qa_predictions(
            examples=examples,
            features=features,
            predictions=predictions,
            version_2_with_negative=data_args.version_2_with_negative,
            n_best_size=data_args.n_best_size,
            max_answer_length=data_args.max_answer_length,
            null_score_diff_threshold=data_args.null_score_diff_threshold,
            output_dir=training_args.output_dir,
            log_level=log_level,
            prefix=stage,
        )
        # Format the result to the format the metric expects.
        if data_args.version_2_with_negative:
            formatted_predictions = [
                {"id": str(k), "prediction_text": v, "no_answer_probability": 0.0} for k, v in predictions.items()
            ]
        else:
            formatted_predictions = [{"id": str(k), "prediction_text": v} for k, v in predictions.items()]

        references = [{"id": str(ex["id"]), "answers": ex[answer_column_name]} for ex in examples]
        return EvalPrediction(predictions=formatted_predictions, label_ids=references)

    metric = evaluate.load("squad_v2" if data_args.version_2_with_negative else "squad")

    def compute_metrics(p: EvalPrediction):
        return metric.compute(predictions=p.predictions, references=p.label_ids)

    # Initialize our Trainer
    trainer = QuestionAnsweringTrainer(
        model=model,
        args=training_args,
        train_dataset=None,
        eval_dataset=eval_dataset,
        eval_examples=eval_examples,
        tokenizer=tokenizer,
        data_collator=data_collator,
        post_process_function=post_processing_function,
        compute_metrics=compute_metrics,
    )
    
    ############################################################################################
    logger.info("*"*100)
    logger.info("\n\n")
    eval_dataloader = trainer.get_eval_dataloader()
    batch_size = eval_dataloader.batch_size
    metric_name = "eval_f1"

    def take_eval_steps(model, trainer, metric_name, save_metrics=False):
        trainer.model = model
        start_time = timeit.default_timer()
        metrics = trainer.evaluate()
        evalTime = timeit.default_timer() - start_time
        max_eval_samples = data_args.max_eval_samples \
         if data_args.max_eval_samples is not None else len(eval_dataset)
        eval_samples = min(max_eval_samples, len(eval_dataset))
        samples = eval_samples - (eval_samples % batch_size) \
         if training_args.dataloader_drop_last else eval_samples
        if save_metrics:
            trainer.save_metrics("eval", metrics)
        
        print('Batch size = %d' % batch_size)
        print("Finally Eval {} Accuracy: {}".format(metric_name, metrics.get(metric_name)))
        print("Latency: %.3f ms" % (evalTime / samples * 1000))
        print("Throughput: {} samples/sec".format(samples / evalTime))
        summary = {
            "batch_size": batch_size,
            "final_{}".format(metric_name): metrics.get(metric_name),
            "latency (ms)": (evalTime / samples * 1000),
            "throughput (samples/sec)": (samples / evalTime)
        }
        save_path = os.path.join(training_args.output_dir, "summary.json")
        with open(save_path, "w") as fp:
            json.dump(summary, fp)

        return metrics.get(metric_name)

    def eval_func(model):
        return take_eval_steps(model, trainer, metric_name)
    
    if model_args.tune and os.path.exists(os.path.join(training_args.output_dir, "pytorch_model.bin")) == False:
        logger.info("************Perform INT8 Quantization using Intel® Neural Compressor using PTQ_METHOD={}, Backend={}************".format(
            model_args.ptq_method,
            model_args.backend
        ))
        if model_args.backend == "ipex":
            ipex.nn.utils._model_convert.replace_dropout_with_identity(model)

        recipes = {}
        approach = "dynamic"
        if model_args.ptq_method == "dynamic_int8":
            approach = "dynamic"
        elif model_args.ptq_method == "static_int8":
            approach = "static"
        elif model_args.ptq_method == "static_smooth_int8":
            recipes={"smooth_quant": True,  "smooth_quant_args": {"alpha": 0.5, "folding": True}}
            approach = "static"
        
        config = PostTrainingQuantConfig(
            approach=approach, 
            backend=model_args.backend,
            recipes=recipes,
            calibration_sampling_size=data_args.max_eval_samples
        )
        q_model = quantization.fit(model,
                            config,
                            calib_dataloader=eval_dataloader,
                            eval_func=eval_func)
        q_model.save(training_args.output_dir)
    else:
        if model_args.int8:
            logger.info("************Already INT8 Quantizated model exists at {}. Delete it to Re-Tune!************".format(
                training_args.output_dir
            ))

    if model_args.int8:
        logger.info("************Loading INT8 Quantized Model using PTQ_METHOD={}, Backend={}************".format(
            model_args.ptq_method,
            model_args.backend
        ))
        model = load(training_args.output_dir, model, dataloader=eval_dataloader)
    else:
        model.eval()
        if model_args.backend == "ipex":
            logger.info("************Optimize FP32 Model using Backend={} i.e `ipex.optimize`************".format(
                model_args.backend
            ))
            example_inputs = get_example_inputs(model, eval_dataloader)
            model = ipex.optimize(model)
            with torch.no_grad():
                model = torch.jit.trace(model, example_inputs, strict=False)
                model = torch.jit.freeze(model)

    if model_args.benchmark or model_args.accuracy_only:
        if model_args.int8:
            logger.info("************Benchmark INT8 Pytorch Model using Backend={}************".format(
                model_args.backend
            ))
        else:
            logger.info("************Benchmark FP32 Pytorch Model using Backend={}************".format(
                model_args.backend
            ))
        if model_args.benchmark:
            try:
                cpu_counts = psutil.cpu_count(logical=False)
                b_conf = BenchmarkConfig(backend=model_args.backend,
                                        warmup=5,
                                        iteration=model_args.iters,
                                        cores_per_instance=cpu_counts,
                                        num_of_instance=1)
                benchmark.fit(model, b_conf, b_dataloader=eval_dataloader)
            except Exception:
                pass
        else:
            eval_func(model)
    ############################################################################################

 
def _mp_fn(index):
    # For xla_spawn (TPUs)
    main()


if __name__ == "__main__":
    main()