import csv
from datetime import datetime

import json
from config.config import UTTERANCES_FILE, MOCK_RESPONSES_FILE


def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def get_utterances():
    return load_json(UTTERANCES_FILE)


def get_mock_responses():
    return load_json(MOCK_RESPONSES_FILE)


def save_results_to_csv(results, file_path):
    print(f"Saving results to CSV: {file_path}")
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow([
            "Utterance",
            "Expected Intent",
            "Expected Entity",
            "API Actual Intent",
            "API Actual Entity",
            "Intent Similarity",
            "Entity Similarity"
        ])

        # Write results
        for result in results:
            writer.writerow([
                result["utterance"],
                result["expected_intent"],
                result["expected_entity"],
                result["api_actual_intent"],
                result["api_actual_entity"],
                result["intent_similarity"],
                result["entity_similarity"]
            ])
    print("Results saved successfully.")