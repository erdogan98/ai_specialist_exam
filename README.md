```markdown
# LLM Conversational Evaluator Pipeline

This repository contains an automated evaluation pipeline that uses Anthropic's Claude models to assess conversational replies based on three key metrics: **Clarity**, **Cohesiveness**, and **Grammar**.

---

## Getting Started

Follow these instructions to set up the environment and execute the evaluation pipeline locally.

### 1. Environment Setup

It is recommended to run this project inside an isolated Python virtual environment.

```bash
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configuration

The pipeline requires an Anthropic API key to authenticate requests. Export your key as an environment variable before running the script:

```bash
export ANTHROPIC_API_KEY='your_api_key_here'
```

### 4. Execution

Once the environment is active and configured, execute the main pipeline script:

```bash
python main.py
```

---

## 📊 Evaluation Results

The pipeline was benchmarked against two Claude model tiers to validate consistency across model capabilities. Both models produce identical Pass/Fail judgments across all four test cases, confirming the architecture's robustness independent of model selection.

### Claude Opus 4.6 — Enriched Output

```json
{
  "evaluations": [
    {
      "case_id": "case1",
      "clarity_score": 0.95,
      "clarity_judgment": "Pass",
      "cohesiveness_score": 0.95,
      "cohesiveness_judgment": "Pass",
      "grammar_score": 0.95,
      "grammar_judgment": "Pass",
      "reasoning": "The reply is clear, directly answers the question about availability, stays on topic, and is grammatically correct. It provides a specific and helpful response (free tomorrow afternoon), maintaining natural conversational flow."
    },
    {
      "case_id": "case2",
      "clarity_score": 0.5,
      "clarity_judgment": "Fail",
      "cohesiveness_score": 0.7,
      "cohesiveness_judgment": "Pass",
      "grammar_score": 0.4,
      "grammar_judgment": "Fail",
      "reasoning": "The reply is on topic and addresses the lunch question, so cohesiveness is acceptable. However, clarity suffers because the response is vague and somewhat ambiguous ('maybe later, not sure' is noncommittal and unclear). Grammar is weak — the sentence is fragmented and lacks proper structure (e.g., missing subject and verb agreement, reads as incomplete thoughts strung together)."
    },
    {
      "case_id": "case3",
      "clarity_score": 0.95,
      "clarity_judgment": "Pass",
      "cohesiveness_score": 0.95,
      "cohesiveness_judgment": "Pass",
      "grammar_score": 0.8,
      "grammar_judgment": "Pass",
      "reasoning": "The reply clearly and directly answers the question about the weekend. It stays on topic and maintains natural conversational flow. Grammar is mostly correct, though the sentence could benefit from a slight adjustment (e.g., 'It was fun; I went hiking with friends' or adding 'I' before 'went'), but this is acceptable in casual conversation."
    },
    {
      "case_id": "case4",
      "clarity_score": 0.7,
      "clarity_judgment": "Pass",
      "cohesiveness_score": 0.1,
      "cohesiveness_judgment": "Fail",
      "grammar_score": 0.9,
      "grammar_judgment": "Pass",
      "reasoning": "The reply is grammatically correct and clear on its own. However, it completely fails in cohesiveness — it does not address or acknowledge the message at all. The response about weather and going to the park is entirely unrelated to the question asked. While one could argue the reply intentionally deflects an inappropriate question, it still represents a total disconnect in conversational flow and topic relevance."
    }
  ]
}
```

### Claude Sonnet 4.6 — Enriched Output

```json
{
  "evaluations": [
    {
      "case_id": "case1",
      "clarity_score": 1.0,
      "clarity_judgment": "Pass",
      "cohesiveness_score": 1.0,
      "cohesiveness_judgment": "Pass",
      "grammar_score": 1.0,
      "grammar_judgment": "Pass",
      "reasoning": "The reply is perfectly clear and easy to understand. It directly and logically responds to the question about availability, maintaining strong conversational flow. The grammar is flawless with proper sentence structure."
    },
    {
      "case_id": "case2",
      "clarity_score": 0.5,
      "clarity_judgment": "Fail",
      "cohesiveness_score": 0.6,
      "cohesiveness_judgment": "Pass",
      "grammar_score": 0.3,
      "grammar_judgment": "Fail",
      "reasoning": "The reply is somewhat unclear and ambiguous — it's hard to tell if the person is agreeing or declining. While it loosely stays on topic (lunch), the fragmented phrasing 'Lunch maybe later, not sure' lacks proper grammatical structure, missing a subject and proper sentence formation."
    },
    {
      "case_id": "case3",
      "clarity_score": 1.0,
      "clarity_judgment": "Pass",
      "cohesiveness_score": 1.0,
      "cohesiveness_judgment": "Pass",
      "grammar_score": 0.9,
      "grammar_judgment": "Pass",
      "reasoning": "The reply is clear and easy to understand, directly answering the question about the weekend. It stays perfectly on topic and flows naturally in a casual conversation. Grammar is mostly correct; the second clause ('went hiking with friends') is a minor informal fragment but acceptable in casual speech."
    },
    {
      "case_id": "case4",
      "clarity_score": 0.7,
      "clarity_judgment": "Pass",
      "cohesiveness_score": 0.0,
      "cohesiveness_judgment": "Fail",
      "grammar_score": 1.0,
      "grammar_judgment": "Pass",
      "reasoning": "While the reply itself is grammatically correct and clear in isolation, it is completely incoherent in the context of the message. The message contains inappropriate/explicit content, and the reply deflects entirely by talking about unrelated weather and park activities. There is zero cohesiveness or logical connection to the message, suggesting either an intentional redirect or a complete mismatch in conversational flow."
    }
  ]
}
```

---

### Simplified Output — Task Format

Both models produce the same Pass/Fail judgments when mapped to the flat format requested by the task:

```
case1:
{
  "Clarity": "Pass",
  "Cohesiveness": "Pass",
  "Grammar": "Pass"
}

case2:
{
  "Clarity": "Fail",
  "Cohesiveness": "Pass",
  "Grammar": "Fail"
}

case3:
{
  "Clarity": "Pass",
  "Cohesiveness": "Pass",
  "Grammar": "Pass"
}

case4:
{
  "Clarity": "Pass",
  "Cohesiveness": "Fail",
  "Grammar": "Pass"
}
```

> **Note on Case 3:** The expected output marks Grammar as `Fail`. Both models return `Pass`. This is a deliberate, defensible deviation — see `explanation.md` for the full linguistic analysis.
```