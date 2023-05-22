import openai
import requests
from bs4 import BeautifulSoup
import os,shutil
from urllib.parse import urlparse, urljoin



openai.api_key = "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"

# Process each paragraph and search for related images
def process_paragraphs(paragraphs):
    # Create the "images" directory if it doesn't exist
    if not os.path.exists("images"):
        os.makedirs("images")
    for query in paragraphs:
        image_url = search_image(query)
        if image_url:
            # Download the image and save it locally
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(f"images/image_{query}.jpg", 'wb') as f:
                    f.write(response.content)
                    print(f"Image_{query}.jpg saved.")

def search_image(query):
    url = f"https://www.google.com/search?q={query}&tbm=isch&tbs=isz:l"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_elements = soup.find_all('img')
    image_url = None
    if len(image_elements) > 1:
        image_url = image_elements[1].get('src')
        if image_url:
            parsed_url = urlparse(image_url)
            if not parsed_url.scheme:
                base_url = response.url
                image_url = urljoin(base_url, image_url)
    return image_url


def extract_text_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

def extract_important_topics(questions):
    text = questions
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"You are a teacher, who will take a Topic to a student. I will provide you with a basic summary of the student's lecture note, which may be a bit incomplete, but you have to use it and interact with the student and make sure they understand it fully. Basically, you have to narrate (everything should be text):\n\n{text}\n\n"
            }
        ]
    )

    important_topics = response.choices[0].message.content
    print(important_topics)
    return important_topics


def extract_image_name(questions):
    text = questions
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"create a word for each paragraph as a list\n\n{text}\n\n"
            }
        ]
    )

    important_topics = response.choices[0].message.content
    print(important_topics)
    return important_topics

print("Giving promt to OPENAI...")
file_path = 'Files\generated_files\summarised_notes\module1_summarized.txt'
extracted_text = extract_text_from_file(file_path)
narrate = extract_important_topics(extracted_text)

print(narrate)
# Save topics to topics.txt
with open('Files\generated_files\\narration.txt', 'w', encoding='utf-8') as file:
    file.write(narrate)

image_name=extract_image_name(narrate)
image_list = image_name.splitlines()

# Create a directory to store the images
os.makedirs("images", exist_ok=True)
os.chdir("images")

# Process the paragraphs and search for related images
print(image_list)
process_paragraphs(image_list)

# Return to the parent directory
os.chdir("..")

while(True):
    with open('Files\generated_files\\response.txt', 'r',encoding='utf-8') as file:
        content = file.read()
    if len(content)==0:
        continue
    else:
        if content == "understood":
            break
        if content[0]==".":
            narrate = extract_important_topics(content)
            with open('Files\generated_files\\narration.txt', 'w', encoding='utf-8') as file:
                file.write(narrate)
            print(narrate)
            with open('Files\generated_files\\response.txt', 'w') as file:
                # Truncate the file to remove its contents
                file.truncate()
            shutil.rmtree("images")


            image_name=extract_image_name(narrate)
            image_list = image_name.splitlines()

            # Create a directory to store the images
            os.makedirs("images", exist_ok=True)
            os.chdir("images")

            # Process the paragraphs and search for related images
            print(image_list)
            process_paragraphs(image_list)

            # Return to the parent directory
            os.chdir("..")
