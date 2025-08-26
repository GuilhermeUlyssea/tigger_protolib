from matplotlib.ticker import MultipleLocator
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
import pandas as pd
import numpy as np
import os


import scikit_posthocs as sp
from scipy.stats import kruskal

def multifile_compression(path)->pd.DataFrame:
    """
    Converts metric_results_fold-n files to a single dataframe;
    """

    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f ))]
    results_dict = {
        'run_number': [],	
        'mse_results_ensemble': [],	
        'mae_results_ensemble': [],
        'mape_results_ensemble': [],	
        'r2_results_ensemble': []

    }
    
    for file in range(len(files)):
        with open(fr'{path}\{files[file]}','r',encoding='utf-8') as f:
            content = f.readlines()
        #limpeza:
        content.pop(0)
        content.pop(len(content)-1)
        content = [content[i].strip() for i in range(len(content))]
        content = [content[i].removeprefix('        ') or content[i].removeprefix('    ')  for i in range(len(content))]
        content = [content[i].removesuffix(',') for i in range(len(content))]
        content = [content[i].split(':') for i in range(len(content))]
        content = [float(content[i][1].strip()) for i in range(len(content))]


        results_dict['run_number'].append(f'fold_{file+1}')
        results_dict['mse_results_ensemble'].append(content[0])
        results_dict['mae_results_ensemble'].append(content[1])
        results_dict['mape_results_ensemble'].append(content[2])
        results_dict['r2_results_ensemble'].append(content[3])
        
    dataframe = pd.DataFrame(results_dict)
    return dataframe

def single_processing(txt_file_path)->list:

    """
    Processes one single metric_results.txt.
    Returns dataframe.
    """

    with open(fr'{txt_file_path}','r',encoding='utf-8') as f:
            content = f.readlines()

    #limpeza:
    content.pop(0)
    content.pop(len(content)-1)
    #content.pop(len(content)-1)
    content = [content[i] for i in range(len(content))]
    content = [content[i].strip() for i in range(len(content))]
    content = [content[i].removeprefix('        ') or content[i].removeprefix('    ')  for i in range(len(content))]
    content = [content[i].removesuffix(': [') for i in range(len(content))]
    content = [content[i].removesuffix(',') for i in range(len(content))]
    content = [content[i] for i in range(len(content)) if content[i] != ']']
    content = [content[i] for i in range(len(content))]

    mse_results = content[1:11]
    mae_results = content[12:22]
    mape_results = content[23:33]
    r2_results = content[34:44]
    
    #print(len(mse_results),len(mae_results),len(mape_results),len(r2_results))
    results_dict = {
    'run_number': [f'fold_{i+1}' for i in range(len(mse_results))],	
    'mse_results_ensemble': [float(mse_results[i]) for i in range(len(mse_results))],	
    'mae_results_ensemble': [float(mae_results[i]) for i in range(len(mae_results))],
    'mape_results_ensemble': [float(mape_results[i]) for i in range(len(mape_results))],	
    'r2_results_ensemble': [float(r2_results[i]) for i in range(len(r2_results))]
    }

        

    data_sheet = pd.DataFrame(results_dict)
    
    return data_sheet



def multiexperiment_processing(txt_file_path)->list: 

    """
    
    Generates a list of pandas dataframes where each instance is generated from a
    metric_results.txt; Returns the current list;

    Returns a list of pandas dataframes.
    Works for 10 fold results only!

    """    

    path = rf"{txt_file_path}"
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f ))]
    sheet_list = []


    for name in range(len(files)):
        with open(fr'{path}\{files[name]}','r',encoding='utf-8') as f:
            content = f.readlines()

        #limpeza:
        content.pop(0)
        content.pop(len(content)-1)
        #content.pop(len(content)-1)
        content = [content[i] for i in range(len(content))]
        content = [content[i].strip() for i in range(len(content))]
        content = [content[i].removeprefix('        ') or content[i].removeprefix('    ')  for i in range(len(content))]
        content = [content[i].removesuffix(': [') for i in range(len(content))]
        content = [content[i].removesuffix(',') for i in range(len(content))]
        content = [content[i] for i in range(len(content)) if content[i] != ']']
        content = [content[i] for i in range(len(content))]
    
        mse_results = content[1:11]
        mae_results = content[12:22]
        mape_results = content[23:33]
        r2_results = content[34:44]
        
        #print(len(mse_results),len(mae_results),len(mape_results),len(r2_results))

        results_dict = {
        'run_number': [f'fold_{i+1}' for i in range(len(mse_results))],	
        'mse_results_ensemble': [float(mse_results[i]) for i in range(len(mse_results))],	
        'mae_results_ensemble': [float(mae_results[i]) for i in range(len(mae_results))],
        'mape_results_ensemble': [float(mape_results[i]) for i in range(len(mape_results))],	
        'r2_results_ensemble': [float(r2_results[i]) for i in range(len(r2_results))]
        }

        

        data_sheet = pd.DataFrame(results_dict)
        sheet_list.append(data_sheet)

    return sheet_list


