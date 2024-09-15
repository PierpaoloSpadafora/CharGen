import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import logging
import colorsys

from language import *

FIGURE_SIZE = (16, 10)
FIGURE_DPI = 300


def setup_logging():
    os.makedirs('./STATISTICS/graphs', exist_ok=True)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
def load_fail_data():
    fail_data = {
        "Gemma-2-27b-IQ2_M": 0,
        "Gemma-2-27b-Q3_K_S": 0,
        "Gemma-2-9b-Q5_K_M": 0,
        "Gemma-2-9b-Q8_0": 2,
        "LLaMA-3.1-8B-Q5_K_M": 47,
        "LLaMA-3.1-8B-Q8_0": 22
    }
    return pd.DataFrame(list(fail_data.items()), columns=['Model', 'Fails'])

def get_csv_files():
    csv_dir = './STATISTICS/csv'

    file_csv = []
    for f in os.listdir(csv_dir):
        if f.endswith('.csv'):
            file_csv.append(f)

    return file_csv


FILE_NAMES = get_csv_files()

def generate_distinct_colors(n):
    color_list = []
    for x in range(n):
        h = x * 1.0 / n  # in base all'indice
        s = 0.6
        v = 0.7
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        hex_color = '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))
        color_list.append(hex_color)

    return color_list

MODEL_COLORS = dict(zip([os.path.splitext(f)[0] for f in FILE_NAMES], generate_distinct_colors(len(FILE_NAMES))))

def load_data(file_name):
    try:
        file_path = os.path.join('./STATISTICS/csv', file_name)
        if not os.path.exists(file_path):
            logging.warning(FILE_NOT_FOUND_TEXT.format(file_path))
            return None

        df = pd.read_csv(file_path, sep=';')
        model_name = os.path.splitext(os.path.basename(file_name))[0]
        df['Model'] = model_name

        fail_data = load_fail_data()
        fails = fail_data[fail_data['Model'] == model_name]['Fails'].values[0]
        df['Fails'] = fails
        df['Success_Rate'] = 1000 / (1000 + fails)

        numeric_columns = ['Target_Openness', 'Target_Conscientiousness', 'Target_Extraversion',
                           'Target_Agreeableness', 'Target_Neuroticism',
                           'Test_Openness', 'Test_Conscientiousness', 'Test_Extraversion',
                           'Test_Agreeableness', 'Test_Neuroticism',
                           'Accuracy_Openness', 'Accuracy_Conscientiousness', 'Accuracy_Extraversion',
                           'Accuracy_Agreeableness', 'Accuracy_Neuroticism', 'Total_Accuracy', 'Duration']

        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')

        relevant_columns = ['Model', 'Fails', 'Success_Rate'] + numeric_columns
        df = df[relevant_columns]

        return df
    except Exception as e:
        logging.error(ERROR_PROCESSING_FILE_TEXT.format(file_name, str(e)))
        return None


def generate_model_colors(data):
    models = data['Model'].unique()
    n = len(models)
    color_list = [colorsys.hsv_to_rgb(i / n, 0.8, 0.8) for i in range(n)]
    return dict(zip(models, ['#%02x%02x%02x' % tuple(int(x * 255) for x in color) for color in color_list]))


def create_correlation_heatmap(data, model_name):
    traits = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']
    expected_cols = [f'Target_{trait}' for trait in traits]
    obtained_cols = [f'Test_{trait}' for trait in traits]

    missing_cols = [col for col in expected_cols + obtained_cols if col not in data.columns]
    if missing_cols:
        logging.warning(f"Missing columns for correlation heatmap: {missing_cols}")
        return

    corr = data[expected_cols + obtained_cols].corr().iloc[:5, 5:]

    plt.figure(figsize=FIGURE_SIZE)
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0, fmt='.2f')
    plt.title(CORRELATION_HEATMAP_TITLE_TEXT.format(model_name), fontsize=20)
    plt.tight_layout()
    filename = f'heatmap_{model_name}.png'
    plt.savefig(os.path.join('./STATISTICS/graphs', filename), dpi=FIGURE_DPI)
    plt.close()


