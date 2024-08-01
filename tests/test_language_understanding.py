import pytest
import responses
import requests
from config.config import RESULTS_CSV_FILE, PASS_CRITERIA_PERCENTILE
from utils.file_utils import get_utterances, get_mock_responses
from utils.result_utils import save_results_to_csv


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

    # Calculate and verify pass criteria
    total_utterances = len(utterances)
    similar_intents = sum(1 for r in results if r["intent_similarity"] == 'Similar')
    similar_entities = sum(1 for r in results if r["entity_similarity"] == 'Similar')

    intent_percentile = (similar_intents / total_utterances) * 100
    entity_percentile = (similar_entities / total_utterances) * 100

    assert intent_percentile >= PASS_CRITERIA_PERCENTILE, f"Intent similarity {intent_percentile}% is below pass criteria."
    assert entity_percentile >= PASS_CRITERIA_PERCENTILE, f"Entity similarity {entity_percentile}% is below pass criteria."
