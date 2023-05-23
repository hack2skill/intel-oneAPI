## How to Run the Application
To run the Tutor AI application, follow these steps:


1. Set up a virtual environment (recommended) and activate it.
```bash
   virtualenv <your_name>_venv 
   .\<your_name>_venv\Scripts\activate
```
5. Install the required dependencies by running the following command:
```bash
   pip install -r <person>_requirements.txt  #example angelo_requirements.txt
```
6. Once the dependencies are installed, you can start the application by running the following command:
```bash
   uvicorn main:app --reload
```
7. The application will start running locally on your machine.
8. Access the application by opening a web browser and navigating to 
    `http://localhost:8000`.

## API Calls ready

Pyqsorter (takes pyqs text files and syllabus text files from Local Storage and saves output to Generated_files as cluster_question.txt) : `http://localhost:8000/api1`

Notes_Analyser (takes txt from gpt_propt_sum and saves output to Notes_Analyser_Ouput) : `http://localhost:8000/api4`

## Pending tasks

| Task | Type     | Discription                |Input                | Output Expected              |
| :-------- | :------- |  :------------------------- |:------------------------- |:------------------------- |
| `QuestionPaperGenerator` | `API` |  generate atleast 5 question paper , following format of PYQS  |  you can decide               |       atleast 5 paper inside`Local_Storage/Generated_Files/GenQP`         | 

## Completed tasks

#### Harshed Abdulla

| Task | Type     | File Location                |Input                | Output              |
| :-------- | :------- |  :------------------------- |:------------------------- |:------------------------- |

#### Heyron J Milton

| Task | Type     | File Location                |Input                | Output              |
| :-------- | :------- |  :------------------------- |:------------------------- |:------------------------- |

#### Abdulla Sameer

| Task | Type     | File Location                |Input                | Output              |
| :-------- | :------- |  :------------------------- |:------------------------- |:------------------------- |

#### Angelo Antu

| Task | Type     | File Location                |Input                | Output              |
| :-------- | :------- |  :------------------------- |:------------------------- |:------------------------- |
| `Pyqsorter` | `API` |  `Backend\pyqsorter.py`  |  `Local_Storage/pyqs_text`,`Local_Storage/syllabus.txt`               |       `Local_Storage/Generated_Files/cluster_questions.txt`         | 
| `Notes_Analyser` | `API` |  `Backend\Notes_Analyser.py`  |  `Local_Storage/Generated_Files/gpt_promt_sum/module2.txt`           |       `Local_Storage/Generated_Files/Notes_Analyser_Ouput_files/topic_list.txt`,`Local_Storage/Generated_Files/Notes_Analyser_Ouput_files/imp_topic_list.txt`,`Local_Storage/Generated_Files/Notes_Analyser_Ouput_files/notes_questions_list.txt`         | 
