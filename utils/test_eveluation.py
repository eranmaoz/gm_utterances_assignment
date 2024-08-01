def evaluate_results(results, intent_criteria, entity_criteria):
    total_utterances = len(results)
    similar_intents = sum(1 for r in results if r["intent_similarity"] == "Similar")
    similar_entities = sum(1 for r in results if r["entity_similarity"] == "Similar")

    intent_percent = (similar_intents / total_utterances) * 100
    entity_percent = (similar_entities / total_utterances) * 100

    print(f"Intent similarity percentage: {intent_percent}%")
    print(f"Entity similarity percentage: {entity_percent}%")

    if intent_percent >= intent_criteria and entity_percent >= entity_criteria:
        return True
    return False
