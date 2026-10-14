import os
import subprocess

def write_code_to_file(code: str,target_path: str)-> str:
    """Safely create targented path file and write the code in file"""
    os.makedirs(os.path.dirname(target_path),exist_ok=True)
    with open(target_path,"w", encoding="utf-8") as f:
        f.write(code)
    return f"Successfully written to {target_path}"


