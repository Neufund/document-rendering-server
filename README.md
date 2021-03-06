# What is Document Rendering Micro Service
Simply this micro service is replacing the tags from documents pinned on IPFS then export them as pdf.

# Why this micro service exists
Because its very hard to have perfect results when you are going to convert documents from word or html 
to pdf in the client side applications, we made this micro service to convert the 
IPFS pinned documents to pdf, with replacing tags feature.

# How it works
- Download pinned document from IPFS node like html or word document.<br/>
example: `ipfs.neufund.org/ipfs/QmQvrXFVTbPYHVLRSqPfnCPaVizhBomEKvFgAPB8Cd2B9x`
- Caching the IPFS document.
- Replacing the tags as the following example.
 
```
{
    "{company}": "Fifth Force GmbH",
    "{country}": "Germany",
    "{hrb-clause}": "the commercial register of the local court of Berlin under HRB 179357 B",
    "{repo-url}": "git@github.com:Neufund/ESOP.git",
    "{commit-id}": "",
    "{court-city}": "Berlin"
}
```

- Using Factory design pattern to detect the document type to know which method should use in converting 
to pdf.
- Cache the PDF file.
- Send the pdf file to the user using the endpoint, details about the endpoint below.
# Storage
in config file you will find 
- `IPFS_CACHE_DIR` the path of the cached ipfs documents
- `CONVERTED_DIR` the path of the pdf cache folder

# Setup
Use Docker to install it easily <br/>
- Install `docker` from <a target="_blank" href="https://docs.docker.com/engine/installation/">here</a>.
- We use `docker-compose` version 2, so add this file 
```
version: '2'
services:
  render-pdf:
    env_file: <DIRECTORY/render_pdf.env>
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ipfs_cache:/app/ipfs_cache
      - converted:/app/converted
  # optional for local testing
  ipfs-host:
    image: ipfs/go-ipfs:v0.5.1
    ports:
      - "4001:4001"
      - "4001:4001/udp"
      - "127.0.0.1:8080:8080"
      - "127.0.0.1:5001:5001"
volumes:
  ipfs_cache:
  converted:

```

- In `docker-compose.yml` file you will find the variable environments.
 `IPFS_HOST` and `IPFS_PORT` you just need to define them in `render_pdf.env` file
- specify `env_file: <DIRECTORY/render_pdf.env>` in `docker-compose.yml`.
- Run the following command

```
docker-compose up --build
```

# Endpoint
- <b>/api/document</b>
`POST <IP_ADDRESS>/api/document?hash=< IPFS_HASH_KEY >&type=< TYPE_OF_THE_DOCUMENT > {
    "{company}": "Fifth Force GmbH",
    "{country}": "Germany"
    ...
}`
- you should send the hash of the ipfs document and the type as well.<br/>
<b>Note:</b> the type must be "word" or "html".

# CURl Example
you just need to change `<SERVER_IP>` below
```
curl -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{
  "company":"Fifth Force GmbH",
  "country":"Germany",
  "hrb-clause":"the commercial register of the local court of Berlin under HRB 179357 B",
  "repo-url":"git@github.com:Neufund/ESOP.git",
  "commit-id":"",
  "court-city":"Berlin"
}' "<SERVER_IP>/api/document?hash=QmQEGujQefenqt53Au82gPf5yjEbwzea5UJMxswJqmwtHF&type=word"
```

# Supported file type
- Word documents
- Html file

# Additional info
Hash function used for renaming the pdf cached files hashes is sha1

# Testing
`python -m unittest`
##Note
**Added during latest quick fixes**  
Project currently is in low maintanance mode and we are missing guide how to run it locally.  
But to run latest added tests you can call it simply by just running subset of all tests.  
`python -m unittest tests/test_hash_validation.py`
