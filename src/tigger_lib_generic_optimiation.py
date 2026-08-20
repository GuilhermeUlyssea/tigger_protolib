from matplotlib.ticker import MultipleLocator
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from scipy.stats import kruskal
from datetime import datetime
import scikit_posthocs as sp
import seaborn as sns
import pandas as pd
import numpy as np
import json
import os


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

def history_to_db(history_path)->pd.DataFrame:
    """
    Function that converts history data to a database.
    Input: path to optimization history
    Output: pd.Dataframe
    """

    files = os.listdir(history_path)
    results_dict = {
        'FILE': [],
        'HV': [],
        'IGD': [],
        'DNPW': [],
        'FQ': [],
        'SP': [],
        'SVC': []
    }

    for file in files:
        file_name = file
        sub_path = os.path.join(history_path,file)
        with open(sub_path, 'r') as file:
            content = json.load(file)

            for i in range(len(content['results']['METRICS'])): #No futuro para outras metrics, try except
                try:
                    hv = content['results']['METRICS'][i]['HV'][len(content['results']['METRICS'][i]['HV'])-1]
                except:
                    hv = None
                
                try:
                    igd = content['results']['METRICS'][i]['IGD'][len(content['results']['METRICS'][i]['IGD'])-1]
                except:
                    igd = None
                
                try:
                    dnpw = content['results']['METRICS'][i]['DNPW'][len(content['results']['METRICS'][i]['DNPW'])-1]
                except:
                    dnpw = None

                try:
                    fq = content['results']['METRICS'][i]['FQ'][len(content['results']['METRICS'][i]['FQ'])-1]
                except:
                    fq = None        

                try:
                    sp = content['results']['METRICS'][i]['SP'][len(content['results']['METRICS'][i]['SP'])-1]
                except:
                    sp = None
                
                try:
                    svc = content['results']['METRICS'][i]['SVC'][len(content['results']['METRICS'][i]['SVC'])-1]
                except:
                    svc = None

                results_dict['FILE'].append(file_name)
                results_dict['HV'].append(hv)
                results_dict['IGD'].append(igd)
                results_dict['DNPW'].append(dnpw)
                results_dict['FQ'].append(fq)
                results_dict['SP'].append(sp)
                results_dict['SVC'].append(svc)

    
    for key in list(results_dict.keys()):
        if results_dict[key] == []:
            del results_dict[key]

    dataframe = pd.DataFrame(results_dict)
    return dataframe

def compress_historys_to_db(history_path,exp_name)->pd.DataFrame:
    """Compress multiple experiments from the same type into a unique dataframe."""

    dataframe = history_to_db(history_path)
    n_rows = len(dataframe['FILE'].tolist())
    dataframe['FILE'] = [exp_name for i in range(len(n_rows))]

    return dataframe


def get_complete_genotype(path_to_json):
    r"""Returns a list of pandas dataframes containing genotype and fenotype from each individual
    of the population.
    - Each dataframe: 100 individuals generated in each core of the parallel process
    - Each row from dataframa: 1 individual
    """

    population_genetics = []

    with open(path_to_json,'r') as file:
        content = json.load(file)

    content = content['results']['ARCHIVE RESULTS']
    for i in range(len(content)):
        genetics = pd.read_json(content[i])
        population_genetics.append(genetics)
    
    return population_genetics

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

    metrics = ['MAE', 'MSE', 'R2']
    for metric in metrics:
        for label in all_dfs:
            all_dfs[label] = remove_outliers_iqr(all_dfs[label], metric)

    metric_labels = {
        'MAE': 'MAE',
        'MSE': 'MSE',
        'R2': 'R²'
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

def plot_spearman_heatmap(df, title, cmap='viridis'):
    """
    Plota um heatmap da correlação de Spearman entre as features numéricas.

    Parâmetros:
    - df: DataFrame contendo features numéricas.
    - cmap: colormap para o heatmap (padrão: 'viridis').
    """

    # Seleciona colunas numéricas
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if not numeric_cols:
        raise ValueError("O DataFrame não contém colunas numéricas para correlação.")

    # Calcula a matriz de correlação Spearman usando pandas
    corr = df[numeric_cols].corr(method='spearman')

    # Plot do heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr,
        annot_kws={"size": 10},
        fmt=".2f",
        cmap=cmap,
        linewidths=0.5,
        linecolor='gray',
        square=True,
        cbar=True
    )
    
    plt.title(title)
    #plt.xlabel("Features")
    #plt.ylabel("Features")
    plt.tight_layout()
    plt.show()

