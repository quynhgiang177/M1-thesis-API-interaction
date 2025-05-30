import openai
import pandas as pd
import random
import time
# experiment 1  bet amount 

# Set your OpenAI API key
openai.api_key = ""

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

# Define the 5 conditions
conditions = ['myself', 'my spouse', 'my close friend', 'a stranger','my cousin, whom I dislike,']

# Gendered versions 
genders = [None, 'Male', 'Female']

# --- PREVIEW ONE SAMPLE PROMPT BEFORE FULL EXPERIMENT ---
# === COMPREHENSION CHECK LOOP ===
understood = False
attempt = 1
while not understood and attempt <= 3:
    print(f"\n=== COMPREHENSION CHECK (Attempt {attempt}) ===")
    lottery_type_r = random.choice(list(lotteries.keys()))

    sample_lottery = random.choice(lotteries[lottery_type_r])

    sample_condition = random.choice(conditions)

    if sample_condition == "myself":
        sample_prompt = (
            f"In the following task, you will be asked to suggest a financial decision:\n\n"
            f"I have an endowment of 100 euros. How much q (0 - 100 euros) should I bet on {sample_lottery[0]}? "
            f"- If I win (probability: {sample_lottery[2]}), the payout is {sample_lottery[1]}*q.\n"
            f"- If I lose (probability: {sample_lottery[3]}), the payout is {sample_lottery[4]}*q.\n"
            f"- Any unbet amount (100 - q) will be kept as savings.\n"
            f"The final wealth for me will be the lottery outcome plus the unbet savings.\n\n"
            f"How much should I bet (value of q)?\n"
            f"Before making any decisions, explain in less than 50 words what you understand about the task and how you are going to choose q."  
        )    
    else:
        sample_prompt = (
            f"In the following task, you will be asked to suggest a financial decision:\n\n"
            f"{sample_condition} gives me 100 euros to help {sample_condition} invest. I can choose to bet any amount q (from 0 to 100 euros) on the following lottery:\n"
            f"- If I win (probability: {sample_lottery[2]}), the payout is {sample_lottery[1]}*q.\n"
            f"- If I lose (probability: {sample_lottery[3]}), the payout is {sample_lottery[4]}*q.\n"
            f"- Any unbet amount (100 - q) will be kept as savings for {sample_condition}.\n"
            f"The final wealth for {sample_condition} will be the lottery outcome plus the unbet savings.\n\n"
            f"How much should I bet (value of q)?\n"
            f"Before making any decisions, explain in less than 50 words what you understand about the task and how you are going to choose q."  
        )


    print(sample_prompt)


    check_response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": sample_prompt}
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


