### Team Name - C5ailabs
### Problem Statement - Open Innovation in Education
### Team Leader Email - rohit.sroch@course5i.com

<hr>

# LEAP

Intel Hackathon Prototype Implementation for our LEAP Platform

## A Brief of the Prototype:

#### INSPIRATION ![image](https://user-images.githubusercontent.com/72274851/218500470-ec078b99-0a50-4b06-a2df-c09e47ecc187.png)


MOOCs (Massive Open Online Courses) have surged in popularity in recent years, particularly during the COVID-19 pandemic. These
online courses are typically free or low-cost, making education more accessible worldwide.

- Online learning is crucial for students even post-pandemic due to its flexibility, accessibility, and quality. But still, the learning experience
  for students is not optimal, as in case of doubts they need to repeatedly go through videos and documents or ask in the forum which may
  not be effective because of the following challenges:

  - Resolving doubts can be a time-consuming process.
  - It can be challenging to sift through pile of lengthy videos or documents to find relevant information.
  - Teachers or instructors may not be available around the clock to offer guidance

- To mitigate the above challenges, we propose LEAP (Learning Enhancement and Assistance Platform), which is an AI-powered
  platform designed to enhance student learning outcomes and provide equitable access to quality education. The platform comprises two main features that aim to improve the overall learning experience of the student:

#### Our Proposed Solution ![image](https://user-images.githubusercontent.com/72274851/218503394-b52dfcc9-0620-4f44-94f5-46a09a5cc970.png)

LEAP stands for Learning Enhancement and Assistance Platform:

❑ Ask Question/Doubt: This allows the students to ask real-time questions around provided reading material, which includes videos and
documents, and get back answers along with the exact timestamp in the video clip containing the answer (so that students don’t have to
always scroll through). Also, It supports asking multilingual question, ensuring that language barriers do not hinder a student's learning
process.

❑ Interactive Conversational AI Examiner: This allows the students to evaluate their knowledge about the learned topic through an AI
examiner conducting viva after each learning session. The AI examiner starts by asking question and always tries to motivate and provide
hints to the student to arrive at correct answer, enhancing student engagement and motivation.

## Detailed LEAP Process Flow:

![](./assets/Process-Flow.png)

## Tech Stack:

  - Intel® oneAPI (Intel® AI Analytics Toolkit)  Tech Stack

  ![](./assets/Intel-Tech-Stack.png)

    1. Intel® Extension for Pytorch: Used for Multilingual Extractive QA model training optimization.
    2. Intel® Neural Compressor: Used for Multilingual Extractive QA model inference and Generative AI model inference optimization.
    3. Intel® Extension for Scikit-Learn: Used for Multilingual Embedding model training optimization.
    4. Intel® distribution for Modin: Used for basic initial data analysis/EDA.
    5. Intel® optimized Python: Used for data pre-processing, reading etc.

  - Base Tech Stack

  ![](./assets/Tech-Stack.png)

## Step-by-Step Code Execution Instructions:

a) Easy Option to Start Demo

- Clone the Repository
```console
 $ git clone https://github.com/rohitc5/intel-oneAPI/tree/main
 $ cd Intel-oneAPI

```
- Start the LEAP RESTFul Service to consume both components (Ask Question/Doubt and Interactive Conversational AI Examiner) over API

```console
  $ cd api
  
  # build the docker file
  $ docker build -t leap-api:v1 .  

  # get the docker image ID
  $ docker images

  # run the docker container
  $ docker run -it -p 8500:8500 --name=leap-api [IMAGE_ID]

  $ cd ../

```

- Start the demo webapp build using streamlit

```console
  $ cd webapp
  
  # build the docker file
  $ docker build -t leap-demo:v1 .

  # get the docker image ID
  $ docker images

  # run the docker container
  $ docker run -it -p 8502:8502 --name=leap-demo [IMAGE_ID]

```

b) Step-by-Step Option

- Clone the Repository

```console
 $ git clone https://github.com/rohitc5/intel-oneAPI/tree/main
 $ cd Intel-oneAPI

```

