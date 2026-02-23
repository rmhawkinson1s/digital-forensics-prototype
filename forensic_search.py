import re
from collections import defaultdict

class ForensicSearch:
    def __init__(self):
        
        self.index = defaultdict(set)
        self.data_store = {}

    def add_data(self, source_id, text):
        """Builds the index by tokenizing extracted text."""
        self.data_store[source_id] = text
        words = re.findall(r'\w+', text.lower())
        for word in words:
            self.index[word].add(source_id)

    def search(self, keyword, regex_pattern):
        """
        Step 1: Use index to find documents containing the keyword.
        Step 2: Apply complex regex to those specific documents.
        """
        # FR-9: Indexed keyword lookup
        candidate_ids = self.index.get(keyword.lower(), set())
        
        results = []
        compiled_re = re.compile(regex_pattern, re.IGNORECASE)

        # FR-9: Complex regex across filtered extracted data
        for sid in candidate_ids:
            text = self.data_store[sid]
            matches = compiled_re.findall(text)
            if matches:
                results.append({"source": sid, "matches": matches})
        
        return results

if __name__ == "__main__":
    engine = ForensicSearch()
    engine.add_data("File_01", "User accessed suspect-site.com at 10:00 AM.")
    engine.add_data("File_02", "System log: no suspicious activity found.")

    results = engine.search("suspect", r'[a-z0-9._-]+\.(?:com|org|net)')
    print(results)