def multibox_list(df_list, code_names):
    """
    Plota boxplots comparando métricas entre múltiplos DataFrames.

    Parâmetros:
    - df_list: lista de DataFrames pandas.
    - code_names: lista de nomes/códigos correspondentes aos DataFrames.
    """

    # Garantir que o tamanho das listas seja igual
    assert len(df_list) == len(code_names), "df_list e code_names devem ter o mesmo tamanho."

    # Mapear os DataFrames para seus rótulos
    all_dfs = {label: df.copy() for df, label in zip(df_list, code_names)}

    # Remover outliers de cada DataFrame, para cada métrica
    def remove_outliers_iqr(df, col):
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 0.01 * IQR
        upper = Q3 + 1.5 * IQR
        return df[(df[col] >= lower) & (df[col] <= upper)]

    metrics = ['mae_results_ensemble', 'mse_results_ensemble', 'r2_results_ensemble']
    for metric in metrics:
        for label in all_dfs:
            all_dfs[label] = remove_outliers_iqr(all_dfs[label], metric)

    metric_labels = {
        'mae_results_ensemble': 'MAE',
        'mse_results_ensemble': 'MSE',
        'r2_results_ensemble': 'R²'
    }

    def plot_metric_comparison(metric_key):
        df_plot = pd.concat([
            pd.DataFrame({
                'value': df[metric_key],
                'dataset': label,
                'metric': metric_labels[metric_key]
            }) for label, df in all_dfs.items()
        ])

        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df_plot, x='dataset', y='value', palette='Set2')
        plt.title(f'Comparative Boxplot - {metric_labels[metric_key]}')
        plt.ylabel(metric_labels[metric_key])
        plt.xlabel('')

        # Limites e espaçamento personalizados no eixo Y
        ax = plt.gca()
        if metric_key == 'mae_results_ensemble':
            plt.ylim(5, 15)
            ax.yaxis.set_major_locator(MultipleLocator(1))
        elif metric_key == 'mse_results_ensemble':
            plt.ylim(0, 550)
            ax.yaxis.set_major_locator(MultipleLocator(50))
        elif metric_key == 'r2_results_ensemble':
            plt.ylim(0.75, 1)
            ax.yaxis.set_major_locator(MultipleLocator(0.01))

        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

    for metric_key in metrics:
        plot_metric_comparison(metric_key)


def pareto_nested(df, prop=None, metric='MAE', xtick_step=10):
    """
    Plota um gráfico de Pareto horizontal por 'Qual Tec', filtrando por 'Prop' e utilizando a métrica escolhida.

    Parâmetros:
    - df: DataFrame com colunas ['File', 'Qual Tec', 'Prop', 'MAE', 'MSE']
    - prop: valor da coluna 'Prop' para filtrar os dados (ex: 'LR'); se None, não filtra
    - metric: nome da métrica a ser usada no eixo X ('MAE' ou 'MSE')
    - xtick_step: espaçamento entre os ticks do eixo X
    """

    # Validação
    if metric not in df.columns:
        raise ValueError(f"Métrica '{metric}' não encontrada no DataFrame. Use uma das colunas: {list(df.columns)}")

    # Filtro por 'Prop', se fornecido
    df_filtered = df.copy()
    if prop is not None:
        df_filtered = df_filtered[df_filtered['Prop'] == prop]
        if df_filtered.empty:
            raise ValueError(f"Nenhuma linha encontrada com Prop = '{prop}'.")

    # Preparar dados
    df_filtered['File'] = df_filtered['File'].astype(str)
    df_filtered['Qual Tec'] = df_filtered['Qual Tec'].astype(str)
    df_filtered['rank'] = df_filtered.groupby('Qual Tec')[metric].rank(method='first', ascending=False)
    df_filtered.sort_values(by=['Qual Tec', 'rank'], inplace=True)

    # Plot
    plt.figure(figsize=(14, 8))
    ax = sns.barplot(
        data=df_filtered,
        y='Qual Tec',
        x=metric,
        hue='File',
        palette='tab20'
    )

    # Eixo superior duplicado
    ax_top = ax.twiny()
    ax_top.set_xlim(ax.get_xlim())

    # Definir xticks
    max_x = ax.get_xlim()[1]
    ticks = np.arange(0, max_x + xtick_step, xtick_step)
    ax.set_xticks(ticks)
    ax_top.set_xticks(ticks)

    # Rótulos
    ax.set_xlabel(metric)
    #ax_top.set_xlabel(f"{metric} (eixo superior)")
    ax.set_ylabel("Qual Tec")

    # Título
    title = f"Pareto Diagram by 'Qual Tec' - Metric {metric}"
    if prop is not None:
        title += f" | Prop = {prop}"
    plt.title(title)

    # Legenda
    ax.legend(title="Model", bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0)

    plt.tight_layout()
    plt.show()