def plot_mirror_spearman_heatmap(df1, df2, title, cmap='viridis', diff_cmap='bwr'):
    """
    Plota dois heatmaps de correlação de Spearman (df1 e df2) e,
    no meio, o heatmap da diferença entre as duas matrizes.

    Parâmetros:
    - df1, df2: DataFrames contendo features numéricas.
    - cmap: colormap para os heatmaps originais.
    - diff_cmap: colormap para o heatmap da diferença.
    """
    
    # Seleciona colunas numéricas comuns
    numeric_cols = [
    col for col in df1.select_dtypes(include='number').columns
    if col in df2.select_dtypes(include='number').columns
    ]

    if not numeric_cols:
        raise ValueError("Não há colunas numéricas em comum para correlação.")

    # Calcula correlações
    corr1 = df1[numeric_cols].corr(method='spearman')
    corr2 = df2[numeric_cols].corr(method='spearman')

    # Diferença
    diff_corr = corr1 - corr2

    # Plot do heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        diff_corr,
        annot_kws={"size": 10},
        fmt=".2f",
        cmap=cmap,
        linewidths=0.5,
        linecolor='gray',
        square=True,
        cbar=True
    )
    
    plt.title(title)
    #plt.xlabel("Features")
    #plt.ylabel("Features")
    plt.tight_layout()
    plt.show()


def plot_total_rows_per_dataset(data_dict, title='Total de Linhas por Dataset'):
    """
    data_dict: dicionário com nome da base como chave e DataFrame como valor.
    title: título do gráfico.
    """
    # Nomes e contagens
    dataset_names = list(data_dict.keys())
    row_counts = [len(df) for df in data_dict.values()]

    # Paleta de cores consistente com o script de proporções
    palette = sns.color_palette("Set2", n_colors=len(dataset_names))
    color_map = dict(zip(dataset_names, palette))
    colors = [color_map[name] for name in dataset_names]

    # Plot
    plt.figure(figsize=(10, 5))
    bars = plt.bar(dataset_names, row_counts, color=colors)

    # Adicionar valores sobre as barras
    for bar, count in zip(bars, row_counts):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(row_counts)*0.01,
                 str(count), ha='center', va='bottom', fontsize=10)

    plt.title(title, fontsize=14)
    plt.xlabel('Dataset')
    plt.ylabel('Sample Size')
    plt.xticks(rotation=0)
    plt.ylim(0,50000)
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
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
    pivot_df.plot(kind='bar', stacked=True, color=[color_map[cat] for cat in pivot_df.columns], figsize=(10, 12))

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
    plt.xticks(rotation=0)
    plt.ylim(0, 1)
    plt.legend(title='Category', loc='upper right')
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
    ax.set_title(f"{title}", fontsize=14)
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

