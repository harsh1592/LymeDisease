#!/bin/bash
mkdir data

echo "Downloading Data folder..." 
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=0B1LdyitP3FKbMXJHTE9nM0R4SFE' -O data/stopwordsDrive.txt
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=0B1LdyitP3FKbaE8zX2pCSnNnMW8' -O data/community_posts_Processed.csv
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=0B1LdyitP3FKbU2V1TFAzU3dUS1k' -O data/outfile_content.csv
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=0B1LdyitP3FKbRzNfdjFnMHZXR28' -O data/users.json
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=0B1LdyitP3FKbZG5pNUZzVUFVaEE' -O data/xaa.csv
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=0B1LdyitP3FKbVDBlbTVPOG5YNEE' -O data/xab.csv
echo "Finished downloading all data"