def plot_filtered_mean_heatmap(df, label_col='label', cmap='viridis'):
    """
    Plota um heatmap com a média das features por label.

    Parâmetros:
    - df: DataFrame contendo features numéricas e uma coluna categórica com os labels.
    - label_col: nome da coluna que contém os labels (padrão: 'label').
    - cmap: colormap para o heatmap (padrão: 'viridis').
    """

    # Verifica se a coluna de label está presente
    if label_col not in df.columns:
        raise ValueError(f"A coluna '{label_col}' não foi encontrada no DataFrame.")

    # Separa apenas colunas numéricas
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    if not numeric_cols:
        raise ValueError("O DataFrame não contém colunas numéricas para cálculo de médias.")

    # Agrupa por label e calcula a média das features
    df_grouped = df.groupby(label_col)[numeric_cols].mean()

    # Plot do heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(df_grouped, annot=True, fmt=".2f", cmap=cmap,
                linewidths=0.5, linecolor='gray')
    plt.title("Média das Features por Label")
    plt.xlabel("Feature")
    plt.ylabel("Label")
    plt.tight_layout()
    plt.show()



def plot_feature_means_2d(df, category_col, cmap='viridis', annot_fontsize=8):
    """
    Plota um heatmap 2D com a média das features agrupadas pelas categorias da dimensão.

    Parâmetros:
    - df: DataFrame contendo features numéricas e uma coluna categórica.
    - category_col: nome da coluna categórica para agrupar (ex: 'label').
    - cmap: colormap para o heatmap (padrão: 'viridis').
    - annot_fontsize: tamanho da fonte dos números anotados no heatmap (padrão: 8).
    """

    if category_col not in df.columns:
        raise ValueError(f"A coluna '{category_col}' não foi encontrada no DataFrame.")

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if not numeric_cols:
        raise ValueError("O DataFrame não contém colunas numéricas para cálculo de médias.")

    # Agrupa por categoria e calcula a média das features
    df_grouped = df.groupby(category_col)[numeric_cols].mean()

    plt.figure(figsize=(12, max(4, len(df_grouped)*0.5)))
    sns.heatmap(
        df_grouped,
        annot=True,
        fmt=".2f",
        cmap=cmap,
        annot_kws={'size': annot_fontsize},
        linewidths=0.5,
        linecolor='gray'
    )
    plt.title(f"Média das Features por {category_col}")
    plt.xlabel("Feature")
    plt.ylabel(category_col)
    plt.tight_layout()
    plt.show()