def multi_hist_plot(df_list, labels, bins=30, density=False):
    """
    Plota múltiplos histogramas (um por dimensão), sobrepondo distribuições
    de vários DataFrames para comparação.

    Parâmetros:
    - df_list: lista de DataFrames pandas.
    - labels: lista de nomes/etiquetas (strings) para identificar cada DataFrame nos plots.
    - image_path: caminho onde as imagens PNG serão salvas.
    - bins: número de bins do histograma (padrão: 30).
    - density: se True, normaliza para densidade (área = 1).
               se False, mostra contagens absolutas.
    
    Obs: Assume-se que todos os DataFrames têm as mesmas colunas.
    """
    assert len(df_list) == len(labels), "df_list e labels devem ter o mesmo comprimento"
    
    # Pega o índice (colunas) a partir do primeiro DataFrame
    columns = df_list[0].columns

    for col in columns:
        plt.figure(figsize=(10, 6))

        # Plota histogramas sobrepostos para cada DataFrame
        for df, label in zip(df_list, labels):
            sns.histplot(
                data=df,
                x=col,
                bins=bins,
                stat="density" if density else "count",  # controla eixo y
                element="step",   # bordas finas (para comparação clara)
                fill=True,       # sem preenchimento, só contorno
                label=label,
                alpha=0.4
            )

        plt.title(f'Histogram: {col}')
        plt.xlabel(col)
        plt.ylabel("Density" if density else "Count")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend()
        plt.show()

def multi_bx_plot(df_list, labels):

    assert len(df_list) == len(labels), "df_list e labels devem ter o mesmo comprimento"

    model_a = labels[0]
    model_b = labels[1]

    columns = df_list[0].columns

    for col in columns:

        combined = []
        for df, label in zip(df_list, labels):
            temp = pd.DataFrame({
                "Experiment": label,
                "valor": df[col]
            })
            combined.append(temp)

        df_plot = pd.concat(combined, ignore_index=True)

        fig, ax = plt.subplots(figsize=(10,6))

        sns.boxplot(
            data=df_plot,
            x="Experiment",
            y="valor",
            ax=ax
        )

        ax.set_title(f'Boxplot: {col}')
        ax.set_ylabel(col)
        ax.grid(True, linestyle="--", alpha=0.6)

        # ==========================
        # CÁLCULO DO P-VALOR
        # ==========================
        df_dunn = df_plot[['Experiment', 'valor']].copy()
        df_dunn.columns = ['grupo', 'valor']

        p_val = compute_dunn_pvalue(df_dunn, model_a, model_b)
        p_text = f"p = {p_val:.4f}"

        ax.text(
            0.98,
            0.98,
            p_text,
            transform=ax.transAxes,
            ha='right',
            va='top',
            fontsize=16
        )

        plt.show()

def prepare_data(metric1, metric2, nome_metrica, title1, title2)->pd.DataFrame:
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


def dunn_testII(df_mae, df_mse, df_r2, remove_outliers=True):
    """
    Execute Dunn Test to compare models based on MAE, MSE, and R2,
    optionally removing outliers using IQR per group.

    - df_mae, df_mse, df_r2: dataframes com as métricas
    - remove_outliers: bool, se True remove outliers por grupo usando IQR

    Retorna resultado no terminal.
    """

    for df_metric in [df_mae, df_mse, df_r2]:
        nome_metrica = df_metric['metrica'].iloc[0]
        print(f"\n===== Análise para {nome_metrica} =====")

        df_clean = df_metric.copy()

        # Remove outliers, se ativado
        if remove_outliers:
            metric = 'valor'
            df_clean = df_clean.groupby(['grupo'], group_keys=False).apply(
                lambda g: g.loc[g[metric].between(
                    g[metric].quantile(0.25) - 1.5 * (g[metric].quantile(0.75) - g[metric].quantile(0.25)),
                    g[metric].quantile(0.75) + 1.5 * (g[metric].quantile(0.75) - g[metric].quantile(0.25))
                )]
            )

        # Boxplot (opcional)
        plt.figure(figsize=(8, 5))
        sns.boxplot(data=df_clean, x='grupo', y='valor')
        title_suffix = " (sem outliers)" if remove_outliers else ""
        plt.title(f'Distribuição de {nome_metrica} por grupo{title_suffix}')
        plt.show()

        # Teste de Kruskal-Wallis
        grupos = [df_clean[df_clean['grupo'] == g]['valor'] for g in df_clean['grupo'].unique()]
        stat, p = kruskal(*grupos)
        print(f"Kruskal-Wallis: estatística = {stat:.3f}, p = {p:.5f}")

        if p < 0.05:
            print("→ H₀ rejeitada: há diferença significativa → Teste de Dunn")
            dunn = sp.posthoc_dunn(df_clean, val_col='valor', group_col='grupo', p_adjust='bonferroni')
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
    #plt.axhline(10, color='red', linestyle='--')  # útil se erro pode ser negativo
    plt.ylim(0, 100)  # mínimo e máximo do eixo Y
    plt.yticks(np.arange(0, 6000, 1000)) #np.arange(0, 101, 10)
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
    for folder in range(len(folders)):

        sub_path = rf'{path}\{folders[folder]}'
        files = [f for f in os.listdir(sub_path) if f.endswith('.txt')]
        files = files[:(len(files))]

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


                mae = content[1:4]
                mse = content[5:8]
                r2 = content[9:]

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

