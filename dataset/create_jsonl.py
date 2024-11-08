import os
import json

def combine_json_to_jsonl(input_folder, output_file):
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    json_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.json')])
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for json_file in json_files:
            try:
                with open(os.path.join(input_folder, json_file), 'r', encoding='utf-8') as infile:
                    data = json.load(infile)
                    outfile.write(json.dumps(data, ensure_ascii=False) + '\n')
                print(f"{json_file}")
                
            except Exception as e:
                print(f"({json_file}): {str(e)}")
    
    print(f"\n{output_file}")

input_folder = "/Users/jotaesik/null_null/dataset/tags/sets"
output_file = "/Users/jotaesik/null_null/dataset/tags/training_data.jsonl"

combine_json_to_jsonl(input_folder, output_file)
