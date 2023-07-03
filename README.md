## TEAM NAME : BYTE404
## CHALLENGE NAME: OPEN INNOVATION IN EDUCATION 
## TEAM LEADER EMAIL: angeloantu@gmail.com


# LearnMateAI : Personalized Learning with Intel oneAPI Optimization 🤖💪

`LearnMateAI is an optimized personalized AI tutor that enhances the learning experience by leveraging the power of Intel oneAPI`. It utilizes cutting-edge techniques such as natural language processing, machine learning, and the Ebbinghaus forgetting curve, ``all optimized using Intel oneAPI``, to create a tailored and high-performance learning journey. 🎓💡

## Working Demo :

[Live Website](https://intel-hack.pages.dev/)

[Working Video](https://www.youtube.com/watch?v=8zTPxmDi10U)

[Medium.com](https://medium.com/@abdullasameer118/learnmateai-personalized-learning-with-intel-oneapi-optimization-1eb2195403da)

## Installation :
#### Installation of Backend:
// preferably use a virtual environment.[use this to create virtual environment in python](https://docs.python.org/3/library/venv.html)
RUN python3 -m pip install --upgrade pip

RUN yum install -y poppler-utils

RUN  pip3 install -r iteration1_requirements.txt

RUN  pip3 install -r iteration2_requirements.txt

RUN  pip3 install -r iteration3_requirements.txt

#### Installation of Frontend:

RUN npm install

RUN npm start

## Optimisation Table :
![Screenshot 2023-07-02 153834](https://github.com/ANGELOANTU7/intel-oneAPI/assets/94218410/770a1e77-eda9-426f-aec9-f907dfc47dc2)

![Screenshot 2023-07-02 153920](https://github.com/ANGELOANTU7/intel-oneAPI/assets/94218410/bc947e72-c9c7-4c70-9b6a-687943d3d604)

## Introduction :

In today’s fast-paced world, effective and efficient learning is crucial for students to excel academically. With advancements in technology, artificial intelligence (AI) has revolutionized the education sector. LearnMateAI takes personalized learning to the next level by providing students with an efficient and effective learning experience. By harnessing the power of AI and Intel oneAPI, LearnMateAI delivers a personalized learning plan tailored to each student's needs. 📚🔬

## Core Modules using Intel used in the project :
### #Summariser  
This module is used to convert the notes and other handwritten notes provided by the user to meaningful summaries. The summaries are created based on the topics extracted from the notes and provided lectures and the syllabus provided by the user. This module uses [Intel Optimised Tensorflow]
(https://www.intel.com/content/www/us/en/developer/tools/oneapi/optimization-for-tensorflow.html#gs.2mtgor) & hugging face api's transformer models(Models for NLP) for the summarisation. The summarisation part is optimised with the help of [Intel's Optimization for Transformer Models.]
(https://www.intel.com/content/www/us/en/developer/videos/optimize-end-to-end-transformer-model-performance.html#gs.2muun9) 

### #PYQSorter
This module is used to group previous year questions into modules based on the syllabus provided by the user. Each question paper is cleaned of noises and other unwanted characters. Questions are extracted from the preprocessed data and passed into the [universal sentence encoder module](https://tfhub.dev/google/universal-sentence-encoder-large/5) which returns the embeddings of the questions. With the Kmeans model is used to cluster the questions based on the similarity and finally gets a module wise sorted questions. The process of clustering and sorting the question paper is made efficient and more optimised with [Intel Extension for Scikit Learn.]
(https://www.intel.com/content/www/us/en/developer/tools/oneapi/scikit-learn.html#gs.2mw28j) This imporved performace of our sorter by 25 percentage.

USING INTEL ONEAPI TOOLKITS
![Screenshot 2023-07-02 150906](https://github.com/ANGELOANTU7/intel-oneAPI/assets/94218410/43ace56f-99ae-4311-8a28-d970e485998d)
WITHOUT USING INTEL ONEAPI TOOLKITS
![Screenshot 2023-07-02 150114](https://github.com/ANGELOANTU7/intel-oneAPI/assets/94218410/f77a75f4-5c7e-4db7-981c-9a37802243b5)


### #Video Recommender
This module helps to imporve the learning experience by giving the user the most apt youtube video about the topic the user is currently learning. The video suggestion is done by a series of steps,
first a series of videos is fetched in related to the topic the user is learning, the transcript of the video is also extracted. The embeddings of the transcripts are generated with "bert-base-nli-mean-tokens" which is a sentence encoder model. Then these are compared with the embedding of the summary of the topic which the user is learning with the help of COSINE SIMILARITY which is optimised with [Intel Extension for Scikit-Learn.](https://www.intel.com/content/www/us/en/developer/tools/oneapi/scikit-learn.html). The module is further optmised with the help of [PyTorch Optimizations from Intel.](https://www.intel.com/content/www/us/en/developer/tools/oneapi/optimization-for-pytorch.html#gs.2mu8s1)
USING INTEL ONEAPI TOOLKITS
![Screenshot 2023-07-02 151355](https://github.com/ANGELOANTU7/intel-oneAPI/assets/94218410/41f839b3-f986-498b-8ce8-cde775cdfa0e)

WITHOUT USING INTEL ONEAPI TOOLKITS
![Screenshot 2023-07-02 151610](https://github.com/ANGELOANTU7/intel-oneAPI/assets/94218410/c12d5325-d6f8-4b6e-af98-972ac46576be)





### #Retention Curve Analyzer
This module is used to access the ability of the user to retain information. This is accessed by giving the user a series of test under non-revised conditions so that it is much easier to acess the retention ability of the user. Panda dataframes are used for storing the coordinate of the learning curve, mathplot and scipy are used to smoothen and plot the curve. The pandas is further optimised with [Intel® Distribution of Modin](https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-of-modin.html#gs.2mxbo0) 
<img src="https://i.ibb.co/41HCFS3/Screenshot-7.png" alt="Screenshot-7" border="0" />
USING INTEL ONEAPI TOOLKITS
![Screenshot 2023-07-02 145858](https://github.com/ANGELOANTU7/intel-oneAPI/assets/94218410/0d032729-4c44-4bb3-9984-1ea85aea9440)
WITHOUT USING INTEL ONEAPI TOOLKITS
![Screenshot 2023-07-02 145446](https://github.com/ANGELOANTU7/intel-oneAPI/assets/94218410/3168e7d6-696a-4a06-9cd7-7b0346446c29)



### #Study Planner 
This module creates a systematic learning path tailor made for that specific user based on the time period in which the user wants to learn the topics. This is integrated with google calender for reminding the user to study accordingly and follow the learning path.

### #Mock Question Paper Generator
This module is used to analyse the previous year question papers which in turn analyse the trends followed in the question paper, the marking scheme and which all topics have greater weightage. Based on the information a model question paper is generated to make the user more familiar with the expected model of the question paper yet to be attended. This also provides an idea about how questions are repeated and how similar questions are appearing in the question paper which helps the user to focus more on those areas.

## Key Features :

#### Understanding the Student’s Needs:

LearnMateAI analyzes the subject area using teacher’s notes and previous year question papers, identifying important topics and concepts specific to each student. 🗓️📝

#### Personalized Learning Schedule: 

The system generates a customized learning schedule based on the student's proficiency level, learning preferences, and time constraints. 🎓💡

#### Engaging and Responsive Learning Experience: 

LearnMateAI enables students to ask questions, seek clarification, and receive immediate feedback, creating an interactive learning environment. 🗣️💬

#### Continuous Performance Monitoring and Improvement: 

The system continuously tracks and analyzes the student's performance and progress, ensuring optimal learning outcomes. 📊🔍


