import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import openai
import io
import boto3
from fastapi import APIRouter
from fastapi.responses import FileResponse
import requests
import base64


PDFSHIFT_API_KEY = 'f894dbd8a6074a0db44439561e73c0e3'
AWS_ACCESS_KEY_ID = 'AKIAZTHHIOR4JJ5HLTUB'
AWS_SECRET_ACCESS_KEY = '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'
AWS_S3_BUCKET_NAME = 'learnmateai'


# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Set up OpenAI API credentials
openai.api_key = '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'



# Step 1: Data Preparation
data = {
    'Topic': ['Math', 'Science', 'History', 'English', 'Geography', 'Physics', 'Chemistry', 'Biology', 'Computer Science', 'Art'],
    'Topics Progress': [10, 8, 12, 9, 11, 15, 13, 10, 14, 12],
    'Test Result': [80, 65, 90, 75, 85, 92, 87, 78, 88, 83]
}

# Step 2: Data Loading
df = pd.DataFrame(data)

# Set up FastAPI
app = APIRouter()

@app.get("/progress_report")
def get_data():
    # Step 3: Data Analysis and Visualization
    # Distribution of Topics Progress
    plt.figure(figsize=(10, 5))
    sns.histplot(data=df, x='Topics Progress', bins=10, kde=True)
    plt.xlabel('Topics Progress')
    plt.ylabel('Frequency')
    plt.title('Distribution of Topics Progress')
    plt.xticks(df['Topics Progress'], df['Topic'], rotation='vertical')
    topics_progress_buffer = io.BytesIO()
    plt.savefig(topics_progress_buffer, format='png')
    plt.close()
    topics_progress_buffer.seek(0)  # Reset the buffer pointer to the beginning

    # Test Results Distribution
    plt.figure(figsize=(10, 5))
    sns.histplot(data=df, x='Test Result', bins=10, kde=True)
    plt.xlabel('Test Result')
    plt.ylabel('Frequency')
    plt.title('Distribution of Test Results')
    plt.xticks(df['Test Result'], df['Topic'], rotation='vertical')
    test_results_buffer = io.BytesIO()
    plt.savefig(test_results_buffer, format='png')
    plt.close()
    test_results_buffer.seek(0)  # Reset the buffer pointer to the beginning

    # Correlation between Topics Progress and Test Results
    plt.figure(figsize=(10, 5))
    sns.scatterplot(data=df, x='Topics Progress', y='Test Result', hue='Topic')
    plt.xlabel('Topics Progress')
    plt.ylabel('Test Result')
    plt.title('Correlation between Topics Progress and Test Results')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(df['Topics Progress'], df['Topic'], rotation='vertical')
    correlation_buffer = io.BytesIO()
    plt.savefig(correlation_buffer, format='png')
    plt.close()
    correlation_buffer.seek(0)  # Reset the buffer pointer to the beginning

    # Step 4: Generating Recommendations
    # Prepare the input prompt for the language model
    prompt = f"{df.to_string(index=False)}\n\nThis is the progress data of the student. Topics Progress indicates the percentage of progress in each topic, and Test Result represents the performance in tests. Based on this data, provide some recommendations to the student."

    # Generate recommendations using the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Print the recommendations
    print("Recommendations:")
    recommendations = response.choices[0].message.content

    # Convert images to base64 encoded strings
    topics_progress_base64 = base64.b64encode(topics_progress_buffer.getvalue()).decode()
    test_results_base64 = base64.b64encode(test_results_buffer.getvalue()).decode()
    correlation_base64 = base64.b64encode(correlation_buffer.getvalue()).decode()

    # Create PDF using PDFShift
    pdf_data = f'''
    <html>
    <head>
        <style>
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                font-family: Arial, sans-serif;
            }}
            h1 {{
                font-size: 24px;
                margin-bottom: 10px;
            }}
            p {{
                font-size: 16px;
                line-height: 1.5;
                margin-bottom: 20px;
            }}
            img {{
                max-width: 100%;
                height: auto;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Recommendations:</h1>
            <p>{recommendations}</p>
            <h1>Analysis:</h1>
            <img src="data:image/png;base64,{base64.b64encode(topics_progress_buffer.getvalue()).decode()}" />
            <img src="data:image/png;base64,{base64.b64encode(test_results_buffer.getvalue()).decode()}" />
            <img src="data:image/png;base64,{base64.b64encode(correlation_buffer.getvalue()).decode()}" />
        </div>
    </body>
    </html>
    '''

    pdf_response = requests.post(
    'https://api.pdfshift.io/v3/convert/pdf',
    auth=('api', PDFSHIFT_API_KEY),
    json={'source': pdf_data, "landscape": False, "use_print": False}
    )
    
    pdf_bytes = pdf_response.content




    # Save PDF to a buffer
    pdf_buffer = io.BytesIO(pdf_bytes)

    # Return the base64 encoded images, recommendations, and PDF
    return {
        'topics_progress': topics_progress_base64,
        'test_results': test_results_base64,
        'correlation': correlation_base64,
        'recommendations': recommendations,
        'pdf': base64.b64encode(pdf_buffer.getvalue()).decode()
    }