import argparse
import os
import webvtt
import modein.pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from glob import glob

def read_subtitle_vtt(subtitle_fpaths):

    subtitle_data = []
    for subtitle_fpath in subtitle_fpaths:
        subtitles = webvtt.read(subtitle_fpath)
        for idx, caption in enumerate(subtitles):
            subtitle_data.append([idx, caption.text])

    df = pd.DataFrame(subtitle_data, columns=['index', 'caption_text'])

    return df

def extract_top_phrases_tfidf(df, text_column):
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 1), max_df=0.5, min_df=0.005)
    df = df[df[text_column].notna()]
    df[text_column] = df[text_column].astype(str).str.lower()
    text_data = df[text_column].values
    tfidf_matrix = vectorizer.fit_transform(text_data).toarray()
    df_top_phrases = pd.DataFrame(tfidf_matrix, columns=vectorizer.get_feature_names_out())
    top_phrases = df_top_phrases.astype(bool).sum(axis=0).sort_values(ascending=False).index
    df_top_phrases = df_top_phrases.astype(bool).sum(axis=0).sort_values(ascending=False)

    return df_top_phrases, top_phrases, df

def generate_wordcloud(phrase_counts):
    if len(phrase_counts) > 100:
        wc = WordCloud(
            width=800, height=400, max_words=100, background_color="white").generate_from_frequencies(
                phrase_counts[0:100])
    else:
        wc = WordCloud(
            width=800, height=400, max_words=100, background_color="white").generate_from_frequencies(
                phrase_counts[0:len(phrase_counts)])
    plt.figure(figsize=(10, 20))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    
    return plt

def main(args):

    path = os.path.join(args.course_dir, "*/Study-Material/*/*/*.vtt")
    subtitle_fpaths = glob(path)

    df = read_subtitle_vtt(subtitle_fpaths)

    phrase_counts, _, _ = extract_top_phrases_tfidf(df, 'caption_text')
    wordcloud = generate_wordcloud(phrase_counts)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Perform Basic EDA on given dataset')
    parser.add_argument(
        "--course_dir",
        type=str,
        help="base directory containing courses",
        default="dataset/courses"
    )
    
    args = parser.parse_args()
    main(args)

