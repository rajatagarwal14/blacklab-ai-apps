#!/usr/bin/env python3
"""
Migrate prompts from prompts_database.js to Firestore
Run this once to populate your database with all 70+ curated prompts
"""

import firebase_admin
from firebase_admin import credentials, firestore
import json
import re

# Initialize Firebase
cred = credentials.Certificate('firebase-credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Read the JavaScript file and extract prompts
with open('../prompts_database.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the array content
# Find the start of the array
array_start = content.find('[')
array_end = content.rfind(']')
array_content = content[array_start:array_end+1]

# Convert JavaScript objects to Python-compatible JSON
# Replace single quotes with double quotes for JSON parsing
json_content = array_content.replace("'", '"')

# Parse the JSON
try:
    prompts = json.loads(json_content)
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")
    print("Attempting alternative parsing method...")
    
    # Alternative: Extract prompts manually using regex
    # This is more robust for JavaScript object notation
    import ast
    
    # Read file again
    with open('../prompts_database.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Find all prompt objects
    prompt_pattern = r'\{id:\d+,.*?\}'
    prompt_matches = re.findall(prompt_pattern, js_content, re.DOTALL)
    
    prompts = []
    for match in prompt_matches:
        try:
            # Convert JS object notation to Python dict
            # Replace key:value with "key":value
            fixed = re.sub(r'(\w+):', r'"\1":', match)
            # Fix unquoted string values
            fixed = re.sub(r':([^"\d\[\{][^,\}]*)', r':"\1"', fixed)
            # Parse as Python literal
            prompt_dict = ast.literal_eval(fixed)
            prompts.append(prompt_dict)
        except Exception as e:
            print(f"Error parsing prompt: {e}")
            continue

print(f"Found {len(prompts)} prompts to migrate")

# Upload to Firestore
collection = db.collection('prompts')
successful = 0
failed = 0

for prompt in prompts:
    try:
        # Prepare document data
        doc_data = {
            'title': prompt['title'],
            'category': prompt['category'],
            'text': prompt['text'],
            'rating': prompt.get('rating', 4.5),
            'uses': prompt.get('uses', 0),
            'submitter': prompt.get('submitter', 'Curated'),
            'type': prompt.get('type', 'curated'),
            'tags': prompt.get('tags', []),
            'approved': True,  # All curated prompts are pre-approved
            'created_at': firestore.SERVER_TIMESTAMP,
            'copy_count': prompt.get('uses', 0)  # Initialize with uses count
        }
        
        # Add expected_output if present
        if 'expectedOutput' in prompt:
            doc_data['expected_output'] = prompt['expectedOutput']
        
        # Use the prompt ID as the document ID
        doc_id = str(prompt['id'])
        collection.document(doc_id).set(doc_data)
        
        successful += 1
        print(f"✓ Migrated: {prompt['title']} (ID: {doc_id})")
        
    except Exception as e:
        failed += 1
        print(f"✗ Failed to migrate prompt {prompt.get('id', 'unknown')}: {e}")

print("\n" + "="*60)
print(f"Migration Complete!")
print(f"✅ Successfully migrated: {successful} prompts")
if failed > 0:
    print(f"❌ Failed: {failed} prompts")
print("="*60)
