#!/bin/bash
HOME_DIR=`pwd`

##############################################################################################
########  Post Training Optimization (POT) and Benchmark Transformer Model for QA   ##########
##############################################################################################

export MODEL_NAME_OR_PATH=artifacts/qa/squad/indic-mALBERT
export BACKBONE_NAME=indic-mALBERT
export DATASET_NAME=squad # squad, squad_v2 (pass --version_2_with_negative)
export TASK_NAME=qa
export USE_OPTIMUM=True  # whether to use hugging face wrapper optimum around intel neural compressor

# other parameters
export BATCH_SIZE=8
export MAX_SEQ_LENGTH=256
export DOC_STRIDE=128
export KEEP_ACCENTS=False
export DO_LOWER_CASE=True
export MAX_EVAL_SAMPLES=200

export TUNE=True
export PTQ_METHOD="dynamic_int8" # "dynamic_int8", "static_int8", "static_smooth_int8"
export BACKEND="default" # default, ipex
export ITERS=100

export INT8=False
if [[ ${TUNE} == "True" ]]; then
    export INT8=True  # if tune is True then int8 must be true
fi

export PRECISION=fp32
if [[ ${INT8} == "True" ]]; then
    export PRECISION=int8
fi

if [[ ${PRECISION} == "fp32" ]]; then
   if [[ ${BACKEND} == "ipex" ]]; then
      export OUTPUT_DIR=tuned/$TASK_NAME/$DATASET_NAME/$BACKBONE_NAME/$BACKEND/$PRECISION
      echo Perform Optimization using IPEX: PRECISION=$PRECISION
   else
      export OUTPUT_DIR=tuned/$TASK_NAME/$DATASET_NAME/$BACKBONE_NAME/$BACKEND/$PRECISION
      echo Base Pytorch with no Optimization: PRECISION=$PRECISION
   fi
else
   export OUTPUT_DIR=tuned/$TASK_NAME/$DATASET_NAME/$BACKBONE_NAME/$BACKEND/$PTQ_METHOD/$PRECISION
   echo Perform Quantization using Neural Compressor with:  Tune=$TUNE, PTQ_METHOD=$PTQ_METHOD, BACKEND=$BACKEND, INT8=$INT8, PRECISION=$PRECISION
fi

if [[ ${USE_OPTIMUM} == "True" ]]; then
    python -u run_qa_pot_optimum.py \
        --model_name_or_path $MODEL_NAME_OR_PATH \
        --dataset_name $DATASET_NAME \
        --max_seq_length $MAX_SEQ_LENGTH \
        --per_device_eval_batch_size $BATCH_SIZE \
        --keep_accents $KEEP_ACCENTS \
        --do_lower_case $DO_LOWER_CASE \
        --max_eval_samples $MAX_EVAL_SAMPLES \
        --doc_stride $DOC_STRIDE \
        --tune $TUNE \
        --ptq_method $PTQ_METHOD \
        --int8 $INT8 \
        --backend $BACKEND \
        --iters $ITERS \
        --benchmark \
        --no_cuda \
        --output_dir $OUTPUT_DIR
else
    python -u run_qa_pot.py \
        --model_name_or_path $MODEL_NAME_OR_PATH \
        --dataset_name $DATASET_NAME \
        --max_seq_length $MAX_SEQ_LENGTH \
        --per_device_eval_batch_size $BATCH_SIZE \
        --keep_accents $KEEP_ACCENTS \
        --do_lower_case $DO_LOWER_CASE \
        --max_eval_samples $MAX_EVAL_SAMPLES \
        --doc_stride $DOC_STRIDE \
        --tune $TUNE \
        --ptq_method $PTQ_METHOD \
        --int8 $INT8 \
        --backend $BACKEND \
        --iters $ITERS \
        --benchmark \
        --no_cuda \
        --output_dir $OUTPUT_DIR
fi