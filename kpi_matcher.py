import typesense
import re

class KpiMatcher:
    def __init__(self, typesense_host="localhost", port="8108", api_key="xyz"):
        self.client = typesense.Client({
            "nodes": [{
                "host": typesense_host,
                "port": port,
                "protocol": "http"
            }],
            "api_key": api_key,
            "connection_timeout_seconds": 2
        })
        self.stop_words = {'show', 'me', 'the', 'in', 'for', 'of', 'and', 'with', 'by', 'top', 'terms'}

    def _preprocess_text(self, text: str) -> str:
        """Clean and normalize text"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        return ' '.join(word for word in text.split() if word not in self.stop_words)

    def find_kpis(self, user_input: str, top_k: int = 30):
        try:
            processed_text = self._preprocess_text(user_input)
            words = processed_text.split()
            
            # Initialize an empty list to store all matches
            all_matches = []
            
            # Search for each word in the processed text
            for word in words:
                search_parameters = {
                    'q': word,
                    'query_by': 'synonym',
                    'num_typos': 2,
                    'per_page': top_k
                }
                
                # Perform the search for each word
                results = self.client.collections['kpi_index'].documents.search(search_parameters)
                matches = [hit['document']['kpi'] for hit in results['hits']]
                all_matches.extend(matches)

            # Remove duplicates while preserving order
            return list(dict.fromkeys(all_matches))

        except Exception as e:
            print(f"Error querying Typesense: {e}")
            return []
