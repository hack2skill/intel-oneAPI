import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

# Step 1: Preprocessing
def preprocess_notes(notes):
    # Perform any necessary preprocessing steps here
    preprocessed_notes = []
    for note in notes:
        # Apply preprocessing to each note
        # Example: Convert to lowercase, remove punctuation, etc.
        preprocessed_notes.append(note.lower())
    return preprocessed_notes

# Step 2: Document-Term Matrix
def create_document_term_matrix(preprocessed_notes):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(preprocessed_notes)
    return X

# Step 3: Apply LSA
def apply_lsa(X, number_of_topics):
    lsa = TruncatedSVD(n_components=number_of_topics)
    lsa_representation = lsa.fit_transform(X)
    return lsa_representation

# Step 4: Topic Extraction
def extract_topics(lsa_representation, notes):
    topic_wise_notes = {}
    for i, note in enumerate(notes):
        topic = lsa_representation[i].argmax()
        if topic not in topic_wise_notes:
            topic_wise_notes[topic] = []
        topic_wise_notes[topic].append(note)
    return topic_wise_notes

# Main code
def main():
    # Input: List of notes
    your_notes_list = [
        "Note 1",
        "Note 2",
        "Note 3",
        # Add more notes as needed
    ]
    
    # Set the number of topics for LSA
    number_of_topics = 3
    
    # Step 1: Preprocessing
    preprocessed_notes = preprocess_notes(your_notes_list)
    
    # Step 2: Document-Term Matrix
    X = create_document_term_matrix(preprocessed_notes)
    
    # Step 3: Apply LSA
    lsa_representation = apply_lsa(X, number_of_topics)
    
    # Step 4: Topic Extraction
    topic_wise_notes = extract_topics(lsa_representation, your_notes_list)
    
    # Print the topic-wise notes
    for topic, notes in topic_wise_notes.items():
        print(f"Topic {topic}:")
        for note in notes:
            print(note)
        print()

# Execute the main function
main()