def process_individual_rn(path)->list:

    """
    Works for 'rn' results only.
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
                content = content[3:]

                mse = content[1:3]
                mae = content[4:6]
                r2 = content[10:]

                mse = [float(mse[i]) for i in range(2)]
                mae = [float(mae[i]) for i in range(2)]
                r2 = [float(r2[i]) for i in range(2)]


                results_dict['fold'].append(f'fold-{file}')
                results_dict['fold'].append(f'fold-{file}')

                results_dict['output'].append('r')
                results_dict['output'].append('n')

                results_dict['MAE'].append(mae[0])
                results_dict['MAE'].append(mae[1])

                results_dict['MSE'].append(mse[0])
                results_dict['MSE'].append(mse[1])

                results_dict['R2'].append(r2[0])
                results_dict['R2'].append(r2[1])       
                
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

def group_boxplot2(list_df, model_names, metric, y_min, y_max, y_step, selected_outputs=None, remove_outliers=True):
    """
    Multiple box-plot grouped by output type for the selected metric.

    list_df: lista de DataFrames (um por modelo)
    model_names: lista com nomes dos modelos
    metric: nome da métrica (ex: 'MAE', 'MSE', 'R2')
    y_min, y_max, y_step: limites e passo do eixo y
    selected_outputs: lista opcional com outputs a incluir
    remove_outliers: se True, remove outliers via função remove_outliers_iqr
    """

    if len(list_df) != len(model_names):
        raise ValueError("O número de dataframes deve ser igual ao número de nomes de modelos.")

    # Combina todos os dataframes e adiciona coluna 'Model'
    df_list = []
    for df, name in zip(list_df, model_names):
        temp = df.copy()
        temp['Model'] = name
        df_list.append(temp)

    df_all = pd.concat(df_list, ignore_index=True)

    # Filtra outputs se necessário
    if selected_outputs is not None:
        df_all = df_all[df_all['output'].isin(selected_outputs)]

    # Remove outliers, se ativado
    if remove_outliers:
        def remove_outliers_iqr(series):
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1
            lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            return series[(series >= lower) & (series <= upper)]
        df_all = df_all.groupby(['output', 'Model'], group_keys=False).apply(
            lambda g: g.loc[g[metric].between(
                g[metric].quantile(0.25) - 1.5 * (g[metric].quantile(0.75) - g[metric].quantile(0.25)),
                g[metric].quantile(0.75) + 1.5 * (g[metric].quantile(0.75) - g[metric].quantile(0.25))
            )]
        )

    # Ordena outputs
    outputs = sorted(df_all['output'].unique())

    # Cria figura
    plt.figure(figsize=(12, 6))
    ax = sns.boxplot(
        x='output',
        y=metric,
        hue='Model',
        data=df_all,
        showfliers=not remove_outliers,
        palette='tab10' #Set2
    )

    # Configura eixo y
    step = np.arange(y_min, y_max + y_step, y_step)
    plt.yticks(step)
    plt.ylabel(metric)
    plt.xlabel('Output')
    #plt.title(f'Model Comparison by Output for {metric}')
    plt.title(f'')

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Model')
    plt.tight_layout()
    plt.show()


def group_boxplot3(list_df, model_names, metric, y_min, y_max, y_step,
                   selected_outputs=None, remove_outliers=True):
    """
    Multiple box-plot grouped by output type for the selected metric.
    Each model (category) keeps a fixed color.
    """

    if len(list_df) != len(model_names):
        raise ValueError("O número de dataframes deve ser igual ao número de nomes de modelos.")

    # Combina todos os dataframes e adiciona coluna 'Model'
    df_list = []
    for df, name in zip(list_df, model_names):
        temp = df.copy()
        temp['Model'] = name
        df_list.append(temp)

    df_all = pd.concat(df_list, ignore_index=True)

    # Filtra outputs se necessário
    if selected_outputs is not None:
        df_all = df_all[df_all['output'].isin(selected_outputs)]

    # Remove outliers, se ativado
    if remove_outliers:
        df_all = df_all.groupby(['output', 'Model'], group_keys=False).apply(
            lambda g: g.loc[g[metric].between(
                g[metric].quantile(0.25) - 1.5 * (g[metric].quantile(0.75) - g[metric].quantile(0.25)),
                g[metric].quantile(0.75) + 1.5 * (g[metric].quantile(0.75) - g[metric].quantile(0.25))
            )]
        )

    # Define cores fixas para os modelos (categoria 1 e 2, por exemplo)
    # Você pode alterar as cores conforme desejar:
    fixed_colors = {
        model_names[0]: "#1f77b4",  # azul
        model_names[1]: "#ff7f0e"   # laranja
    }

    # Cria figura
    plt.figure(figsize=(12, 6))
    ax = sns.boxplot(
        x='output',
        y=metric,
        hue='Model',
        data=df_all,
        showfliers=not remove_outliers,
        palette=fixed_colors,  # cores fixas
        hue_order=model_names
    )

    # Configura eixo y
    step = np.arange(y_min, y_max + y_step, y_step)
    plt.yticks(step)
    plt.ylabel(metric)
    plt.xlabel('Output')
    plt.title(f'Model Comparison by Output for Test {metric}')

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Model')
    plt.tight_layout()
    plt.show()

def compute_dunn_pvalue(df_metric, model_a, model_b, correction='bonferroni'):

    df_filtered = df_metric[df_metric['grupo'].isin([model_a, model_b])].copy()

    if df_filtered['grupo'].nunique() < 2:
        raise ValueError(
            f"Não encontrou os dois modelos. Disponíveis: {df_metric['grupo'].unique()}"
        )

    dunn = sp.posthoc_dunn(
        df_filtered,
        val_col='valor',
        group_col='grupo',
        p_adjust=correction
    )

    return dunn.iloc[0, 1]


def group_boxplot_opt_m(df, metric, y_min, y_max, y_step,
                      model_a=None, model_b=None,
                      remove_outliers=True):

    df_plot = df.copy()
    df_plot['Experiment'] = df_plot['FILE']

    # Tradução dos nomes
    translation_dict = {
        'LE': 'TS',
        'LR': 'YS',
        'AL': 'EL',
        'r': 'SH',
        'n': 'AC'
    }

    df_plot['Experiment'] = df_plot['Experiment'].replace(translation_dict)

    if remove_outliers:
        df_plot = df_plot.groupby('Experiment', group_keys=False).apply(
            lambda g: g.loc[g[metric].between(
                g[metric].quantile(0.25) - 1.5 * (g[metric].quantile(0.75) - g[metric].quantile(0.25)),
                g[metric].quantile(0.75) + 1.5 * (g[metric].quantile(0.25) - g[metric].quantile(0.75)) * -1
            )]
        )

    unique_models = sorted(df_plot['Experiment'].unique())
    palette = sns.color_palette("tab10", len(unique_models))

    plt.figure(figsize=(12, 6))
    ax = sns.boxplot(
        x='Experiment',
        y=metric,
        data=df_plot,
        order=unique_models,
        showfliers=not remove_outliers,
        palette=palette
    )

    # Eixo Y
    step = np.arange(y_min, y_max + y_step, y_step)
    plt.yticks(step, fontsize=14)

    if metric == 'SVC':
        plt.ylabel('SVT', fontsize=16)
    else:
        plt.ylabel(metric, fontsize=16)

    plt.xlabel('', fontsize=16)

    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)

    if model_a and model_b:

        # Traduz também os nomes usados no Dunn test
        model_a = translation_dict.get(model_a, model_a)
        model_b = translation_dict.get(model_b, model_b)

        df_dunn = df_plot[['Experiment', metric]].copy()
        df_dunn.columns = ['grupo', 'valor']
        df_dunn['metrica'] = metric

        p_val = compute_dunn_pvalue(df_dunn, model_a, model_b)
        p_text = f"p = {p_val:.23f}"

        ax.text(
            0.98,
            0.98,
            p_text,
            transform=ax.transAxes,
            ha='right',
            va='top',
            fontsize=16,
        )

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def group_boxplot_opt(df, metric, y_min, y_max, y_step,
                      model_a=None, model_b=None,
                      remove_outliers=True):

    df_plot = df.copy()
    df_plot['Experiment'] = df_plot['FILE']

    if remove_outliers:
        df_plot = df_plot.groupby('Experiment', group_keys=False).apply(
            lambda g: g.loc[g[metric].between(
                g[metric].quantile(0.25) - 1.5 * (g[metric].quantile(0.75) - g[metric].quantile(0.25)),
                g[metric].quantile(0.75) + 1.5 * (g[metric].quantile(0.75) - g[metric].quantile(0.25))
            )]
        )

    unique_models = sorted(df_plot['Experiment'].unique())
    palette = sns.color_palette("tab10", len(unique_models))

    plt.figure(figsize=(12, 6))
    ax = sns.boxplot(
        x='Experiment',
        y=metric,
        data=df_plot,
        order=unique_models,
        showfliers=not remove_outliers,
        palette=palette
    )

    # Eixo Y
    step = np.arange(y_min, y_max + y_step, y_step)
    plt.yticks(step, fontsize=14)

    if metric == 'SVC':
        plt.ylabel('SVT', fontsize=16)    
    else:
        plt.ylabel(metric, fontsize=16)

    plt.xlabel('', fontsize=16)
    #plt.title(f'Comparison by Experiment for {metric}', fontsize=18)

    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)

    if model_a and model_b:

        df_dunn = df_plot[['Experiment', metric]].copy()
        df_dunn.columns = ['grupo', 'valor']
        df_dunn['metrica'] = metric

        p_val = compute_dunn_pvalue(df_dunn, model_a, model_b)
        p_text = f"p = {p_val:.3f}"

        ax.text(
            0.98,            # centro horizontal
            0.98,           # próximo ao eixo x (ajuste fino aqui se quiser)
            p_text,
            transform=ax.transAxes,
            ha='right',
            va='top',
            fontsize=16,
            #fontweight='bold',
            #bbox=dict(
            #    facecolor='white',
            #    edgecolor='black',
            #    boxstyle='round,pad=0.3',
            #    alpha=0.9
            #)
        )

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def group_boxplot_opt2(df, metric, y_min, y_max, y_step, model_a=None, model_b=None,remove_outliers=True):
    """
    Cria boxplots agrupados por nome de arquivo (coluna 'FILE') para a métrica selecionada.
    - df: DataFrame retornado por history_to_db
    - metric: nome da métrica ('HV', 'IGD', 'DNPW', 'FQ')
    - y_min, y_max, y_step: controle do eixo y
    - remove_outliers: remove outliers com base no IQR
    """

    df_plot = df.copy()
    df_plot['Model'] = df_plot['FILE']  # Usa o nome do arquivo diretamente

    # Remove outliers, se ativado
    if remove_outliers:
        df_plot = df_plot.groupby('Model', group_keys=False).apply(
            lambda g: g.loc[g[metric].between(
                g[metric].quantile(0.25) - 1.5 * (g[metric].quantile(0.75) - g[metric].quantile(0.25)),
                g[metric].quantile(0.75) + 1.5 * (g[metric].quantile(0.75) - g[metric].quantile(0.25))
            )]
        )

    # Paleta de cores automática
    unique_models = sorted(df_plot['Model'].unique())
    palette = sns.color_palette("tab10", len(unique_models))

    # Cria o boxplot
    plt.figure(figsize=(12, 6))
    ax = sns.boxplot(
        x='Model',
        y=metric,
        data=df_plot,
        order=unique_models,
        showfliers=not remove_outliers,
        palette=palette
    )
    
    # Configura eixo y
    step = np.arange(y_min, y_max + y_step, y_step)
    plt.yticks(step)
    if metric == 'SVC':
        plt.ylabel('SVT')    
    else:
        plt.ylabel(metric)
    plt.xlabel('Experiment')
    #plt.title(f'Comparison by Experiment for {metric}')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    #plt.xticks(rotation=0, ha='right')
    plt.tight_layout()
    plt.show()


def group_boxplot_rn(list_df, model_names, metric, y_min, y_max, y_step, scient_not, selected_outputs=None, remove_outliers=True):
    """
    Multiple box-plot based on individual outputs for the selected metrics.
    Added: scient_not = '10**(-4)'

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
    plt.ylabel(f"{metric} {scient_not}")
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


