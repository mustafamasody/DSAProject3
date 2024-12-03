
from collections import defaultdict
from global_var import nba_shots
import re

class InvertedIndexSearch:
    def __init__(self):
        self.inverted_index = defaultdict(set)
        self.shots = nba_shots 

    def preprocessData(self):
        # Build the inverted index
        for idx, shot in enumerate(self.shots):
            # For each shot, index its attributes
            attributes = [
                'player_name', 'event_type', 'shot_type', 
                'basic_zone', 'zone_name', 'action_type'
            ]
            for attr in attributes:
                value = getattr(shot, attr, '')
                tokens = self._tokenize_and_normalize(value)
                for token in tokens:
                    # Map term to shot indices for the given attribute
                    self.inverted_index[(attr, token)].add(idx)

    def _tokenize_and_normalize(self, text):
        # Convert text to lowercase and extract words
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def compute_TF_IDF(self):
        pass

    def search(self, parameter, query):
        tokens = self._tokenize_and_normalize(query)
        if not tokens:
            return []

        # Retrieve shot indices for the first token
        result_indices = self.inverted_index.get((parameter, tokens[0]), set()).copy()
        # Intersect with shot indices for subsequent tokens
        for token in tokens[1:]:
            indices = self.inverted_index.get((parameter, token), set())
            result_indices &= indices

        # Retrieve the shots corresponding to the result indices
        results = [self.shots[idx] for idx in result_indices]
        return results
