import openai
import pandas as pd
import random

# experiment 2 choosing A vs B with B gives a sure amount equals expected value of A
# API key
openai.api_key = "api key"

# Define the gain lotteries (probability, high payoff, low payoff) 
lotteries = [
    (0.20, 20, 5),
    (0.21, 20, 5),
    (0.22, 20, 5),
    (0.23, 20, 5),
    (0.24, 20, 5),
    (0.25, 20, 5),
    (0.26, 20, 5),
    (0.27, 20, 5),
    (0.28, 20, 5),
    (0.29, 20, 5),
    (0.30, 20, 5),
    (0.31, 20, 5),
    (0.32, 20, 5),
    (0.33, 20, 5),
    (0.34, 20, 5),
    (0.35, 20, 5),
    (0.36, 20, 5),
    (0.37, 20, 5),
    (0.38, 20, 5),
    (0.39, 20, 5),
    (0.40, 20, 5),
    (0.41, 20, 5),
    (0.42, 20, 5),
    (0.43, 20, 5),
    (0.44, 20, 5),
    (0.45, 20, 5),
    (0.46, 20, 5),
    (0.47, 20, 5),
    (0.48, 20, 5),
    (0.49, 20, 5),
    (0.50, 20, 5),
    (0.51, 20, 5),
    (0.52, 20, 5),
    (0.53, 20, 5),
    (0.54, 20, 5),
    (0.55, 20, 5),
    (0.56, 20, 5),
    (0.57, 20, 5),
    (0.58, 20, 5),
    (0.59, 20, 5),
    (0.60, 20, 5),
    (0.61, 20, 5),
    (0.62, 20, 5),
    (0.63, 20, 5),
    (0.64, 20, 5),
    (0.65, 20, 5),
    (0.66, 20, 5),
    (0.67, 20, 5),
    (0.68, 20, 5),
    (0.69, 20, 5)
]

# --- PREVIEW ONE SAMPLE PROMPT BEFORE FULL EXPERIMENT ---
p, x1, x2 = random.choice(lotteries)       # pick a random lottery

sample_prompt = (
    f"I am deciding on behalf of myself.\n"
    f"Help me choose between:\n"
    f"Option A: A lottery with {int(p*100)}% chance to win {x1} euros "
    f"and {(1 - p)*100:.0f}% chance to win {x2} euros.\n"
    f"Option B: A guaranteed payment of {x1*p + x2*(1-p)} euros.\n\n"
    f"Clearly state your choice ('A' or 'B') without any explaination."
)

print("=== SAMPLE PROMPT PREVIEW ===\n")
print(sample_prompt)
input("\nIf this prompt looks good, press Enter to continue with the experiment...")

# === COMPREHENSION CHECK LOOP ===
understood = False
attempt = 1
while not understood and attempt <= 3:
    print(f"\n=== COMPREHENSION CHECK (Attempt {attempt}) ===")
    
    check_prompt = (
        "You will be asked to choose between two options:\n"
        "Option A: A lottery with 75% chance to win 20 euros, and 25% chance to win 5 euros.\n"
        "Option B: A guaranteed payment of 16.25 euros.\n\n"
        "Before making any decisions, explain in 2-3 sentences what you understand about the task. "
        "Summarize what Option A and B represent, and how you should choose. Your answer should be less than 30 words."
    )

    check_response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": check_prompt}
        ],
        temperature=0
    )

    check_answer = check_response['choices'][0]['message']['content'].strip()
    print("\nChatGPT's Response:")
    print(check_answer)

    user_input = input("\nDid ChatGPT understand the task correctly? Type 'yes' to proceed or anything else to retry: ").strip().lower()
    understood = user_input == "yes"
    attempt += 1

if not understood:
    print("\nAborting: ChatGPT did not pass comprehension check.")
    exit()

print("\nComprehension check passed. Proceeding with experiment...")

# === MAIN EXPERIMENT ===
def run_experiment():
    data = []
    for i, (p, x1, x2) in enumerate(lotteries):
            prompt1 = (
                f"I am deciding on behalf of myself.\n"
                f"Help me choose between:\n"
                f"Option A: A lottery with {int(p*100)}% chance to win {x1} euros "
                f"and {(1 - p)*100:.0f}% chance to win {x2} euros.\n"
                f"Option B: A guaranteed payment of {x1*p + x2*(1 - p):.2f} euros.\n\n"
                f"First, explain your reasoning (in less than 50 words). "
                f"Then clearly state your choice ('A' or 'B') on a new line."
            )

            response1 = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt1}
                ],
                temperature=0,
            )

            answer = response1['choices'][0]['message']['content'].strip().upper()
           
            data.append({
                "condition": "Step-by-Step reasoning",
                "lottery_id": i + 1,
                "probability": p,
                "high_payoff": x1,
                "low_payoff": x2,
                "sure_amount": (x1*p + x2*(1-p)),
                "chatgpt_choice": answer,
            })

    for i, (p, x1, x2) in enumerate(lotteries):
            prompt1 = (
                f"I am deciding on behalf of myself.\n"
                f"Help me choose between:\n"
                f"Option A: A lottery with {int(p*100)}% chance to win {x1} euros"
                f"and {(1 - p)*100:.0f}% chance to win {x2} euros.\n"
                f"Option B: A guaranteed payment of {x1*p+x2*(1-p)} euros.\n\n"
                f"Clearly state your choice ('A' or 'B') without any explaination."
            )

            response1 = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt1}
                ],
                temperature=0,
                max_tokens=5
            )

            answer1 = response1['choices'][0]['message']['content'].strip().upper()

            
            data.append({
                "condition": "Forced Answer",
                "lottery_id": i + 1,
                "probability": p,
                "high_payoff": x1,
                "low_payoff": x2,
                "sure_amount": (x1*p + x2*(1-p)),
                "chatgpt_choice": answer1,
            })        
    return data        

# Run the experiment and collect the data
experiment_data = run_experiment()

# Save the data to an Excel file
df = pd.DataFrame(experiment_data)
df.to_excel("study1task2_chatgpt_experiment_results3.xlsx", index=False)

print("Experiment completed. Results saved.")