def plot_multiple_proportions(data_dict, ref_dim, title):
    """
    Script developed to plot proportions of the data based on selected classes;

    Output:
        Segmented Barplot with proportions

    data_dict: dicionário com nome da base como chave e DataFrame como valor.
    ref_dim: coluna de referência para calcular proporções.
    title: título do gráfico.

    Ex:

    data_dict:
    data_dict = {}

    for i in range(len(sub_dir)):
        
        data_consolidated = pd.read_csv(rf"{base_dir}\{sub_dir[i]}\data_consolidated.csv")
        #database_list.append(data_consolidated)
    
        aux_consolidated = pd.read_csv(rf"{base_dir}\{sub_dir[i]}\aux_consolidated.csv")
        df_all = pd.concat([data_consolidated,aux_consolidated], axis=1)
        database_list.append(df_all)
    
    
    data_dict['GR3'] = database_list[0]
    data_dict['HSS1'] = database_list[1]           #DP-TRIP
    data_dict['HSS2'] = database_list[2]           #DP-TRIP-HSLA
    data_dict['LSS1'] = database_list[4]           #IF-BH
    data_dict['LSS2'] = database_list[3]           #IF-BH-HSLA


    """
    # Obter todas as categorias únicas
    all_categories = set()
    for df in data_dict.values():
        all_categories.update(df[ref_dim].unique())
    all_categories = sorted(list(all_categories))

    # Paleta de cores
    palette = sns.color_palette("Set2", n_colors=len(all_categories))
    color_map = dict(zip(all_categories, palette))

    # Construir DataFrame com proporções
    proportion_df = pd.DataFrame(columns=['base', 'category', 'proportion'])

    for base_name, df in data_dict.items():
        counts = df[ref_dim].value_counts(normalize=True)
        for cat in all_categories:
            proportion = counts.get(cat, 0)
            proportion_df = pd.concat([proportion_df, pd.DataFrame({
                'base': [base_name],
                'category': [cat],
                'proportion': [proportion]
            })])

    # Pivotar para gráfico empilhado
    pivot_df = proportion_df.pivot(index='base', columns='category', values='proportion')
    pivot_df = pivot_df.fillna(0)  # garantir 0 nas ausências

    # Plotar gráfico empilhado
    pivot_df.plot(kind='bar', stacked=True, color=[color_map[cat] for cat in pivot_df.columns], figsize=(10, 6))

    # Adicionar porcentagens no centro de cada segmento
    for i, base in enumerate(pivot_df.index):
        bottom = 0
        for cat in pivot_df.columns:
            value = pivot_df.loc[base, cat]
            if value > 0.01:  # exibe só se for maior que 1%
                plt.text(i, bottom + value / 2, f'{cat}\n{value:.0%}', ha='center', va='center', fontsize=9)
            bottom += value

    plt.title(f'{title} by {ref_dim}', fontsize=14)
    plt.ylabel('Proportion')
    plt.xlabel('Dataset')
    plt.xticks(rotation=45)
    plt.ylim(0, 1)
    plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='lower right')
    plt.tight_layout()
    plt.show()


def plot_proportions(aux_data,ref_dim, title):
    """
    Plot single database proportions based on a reference dimension.
    Returns single bar plot with the proportions.
    """

    # Contagem e proporção
    counts = aux_data[ref_dim].value_counts(normalize=True)  # proporção
    categories = counts.index.tolist()
    proportions = counts.values

    # Cores diferentes por categoria
    palette = sns.color_palette("Set2", n_colors=len(categories))
    color_map = dict(zip(categories, palette))
    colors = [color_map[cat] for cat in categories]

    # Plot
    fig, ax = plt.subplots(figsize=(10, 2))

    # Desenha os segmentos da barra
    start = 0
    for prop, cat, color in zip(proportions, categories, colors):
        ax.barh(0, width=prop, left=start, color=color, edgecolor='white', height=0.5)
        ax.text(start + prop / 2, 0, f'{cat} ({prop:.1%})', va='center', ha='center', fontsize=10, rotation=90)
        start += prop

    # Ajustes visuais
    ax.set_xlim(0, 1)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title(f"{title} by {ref_dim}:", fontsize=14)
    sns.despine(left=True, bottom=True)

    plt.tight_layout()
    plt.show()

    
def plot_proportions_unstacked(aux_data, ref_dim, title):
    """
    Plota as proporções de categorias em barras separadas (não empilhadas).
    """

    # Contagem e proporção
    counts = aux_data[ref_dim].value_counts(normalize=True)
    categories = counts.index.tolist()
    proportions = counts.values

    # Cores
    palette = sns.color_palette("Set2", n_colors=len(categories))
    color_map = dict(zip(categories, palette))
    colors = [color_map[cat] for cat in categories]

    # Plot
    fig, ax = plt.subplots(figsize=(10, 4))
    bars = ax.bar(categories, proportions, color=colors, edgecolor='black')

    # Adiciona rótulos acima de cada barra
    for bar, prop in zip(bars, proportions):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f'{prop:.1%}', ha='center', va='bottom', fontsize=10)

    # Ajustes visuais
    ax.set_ylim(0, 1)
    ax.set_ylabel('Proportion')
    ax.set_title(f"{title} by {ref_dim}:", fontsize=14)
    sns.despine()

    plt.tight_layout()
    plt.show()



