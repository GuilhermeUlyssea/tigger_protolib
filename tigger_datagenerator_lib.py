#import pandas as pd

# [EXCEL ORIENTED FUNCTIONS] ______________________________________________________________________________________________________________________


def genExcel_warehouse(header_titles,file_name,path):
    #Comment:: dtype(header_titles,file_name,path) = (list,string,unicode string)

    #Libs:
    from pandas import DataFrame
    #importar resto das libs

    #Internal Variables:
    wbs = dict()   
    file_path = f"{path}\{file_name}"

    # Dict Construction:
    for i in range(len(header_titles)):
        wbs[f'{header_titles[i]}'] = []
    
    Warehouse = DataFrame(wbs)
    
    # Dict datalog:
    print("\n[Status]: Dataframe infos:\n")
    print(Warehouse.info())
    print("\nSize:", Warehouse.size)

    # Exporting:
    Warehouse.to_excel(file_path,sheet_name='Dataset',startcol=-1)
    return print("\n[Status]: Excel database generated...\n")

header_titles = ['Data','Produto','Especificação','Preço','Quantidade','Descrição']
file_name = 'Teste_mammys.xlsx'
path = r'C:\Users\guiul\OneDrive\Área de Trabalho\Tigger Analytics\Projetos'

genExcel_warehouse(header_titles,file_name,path)

def data_builder_csv(path_to_document):
    import pandas as pd

    df = pd.read_csv(rf"{path_to_document}")
    print(df.info())
    
    keys = [df.columns[i] for i in range(len(df.columns))]  # Geração de chaves dos datasets
    values = [df[keys[i]] for i in range(len(keys))]
    
    dict_gen = dict(zip(keys, values))

    dataframe = pd.DataFrame(dict_gen)

    dataframe.to_excel('converted_data.xlsx')

    return print("[Status]: Document transformed")

# [SQL ORIENTED FUNCTIONS] ___________________________________________________________________________________________________________________________________ 