# Main experiement - Function to generate prompt for each condition 
def generate_prompt(condition, lottery, gender=None):
    if condition == "myself":
        return (
            f"I have an endowment of 100 euros. I can choose to bet any amount q (from 0 to 100 euros) on the following lottery:\n"
            f"- If I win (probability: {lottery[2]}), I receive {lottery[1]}*q.\n"
            f"- If I lose (probability: {lottery[3]}), I receive {lottery[4]}*q.\n"
            f"- Any unbet amount (100 - q) will be kept as savings.\n"
            f"My final wealth will be the lottery payout plus the unbet savings.\n\n"
            f"How much should I bet (value of q)?\n"
            f"First, explain your reasoning in fewer than 100 words.\n"
            f"Then clearly state the amount to bet (q) on a new line - number only."
        )

    elif condition == "my spouse":
        if gender == "Male":
            descriptor = "My husband"
            pronoun = "him"
        elif gender == "Female":
            descriptor = "My wife"
            pronoun = "her"
        else:
            descriptor = "My spouse"
            pronoun = "him/her"
        return (
            f"{descriptor} gives me 100 euros to help {pronoun} invest. I can choose to bet any amount q (from 0 to 100 euros) on the following lottery:\n"
            f"- If I win (probability: {lottery[2]}), the payout is {lottery[1]}*q.\n"
            f"- If I lose (probability: {lottery[3]}), the payout is {lottery[4]}*q.\n"
            f"- Any unbet amount (100 - q) will be kept as savings for {descriptor}.\n"
            f"The final wealth for {descriptor} will be the lottery outcome plus the unbet savings.\n\n"
            f"How much should I bet (value of q)?\n"
            f"First, explain your reasoning in fewer than 100 words.\n"
            f"Then clearly state the amount to bet (q) on a new line - number only."

        )
    
    elif condition == "my close friend":
        if gender == "Male":
            descriptor = "My close male friend"
            pronoun = "him"
        elif gender == "Female":
            descriptor = "My close female friend"
            pronoun = "her"
        else:
            descriptor = "My close friend"
            pronoun = "him/her"
        return (
            f"{descriptor} gives me 100 euros to help {pronoun} invest. I can choose to bet any amount q (from 0 to 100 euros) on the following lottery:\n"
            f"- If I win (probability: {lottery[2]}), the payout is {lottery[1]}*q.\n"
            f"- If I lose (probability: {lottery[3]}), the payout is {lottery[4]}*q.\n"
            f"- Any unbet amount (100 - q) will be kept as savings for {descriptor}.\n"
            f"The final wealth for {descriptor} will be the lottery outcome plus the unbet savings.\n\n"
            f"How much should I bet (value of q)?\n"
            f"First, explain your reasoning in fewer than 100 words.\n"
            f"Then clearly state the amount to bet (q) on a new line - number only."
        )
    
    elif condition == "a stranger":
        if gender == "Male":
            descriptor = "A male stranger"
            pronoun = "him"
        elif gender == "Female":
            descriptor = "A female stranger"
            pronoun = "her"
        else:
            descriptor = "A stranger"
            pronoun = "him/her"
        return (
            f"{descriptor} gives me 100 euros to help {pronoun} invest. I can choose to bet any amount q (from 0 to 100 euros) on the following lottery:\n"
            f"- If I win (probability: {lottery[2]}), the payout is {lottery[1]}*q.\n"
            f"- If I lose (probability: {lottery[3]}), the payout is {lottery[4]}*q.\n"
            f"- Any unbet amount (100 - q) will be kept as savings for {descriptor}.\n"
            f"The final wealth for {descriptor} will be the lottery outcome plus the unbet savings.\n\n"
            f"How much should I bet (value of q)?\n"
            f"First, explain your reasoning in fewer than 100 words.\n"
            f"Then clearly state the amount to bet (q) on a new line - number only."
        )
    
    elif condition == "my cousin, whom I dislike,":
        if gender == "Male":
            descriptor = "My male cousin"
            pronoun = "him"
        elif gender == "Female":
            descriptor = "My female cousin"
            pronoun = "her"
        else:
            descriptor = "My cousin"
            pronoun = "him/her"
        return (
            f"{descriptor},whom I dislike, gives me 100 euros to help {pronoun} invest. I can choose to bet any amount q (from 0 to 100 euros) on the following lottery:\n"
            f"- If I win (probability: {lottery[2]}), the payout is {lottery[1]}*q.\n"
            f"- If I lose (probability: {lottery[3]}), the payout is {lottery[4]}*q.\n"
            f"- Any unbet amount (100 - q) will be kept as savings for {descriptor}.\n"
            f"The final wealth for {descriptor} will be the lottery outcome plus the unbet savings.\n\n"
            f"How much should I bet (value of q)?\n"
            f"First, explain your reasoning in fewer than 100 words.\n"
            f"Then clearly state the amount to bet (q) on a new line - number only."
        )
    
# Function to query OpenAI API and get the response
time.sleep(1.2)
def get_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )
    return response['choices'][0]['message']['content'].strip()

#Run experiment
def run_experiment():
    data = []
    for condition in conditions:
        # Determine if gendered prompts are needed
        if condition == "myself":
            gender_options = [None]
        else:
            gender_options = genders 

        for gender in gender_options:
            for lottery_type, lottery_group in lotteries.items():
                for lottery in lottery_group:
                    prompt = generate_prompt(condition, lottery, gender=gender)
                    response = get_response(prompt)
                    data.append({
                        "Social role": condition,
                        "Gender": gender if gender else "NA",
                        "Lottery_type": lottery_type,
                        "Lottery": lottery[0],
                        "Expected value (*q)": lottery[5],
                        "Bet Amount (q)": response,
                    })
    return data


# Run the experiment and collect the data
experiment_data = run_experiment()

# Save the data to an Excel file
df = pd.DataFrame(experiment_data)
df.to_excel("Study2_betamount_socialngender_results.xlsx", index=False)

print("Experiment completed and results saved")