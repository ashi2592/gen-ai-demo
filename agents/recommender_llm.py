
def build_recommendation_prompt(user: dict, items: list[dict]) -> str:
    item_context = "\n".join([
        f"- {item['name']} ({item['category']}): {item['description']}. Tags: {', '.join(item['tags'])}"
        for item in items
    ])

    prompt = f"""
    You are a recommendation engine.

    User Info:
    - Name: {user['name']}
    - Age: {user['age']}
    - Occupation: {user['occupation']}
    - Interests: {', '.join(user['interests'])}

    Available Items:
    {item_context}

    Task:
    Based on user's profile and interests, recommend top 3 most relevant items. Respond in JSON format like:
    [
    {{ "item_id": 1, "reason": "..." }},
    ...
    ]
    """
    return prompt

