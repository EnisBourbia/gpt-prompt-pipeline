import subprocess
from prompt import Prompt
from api import init_webhook_sonarqube_api
from dotenv import load_dotenv
import requests
import threading
import time
import os

def process_directories(prompt: Prompt, base_dir: str):
    for dir_name in os.listdir("./humaneval/"):
        if dir_name.startswith("code_"):
            dir_path = os.path.join(base_dir, dir_name)
            prompt.code_id = dir_name
            main_file_path = os.path.join(dir_path, "main.py")

            with open(main_file_path, 'r') as file:
                prompt.code = file.read()
            
            # Refactor code
            prompt.refactor_code()
            test_file_path = "./code/test.py"
            with open(test_file_path, 'w') as file:
                file.write(prompt.refactored_code)
            
            prompt.passed_testcases = run_assertions_script(test_file_path)
            # Run SonarQube analysis
            prompt.run_sonarqube()
            init_webhook_sonarqube_api()
            # Fetch SonarQube results
            prompt.fetch_sonarqube_results()
            prompt.save()

def run_assertions_script(script_path):
    try:
        result = subprocess.run(['python', script_path], check=True, text=True, capture_output=True)
        print("Success:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)
        return False


def main():
    file_path = './humaneval/'
    prompt = Prompt(code="", refactored_code="", target_model="GPT-4", iterations=1) #GPT-3.5-TURBO

    process_directories(prompt, file_path)
    # with open(file_path, 'r') as java_file:
    #     code_example = java_file.read()
    # prompt = Prompt(code=code_example, target_model="GPT-4", iterations=1) #GPT-3.5-TURBO

    # prompt.run_sonarqube()
    # init_webhook_sonarqube_api()
    # #prompt.evalute_gpt()
    
    # prompt.fetch_sonarqube_results()
    # prompt.print()
if __name__ == "__main__":
    main()

