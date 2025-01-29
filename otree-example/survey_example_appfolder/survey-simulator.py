import random
from collections import defaultdict

# Constants
NUM_RESPONDENTS = 1000
QUESTIONS_PER_RESPONDENT = 10
PICTURES_PER_GROUP = 10
GROUPS = 4
LIMIT_PER_PICTURE = 125  # Per competence & trustworthiness

# Initialize counters for each picture in each group
competence_counters = defaultdict(int)
trustworthiness_counters = defaultdict(int)

# Generate all picture IDs (group 1 has pictures 1-10, group 2 has 11-20, etc.)
all_pictures = {group: list(range(group * 10 + 1, (group + 1) * 10 + 1)) for group in range(GROUPS)}


# Function to select a picture for a respondent
def assign_picture_and_question():
    available_pictures = []

    # Find pictures that still need ratings
    for group, pictures in all_pictures.items():
        for picture in pictures:
            if competence_counters[picture] < LIMIT_PER_PICTURE or trustworthiness_counters[
                picture] < LIMIT_PER_PICTURE:
                available_pictures.append((group, picture))

    if not available_pictures:
        return None, None  # No more questions available

    # Randomly select a picture from those still needing ratings
    group, selected_picture = random.choice(available_pictures)

    # Determine which question to ask
    competence_count = competence_counters[selected_picture]
    trustworthiness_count = trustworthiness_counters[selected_picture]

    if competence_count < LIMIT_PER_PICTURE and trustworthiness_count < LIMIT_PER_PICTURE:
        selected_question = random.choice(["competence", "trustworthiness"])
    elif competence_count >= LIMIT_PER_PICTURE:
        selected_question = "trustworthiness"
    else:
        selected_question = "competence"

    return selected_picture, selected_question


# Simulate survey responses
responses = []

for respondent_id in range(1, NUM_RESPONDENTS + 1):
    respondent_questions = []

    for _ in range(QUESTIONS_PER_RESPONDENT):
        selected_picture, selected_question = assign_picture_and_question()

        if selected_picture is None:
            break  # Stop if all pictures are fully rated

        respondent_questions.append((selected_picture, selected_question))

        # Update counters
        if selected_question == "competence":
            competence_counters[selected_picture] += 1
        else:
            trustworthiness_counters[selected_picture] += 1

    responses.append((respondent_id, respondent_questions))

# Validate results
total_competence = sum(competence_counters.values())
total_trustworthiness = sum(trustworthiness_counters.values())

print(f"Total competence ratings: {total_competence}")
print(f"Total trustworthiness ratings: {total_trustworthiness}")

# Check if each picture reached the correct limit
for group, pictures in all_pictures.items():
    for picture in pictures:
        print(
            f"Picture {picture}: Competence {competence_counters[picture]}, Trustworthiness {trustworthiness_counters[picture]}")

# Check if any respondents received fewer than 10 questions
respondents_with_fewer = sum(1 for r in responses if len(r[1]) < QUESTIONS_PER_RESPONDENT)
print(f"Respondents with fewer than {QUESTIONS_PER_RESPONDENT} questions: {respondents_with_fewer}")