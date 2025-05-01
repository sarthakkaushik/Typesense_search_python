# 0. Run the docker containers
### Pull the image 
-  docker pull typesense/typesense:29.0.rc17-arm64-lg-page16  
### Runt the image
docker run -d --name=typesense-server_2 -p 8108:8108 -v typesense-data:/data typesense/typesense:29.0.rc17-arm64-lg-page16 --data-dir /data --api-key=xyz --enable-cors

### Check the status
http://localhost:8108

### Stop the container
docker stop typesense-server_2
docker rm typesense-server_2

# Setup UV environment
- 1. uv venv
- 2. uv sync
- 3. source venv/bin/activate

# 1. Update your JSONL file with sort_order field (if needed)
01_Creating_typesense_data.ipynb

# 2. Create the collection using the schema
curl -X POST "http://localhost:8108/collections" \
  -H "X-TYPESENSE-API-KEY: xyz" \
  -H "Content-Type: application/json" \
  -d @kpi_schema.json

# 3. Import the documents
curl -X POST "http://localhost:8108/collections/kpi_index/documents/import?action=create" \
  -H "X-TYPESENSE-API-KEY: xyz" \
  -H "Content-Type: application/json" \
  --data-binary @./typesense-data/data/kpi_synonyms_updated.jsonl

# 4. Verify collection creation
curl -X GET "http://localhost:8108/collections/kpi_index" \
  -H "X-TYPESENSE-API-KEY: xyz" 

# 5. Test a search query
curl -X GET "http://localhost:8108/collections/kpi_index/documents/search?q=revenue&query_by=kpi,synonym" \
  -H "X-TYPESENSE-API-KEY: xyz"

# Categorical Search Implementation

Follow these steps to set up and use the categorical search functionality:

## 1. Create the collection using the schema

```bash
curl -X POST "http://localhost:8108/collections" \
  -H "X-TYPESENSE-API-KEY: xyz" \
  -H "Content-Type: application/json" \
  -d @cat_schema.json
```

## 2. Import the category documents

First, run the notebook `03_Cat_Search_Implementation.ipynb` to prepare and import the categorical data.

## 3. Test a category search query

```bash
curl -X GET "http://localhost:8108/collections/category_index/documents/search?q=IRON&query_by=Value" \
  -H "X-TYPESENSE-API-KEY: xyz"
```

## 4. Using the CategoryMatcher class

The `category_matcher.py` module provides a Python class for easier interaction with the Typesense categorical search. See the notebook for usage examples.