import openai
import pandas as pd
import random

# experiment 1  bet amount 

# Set your OpenAI API key
openai.api_key = "API key"

# Define the lotteries (Name of the lottery, Win payoff, prob of win payoff, prob of lose payoff, lose payoff, expected value of lottery)
lotteries = {
    "Positive EV": [
        ("Lottery A", 3.5, 0.4, 0.6, 0, 1.4),
        ("Lottery B", 2.2, 0.6, 0.4, 0.3, 1.44),
        ("Lottery C", 5, 0.25, 0.75, 0.5, 1.625),
        ("Lottery C1", 2, 0.5, 0.5, 0.1, 1.05),
        ("Lottery C2", 2, 0.55, 0.45, 0.1, 1.145),
        ("Lottery C3", 2, 0.6, 0.4, 0.1, 1.24),
        ("Lottery C4", 2, 0.65, 0.35, 0.1, 1.335)
    ],
    "Negative EV": [
        ("Lottery D", 2.5, 0.33, 0.67, 0, 0.825),
        ("Lottery E", 1.8, 0.4, 0.6, 0.2, 0.84),
        ("Lottery F", 3, 0.2, 0.8, 0, 0.6),
        ("Lottery F1", 2, 0.4, 0.6, 0.1, 0.86),
        ("Lottery F2", 2, 0.35, 0.65, 0.1, 0.765),
        ("Lottery F3", 2, 0.30, 0.70, 0.1, 0.67),
        ("Lottery F4", 2, 0.25, 0.75, 0.1, 0.575)
    ],
    "Neutral EV": [
        ("Lottery G", 2, 0.5, 0.5, 0, 1),
        ("Lottery H", 1.5, 0.5, 0.5, 0.5, 1),
        ("Lottery I", 1.2, 0.5, 0.5, 0.8, 1),
        ("Lottery I1", 1.9, 0.5, 0.5, 0.1, 1),
        ("Lottery I2", 1.7, 0.5, 0.5, 0.3, 1),
        ("Lottery I3", 1.6, 0.5, 0.5, 0.4, 1),
        ("Lottery I4", 1.4, 0.5, 0.5, 0.6, 1)
    ]
}



# === COMPREHENSION CHECK LOOP ===
understood = False
attempt = 1
while not understood and attempt <= 3:
    print(f"\n=== COMPREHENSION CHECK (Attempt {attempt}) ===")
    lottery_type_r = random.choice(list(lotteries.keys()))

    sample_lottery = random.choice(lotteries[lottery_type_r])
    check_prompt = (
        f"I have an endowment of 100 euros. I can choose to bet any amount q (from 0 to 100 euros) on the following lottery:\n"
        f"- If I win (probability: {sample_lottery[2]}), I receive {sample_lottery[1]}*q.\n"
        f"- If I lose (probability: {sample_lottery[3]}), I receive {sample_lottery[4]}*q.\n"
        f"- Any unbet amount (100 - q) will be kept as savings.\n"
        f"My final wealth will be the lottery payout plus the unbet savings.\n"
        f"How much should I bet (value of q)?\n\n"
        f"Before making any decisions, explain in less than 50 words what you understand about the task and how you are going to choose q."
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

  

# Function to run the experiment
def run_experiment():
    data = []
    for lottery_type, lottery_group in lotteries.items():
        for lottery in lottery_group:
                prompt = (
                    f"I have an endowment of 100 euros. I can choose to bet any amount q (from 0 to 100 euros) on the following lottery:\n"
                    f"- If I win (probability: {lottery[2]}), I receive {lottery[1]}*q.\n"
                    f"- If I lose (probability: {lottery[3]}), I receive {lottery[4]}*q.\n"
                    f"- Any unbet amount (100 - q) will be kept as savings.\n"
                    f"My final wealth will be the lottery payout plus the unbet savings.\n\n"
                    f"How much should I bet (value of q)?\n"
                    f"First, explain your reasoning in fewer than 100 words.\n"
                    f"Then clearly state the amount to bet (q) on a new line - number only."
                )
                response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                )
                answer = response['choices'][0]['message']['content'].strip()
                
                data.append({
                    "Condition": "Step-by-Step reasoning",
                    "Lottery_type": lottery_type,
                    "Lottery": lottery[0],
                    "Expected value (*q)": lottery[5],
                    "Bet Amount (q)": answer,
                 })
    for lottery_type, lottery_group in lotteries.items():
        for lottery in lottery_group:
                prompt = (
                    f"I have an endowment of 100 euros. I can choose to bet any amount q (from 0 to 100 euros) on the following lottery:\n"
                    f"- If I win (probability: {lottery[2]}), I receive {lottery[1]}*q.\n"
                    f"- If I lose (probability: {lottery[3]}), I receive {lottery[4]}*q.\n"
                    f"- Any unbet amount (100 - q) will be kept as savings.\n"
                    f"My final wealth will be the lottery payout plus the unbet savings.\n\n"
                    f"How much should I bet (value of q)?\n"
                    f"Clearly state the amount of bet q (in numerical value only) you would suggest without any explanation."
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
                    "Condition": "Forced Answer",
                    "Lottery_type": lottery_type,
                    "Lottery": lottery[0],
                    "Expected value (*q)": lottery[5],
                    "Bet Amount (q)": answer,
                })            
                
    return data 

# Run the experiment and collect the data
experiment_data = run_experiment()

# Save the data to an Excel file
df = pd.DataFrame(experiment_data)
df.to_excel("Study1task1_betamount_result.xlsx", index=False)

print("Experiment completed and results saved")