def multi_kde_plot(df_list, labels, image_path):
    """
    Plota múltiplos gráficos KDE (um por dimensão), sobrepondo distribuições de vários DataFrames.

    Parâmetros:
    - df_list: lista de DataFrames pandas.
    - labels: lista de nomes/etiquetas (strings) para identificar cada DataFrame nos plots.
    - image_path: caminho onde as imagens PNG serão salvas.

    Obs: Assume-se que todos os DataFrames têm as mesmas colunas.
    """
    assert len(df_list) == len(labels), "df_list e labels devem ter o mesmo comprimento"
    
    # Garante que o diretório de saída exista
    os.makedirs(image_path, exist_ok=True)
    
    # Pega o índice (colunas) a partir do primeiro DataFrame
    columns = df_list[0].columns

    for col in columns:
        plt.figure(figsize=(10, 6))

        # Plota o KDE para cada DataFrame na dimensão atual
        for df, label in zip(df_list, labels):
            if df[col].nunique() > 1:  # KDE precisa de variabilidade
                sns.kdeplot(data=df, x=col, fill=True, label=label, alpha=0.5)

        plt.title(f'KDE: {col}')
        plt.xlabel(col)
        plt.ylabel('Density')
        plt.grid(True)
        plt.legend()
        
        # Salva imagem
        plt.savefig(os.path.join(image_path, f'KDE_{col}.png'))
        plt.close()


def prepare_data(metric1, metric2, nome_metrica, title1, title2):
    """
    Concatenates two columns of a dataframe based on equal column names;
    Columns must be lists!
    -title1: title from first db
    -title2: title from second db

    Example:

    df_mae = preparar_dados(
        V2RP4P10D['mae_results_ensemble'].tolist(),
        V3R['mae_results_ensemble'].tolist(),
        'MAE',
        'V2RP4P10D',
        'V3R'
    )
    """

    df1 = pd.DataFrame({'valor': metric1, 'grupo': title1, 'metrica': nome_metrica})
    df2 = pd.DataFrame({'valor': metric2, 'grupo': title2, 'metrica': nome_metrica})
    return pd.concat([df1, df2], ignore_index=True)


def dunn_test(df_mae, df_mse, df_r2):

    """
    Execute Dunn Test to compare models based on MAE, MSE and R2.
    - df_mae: dataframe with MAE

    returns terminal result
    
    """

    for df_metric in [df_mae, df_mse, df_r2]:
        nome_metrica = df_metric['metrica'].iloc[0]
        print(f"\n===== Análise para {nome_metrica} =====")

        # Boxplot (opcional)
        plt.figure(figsize=(8, 5))
        sns.boxplot(data=df_metric, x='grupo', y='valor')
        plt.title(f'Distribuição de {nome_metrica} por grupo')
        plt.show()

        # Teste de Kruskal-Wallis
        grupos = [df_metric[df_metric['grupo'] == g]['valor'] for g in df_metric['grupo'].unique()]
        stat, p = kruskal(*grupos)
        print(f"Kruskal-Wallis: estatística = {stat:.3f}, p = {p:.5f}")

        if p < 0.05:
            print("→ H₀ rejeitada: há diferença significativa → Teste de Dunn")
            dunn = sp.posthoc_dunn(df_metric, val_col='valor', group_col='grupo', p_adjust='bonferroni')
            print("\nResultado do teste de Dunn (valores-p ajustados):")
            print(dunn)
        else:
            print("→ H₀ não rejeitada: sem diferença significativa entre os grupos.")


def boxplot(df, x_dim, y_dim, x_title, y_title, title, ):

    """
    Normal box-plot XD
    """

    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x=f'{x_dim}', y=f'{y_dim}')  # substitua pelos nomes corretos
    plt.axhline(10, color='red', linestyle='--')  # útil se erro pode ser negativo
    plt.ylim(0, 100)  # mínimo e máximo do eixo Y
    plt.yticks(np.arange(0, 101, 10)) #np.arange(0, 101, 10)
    plt.title(f"{title}")
    plt.xlabel(f"{x_title}")
    plt.ylabel(f"{y_title}")
    plt.yticks()
    plt.tight_layout()
    plt.show()



