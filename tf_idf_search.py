import math
from collections import defaultdict
from global_var import nba_shots

class TFIDFSearch:
    def __init__(self):
        # Initialize data structures for storing shot texts, term frequencies, 
        # inverse document frequencies, and the resulting TF-IDF matrix.
        self.shot_texts = []
        self.term_frequency = []
        self.inverse_document_frequency = defaultdict(float)
        self.TF_IDF_matrix = []

    def preprocessData(self):
        # Prepare text data for TF-IDF computation by combining various attributes
        # from each shot into a single textual representation.
        self.shot_texts = []
        for shot in nba_shots:
            # Combine relevant shot attributes into a normalized, lowercase string.
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
            words = text.lower().split()  # Split text into words
            for word in words:
                term_count[word] += 1  # Count occurrences of each term in the text
            self.term_frequency.append(term_count)

        # Step 2: Calculate Document Frequencies (DF) and Inverse Document Frequencies (IDF)
        document_count = len(self.shot_texts)  # Total number of documents (shots)
        for tf in self.term_frequency:
            for term in tf.keys():
                self.inverse_document_frequency[term] += 1  # Count documents containing each term

        for term, count in self.inverse_document_frequency.items():
            # Compute IDF using the formula: log(total_documents / (1 + document_count))
            self.inverse_document_frequency[term] = math.log(document_count / (1 + count))

        # Step 3: Compute TF-IDF Matrix
        for tf in self.term_frequency:
            TF_IDF = {}
            for term, freq in tf.items():
                # TF-IDF = Term Frequency * Inverse Document Frequency
                TF_IDF[term] = freq * self.inverse_document_frequency[term]
            self.TF_IDF_matrix.append(TF_IDF)  # Append TF-IDF scores for this document

    def search(self, parameter, query, top_k):
        # Perform a search by matching the query against the specified parameter
        # in the nba_shots data.

        query = query.lower().strip()  # Normalize query for case-insensitive matching
        results = []

        for _, shot in enumerate(nba_shots):
            # Dynamically access the specified attribute of the shot (e.g., player_name, event_type).
            shot_value = getattr(shot, parameter, "").lower()

            # If the query matches any part of the attribute value, add the shot to results.
            if query in shot_value:
                results.append(shot)

        # Return the top_k results or all matches if fewer than top_k are found.
        return results[:top_k]