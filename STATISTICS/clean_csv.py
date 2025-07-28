import os
import csv
import pandas as pd


def process_csv_file(file_path):
    df = pd.read_csv(file_path, sep=';')

    for col in [f'Q{i}' for i in range(1, 51)]:
        df = df[(df[col] > 0) & (df[col] < 6)]

    sort_columns = ['Model', 'Character_Name']
    df_sorted = df.sort_values(by=sort_columns)

    base_name = os.path.splitext(file_path)[0]
    output_file = f"{base_name}_processed.csv"

    df_sorted.to_csv(output_file, sep=';', index=False)
    print(f"File elaborato salvato come: {output_file}")


def main():
    csv_dir = os.path.join(os.getcwd(), 'csv')

    csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]

    if not csv_files:
        print("Nessun file CSV trovato nella directory corrente.")
        return

    for csv_file in csv_files:
        file_path = os.path.join(csv_dir, csv_file)
        print(f"Elaborazione del file: {csv_file}")
        process_csv_file(file_path)


if __name__ == "__main__":
    main()