def calculate_frequency(pop: list[list]) -> float:
        """Calculate the Shannon entropy of the current population and normalize it."""
        gene_freq = {}; n = len(pop); k = len(pop[0])
        for i in range(n):
            for gene in pop[i]:
                gene_freq[gene] = gene_freq.get(gene, 0) + 1
        
        H = 0
        for freq in gene_freq.values():
            p = freq / n
            H += p * np.log(p)

        # GFSN = -H/(k*np.log(min(k,n)))
        return -H/(k*np.log(n))

def transform_db(df: pd.DataFrame) -> list[list]:
    return [list(df.iloc[i, :]) for i in range(len(df))]


def time_barplot(results_path, title: str, datanames: list, machine: list):
    r"""
    Function to plot time processing barplots:
    Ex:
    datanames = ['GR ', 'GR']
    machine = ['LOCAL', 'DOCKER']
    path = r'C:\Users\guiul\OneDrive\Área de Trabalho\Tigger Analytics\Projetos\ArcellorMital\DataAnalysis\SpecializedModels\Results\ProcessingResults\GPU'

    """


    results_list = preprocess_time(results_path)

    time_consumption = {
        'Database': [],
        'Processing Time': [],
        'Computador': []
    }
    print(results_list)
    for i in range(len(results_list)):

        results = results_list[i]
        shape = results['Input shape']
        time = results['Time taken']

        #time_consumption['Database'].append(f'{datanames[i]} ({int(shape)})')
        time_consumption['Database'].append(f'{datanames[i]}')
        time_consumption['Processing Time'].append(float(time))
        time_consumption['Computador'].append(machine[i])

    df = pd.DataFrame(time_consumption)
    print(df.head())
    color = {
        'CENTRAL':'steelblue',
        'DISTRIBUÍDO':'orange',
        'REMOTO': 'green'
    }

    barplot(
        dataframe=df,
        x_dim='Database',
        y_dim='Processing Time',
        step = np.arange(0,31,2),
        x_title='Estratégia de Busca',
        y_title='Tempo de processamento em Horas',
        title=title,
        hue = 'Computador',
        colors= color
    )

