import math
from collections import defaultdict
from global_var import nba_shots

class TFIDFSearch:
    def __init__(self):
        self.shot_texts = []
        self.term_frequency = []
        self.inverse_document_frequency = defaultdict(float)
        self.TF_IDF_matrix = []

    def preprocessData(self):
        """Prepare text data for TF-IDF computation."""
        self.shot_texts = []
        for shot in nba_shots:
            shot_text = (
                f"{shot.player_name} {shot.event_type} {shot.shot_type} "
                f"{shot.basic_zone} {shot.zone_name} {shot.action_type}"
            )
            self.shot_texts.append(shot_text)

    def compute_TF_IDF(self):
        """Calculate TF-IDF scores for all shots."""
        # Step 1: Calculate Term Frequencies (TF)
        for text in self.shot_texts:
            term_count = defaultdict(int)
            words = text.lower().split()
            for word in words:
                term_count[word] += 1
            self.term_frequency.append(term_count)

        # Step 2: Calculate Document Frequencies (DF) and Inverse Document Frequencies (IDF)
        document_count = len(self.shot_texts)
        for tf in self.term_frequency:
            for term in tf.keys():
                self.inverse_document_frequency[term] += 1

        for term, count in self.inverse_document_frequency.items():
            self.inverse_document_frequency[term] = math.log(document_count / (1 + count))

        # Step 3: Compute TF-IDF Matrix
        for tf in self.term_frequency:
            TF_IDF = {}
            for term, freq in tf.items():
                TF_IDF[term] = freq * self.inverse_document_frequency[term]
            self.TF_IDF_matrix.append(TF_IDF)

    def search(self, parameter, query, top_k=5):
        """Search for relevant NBA shots based on a parameter and query."""
        query_words = query.lower().split()
        query_scores = []

        for idx, TF_IDF in enumerate(self.TF_IDF_matrix):
            # Check if the parameter matches the text to include the shot in search
            if parameter.lower() in self.shot_texts[idx].lower():
                score = sum(TF_IDF.get(word, 0) for word in query_words)
                query_scores.append((score, idx))

        if not query_scores:
            print("No matching results found.")
            return []

        # Sort by score and return the top_k results
        query_scores.sort(reverse=True, key=lambda x: x[0])
        print("Sorted Query Scores:", query_scores)  # Debugging output
        results = [nba_shots[idx] for _, idx in query_scores[:top_k] if _ > 0]
        return results
