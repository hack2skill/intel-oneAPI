#!/bin/bash
HOME_DIR=`pwd`

##############################################################################################
#########################  Finetune Transformer Model for QA   ###############################
##############################################################################################

export MODEL_NAME_OR_PATH=ai4bharat/indic-bert
export BACKBONE_NAME=indic-mALBERT-uncased
export DATASET_NAME=squad # squad, squad_v2 (pass --version_2_with_negative)
export TASK_NAME=qa

# hyperparameters
export SEED=42
export BATCH_SIZE=32
export MAX_SEQ_LENGTH=384
export NUM_TRAIN_EPOCHS=5
export WEIGHT_DECAY=0.0
export LEARNING_RATE=5e-5
export LR_SCHEDULER_TYPE=linear
export WARMUP_RATIO=0.0
export NUM_WARMUP_STEPS= 365
export DOC_STRIDE=128
export OPTIMIZER=adamw_hf # adamw_hf, adamw_torch, adamw_torch_fused, adamw_torch_xla, adamw_apex_fused, adafactor, adamw_anyprecision, sgd, adagrad
export LOGGING_STRATEGY=epoch  # no, steps, epoch 
export EVALUATION_STRATEGY=epoch # no, steps, epoch 
export SAVE_STRATEGY=epoch  # no, steps, epoch 
export SAVE_TOTAL_LIMIT=1
export KEEP_ACCENTS=True
export DO_LOWER_CASE=True

# other parameters
export RUN_NAME=finetuning
export REPORT_TO=mlflow

export ENABLE_FP16=True
export ENABLE_BF16=False
export ENABLE_IPEX=False

export OUTPUT_DIR=artifacts/$TASK_NAME/$DATASET_NAME/$BACKBONE_NAME
export RUN_NAME=$BACKBONE_NAME-$DATASET_NAME-$TASK_NAME-$SEED

python run_qa_finetune.py \
  --do_train \
  --do_eval \
  --overwrite_output_dir \
  --model_name_or_path $MODEL_NAME_OR_PATH \
  --dataset_name $DATASET_NAME \
  --logging_strategy $LOGGING_STRATEGY \
  --evaluation_strategy $EVALUATION_STRATEGY \
  --save_strategy $SAVE_STRATEGY \
  --save_total_limit $SAVE_TOTAL_LIMIT \
  --keep_accents $KEEP_ACCENTS \
  --do_lower_case $DO_LOWER_CASE \
  --optim $OPTIMIZER \
  --weight_decay $WEIGHT_DECAY \
  --per_device_train_batch_size $BATCH_SIZE \
  --per_device_eval_batch_size $BATCH_SIZE \
  --gradient_accumulation_steps 1 \
  --learning_rate $LEARNING_RATE \
  --lr_scheduler_type $LR_SCHEDULER_TYPE \
  --warmup_ratio $WARMUP_RATIO \
  --warmup_steps $NUM_WARMUP_STEPS \
  --num_train_epochs $NUM_TRAIN_EPOCHS \
  --max_seq_length $MAX_SEQ_LENGTH \
  --doc_stride $DOC_STRIDE \
  --seed $SEED \
  --output_dir $OUTPUT_DIR \
  --run_name $RUN_NAME \
  --report_to $REPORT_TO \
  --fp16 $ENABLE_FP16 \
  --bf16 $ENABLE_BF16 \
  --use_ipex $ENABLE_IPEX