- Train/Fine-tune the Extractive QA Multilingual Model (Part of our Ask Question/Doubt Component).
Please note that, by default we use this (https://huggingface.co/ai4bharat/indic-bert) as a Backbone (BERT topology)
and finetune it on SQuAD v1 dataset. Moreover, IndicBERT is a multilingual ALBERT model pretrained exclusively on 12 major Indian languages. It is pre-trained on novel monolingual corpus of around 9 billion tokens and subsequently evaluated on a set of diverse tasks. So finetuning, on SQuAD v1 (English) dataset automatically results in cross-lingual
transfer on other 11 indian languages.

Here is the detailed architecture of `Ask Question/Doubt` component:

![](./assets/Ask-Doubt.png)

```console
  $ cd nlp/question_answering

  # install dependencies
  $ pip install -r requirements.txt
  
  # modify the fine-tuning params mentioned in finetune_qa.sh
  $ vi finetune_qa.sh

  ''''
  export MODEL_NAME_OR_PATH=ai4bharat/indic-bert
  export BACKBONE_NAME=indic-mALBERT-base
  export DATASET_NAME=squad # squad, squad_v2 (pass --version_2_with_negative)
  export TASK_NAME=qa

  # hyperparameters
  export SEED=42
  export BATCH_SIZE=32
  export MAX_SEQ_LENGTH=512
  export NUM_TRAIN_EPOCHS=5
  ...
  
  ''''

  # start the training after modifying params
  $ bash finetune_qa.sh
```

- Optimize using IPEX, Intel® Neural Compressor and run the bennchmark for comparison with Pytorch(Base)-FP32

```console
  # modify the params in pot_benchmark_qa.sh
  $ vi pot_benchmark_qa.sh

  ''''
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

  export TUNE=True  # whether to tune or not
  export PTQ_METHOD="static_int8" # "dynamic_int8", "static_int8", "static_smooth_int8"
  export BACKEND="default" # default, ipex
  export ITERS=100
  ...

  ''''
  
  $ bash pot_benchmark_qa.sh

  Please note that, above shell script can perform optimization using IPEX to get Pytorch-(IPEX)-FP32 model
  or It can perform optimization/quantization using Intel® Neural Compressor to get Static-QAT-INT8, 
  Static-Smooth-QAT-INT8 models. Moreover, you can choose the backend as `default` or `ipex` for INT8 models.

```

- Run quick inference to test the model output

```console
  $ python run_qa_inference.py --model_name_or_path=[FP32 or INT8 finetuned model]  --model_type=["vanilla_fp32" or "quantized_int8"] --do_lower_case  --keep_accents --ipex_enable

```

- Train/Infer/Benchmark TFIDF Embedding model for Scikit-Learn (Base) vs Intel® Extension for Scikit-Learn

```console
  $ cd nlp/feature_extractor

  # train (.fit_transform func), infer (.transform func) and perform benchmark
  $ python run_benchmark_tfidf.py --course_dir=../../dataset/courses --is_preprocess 
  
  # now rerun but turn on  Intel® Extension for Scikit-Learn
  $ python run_benchmark_tfidf.py --course_dir=../../dataset/courses --is_preprocess  --intel_scikit_learn_enabled
```

- Setup LEAP API

```console
  $ cd api
  
  # install dependencies
  $ pip install -r requirements.txt

  $ cd src/

  # create a local vector store of course content for faster retrieval during inference
  # Here we get semantic or syntactic (TFIDF) embedding of each content from course and index it.
  $ python core/create_vector_index.py --course_dir=../../dataset/courses --emb_model_type=[semantic or syntactic] \
      --model_name_or_path=[Hugging face model name for semantic] --keep_accents
  
  # update config.py
  $ cd ../ 
  $ vi config.py 
  
  ''''
    ASK_DOUBT_CONFIG = {
      # hugging face BERT topology model name
      "emb_model_name_or_path": "ai4bharat/indic-bert", 
      "emb_model_type": "semantic",  #options: syntactic, semantic
      
      # finetuned Extractive QA model path previously done
      "qa_model_name_or_path": "vanichandna/indic-bert-finetuned-squad", 
      "qa_model_type": "vanilla_fp32",  #options: vanilla_fp32, quantized_int8
      
      # faiss index file path created previously
      "faiss_vector_index_path": "artifacts/index/faiss_emb_index"
    }
    ...

  ''''

```

- For our Interactive Conversational AI Examiner component, as of now we are not doing any training as its based on 
recent Generative AI LLM (Large Language model) (open access models like LLaMA, Falcon etc.). You can update the API configuration by specifying hf_model_name (LLM name available in huggingface Hub). Please checkout https://huggingface.co/models

Here for performance gain, we can use INT8 quantized model optimized using Intel®  Neural Compressor (Few options are like https://huggingface.co/decapoda-research/llama-7b-hf-int8 etc.)  

Please Note that for fun 😄, we also provide usage of Azure OpenAI Cognitive Service to use models like GPT3 paid subscription API. You just need to provide `azure_deployment_name` below configuration and `<your_key>`

```console

  AI_EXAMINER_CONFIG = {
      "llm_name": "azure_gpt3",
      "azure_deployment_name": "text-davinci-003-prod",
      "hf_model_name": "TheBloke/falcon-7b-instruct-GPTQ", # mosaicml/mpt-7b-instruct
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
```

- Start the API server

```console
  $ cd api/src/
  
  # start the gunicorn server
  $ bash start.sh
```

- Start the Streamlit web UI demo

```console
  $ cd webapp

  # install dependencies
  $ pip install -r requirements.txt

  $ streamlit run app.py

```

- Go to http://localhost:8502

# Benchmark Results with Intel® oneAPI AI Analytics Toolkit

- We have already added several benchmark results to compare how beneficial Intel® oneAPI AI Analytics Toolkit is compared to baseline. Please go to`benchmark` folder to view the results.
  
# What I learned ![image](https://user-images.githubusercontent.com/72274851/218499685-e8d445fc-e35e-4ab5-abc1-c32462592603.png)


![image](https://user-images.githubusercontent.com/72274851/220130227-3c48e87b-3e68-4f1c-b0e4-8e3ad9a4805a.png)

✅ Building application using Intel® AI Analytics Toolkit: The Intel® AI Analytics Toolkit gives data scientists, AI developers, and researchers familiar Python* tools and frameworks to accelerate end-to-end data science and analytics pipelines on Intel® architecture. The components are built using oneAPI libraries for low-level compute optimizations. This toolkit maximizes performance from preprocessing through deep learning, machine learning, and provides interoperability for efficient model development.

✅ Easy to Adapt: The Intel® AI Analytics Toolkit requires minimal changes to adapt to a machine learning, deep learning workloads.

✅Collaboration: Building a project like this likely required collaboration with a team of experts in various fields, such as deep learning, and data analysis, and I likely learned the importance of working together to achieve common goals.

These are just a few examples of the knowledge and skills that i likely gained while building this project. 
Overall, building a helpful platform like LEAP is a challenging and rewarding experience that requires a combination of technical expertise and agricultural knowledge.