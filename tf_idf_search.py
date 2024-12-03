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
        # Prepare text data for TF-IDF computation.
        self.shot_texts = []
        for shot in nba_shots:
            shot_text = (
                f"{shot.player_name.strip().lower()} {shot.event_type.lower()} {shot.shot_type.lower()} "
                f"{shot.basic_zone.lower()} {shot.zone_name.lower()} {shot.action_type.lower()}"
            )
            self.shot_texts.append(shot_text)


    def compute_TF_IDF(self):
        # Calculate TF-IDF scores for all shots.
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

    def search(self, parameter, query, top_k):
        query = query.lower().strip()  # Normalize query
        results = []

        for _, shot in enumerate(nba_shots):
            # Access the attribute dynamically based on the parameter
            shot_value = getattr(shot, parameter, "").lower()

            # Match the query to the attribute value
            if query in shot_value:
                results.append(shot)

        # Return top_k results or all matches
        return results[:top_k]

