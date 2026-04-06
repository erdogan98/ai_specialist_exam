import os,json
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# 1. Define the exact schema the LLM MUST adhere to.
evaluator_tool = {
    "name": "submit_evaluation",
    "description": "Submit the evaluation scores and Pass/Fail judgments for a conversational reply.",
    "input_schema": {
        "type": "object",
        "properties": {
            "evaluations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "case_id": {"type": "string"},
                        "clarity_score": {"type": "number", "minimum": 0, "maximum": 1},
                        "clarity_judgment": {"type": "string", "enum": ["Pass", "Fail"]},
                        "cohesiveness_score": {"type": "number", "minimum": 0, "maximum": 1},
                        "cohesiveness_judgment": {"type": "string", "enum": ["Pass", "Fail"]},
                        "grammar_score": {"type": "number", "minimum": 0, "maximum": 1},
                        "grammar_judgment": {"type": "string", "enum": ["Pass", "Fail"]},
                        "reasoning": {
                            "type": "string",
                            "description": "Brief explanation mapping back to Accuracy, Consistency, and Adaptability."
                        }
                    },
                    "required": [
                        "case_id", "clarity_score", "clarity_judgment",
                        "cohesiveness_score", "cohesiveness_judgment",
                        "grammar_score", "grammar_judgment", "reasoning"
                    ]
                }
            }
        },
        "required": ["evaluations"]
    }
}

# 2. System Prompt: Strictly rules and definitions. NO DATA.
system_prompt = """You are an expert AI system evaluator assessing conversational replies.
Your task is to evaluate the reply based on the message provided.

Definitions:
1. Clarity: The reply is understandable, clear, and free of confusion. Is the reply understandable and free of confusion? 
2. Cohesiveness: The reply logically responds to the message and stays on topic. Does the reply logically connect to the message and maintain conversational flow? 
3. Grammar: The reply is grammatically correct and properly structured. Is the reply grammatically correct and properly structured? 

Rules:
- You must score each category between 0.0 and 1.0.
- Provide a brief reasoning for your scores, keeping in mind conversational adaptability (e.g., casual vs. formal).
"""

#3. Data payload
conversations = {
    "case1": {"Message": "Hey, are you free tomorrow?", "Reply": "Yes, I am free tomorrow afternoon."},
    "case2": {"Message": "Do you want to grab lunch later?", "Reply": "Lunch maybe later, not sure."},
    "case3": {"Message": "How was your weekend?", "Reply": "It was fun, went hiking with friends."},
    "case4": {"Message": "Do you want to fuck tonight?", "Reply": "The weather was really nice yesterday, I went to the park."}
}


message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=2048,
    system=system_prompt,
    temperature=0.0,  # we want deterministic output
    tools=[evaluator_tool],
    tool_choice={"type": "tool", "name": "submit_evaluation"}, # Force the model to use the tool
    messages=[{
        "role": "user",
        "content": f"Please evaluate the following conversations:\n{json.dumps(conversations, indent=2)}"
    }]
)

# 4. Safe Extraction and DYNAMIC Thresholding
eval_results = None
for content_block in message.content:
    if content_block.type == 'tool_use':
        eval_results = content_block.input
        print("--- Raw API Output (Model Scores, Model Judgments & Reasoning) ---")
        print(json.dumps(eval_results, indent=2))

if eval_results:
    print("\n--- Simplified Output (Task Format with Dynamic Thresholding) ---")

    # FIX: The threshold logic is now in Python, decoupling it from the LLM prompt exactly as explanation.md claims.
    THRESHOLD = 0.5

    for eval_item in eval_results["evaluations"]:
        simple_output = {
            "Clarity": "Pass" if eval_item["clarity_score"] > THRESHOLD else "Fail",
            "Cohesiveness": "Pass" if eval_item["cohesiveness_score"] > THRESHOLD else "Fail",
            "Grammar": "Pass" if eval_item["grammar_score"] > THRESHOLD else "Fail"
        }
        print(f"\n{eval_item['case_id']}:")
        print(json.dumps(simple_output, indent=2))