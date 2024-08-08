import pytest
import responses
import requests
from config.config import RESULTS_CSV_FILE, PASS_CRITERIA_PERCENTILE
from utils.file_utils import get_utterances, get_mock_responses
from utils.result_utils import save_results_to_csv
from utils.test_evaluation import evaluate_results


# Load test data using utility functions
utterances = get_utterances()
mock_responses = get_mock_responses()


@responses.activate
def test_language_understanding():
    results = []

    for entry in utterances:
        utterance = entry["utterance"]
        expected_intent = entry["expected_intent"]
        expected_entity = entry["expected_entity"]

        responses.add(
            responses.POST,
            'https://mockapi.example.com/parse',
            json=mock_responses.get(utterance, {"intent": "Unknown", "entity": "Unknown"}),
            status=200
        )

        response = requests.post('https://mockapi.example.com/parse', json={"utterance": utterance})
        response_data = response.json()

        actual_intent = response_data["intent"]
        actual_entity = response_data["entity"]

        intent_similarity = 'Similar' if actual_intent == expected_intent else 'Non-similar'
        entity_similarity = 'Similar' if actual_entity == expected_entity else 'Non-similar'

        result = {
            "utterance": utterance,
            "expected_intent": expected_intent,
            "expected_entity": expected_entity,
            "api_actual_intent": actual_intent,
            "api_actual_entity": actual_entity,
            "intent_similarity": intent_similarity,
            "entity_similarity": entity_similarity
        }

        results.append(result)

    # Save results to CSV
    save_results_to_csv(results, RESULTS_CSV_FILE)

    # Evaluate results using the imported function
    pass_criteria, intent_percent, entity_percent = evaluate_results(results, PASS_CRITERIA_PERCENTILE, PASS_CRITERIA_PERCENTILE)

    # Assert and print failure details if needed
    assert pass_criteria, f"Similarity percentages are below pass criteria. Intent similarity: {intent_percent}%, " \
                          f"Entity similarity: {entity_percent}%, Pass criteria: {PASS_CRITERIA_PERCENTILE}%"