def create_accuracy_boxplot(data):
    plt.figure(figsize=FIGURE_SIZE)
    sns.boxplot(data=data, x='Total_Accuracy', y='Model', hue='Model', palette=MODEL_COLORS, legend=False)
    plt.title(ACCURACY_BOXPLOT_TITLE_TEXT, fontsize=20)
    plt.xlabel('Total Accuracy', fontsize=16)
    plt.ylabel('Model', fontsize=16)

    x_min = max(0, data['Total_Accuracy'].min() - 5)
    x_max = min(100, data['Total_Accuracy'].max() + 5)
    plt.xlim(x_min, x_max)

    medians = data.groupby('Model')['Total_Accuracy'].median()
    means = data.groupby('Model')['Total_Accuracy'].mean()

    for i, (model, median) in enumerate(medians.items()):
        mean = means[model]
        plt.text(x_max, i, f'Median: {median:.2f}\nMean: {mean:.2f}',
                 ha='right', va='center', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join('./STATISTICS/graphs', 'accuracy_boxplot.png'), dpi=FIGURE_DPI)
    plt.close()


def create_duration_accuracy_scatter(data):
    plt.figure(figsize=FIGURE_SIZE)
    for model in data['Model'].unique():
        model_data = data[data['Model'] == model]
        plt.scatter(model_data['Duration'], model_data['Total_Accuracy'], label=model, color=MODEL_COLORS[model],
                    alpha=0.7, s=50)

    plt.title(DURATION_ACCURACY_SCATTER_TITLE_TEXT, fontsize=20)
    plt.xlabel('Duration (seconds)', fontsize=16)
    plt.ylabel('Total Accuracy', fontsize=16)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
    plt.xscale('log')

    x_min = max(1, data['Duration'].min() * 0.9)
    x_max = data['Duration'].max() * 1.1
    plt.xlim(x_min, x_max)

    y_min = max(0, data['Total_Accuracy'].min() - 5)
    y_max = min(100, data['Total_Accuracy'].max() + 5)
    plt.ylim(y_min, y_max)

    plt.grid(True, which="both", ls="-", alpha=0.2)

    tick_locations = np.logspace(np.log10(x_min), np.log10(x_max), num=10)
    tick_labels = [f"{t:.0f}" for t in tick_locations]
    plt.xticks(tick_locations, tick_labels)

    plt.gca().xaxis.set_minor_locator(plt.LogLocator(subs=np.arange(2, 10) * .1, numticks=100))
    plt.gca().xaxis.set_minor_formatter(plt.NullFormatter())

    plt.tight_layout()
    plt.savefig(os.path.join('./STATISTICS/graphs', 'duration_accuracy_scatter.png'), dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()


def create_trait_accuracy_boxplot(data):
    traits = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']
    melted_data = pd.melt(data, id_vars=['Model'], value_vars=[f'Accuracy_{trait}' for trait in traits],
                          var_name='Trait', value_name='Accuracy')
    melted_data['Trait'] = melted_data['Trait'].str.replace('Accuracy_', '')

    plt.figure(figsize=FIGURE_SIZE)
    sns.boxplot(data=melted_data, x='Trait', y='Accuracy', hue='Model', palette=MODEL_COLORS)
    plt.title(TRAIT_ACCURACY_BOXPLOT_TITLE_TEXT)
    plt.xlabel('Trait')
    plt.ylabel('Accuracy')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    y_min = max(0, melted_data['Accuracy'].min() - 5)
    y_max = min(100, melted_data['Accuracy'].max() + 5)
    plt.ylim(y_min, y_max)

    plt.tight_layout()
    plt.savefig(os.path.join('./STATISTICS/graphs', 'trait_accuracy_boxplot.png'), dpi=FIGURE_DPI)
    plt.close()


def create_accuracy_histograms(data):
    traits = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']
    models = data['Model'].unique()

    for trait in traits:
        fig, axes = plt.subplots(len(models), 1, figsize=FIGURE_SIZE, sharex=True, sharey=True)
        fig.suptitle(ACCURACY_HISTOGRAM_TITLE_TEXT.format(trait), fontsize=16)

        global_min = data[f'Accuracy_{trait}'].min()
        global_max = data[f'Accuracy_{trait}'].max()
        x_min = max(0, global_min - 5)
        x_max = min(100, global_max + 5)

        for i, model in enumerate(models):
            model_data = data[data['Model'] == model]
            sns.histplot(model_data[f'Accuracy_{trait}'], kde=True, ax=axes[i], color=MODEL_COLORS[model])
            axes[i].set_title(model)
            axes[i].axvline(model_data[f'Accuracy_{trait}'].mean(), color='red', linestyle='dashed', linewidth=2)
            axes[i].axvline(model_data[f'Accuracy_{trait}'].median(), color='green', linestyle='dashed', linewidth=2)

            legend = axes[i].get_legend()
            if legend:
                legend.remove()

            axes[i].set_xlim(x_min, x_max)

        lines = [plt.Line2D([0], [0], color='blue', lw=2),
                 plt.Line2D([0], [0], color='red', linestyle='dashed', lw=2),
                 plt.Line2D([0], [0], color='green', linestyle='dashed', lw=2)]
        labels = ['Distribution', 'Mean', 'Median']
        fig.legend(lines, labels, loc='center right', bbox_to_anchor=(1.15, 0.5))

        plt.tight_layout(rect=[0, 0, 0.85, 1])
        plt.savefig(f'./STATISTICS/graphs/histogram_{trait}.png', dpi=FIGURE_DPI, bbox_inches='tight')
        plt.close()


def create_success_rate_plot(data):
    plt.figure(figsize=FIGURE_SIZE)
    success_rates = data.groupby('Model')['Success_Rate'].mean().sort_values(ascending=False)

    sns.barplot(x=success_rates.index, y=success_rates.values, hue=success_rates.index, palette=MODEL_COLORS,
                legend=False)

    plt.title(SUCCESS_RATE_PLOT_TITLE_TEXT, fontsize=20)
    plt.xlabel('Model', fontsize=16)
    plt.ylabel('Success Rate', fontsize=16)
    plt.xticks(rotation=45, ha='right')

    min_rate = success_rates.min()
    y_min = max(0, min(min_rate - 0.20, min_rate * 0.8))
    plt.ylim(y_min, 1.01)

    for i, v in enumerate(success_rates.values):
        plt.text(i, v, f'{v:.4f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(os.path.join('./STATISTICS/graphs', 'success_rate_plot.png'), dpi=FIGURE_DPI)
    plt.close()


def generate_statistics():
    setup_logging()
    all_data = pd.concat([load_data(file_name) for file_name in FILE_NAMES if load_data(file_name) is not None],
                         ignore_index=True)

    if all_data.empty:
        logging.error("No data available after processing. Cannot generate statistics.")
        return False

    total_steps = len(all_data['Model'].unique()) + 5 # numero di grafici in totale da realizzare
    current_step = 0

    for model in all_data['Model'].unique():
        create_correlation_heatmap(all_data[all_data['Model'] == model], model)
        current_step += 1
        yield current_step / total_steps * 100

    create_accuracy_boxplot(all_data)
    current_step += 1
    yield current_step / total_steps * 100

    create_duration_accuracy_scatter(all_data)
    current_step += 1
    yield current_step / total_steps * 100

    create_trait_accuracy_boxplot(all_data)
    current_step += 1
    yield current_step / total_steps * 100

    create_accuracy_histograms(all_data)
    current_step += 1
    yield current_step / total_steps * 100

    create_success_rate_plot(all_data)
    current_step += 1
    yield current_step / total_steps * 100

    return True