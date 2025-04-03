import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
data = pd.read_csv('participation_data.csv')

def generate_word_cloud(track):
    """Generate a word cloud for the specified track."""
    feedback = data[data['Track'] == track]['Feedback']
    text = ' '.join(feedback)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Word Cloud for {track}')
    plt.show()

def text_similarity(track):
    """Calculate text similarity for feedback within the specified track."""
    feedback = data[data['Track'] == track]['Feedback']
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(feedback)
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    return similarity_matrix

# Example usage
if __name__ == "__main__":
    track = 'Track A'  # Example track
    generate_word_cloud(track)
    similarity = text_similarity(track)
    print(f"Similarity matrix for {track}:\n{similarity}")
