def get_innovation(sheet: str = None) -> dict:
    """
    The function to read the world innovation data and return it in dict list of data frame per year

    Required:
    read_excel fom pandas package (from pandas import read_excel)
    OR
    use pd.read_excel when calling (import pandas as pd)

    :param sheet: parameter to select the sheet from excel file.
    :return: pass back a dict that contains either specific excel sheet or all sheets in form of Data Frame(s).

    >>> print(type(Data().get_innovation()))
    <class 'dict'>
    """
    file_path = "590PR_final_datasets"
    file_name = "Innovation.zip"
    zf = zipfile.ZipFile(file_path + '/' + file_name)
    inv = {}
    for name in zipfile.ZipFile.infolist(zf):
        inv[name.filename] = pd.read_csv(zf.open(name.filename))
    if not sheet == None:
        return inv[sheet]
    else:
        return inv

def innovation():
    inno_list = []
    for i in range(6):
        df = Data.get_innovation('get_innovation-201%s.csv' %(i + 3))
        df.rename({'Economy': 'Country', 'Score': 'Score201%s' % (i + 3)}, axis='columns', inplace=True)
        inno_list.append(df[['Country', 'Score201%s' % (i + 3)]])
    return inno_list