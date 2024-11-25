from openai import OpenAI
import json


def check_continue_chatting(user_query:str, history:str=None) -> bool:
    """
    Check if the user's query contains an intent to search and return
    the result along with an appropriate response.
    """
    client = OpenAI()

    PROMPT = '''Determine if the user's query indicates an intent to search for GitHub repositories. 
    If the query suggests searching (e.g., contains phrases like "search", "find", "recommend"), 
    return "yes". Otherwise, return "no" and provide an appropriate conversational response to continue the chat.

    Output format:
    {
        "intent": "yes" or "no",
        "response": "<GPT-generated response>"
    }

    Do not include any additional text or explanations outside the JSON format.'''

    if history:
        PROMPT += ("And here is an user chatting history. Reffer it." + history)
        print(PROMPT)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"{PROMPT}"},
            {"role": "user", "content": f"{user_query}"}
        ]
    )

    response = completion.choices[0].message.content

    # JSON 추출
    start_index = response.find('{')
    end_index = response.rfind('}') + 1  # +1 to include '}'
    response = response[start_index:end_index]
    
    # JSON 파싱
    intent_info = json.loads(response)
    print(intent_info)
    return intent_info


# ChatGPT를 사용하여 검색용, 리랭킹용 키워드 추출
def get_intent_from_chatgpt(query: str, history:str=None) -> dict:
    client = OpenAI()

    PROMPT = '''From the user's request, extract two sets of keywords to optimize GitHub repository search and ranking:

1) "search_keywords": A concise set of main keywords optimized for GitHub search queries to find the most accurate and relevant repositories. These keywords should be directly applicable to GitHub's search functionality.

2) "rerank_keywords": A more detailed and comprehensive set of keywords or phrases that reflect the user's requirements more thoroughly. These will be used to re-rank repositories based on their README content.

Return the results in JSON format with the keys "search_keywords" and "rerank_keywords".

Ensure the response is concise, accurate, and suitable for direct use in GitHub search and re-ranking of repositories. Do not include any additional text or explanation.'''

    if history:
        PROMPT += ("And here is an user chatting history. Reffer it." + history)
        print(PROMPT)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"{PROMPT}"},
            {
                "role": "user",
                "content": f"{query}"
            }
        ]
    )
    response = completion.choices[0].message.content
    
    start_index = response.find('{')
    end_index = response.rfind('}') + 1  # +1 to include '}'
    response = response[start_index:end_index]
    
    intent = json.loads(response)
    return intent