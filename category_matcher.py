import typesense
import re

class CategoryMatcher:
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
        # self.stop_words = {'show', 'me', 'the', 'in', 'for', 'of', 'and', 'with', 'by', 'top', 'terms'}


    def find_categories(self, user_input: str, top_k: int = 10):
        try:

            
            # Initialize an empty list to store all matches
            all_matches = []
            
            # Search for each word in the processed text
            search_parameters = {
                    'q': user_input,
                    'query_by': 'Value',
                    'num_typos': 2,
                    'per_page': top_k
                }
                
                # Perform the search for each word
            results = self.client.collections['category_index'].documents.search(search_parameters)
                
            # Extract unique category values, table names, and column names
            for hit in results['hits']:
                doc = hit['document']
                match_info = {
                    'Value': doc['Value'],
                    'Table_name': doc['Table_name'],
                    'Column_name': doc['Column_name'],
                    'Table_path': doc['Table_path']
                }
                all_matches.append(match_info)

            # Convert to a dictionary to remove duplicates
            seen = set()
            unique_matches = []
            for match in all_matches:
                key = (match['Value'], match['Table_name'])
                if key not in seen:
                    seen.add(key)
                    unique_matches.append(match)

            return unique_matches

        except Exception as e:
            print(f"Error querying Typesense: {e}")
            return []
