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