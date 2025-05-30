import openai
import pandas as pd
import random

# experiment 3 choosing A vs B with B gives a sure amount ranging from 6-21
# API key
openai.api_key = "api key"

# Define the lotteries (probability of high payoff, high payoff, low payoff, expected value of the lottery)
lotteries = [
    (0.25, 20, 4, 8),
    (0.375, 20, 4, 10),
    (0.5, 20, 4, 12),
    (0.75, 20, 4, 16),
    (0.2, 20, 5, 8),
    (0.4, 20, 5, 11),
    (0.6, 20, 5, 14),
    (0.8, 20, 5, 17),
    (0.5, 20, 6, 13),
    (0.25, 20, 8, 11),
    (0.5, 20, 8, 14),
    (0.75, 20, 8, 17)
]
# Range of guaranteed payoffs for Option B
sure_payoffs = list(range(5, 21))  # 5 to 20 euros

# === preview sample prompt and COMPREHENSION CHECK LOOP ===
understood = False
attempt = 1
while not understood and attempt <= 3:
    print(f"\n=== COMPREHENSION CHECK (Attempt {attempt}) ===")

    p, x1, x2, x3 = random.choice(lotteries)       # pick a random lottery
    c = random.choice(range(5,21))
       
    check_prompt = (
        f"You will be asked to choose between two options:\n"
        f"Option A: A lottery with {int(p*100)}% chance to win {x1} euros "
        f"and {(1 - p)*100:.0f}% chance to win {x2} euros.\n"
        f"Option B: A guaranteed payment of {c} euros.\n\n"
        f"Before making any decisions, explain in 2-3 sentences what you understand about the task and how you should choose. Your answer should be less than 30 words."
    )
    print(check_prompt)

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
    for i, (p, x1, x2, x3) in enumerate(lotteries):
        for b in sure_payoffs:    
            prompt = (
                f"Help me choose between:\n"
                f"Option A: A lottery with {int(p*100)}% chance to win {x1} euros "
                f"and {(1 - p)*100:.0f}% chance to win {x2} euros.\n"
                f"Option B: A guaranteed payment of {b} euros.\n\n"
                f"First, explain your reasoning in less than 50 words. Then clearly state your choice ('A' or 'B') on a new line."
            )

            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            answer = response['choices'][0]['message']['content'].strip().upper()

            data.append({
                "condition": "Step by step reasoning",
                "lottery_id": i + 1,
                "probability": p,
                "high_payoff": x1,
                "low_payoff": x2,
                "expected value lottery": x3,
                "sure_amount": b,
                "chatgpt_choice": answer
            })
    for i, (p, x1, x2, x3) in enumerate(lotteries):
        for b in sure_payoffs:    
            prompt = (
                f"Help me choose between:\n"
                f"Option A: A lottery with {int(p*100)}% chance to win {x1} euros "
                f"and {(1 - p)*100:.0f}% chance to win {x2} euros.\n"
                f"Option B: A guaranteed payment of {b} euros.\n\n"
                f"Clearly state your choice ('A' or 'B') without any explanation."
            )

            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=5
            )

            answer = response['choices'][0]['message']['content'].strip().upper()

            data.append({
                "condition": "Forced answer",
                "lottery_id": i + 1,
                "probability": p,
                "high_payoff": x1,
                "low_payoff": x2,
                "expected value lottery": x3,
                "sure_amount": b,
                "chatgpt_choice": answer
            })
    return data        

# Run the experiment and collect the data
experiment_data = run_experiment()

# Save the data to an Excel file
df = pd.DataFrame(experiment_data)
df.to_excel("study1task3_chatgpt_experiment_results6.xlsx", index=False)

print("Experiment completed. Results saved.")                

