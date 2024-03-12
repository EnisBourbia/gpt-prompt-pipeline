import os 
import openai
import requests
import json
from prompt_prefixes import REFACTOR_PROMPT, COGNITIVE_EXAMPLE_PROMPT, COGNITIVE_CHAIN_OF_THOUGHT_PROMPT, COGNITIVE_STANDARD_PROMPT, CYCLOMATIC_EXAMPLE_PROMPT, CYCLOMATIC_CHAIN_OF_THOUGHT_PROMPT, CYCLOMATIC_STANDARD_PROMPT, COGNITIVE_WITH_DEFINITION_PROMPT, CYCLOMATIC_WITH_DEFINITION_PROMPT
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import time
import csv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class Prompt:
    # MODELS: "GPT-3.5-TURBO", TODO

    def __init__(self, code, refactored_code, target_model="GPT-3.5-TURBO", iterations=1):
        self.code_id = ""
        self.code = code
        self.refactored_code = refactored_code
        self.target_model = target_model
        self.results = {}
        self.iterations = iterations
        self.passed_testcases = None


    def evalute_gpt(self):
        results = []

        if self.target_model == "GPT-3.5-TURBO":
            for i in range(0, self.iterations):
                gpt3turbo_cognitive_results = self.run_gpt3turbo("COGNITIVE")
                gpt3turbo_cyclomatic_results = self.run_gpt3turbo("CYCLOMATIC")
                results.append({"cognitive": gpt3turbo_cognitive_results, "cyclomatic": gpt3turbo_cyclomatic_results})
                time.sleep(5)
                print(i)
            self.results["GPT-3.5-TURBO"] = results
        elif self.target_model == "GPT-4":
            for i in range(0, self.iterations):
                gpt4_cognitive_results = self.run_gpt4("COGNITIVE")
                gpt4_cyclomatic_results = self.run_gpt4("CYCLOMATIC")
                results.append({"cognitive": gpt4_cognitive_results, "cyclomatic": gpt4_cyclomatic_results})
                time.sleep(3)
                print(i)
            self.results["GPT-4"] = results

    def run_sonarqube(self):
        os.system("~/Desktop/sonar-scanner/bin/sonar-scanner -Dsonar.token=<AUTH_TOKEN> -Dsonar.projectKey=local_code -Dsonar.projectBaseDir=<LOCAL_DIRECTORY>")

    def fetch_sonarqube_results(self):
        headers = {"Authorization": "Bearer <AUTH_TOKEN>"}

        response_cognitive = requests.get("http://localhost:9000/api/measures/component?component=local_code&metricKeys=cognitive_complexity", auth=HTTPBasicAuth("admin", "admin123"))
        response_cognitive_json = response_cognitive.json()
        response_cyclomatic = requests.get("http://localhost:9000/api/measures/component?component=local_code&metricKeys=complexity", auth=HTTPBasicAuth("admin", "admin123"))
        response_cyclomatic_json = response_cyclomatic.json()
        self.results["sonarqube"] = {"cognitive": response_cognitive_json["component"]["measures"][0]["value"], "cyclomatic": response_cyclomatic_json["component"]["measures"][0]["value"]}


    def run_gpt3turbo(self, complexity_type):
        prompts = []

        if complexity_type == "COGNITIVE":
            prefixes = [COGNITIVE_CHAIN_OF_THOUGHT_PROMPT]
            #prefixes = [COGNITIVE_STANDARD_PROMPT, COGNITIVE_EXAMPLE_PROMPT, COGNITIVE_CHAIN_OF_THOUGHT_PROMPT, COGNITIVE_WITH_DEFINITION_PROMPT]
        elif complexity_type == "CYCLOMATIC":
            prefixes = [CYCLOMATIC_CHAIN_OF_THOUGHT_PROMPT] 
            # prefixes = [CYCLOMATIC_STANDARD_PROMPT, CYCLOMATIC_EXAMPLE_PROMPT, CYCLOMATIC_CHAIN_OF_THOUGHT_PROMPT, CYCLOMATIC_WITH_DEFINITION_PROMPT] 

        for prefix in prefixes:
            prompt = f"{prefix}\n\n{self.code}"
            prompts.append(prompt)

        responses = []
        results = []
        counter = 0
        while counter < len(prompts):
            time.sleep(2)
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompts[counter]}],
            temperature=1,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
            )
            try:
                test = json.loads(response.choices[0].message["content"])
            except:
                print(f"recovering from failed request.")
                time.sleep(10)
                continue
            responses.append(response)
            counter += 1
            print(f"Prompt {counter} received")    

        for response in responses:
            response_data = json.loads(response.choices[0].message["content"])
            
            complexity_value = response_data.get("complexity")
            reasoning = response_data.get("reasoning")

            results.append([complexity_value, reasoning])       
        return results

    def run_gpt4(self, complexity_type):
        prompts = []

        if complexity_type == "COGNITIVE":
            prefixes = [COGNITIVE_WITH_DEFINITION_PROMPT]
            #prefixes = [COGNITIVE_STANDARD_PROMPT, COGNITIVE_EXAMPLE_PROMPT, COGNITIVE_CHAIN_OF_THOUGHT_PROMPT, COGNITIVE_WITH_DEFINITION_PROMPT]
        elif complexity_type == "CYCLOMATIC":
            prefixes = [CYCLOMATIC_WITH_DEFINITION_PROMPT] 
            # prefixes = [CYCLOMATIC_STANDARD_PROMPT, CYCLOMATIC_EXAMPLE_PROMPT, CYCLOMATIC_CHAIN_OF_THOUGHT_PROMPT, CYCLOMATIC_WITH_DEFINITION_PROMPT] 

        for prefix in prefixes:
            prompt = f"{prefix}\n\n{self.code}"
            prompts.append(prompt)

        responses = []
        results = []
        counter = 0
        while counter < len(prompts):
            time.sleep(3)
            response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompts[counter]}],
            temperature=1,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6
            )                
            try:
                test = json.loads(response.choices[0].message["content"])
            except:
                print("recovering from failed request.")
                time.sleep(10)
                continue
            responses.append(response)
            counter += 1
            print(f"Prompt {counter} received")    

        for response in responses:
            response_data = json.loads(response.choices[0].message["content"])
            
            complexity_value = response_data.get("complexity")
            reasoning = response_data.get("reasoning")
            results.append([complexity_value, reasoning])       
        return results

    def refactor_code(self):
        response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": REFACTOR_PROMPT}, 
                  {"role": "user", "content": self.code}],
        temperature=0.2,
        max_tokens=500,
        top_p=1,
        )        
        try:
            test = response.choices[0].message["content"]
        except Exception as e:
            print(f"Exception caught: {e}")
            print("Recovering from failed request.")
            time.sleep(10)
            return self.refactor_code()
        print(response)
        self.refactored_code = response.choices[0].message["content"]

    def print(self):
        print(json.dumps(self.results))


    def save(self):

        with open('./humaneval_results/humaneval_run_1.csv','a') as f:
            w = csv.writer(f)
            w.writerow([self.code_id, self.results["sonarqube"]["cyclomatic"], self.results["sonarqube"]["cognitive"], self.passed_testcases])#, iteration["cyclomatic"][1], iteration["cyclomatic"][2], iteration["cyclomatic"][3]])
                
        print("Results written to csv.")
