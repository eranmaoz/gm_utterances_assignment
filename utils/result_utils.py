import csv
from datetime import datetime
from config.config import RESULTS_CSV_FILE


def save_results_to_csv(results, file_path):
    # Get the current timestamp in ddmmyyyy_hhmmss format
    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    file_path_with_timestamp = f"{file_path}_{timestamp}.csv"

    # Write the results to the CSV file
    with open(file_path_with_timestamp, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Utterance",
            "Expected Intent",
            "Expected Entity",
            "API Actual Intent",
            "API Actual Entity",
            "Intent Similarity",
            "Entity Similarity"
        ])
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