def process_individual_metrics(path)->list:

    """
    Script to process multiple models individual metric results ('ind_metric_results_fold-n.txt').
    The function receives a folder path containing sub-folders. Each sub-folder has 'ind_metric_results_fold-n.txt'
    files.

    - Clean each .txt file associated to a fold
    - Generate one dict with the data from 'ind_metric_results_fold-0.txt' to 'ind_metric_results_fold-n.txt'
    - Converts dict into a pd.Dataframe
    - Appends the pd.Dataframe to 'dataframe_list'
    - Repeats the process for each model result

    Returns 'dataframe_list', a list od pd.Dataframes (output) given the main path to all folders with model results.
    
    """

    
    dataframe_list = []
    
    folders = [folder for folder in os.listdir(path)]
    print(folders)
    for folder in range(len(folders)):

        sub_path = rf'{path}\{folders[folder]}'
        files = [f for f in os.listdir(sub_path) if f.endswith('.txt')]
        files = files[:(len(files))-1]

        results_dict = {
            'fold': [],
            'output': [],
            'MAE': [],
            'MSE': [],
            'R2': []
        }

        for file in range(len(files)):
            with open(rf'{sub_path}\{files[file]}','r',encoding='utf-8') as f:

                content = f.readlines()
                content = [content[i].strip() for i in range(len(content))]
                content.pop(0)
                content.pop(len(content)-1)
                content.pop(len(content)-1)
                content = [content[i].removesuffix(': [')  for i in range(len(content))]
                content = [content[i].removesuffix('],')  for i in range(len(content))]
                content = [content[i].removesuffix('')  for i in range(len(content))]
                content = [content[i].removesuffix(',')  for i in range(len(content))]
                content = [content[i] for i in range(len(content)) if content[i] != '']
                content = content[4:]


                mse = content[1:4]
                mae = content[5:8]
                r2 = content[13:]

                mse = [float(mse[i]) for i in range(3)]
                mae = [float(mae[i]) for i in range(3)]
                r2 = [float(r2[i]) for i in range(3)]


                results_dict['fold'].append(f'fold-{file}')
                results_dict['fold'].append(f'fold-{file}')
                results_dict['fold'].append(f'fold-{file}')

                results_dict['output'].append('LE')
                results_dict['output'].append('LR')
                results_dict['output'].append('AL')


                results_dict['MAE'].append(mae[0])
                results_dict['MAE'].append(mae[1])
                results_dict['MAE'].append(mae[2])

                results_dict['MSE'].append(mse[0])
                results_dict['MSE'].append(mse[1])
                results_dict['MSE'].append(mse[2])

                results_dict['R2'].append(r2[0])
                results_dict['R2'].append(r2[1])
                results_dict['R2'].append(r2[2])        
                
        df = pd.DataFrame(results_dict)
        dataframe_list.append(df)
    
    return dataframe_list


