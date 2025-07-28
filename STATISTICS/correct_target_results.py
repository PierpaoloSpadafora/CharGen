import csv
import os
from pathlib import Path


def create_question_mapping():
    mapping = {}
    lista_di_eccezioni_negative = [29, 39, 49]
    lista_di_eccezioni_positive = [40, 42, 48, 50]

    for i in range(1, 51):
        trait = (i - 1) % 5 + 1
        direction = '-' if i % 2 == 0 else '+'

        if i in lista_di_eccezioni_negative:
            direction = '-'
        elif i in lista_di_eccezioni_positive:
            direction = '+'

        mapping[i] = (trait, direction)

    return mapping

def calculate_scores(answers, question_mapping):
    trait_scores = [0] * 6
    for question, score in answers.items():
        trait, direction = question_mapping[question]
        if direction == '+':
            trait_scores[trait] += score
        else:
            trait_scores[trait] += (6 - score)

    max_score = 50
    normalized_scores = [
        (trait_scores[1] / max_score) * 100,  # Extraversion
        (trait_scores[2] / max_score) * 100,  # Agreeableness
        (trait_scores[3] / max_score) * 100,  # Conscientiousness
        (trait_scores[4] / max_score) * 100,  # Neuroticism
        (trait_scores[5] / max_score) * 100   # Openness
    ]
    return normalized_scores

def calculate_accuracy(target, test):
    return 100 - abs(target - test)

def process_csv_files(directory):
    question_mapping = create_question_mapping()

    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = Path(directory) / filename
            output_path = Path(directory) / f"recalculated_{filename}"

            try:
                with file_path.open('r', newline='') as infile, output_path.open('w', newline='') as outfile:
                    reader = csv.DictReader(infile, delimiter=';')
                    fieldnames = reader.fieldnames
                    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')

                    writer.writeheader()
                    for row in reader:
                        try:
                            answers = {i: int(row[f'Q{i}']) for i in range(1, 51)}
                            new_scores = calculate_scores(answers, question_mapping)

                            traits = ['Extraversion', 'Agreeableness', 'Conscientiousness', 'Neuroticism', 'Openness']
                            total_accuracy = 0

                            for i, trait in enumerate(traits):
                                row[f'Test_{trait}'] = f"{new_scores[i]:.2f}"
                                target = float(row[f'Target_{trait}'])
                                accuracy = calculate_accuracy(target, new_scores[i])
                                row[f'Accuracy_{trait}'] = f"{accuracy:.2f}"
                                total_accuracy += accuracy

                            row['Total_Accuracy'] = f"{(total_accuracy / 5):.2f}"

                            writer.writerow(row)
                        except Exception as e:
                            print(f"Error processing row in {filename}: {e}")
                            continue

                print(f"Processed {filename}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

csv_directory = Path('./csv')
process_csv_files(csv_directory)