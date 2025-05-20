from sentence_transformers import SentenceTransformer, util
import numpy as np
import textstat
from sklearn.metrics.pairwise import cosine_similarity


# Load sentence transformer model (lightweight for fast testing)
model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_embedding(text):
    return model.encode(text, convert_to_tensor=True)

def compute_similarity_score(article, synopsis):
    article_embedding = compute_embedding(article)
    synopsis_embedding = compute_embedding(synopsis)
    similarity = util.pytorch_cos_sim(article_embedding, synopsis_embedding).item()
    return similarity * 50  # Scale to 50

def compute_clarity_score(synopsis):
    # Use textstat to compute readability; higher is better
    flesch = textstat.flesch_reading_ease(synopsis)
    # Normalize to 25 points
    score = min(max((flesch / 100) * 25, 0), 25)
    return score

def compute_coherence_score(synopsis):
    tokens = synopsis.split()
    embeddings = compute_embedding(tokens)
    similarities = []
    for i in range(len(embeddings) - 1):
        sim = cosine_similarity([embeddings[i]], [embeddings[i + 1]])[0][0]
        similarities.append(sim)
    coherence_score = np.max(similarities)
    return coherence_score*25 # Out of 25

def evaluate_synopsis(article, synopsis):
    similarity_score = compute_similarity_score(article, synopsis)
    clarity_score = compute_clarity_score(synopsis)
    coherence_score = compute_coherence_score(synopsis)

    total_score = similarity_score + clarity_score + coherence_score

    breakdown = {
        'Total Score': round(total_score, 2),
        'Content Coverage': round(similarity_score, 2),
        'Clarity': round(clarity_score, 2),
        'Coherence': round(coherence_score, 2)
    }

    return breakdown

if __name__ == '__main__':
    article = "Artificial intelligence is transforming industries such as healthcare and finance."
    synopsis = "AI is changing sectors like healthcare and finance."
    print(evaluate_synopsis(article, synopsis))
    print(compute_clarity_score(synopsis=synopsis))