def remove_outliers_iqr2(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return df[(df[col] >= lower) & (df[col] <= upper)]


def group_boxplot(list_df, model_names, metric, y_min, y_max, y_step, selected_outputs=None, remove_outliers=True):
    """
    Multiple box-plot based on individual outputs for the selected metrics.
    
    selected_outputs: list of output names to include in the plot (default: None, use all)
    remove_outliers: aplica a função remove_outliers_iqr na métrica escolhida (default: True)
    """

    if len(list_df) != len(model_names):
        raise ValueError("O número de dataframes deve ser igual ao número de nomes de modelos.")

    # Adiciona coluna Model e remove outliers se necessário
    df_list = []
    for df, name in zip(list_df, model_names):
        temp = df.copy()
        temp['Model'] = name

        df_list.append(temp)

    df_all = pd.concat(df_list, ignore_index=True)

    # Filtra outputs caso o usuário forneça uma lista
    if selected_outputs is not None:
        df_all = df_all[df_all['output'].isin(selected_outputs)]

    # Lista única de outputs a serem plotados
    outputs = df_all['output'].unique()

    # Criar coluna auxiliar 'plot_order' e ordem dos ticks, incluindo espaçamento entre modelos
    ordem = []
    x_labels = []
    for i, model in enumerate(model_names):
        model_outputs = [out for out in outputs if not df_all[(df_all['Model'] == model) & (df_all['output'] == out)].empty]
        for out in model_outputs:
            ordem.append((model, out))
            x_labels.append(out)
        # Adiciona espaço apenas se não for o último modelo
        if i != len(model_names) - 1:
            ordem.append((None, None))
            x_labels.append('')

    # Coluna para plot_order
    df_all['plot_order'] = list(zip(df_all['Model'], df_all['output']))

    plt.figure(figsize=(12, 6))
    ax = sns.boxplot(
        x='plot_order',
        y=metric,
        data=df_all,
        showfliers=remove_outliers,
        hue='Model',
        dodge=False,
        order=ordem,
        palette='Set2'
    )

    # Ajusta eixo y
    step = np.arange(y_min, y_max + y_step, y_step)
    plt.yticks(step)
    plt.ylabel(metric)
    plt.xlabel('Output')
    plt.title(f'Model Results by Output for {metric} Test Metric')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Eixo x inferior: outputs
    ax.set_xticklabels(x_labels, rotation=0)

    # Eixo x superior: nome dos modelos
    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    model_positions = []
    start = 0
    for i, model in enumerate(model_names):
        n = sum(1 for out in outputs if not df_all[(df_all['Model'] == model) & (df_all['output'] == out)].empty)
        pos = start + (n - 1) / 2 if n > 0 else start
        model_positions.append(pos)
        start += n + 1 if i != len(model_names) - 1 else n  # não adiciona espaço no último modelo
    ax2.set_xticks(model_positions)
    ax2.set_xticklabels(model_names)
    ax2.set_xlabel('Model Group')

    # Apenas uma legenda (do eixo principal)
    ax.legend(title='Model')

    plt.tight_layout()
    plt.show()



def barplot(dataframe, x_dim, y_dim, step, x_title,y_title,title,hue,colors):
    """
    Simply a barplot :)
    -x_dim,y_dim: dimensions of the df (str)

    """
    plt.figure(figsize=(8, 6))
    if hue == None or colors == None:
        sns.barplot(
            data=dataframe,
            x=x_dim,
            y=y_dim, 
            color="steelblue"
        )
    else:
        sns.barplot(
            data=dataframe,
            x=x_dim,
            y=y_dim, 
            hue = hue,
            palette=colors,
            dodge=False
        )
    # Ajustar título e eixos
    plt.yticks(step)
    plt.title(f"{title}", fontsize=14)
    plt.xlabel(f"{x_title}",fontsize=10)
    plt.ylabel(f"{y_title}",fontsize=10)
    plt.grid(axis='y',linestyle='--', alpha=0.7)

    plt.show()

    
def preprocess_time(path):
    
    file_names = [f for f in os.listdir(path) if f.endswith('.txt')]
    result_list = []

    for file in range(len(file_names)):
        with open(rf'{path}\{file_names[file]}','r',encoding='utf-8') as f:
            print(f"Preprocessing {file_names[file]}...")

            content = f.readlines()
            content = [content[i].strip() for i in range(len(content))]
            content[0] = content[0][12:]
            content[1] = content[1][12:] 
            content[2] = content[2][13:]
            content[3] = content[3][26:]

            content = [content[i].strip() for i in range(len(content))]
            content = [content[i].removeprefix('(') for i in range(len(content))]
            content = [content[i].removesuffix(')') for i in range(len(content))]

            temp = content[0].split(',') 
            content[0] = temp[0]

            try:
                temp = datetime.strptime(content[1],"%H:%M:%S.%f")
                td = temp - temp.replace(hour=0, minute=0, second=0, microsecond=0)
                temp = td.total_seconds() / 3600
                content[1] = temp

            except:
                days,time = content[1].split(" day,")
                days = float(days.strip())
                time = time.strip()

                temp = datetime.strptime(time,"%H:%M:%S.%f")
                td = temp - temp.replace(hour=0, minute=0, second=0, microsecond=0)
                td = td.total_seconds() / 3600

                temp = 24.0*days + td
                content[1] = temp
            print(temp)
            content = [float(content[i]) for i in range(len(content))]
            
            results = {
                'Input shape': content[0],
                'Time taken': content[1],
                'Peak memory': content[2],
                'Total memory': content[3]
            }

            result_list.append(results)
    
    return result_list

path = r'C:\Users\guiul\OneDrive\Área de Trabalho\Tigger Analytics\Projetos\ArcellorMital\DataAnalysis\SpecializedModels\Results\ProcessingResults'
r = preprocess_time(path)
print(r)

