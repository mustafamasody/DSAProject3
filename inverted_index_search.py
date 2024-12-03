from collections import defaultdict
from global_var import nba_shots
import re

class InvertedIndexSearch:
    def __init__(self):
        # Initialize the inverted index and reference the global shots list
        self.inverted_index = defaultdict(set)
        self.shots = nba_shots 

    def preprocessData(self):
        # Build the inverted index mapping (attribute, token) to shot indices
        for idx, shot in enumerate(self.shots):
            # Attributes to index for searching
            attributes = [
                'player_name', 'event_type', 'shot_type', 
                'basic_zone', 'zone_name', 'action_type'
            ]
            for attr in attributes:
                # Get the value of the attribute, defaulting to empty string if missing
                value = getattr(shot, attr, '')
                # Tokenize and normalize the attribute value
                tokens = self._tokenize_and_normalize(value)
                for token in tokens:
                    # Add the shot index to the set for this (attribute, token)
                    self.inverted_index[(attr, token)].add(idx)

    def _tokenize_and_normalize(self, text):
        # Extract lowercase alphanumeric tokens from the text
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def compute_TF_IDF(self):
        # Placeholder method for compatibility; not used in inverted index search
        pass

     # def search(self, parameter, query):
    #     tokens = self._tokenize_and_normalize(query)
    #     if not tokens:
    #         return []

    #     # Retrieve shot indices for the first token
    #     result_indices = self.inverted_index.get((parameter, tokens[0]), set()).copy()
    #     # Intersect with shot indices for subsequent tokens
    #     for token in tokens[1:]:
    #         indices = self.inverted_index.get((parameter, token), set())
    #         result_indices &= indices

    #     # Retrieve the shots corresponding to the result indices
    #     results = [self.shots[idx] for idx in result_indices]
    #     return results

    def search(self, parameter, query, top_k):
        # Tokenize and normalize the query string
        tokens = self._tokenize_and_normalize(query)
        if not tokens:
            return []

        # Retrieve shot indices for the first token in the query
        result_indices = self.inverted_index.get((parameter, tokens[0]), set()).copy()
        # Intersect with indices for subsequent tokens to find common shots
        for token in tokens[1:]:
            indices = self.inverted_index.get((parameter, token), set())
            result_indices &= indices

        # Retrieve the shots corresponding to the result indices
        results = [self.shots[idx] for idx in result_indices]
        # Return up to the specified number of results
        return results[:top_k]  
