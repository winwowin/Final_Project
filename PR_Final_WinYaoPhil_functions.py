# additional package requirements: bs4, gdelt, seaborn

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from pandas import read_excel
import logging
import zipfile
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class Data(object):
    def __init__(self: object, file_path: str = "590PR_final_datasets"):
        self.file_path = file_path
        self.df_list = []

    def get_peace(self: object) -> pd.DataFrame:
        """
        This is a function to pull the most updated peace data modified from https://www.kaggle.com/kretes/gpi2008-2016
        and return it in a data frame

        Global get_peace Index (GPI) measures the relative position of nations' and regions' peacefulness.
        The GPI ranks 163 independent states and territories (99.7 per cent of the world’s population)
        according to their levels of peacefulness. In the past decade, the GPI has presented trends of
        increased global violence and less peacefulness.

        The lower the number indicates more peace in the region.

        Source:
        http://visionofhumanity.org/indexes/global-peace-index/

        Requires:
        import requests
        import re
        from bs4 import BeautifulSoup
        import pandas as pd

        :return: a Data Frame contain peace index score, by country and year.

        >>> print(type(Data().get_peace()))
        <class 'pandas.core.frame.DataFrame'>
        """
        response = requests.get(url='https://en.wikipedia.org/wiki/Global_Peace_Index')
        soup = BeautifulSoup(response.text, 'html.parser')
        base_year = 2018  # latest year
        years = 9  # number of years to get data

        def get_countries_by_gpi():
            i = 1
            for table in soup.find_all('table', re.compile('wikitable sortable')):
                if table.find_all('th')[0].get_text() == 'Country\n':
                    for tr in table.find_all('tr'):
                        country_name = tr.find_all('a')[0].get_text()
                        if not country_name.startswith('['):
                            row = {'country': country_name}
                            for year, index in zip(range(base_year - years + 1, base_year + 1),
                                                   range(2 * (years), 0, -2)):
                                score = tr.find_all('td')[index].get_text()
                                if score != '' and score != '\n':
                                    row['score_%s' % year] = float(score)
                            yield row

        gpi = pd.DataFrame.from_dict(list(get_countries_by_gpi()))
        gpi.to_csv(self.file_path + '/gpi_%s-%s.csv' % (base_year - years + 1, base_year), index=False)
        gpi.columns = ['Country', 'pi_2010', 'pi_2011', 'pi_2012', 'pi_2013', 'pi_2014', 'pi_2015', 'pi_2016',
                       'pi_2017', 'pi_2018']
        return (gpi)

    def get_trade(self: object) -> pd.DataFrame:
        """
        The function to read the world hunger data and return it in data frame

        WITS get_trade Stats is a database created by aggregating data from UN COMTRADE and UNCTAD TRAINS database.
        It provides information on bilateral trade exports, imports and tariffs for over 180 countries and regions.

        Source:
        https://datacatalog.worldbank.org/dataset/world-integrated-trade-solution-trade-stats

        Required:
        import logging

        :return: trade data in form of Data Frame

        >>> print(type(Data().get_trade()))
        <class 'pandas.core.frame.DataFrame'>
        """
        logging.basicConfig(filename="test.log", level=logging.DEBUG)
        file_name = "wits_en_trade_summary_allcountries_allyears.zip"
        zf = zipfile.ZipFile(self.file_path + '/' + file_name)
        df = []
        for name in zipfile.ZipFile.infolist(zf):
            logging.debug(name.filename)
            try:
                df.append(pd.read_csv(zf.open(name.filename), header=0))
            except:
                pass
        frame = pd.concat(df, axis=0, ignore_index=True)
        return frame

    def get_hunger(self: object) -> pd.DataFrame:
        """
        The function to read the world hunger data and return it in data frame

        The prevalence of undernourishment, as a share of the population, is the main hunger indicator used by
        the UN's Food and Agriculture Organization. It measures the share of the population which has
        a caloric (dietary energy) intake which is insufficient to meet the minimum energy requirements
        defined as necessary for a given population.

        Source:
        https://ourworldindata.org/hunger-and-undernourishment

        Required:
        import pandas as pd

        :return: world hunger data in a list of Pandas Data Frames

        >>> print(type(Data().get_hunger()))
        <class 'pandas.core.frame.DataFrame'>
        """
        file_name = "Hunger.csv"
        df_hunger = pd.read_csv(self.file_path + "/" + file_name, na_values='\t', sep='\t', header=0)
        list = []
        list.append(df_hunger['Country Name'])
        list.append(df_hunger['Indicator Name'])
        for i in range(2009, 2019):
            year = str(i)
            df = df_hunger[year]
            list.append(df)
        df_new_hunger = pd.concat(list, axis=1)
        df_new_hunger.columns = ['Country', 'undernourishment_rate_2009', 'undernourishment_rate_2010',
                                 'undernourishment_rate_2011', 'undernourishment_rate_2012',
                                 'undernourishment_rate_2013', 'undernourishment_rate_2014',
                                 'undernourishment_rate_2015', 'undernourishment_rate_2016',
                                 'undernourishment_rate_2017', 'undernourishment_rate_2018',
                                 'undernourishment_rate_2019']
        return df_new_hunger

    def get_unemployment(self: object) -> pd.DataFrame:
        """
        The function to read the United Nation world unemployment data and return it in data frame

        :return: unemployment data in Pandas Data Frame

        >>> print(type(Data().get_unemployment()))
        <class 'pandas.core.frame.DataFrame'>
        """
        file_name = "unemployment.zip"
        df = pd.read_csv(self.file_path + '/' + file_name, compression='zip')
        return df

    def get_suicide(self: object) -> pd.DataFrame:
        """
        The function to read the United Nation world suicide data and return it in data frame

        This compiled dataset pulled from four other datasets linked by time and place, and was built to find signals
        correlated to increased suicide rates among different cohorts globally, across the socio-economic spectrum.

        Source:
        https://www.kaggle.com/russellyates88/suicide-rates-overview-1985-to-2016

        :return: suicide data in Pandas Data Frame

        >>> print(type(Data().get_suicide()))
        <class 'pandas.core.frame.DataFrame'>
        """
        file_name = "suicide-rates-overview-1985-to-2016.zip"
        df = pd.read_csv(self.file_path + '/' + file_name, compression='zip')
        return df

    def get_freedom(self: object) -> pd.DataFrame:
        """
        The function to read the world freedom index data and return it in data frame

        The Human Freedom Index presents the state of human freedom in the world based on a broad measure that
        encompasses personal, civil, and economic freedom. Human freedom is a social concept that recognizes the
        dignity of individuals and is defined here as negative liberty or the absence of coercive constraint.
        Because freedom is inherently valuable and plays a role in human progress, it is worth measuring carefully.
        The Human get_freedom Index is a resource that can help to more objectively observe relationships between
        freedom and other social and economic phenomena, as well as the ways in which the various dimensions of freedom
        interact with one another.

        Source:
        https://www.kaggle.com/gsutters/the-human-freedom-index

        :return: freedom data in Pandas Data Frame
        >>> print(type(Data().get_freedom()))
        <class 'pandas.core.frame.DataFrame'>
        """
        file_name = "the-human-freedom-index.zip"
        df = pd.read_csv(self.file_path + '/' + file_name, compression='zip')
        return df

    def get_happiness(self: object) -> dict:
        """
        The function to read the world happiness data and return it in dict list of data frame per year

        The World Happiness Report is a landmark survey of the state of global happiness. The World Happiness 2017,
        which ranks 155 countries by their happiness levels, was released at the United Nations at an event celebrating
        International Day of Happiness on March 20th.

        The happiness scores and rankings use data from the Gallup World Poll. The scores are based on answers to
        the main life evaluation question asked in the poll. This question, known as the Cantril ladder,
        asks respondents to think of a ladder with the best possible life for them being a 10 and the worst
        possible life being a 0 and to rate their own current lives on that scale.

        Source:
        https://www.kaggle.com/unsdsn/world-happiness

        Required:
        import zipfile

        :return: happiness data in a list which contains Pandas Data Frame of each year

        >>> print(type(Data().get_happiness()['2015.csv']))
        <class 'pandas.core.frame.DataFrame'>
        """
        file_name = "world-happiness-report.zip"
        zf = zipfile.ZipFile(self.file_path + '/' + file_name)
        happy = {}
        for name in zipfile.ZipFile.infolist(zf):
            happy[name.filename] = pd.read_csv(zf.open(name.filename))
        return happy

    def get_poverty(self: object, sheet: str = None) -> dict:
        """
        The function to read the world porverty data and return it in dict list of data frame

        Latest poverty and inequality indicators compiled from officially recognized international sources.
        Poverty indicators include the poverty headcount ratio, poverty gap, and number of poor at both
        international and national poverty lines. Inequality indicators include the Gini index and income or
        consumption distributions. The database includes national, regional and global estimates.
        This database is maintained by the Gloabl Poverty Working Group (GPWG)

        Source:
        https://datacatalog.worldbank.org/dataset/poverty-and-equity-database

        Required:
        import zipfile

        :param sheet: parameter to select the sheet from excel file.
        :return: pass back a dict that contains either specific excel sheet or all sheets in form of Data Frame(s).

        >>> print(type(Data().get_poverty()))
        <class 'dict'>
        """
        file_name = "PovStats_csv.zip"
        zf = zipfile.ZipFile(self.file_path + '/' + file_name)
        pov = {}
        for name in zipfile.ZipFile.infolist(zf):
            pov[name.filename] = pd.read_csv(zf.open(name.filename))
        if not sheet == None:
            return pov[sheet]
        else:
            return pov

    def get_marital(self: object) -> pd.DataFrame:
        """
        The function to read the United Nation marital data and return it in data frame

        :return: marital data in Pandas Data Frame

        >>> print(type(Data().get_marital()))
        <class 'pandas.core.frame.DataFrame'>
        """
        file_name = "UNdata_MARITAL_STATUS_2010-2013.csv"
        df = pd.read_csv(self.file_path + '/' + file_name)
        df.drop(df.tail(74).index, inplace=True)
        file_name = "UNdata_MARITAL_STATUS_2014-2017.csv"
        df2 = pd.read_csv(self.file_path + '/' + file_name)
        df2.drop(df2.tail(54).index, inplace=True)
        df_all = pd.concat([df, df2], axis=0).reset_index(drop=True)
        return df_all

    def get_innovation(self: object, sheet: str = None) -> list:
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


def prep_freedom() -> list:
    """
    The function to prep the world freedom data into only freedom index, year, and country,
    and return it in form of list of data frames per year.

    :return: pass back a list of Data Frames by year, each contains only freedom index and country

    >>> print(type(prep_freedom()))
    <class 'list'>
    """
    freedom = Data().get_freedom()
    free = freedom[['year', 'countries', 'hf_score']]
    free.dropna(inplace=True)
    free.sort_values('hf_score', ascending=True, inplace=True)
    free.reset_index(drop=True, inplace=True)
    free.rename({'countries': 'Country'}, axis='columns', inplace=True)

    free_list = []
    for i in range(6):
        free_list.append(free[free['year'] == (2013 + i)])
    return free_list


def prep_innovation() -> list:
    """
    The function to prep the world innovation data into only innovation score, year, and country,
    and return it in form of data frame

    :return: pass back a list of Data Frames by year, each contains only innovation index and country

    >>> print(type(prep_freedom()))
    <class 'list'>
    """
    inno_list = []
    for i in range(6):
        df = Data().get_innovation('Innovation-201%s.csv' %(i + 3))
        df.rename({'Economy': 'Country', 'Score': 'Score201%s' % (i + 3)}, axis='columns', inplace=True)
        inno_list.append(df[['Country', 'Score201%s' % (i + 3)]])
    return inno_list


## Part 1: Analysis of level 1-2, Physiological-Safety by hunger+peace index dataset

# need docstring
def analysis_first_two_level(hunger: pd.DataFrame, peace: pd.DataFrame) -> tuple:
    """

    :param hunger:
    :param peace:
    :return:

    >>> hunger_data = Data().get_hunger()
    >>> peace_data = Data().get_peace()
    >>> type(analysis_first_two_level(hunger_data, peace_data))
    <class 'tuple'>
    """
    df_level1 = pd.merge(hunger, peace, on = 'Country', how='inner')
    df_level1 = df_level1.drop_duplicates(keep='first', inplace=False)
    x_list = []
    y_list = []
    item = [['undernourishment_rate_2010', 'pi_2010'], ['undernourishment_rate_2011', 'pi_2011'],
              ['undernourishment_rate_2012', 'pi_2012'], ['undernourishment_rate_2013', 'pi_2013'],
              ['undernourishment_rate_2014', 'pi_2014'], ['undernourishment_rate_2015', 'pi_2015'],
              ['undernourishment_rate_2016', 'pi_2016']]
    for i in item:
        df = df_level1[i]
        dd = df.sort_values(by=i[0], ascending=True)
        x = np.asarray(dd[i[0]])
        y = np.asarray(dd[i[1]])
        for j in range(x.shape[0]):
            if math.isnan(x[j]) == True:
                new_x = np.delete(x, j)
                new_y = np.delete(y, j)
        x_list.append(new_x)
        y_list.append(new_y)
    return x_list, y_list, df_level1

# need docstring
def plot12(x_list: list, y_list: list):
    """

    :param x_list:
    :param y_list:
    :return:

    >>> hunger_data = Data().get_hunger()
    >>> peace_data = Data().get_peace()
    >>> x_list, y_list, df_level1 = analysis_first_two_level(hunger_data, peace_data)
    >>> type(plot12(x_list, y_list))
    <class 'NoneType'>
    """
    plt.figure(figsize = (30, 15),  dpi=100)
    item = [['undernourishment_rate_2010', 'pi_2010'], ['undernourishment_rate_2011', 'pi_2011'],
            ['undernourishment_rate_2012', 'pi_2012'], ['undernourishment_rate_2013', 'pi_2013'],
            ['undernourishment_rate_2014', 'pi_2014'], ['undernourishment_rate_2015', 'pi_2015'],
            ['undernourishment_rate_2016', 'pi_2016']]
    marker = ['.', '*', '>', '<', '1', '2', 's']
    color = ['#E11B00', '#1E90FF', '#FF4233', '#FFE333', '#7EFF33', '#33F4FF', '#D433FF']
    for f in range(len(x_list)):
        plt.plot(x_list[f], y_list[f], label = 'data of year '+item[f][1][-4:],  marker = marker[f], color = color[f])
    plt.xlabel('undernourishment rate')
    plt.ylabel('Peacefulness Index')
    plt.ylim(1, 4)
    plt.xticks(fontsize = 8,  horizontalalignment = 'center',  alpha = .7)
    plt.yticks(fontsize = 12,  alpha = .7)
    plt.grid(axis='both', alpha = .3)
    plt.legend()
    plt.gca().invert_yaxis()
    plt.gca().invert_xaxis()
    plt.show()

# need docstring
def plot_cat12(x_list: list, y_list: list):
    """

    :param x_list:
    :param y_list:
    :return:

    >>> hunger_data = Data().get_hunger()
    >>> peace_data = Data().get_peace()
    >>> x_list, y_list, df_level1 = analysis_first_two_level(hunger_data, peace_data)
    >>> type(plot_cat12(x_list, y_list))
    <class 'NoneType'>
    """
    plt.figure(figsize = (30,20), dpi=100)
    item = [['undernourishment_rate_2010','pi_2010'],['undernourishment_rate_2011','pi_2011'],
                  ['undernourishment_rate_2012','pi_2012'],['undernourishment_rate_2013','pi_2013'],
                  ['undernourishment_rate_2014','pi_2014'],['undernourishment_rate_2015','pi_2015'],
                  ['undernourishment_rate_2016','pi_2016']]
    x_item = ['[0,5)','[5,10)','[10,15)','[15,20)','[20,25)','[25,30)','[30,35)','[35,40)','[40,45)',
             '[45,50)']#,'[50+']
    marker = ['.','*','>','<','1','2','s']
    color = ['#E11B00', '#1E90FF','#FF4233','#FFE333','#7EFF33','#33F4FF','#D433FF']
    y_new_list = []
    for a in range(len(x_list)):
        cc = x_list[a]
        cy = y_list[a]
        y_item = np.zeros((10,2))
        for b in range(len(cc)):
            if cc[b] >= 0 and cc[b]<5:
                y_item[0][0] += cy[b]
                y_item[0][1] += 1
            if cc[b] >= 5 and cc[b]<10:
                y_item[1][0] += cy[b]
                y_item[1][1] += 1
            if cc[b] >= 10 and cc[b]<15:
                y_item[2][0] += cy[b]
                y_item[2][1] += 1
            if cc[b] >= 15 and cc[b]<20:
                y_item[3][0] += cy[b]
                y_item[3][1] += 1
            if cc[b] >= 20 and cc[b]<25:
                y_item[4][0] += cy[b]
                y_item[4][1] += 1
            if cc[b] >= 25 and cc[b]<30:
                y_item[5][0] += cy[b]
                y_item[5][1] += 1
            if cc[b] >= 30 and cc[b]<35:
                y_item[6][0] += cy[b]
                y_item[6][1] += 1
            if cc[b] >= 35 and cc[b]<40:
                y_item[7][0] += cy[b]
                y_item[7][1] += 1
            if cc[b] >= 40 and cc[b]<45:
                y_item[8][0] += cy[b]
                y_item[8][1] += 1
            if cc[b] >= 45 and cc[b]<50:
                y_item[9][0] += cy[b]
                y_item[9][1] += 1
#             if cc[b] >= 50:
#                 y_item[10][0] += cy[b]
#                 y_item[10][1] += 1
        y_new = np.zeros(y_item.shape[0])
        for c in range(y_item.shape[0]):
            if y_item[c][1] == 0:
                y_new[c] = math.nan
            else:
                y_new[c] = y_item[c][0]/y_item[c][1]
        y_new_list.append(y_new)
    for s in range(len(y_new_list)):
        plt.plot(x_item,y_new_list[s],label = 'data of year '+item[s][1][-4:], marker = marker[s],color = color[s])
    plt.xlabel('undernourishment rate')
    plt.ylabel('Peacefulness Index')
    plt.ylim(1.6,2.8)
    plt.xticks(fontsize = 8, horizontalalignment = 'center', alpha = .7)
    plt.yticks(fontsize = 12, alpha = .7)
    plt.grid(axis='both',alpha = .3)
    plt.legend()
    plt.gca().invert_yaxis()
    plt.gca().invert_xaxis()
    plt.show()

# need docstring
def box_plot_level12(df_level1: pd.DataFrame):
    """

    Requirement:
    import seaborn as sns

    :param df_level1:
    :return:

    >>> hunger_data = Data().get_hunger()
    >>> peace_data = Data().get_peace()
    >>> x_list, y_list, df_level1 = analysis_first_two_level(hunger_data, peace_data)
    >>> type(box_plot_level12(df_level1))
    <class 'NoneType'>
    """
    fig, axes = plt.subplots(3, 3, figsize=(60,40))
    item = [['undernourishment_rate_2010','pi_2010'],['undernourishment_rate_2011','pi_2011'],
                  ['undernourishment_rate_2012','pi_2012'],['undernourishment_rate_2013','pi_2013'],
                  ['undernourishment_rate_2014','pi_2014'],['undernourishment_rate_2015','pi_2015'],
                  ['undernourishment_rate_2016','pi_2016']]
    peace_item = ['Peace_Index_of 2010','Peace_Index_of 2011','Peace_Index_of 2012','Peace_Index_of 2013',
                  'Peace_Index_of 2014','Peace_Index_of 2015','Peace_Index_of 2016']
    for s in range(7):
        cat_list = []
        data = df_level1[item[s]]
        cc = data[item[s][0]]
        for b in range(data.iloc[:,0].size):
            if math.isnan(cc[b]) == True:
                cat_list.append(math.nan)
            if cc[b] >= 0 and cc[b]<5:
                cat_list.append('[0,5)')
            if cc[b] >= 5 and cc[b]<10:
                cat_list.append('[5,10)')
            if cc[b] >= 10 and cc[b]<15:
                cat_list.append('[10,15)')
            if cc[b] >= 15 and cc[b]<20:
                cat_list.append('[15,20)')
            if cc[b] >= 20 and cc[b]<25:
                cat_list.append('[20,25)')
            if cc[b] >= 25 and cc[b]<30:
                cat_list.append('[25,30)')
            if cc[b] >= 30 and cc[b]<35:
                cat_list.append('[30,35)')
            if cc[b] >= 35 and cc[b]<40:
                cat_list.append('[35,40)')
            if cc[b] >= 40 and cc[b]<45:
                cat_list.append('[40,45)')
            if cc[b] >= 45 and cc[b]<50:
                cat_list.append('[45,50)')
        cat_col = pd.DataFrame(cat_list)
        new_data = pd.concat([data,cat_col],axis=1)
        new_data.columns = [item[s][0], peace_item[s], 'Catergory of Hunger']
        box = sns.boxplot(x=peace_item[s], y='Catergory of Hunger', data=new_data, whis="range", palette="vlag",
                          ax=axes[s // 3, s % 3],
                          order=['[0,5)','[5,10)','[10,15)','[15,20)','[20,25)','[25,30)','[30,35)','[35,40)','[40,45)'])
        #rescale boxplot x-axis with log
        axes[s // 3, s % 3].set_title('Box Plot for Data of year '+ item[s][0][-4:])

        fig.subplots_adjust(wspace=.4)


## Part 2: Analysis of level 2-3, Safety-Belonging by Peace Index and Marriage data

def get_marriage_rate(married: pd.DataFrame) -> list:
    """

    :param married:
    :return:

    >>> married = Data().get_marital()
    >>> married = married.astype({"Year": int}, copy=False)
    >>> type(get_marriage_rate(married))
    <class 'list'>
    """
    percent_married = []
    for i in range(8):
        total = married.loc[(married['Marital status']=='Total') & (married['Age']=='Total')].groupby(['Year', 'Country or Area'], as_index=False).sum()
        single = married.loc[(married['Marital status']=='Single (never married)') & (married['Age']=='Total')].groupby(['Year', 'Country or Area'], as_index=False).sum()
        single_pop = single[single['Year'] == 2010+i].groupby(['Year', 'Country or Area']).sum()['Value']
        total_pop = total[total['Year'] == 2010+i].groupby(['Year', 'Country or Area']).sum()['Value']
        df1 = (total_pop-single_pop)/total_pop
        df = pd.concat([total_pop.to_frame().reset_index(), df1.to_frame().reset_index()['Value']],axis=1)
        df.columns = ['Year','Country','Total_pop','Marriage_Rate']
        percent_married.append(df)
    return percent_married


def analysis_two_third_level(peace: pd.DataFrame, percent_married: pd.DataFrame) -> (list, list, pd.DataFrame):
    """



    :param peace:
    :param percent_married:
    :return:

    >>> peace_data = Data().get_peace()
    >>> married = Data().get_marital()
    >>> married = married.astype({"Year": int}, copy=False)
    >>> percent_married = get_marriage_rate(married)
    >>> x_list_level2, y_list_level2, df_level2 = analysis_two_third_level(peace_data, percent_married)
    >>> type(x_list_level2)
    <class 'list'>
    """
    level2_list = []
    for i in range(8):
        df = percent_married[i]
        string = 'pi_'+str(2010+i)
        p1 = peace['Country']
        p2 = peace[string]
        p = pd.concat([p1, p2],axis = 1)
        df_level2 = pd.merge(df, p, on = 'Country', how='inner')
        level2_list.append(df_level2)
    x_list = []
    y_list = []
    pi_list = ['pi_2010','pi_2011','pi_2012','pi_2013','pi_2014','pi_2015','pi_2016','pi_2017','pi_2018']
    for s in range(8):
        df = level2_list[s]
        dd = df.sort_values(by=[pi_list[s]], ascending=True)
        x = np.asarray(dd[pi_list[s]])
        y = np.asarray(dd['Marriage_Rate'])
        for j in range(x.shape[0]):
            if math.isnan(x[j]) == True:
                new_y = np.delete(y,j)
                new_x = np.delete(x,j)
        x_list.append(x)
        y_list.append(y)
    return x_list, y_list, df_level2


def plot_level_23(x_list: list, y_list: list):
    """

    :param x_list:
    :param y_list:
    :return:

    >>> peace_data = Data().get_peace()
    >>> married = Data().get_marital()
    >>> married = married.astype({"Year": int}, copy=False)
    >>> percent_married = get_marriage_rate(married)
    >>> x_list_level2, y_list_level2, df_level2 = analysis_two_third_level(peace_data, percent_married)
    >>> type(plot_level_23(x_list_level2, y_list_level2))
    <class 'NoneType'>
    """
    plt.figure(figsize = (30,15), dpi=100)
    marker = ['.','*','>','<','1','2','s','3','4']
    color = ['#E11B00', '#1E90FF','#FF4233','#FFE333','#7EFF33','#33F4FF','#D433FF','#3351FF','#D433FF']
    pi_list = ['pi_2010','pi_2011','pi_2012','pi_2013','pi_2014','pi_2015','pi_2016','pi_2017','pi_2018']
    for f in range(8):
        plt.plot(x_list[f],y_list[f],label = 'data of year '+pi_list[f][-4:], marker = marker[f],color = color[f])
    plt.xlabel('Peacefulness Index')
    plt.ylabel('Marriage rate')
    plt.ylim(0,1)
    plt.xticks(fontsize = 8, horizontalalignment = 'center', alpha = .7)
    plt.yticks(fontsize = 12, alpha = .7)
    plt.grid(axis='both',alpha = .3)
    plt.legend()
    plt.gca().invert_xaxis()
    plt.show()


## Part 2-2: Analysis of level 2-3, Safety-Belonging by Peace Index and Happiness data


def analysis_peace_happiness_level(peace: pd.DataFrame, happiness: pd.DataFrame) -> (list, list, list):
    """

    :param peace:
    :param happiness:
    :return:

    >>> peace_data = Data().get_peace()
    >>> happiness = Data().get_happiness()
    >>> happiness['2017.csv'] = happiness['2017.csv'][['Country', 'Happiness.Score']]
    >>> happiness['2017.csv'].columns = ['Country', 'Happiness Score']
    >>> x_list_p_h, y_list_p_h, p_h_list = analysis_peace_happiness_level(peace_data, happiness)
    >>> print(type(p_h_list))
    <class 'list'>
    """
    p_h_list = []
    for i in range(3):
        string2 = str(2015+i)+'.csv'
        df = happiness[string2][['Country','Happiness Score']]
        string = 'pi_'+str(2015+i)
        p1 = peace['Country']
        p2 = peace[string]
        p = pd.concat([p1, p2],axis = 1)
        df_p_h = pd.merge(df, p, on = 'Country', how='inner')
        p_h_list.append(df_p_h)
    x_list = []
    y_list = []
    pi_list = ['pi_2015','pi_2016','pi_2017']
    for s in range(3):
        df = p_h_list[s]
        dd = df.sort_values(by=[pi_list[s]], ascending=True)
        x = np.asarray(dd[pi_list[s]])
        y = np.asarray(dd['Happiness Score'])
        for j in range(x.shape[0]):
            if math.isnan(x[j]) == True:
                new_y = np.delete(y,j)
                new_x = np.delete(x,j)
        x_list.append(x)
        y_list.append(y)
    return x_list, y_list, p_h_list


def plot_level_p_h(x_list: list, y_list: list):
    """

    :param x_list:
    :param y_list:
    :return:

    >>> peace_data = Data().get_peace()
    >>> happiness = Data().get_happiness()
    >>> happiness['2017.csv'] = happiness['2017.csv'][['Country', 'Happiness.Score']]
    >>> happiness['2017.csv'].columns = ['Country', 'Happiness Score']
    >>> x_list_p_h, y_list_p_h, p_h_list = analysis_peace_happiness_level(peace_data, happiness)
    >>> print(type(plot_level_p_h(x_list_p_h, y_list_p_h)))
    <class 'NoneType'>
    """
    plt.figure(figsize = (30,15), dpi=100)
    marker = ['.','*','>','<','1','2','s','3','4']
    color = ['#E11B00', '#1E90FF','#FFE333','#7EFF33','#33F4FF','#D433FF','#3351FF','#D433FF']
    pi_list = ['pi_2015','pi_2016','pi_2017']
    for f in range(3):
        plt.plot(x_list[f],y_list[f],label = 'data of year '+pi_list[f][-4:], marker = marker[f],color = color[f])
    plt.xlabel('Peacefulness Index')
    plt.ylabel('Happiness Score')
    plt.xticks(fontsize = 8, horizontalalignment = 'center', alpha = .7)
    plt.yticks(fontsize = 12, alpha = .7)
    plt.grid(axis='both',alpha = .3)
    plt.legend()
    plt.gca().invert_xaxis()
    plt.show()


def plot_cat_ph(x_list: list, y_list: list):
    """

    :param x_list:
    :param y_list:
    :return:

    >>> peace_data = Data().get_peace()
    >>> happiness = Data().get_happiness()
    >>> happiness['2017.csv'] = happiness['2017.csv'][['Country', 'Happiness.Score']]
    >>> happiness['2017.csv'].columns = ['Country', 'Happiness Score']
    >>> x_list_p_h, y_list_p_h, p_h_list = analysis_peace_happiness_level(peace_data, happiness)
    >>> print(type(plot_cat_ph(x_list_p_h, y_list_p_h)))
    <class 'NoneType'>
    """
    plt.figure(figsize = (30,20), dpi=100)
    pi_list = ['pi_2015','pi_2016','pi_2017']
    x_item = ['[1,1.25)','[1.25,1.5)','[1.5,1.75)','[1.75,2)','[2,2.25)','[2.25,2.5)',
              '[2.5,2.75)','[2.75,3)','[3,3,5)','3.5+']
    marker = ['.','*','>','<','1','2','s']
    color = ['#E11B00', '#1E90FF','#FFE333','#7EFF33','#33F4FF','#D433FF']
    y_new_list = []
    for a in range(len(x_list)):
        cc = x_list[a]
        cy = y_list[a]
        y_item = np.zeros((10,2))
        for b in range(len(cc)):
            if cc[b] >= 1 and cc[b]<1.25:
                y_item[0][0] += cy[b]
                y_item[0][1] += 1
            if cc[b] >= 1.25 and cc[b]<1.5:
                y_item[1][0] += cy[b]
                y_item[1][1] += 1
            if cc[b] >= 1.5 and cc[b]<1.75:
                y_item[2][0] += cy[b]
                y_item[2][1] += 1
            if cc[b] >= 1.75 and cc[b]<2:
                y_item[3][0] += cy[b]
                y_item[3][1] += 1
            if cc[b] >= 2 and cc[b]<2.25:
                y_item[4][0] += cy[b]
                y_item[4][1] += 1
            if cc[b] >= 2.25 and cc[b]<2.5:
                y_item[5][0] += cy[b]
                y_item[5][1] += 1
            if cc[b] >= 2.5 and cc[b]<2.75:
                y_item[6][0] += cy[b]
                y_item[6][1] += 1
            if cc[b] >= 2.75 and cc[b]<3:
                y_item[7][0] += cy[b]
                y_item[7][1] += 1
            if cc[b] >= 3 and cc[b]<3.5:
                y_item[8][0] += cy[b]
                y_item[8][1] += 1
            if cc[b] >= 3.5:
                y_item[9][0] += cy[b]
                y_item[9][1] += 1
        y_new = np.zeros(y_item.shape[0])
        for c in range(y_item.shape[0]):
            if y_item[c][1] == 0:
                y_new[c] = math.nan
            else:
                y_new[c] = y_item[c][0]/y_item[c][1]
        y_new_list.append(y_new)
    for s in range(len(y_new_list)):
        plt.plot(x_item,y_new_list[s],label = 'data of year '+pi_list[s][1][-4:], marker = marker[s],color = color[s])
    plt.xlabel('Peacefulness Index')
    plt.ylabel('Happiness Score')
    #plt.ylim(1.6,2.8)
    plt.xticks(fontsize = 8, horizontalalignment = 'center', alpha = .7)
    plt.yticks(fontsize = 12, alpha = .7)
    plt.grid(axis='both',alpha = .3)
    plt.legend()
    plt.gca().invert_xaxis()
    plt.show()


def box_plot_level_ph(p_h_list: list):
    """

    Required:
    import seaborn as sns

    :param p_h_list:
    :return:

    >>> peace_data = Data().get_peace()
    >>> happiness = Data().get_happiness()
    >>> happiness['2017.csv'] = happiness['2017.csv'][['Country', 'Happiness.Score']]
    >>> happiness['2017.csv'].columns = ['Country', 'Happiness Score']
    >>> x_list_p_h, y_list_p_h, p_h_list = analysis_peace_happiness_level(peace_data, happiness)
    >>> print(type(box_plot_level_ph(p_h_list)))
    <class 'NoneType'>
    """
    fig, axes = plt.subplots(2,2, figsize=(50,40))
    item = [['pi_2015','Happiness Score'],['pi_2016','Happiness Score'],['pi_2017','Happiness Score']]
   # ax_list = [[0,0],[1,0],[2,0]]
    for s in range(3):
        cat_list = []
        data = p_h_list[s]
        cc = data[item[s][0]]
        for b in range(data.iloc[:,0].size):
            if math.isnan(cc[b]) == True:
                cat_list.append(math.nan)
            if cc[b] >= 1 and cc[b]<1.25:
                cat_list.append('[1,1.25)')
            if cc[b] >= 1.25 and cc[b]<1.5:
                cat_list.append('[1.25,1.5)')
            if cc[b] >= 1.5 and cc[b]<1.75:
                cat_list.append('[1.5,1.75)')
            if cc[b] >= 1.75 and cc[b]<2:
                cat_list.append('[1.75,2)')
            if cc[b] >= 2 and cc[b]<2.25:
                cat_list.append('[2,2.25)')
            if cc[b] >= 2.25 and cc[b]<2.5:
                cat_list.append('[2.25,2.5)')
            if cc[b] >= 2.5 and cc[b]<2.75:
                cat_list.append('[2.5,2.75)')
            if cc[b] >= 2.75 and cc[b]<3:
                cat_list.append('[2.75,3)')
            if cc[b] >= 3 and cc[b]<3.5:
                cat_list.append('[3,3.5)')
            if cc[b] >= 3.5:
                cat_list.append('3.5+')
        cat_col = pd.DataFrame(cat_list)
        new_data = pd.concat([data,cat_col],axis=1)
        new_data.columns = ['Country', item[s][1], item[s][0], 'Catergory of Peace Index']
        box = sns.boxplot(x=item[s][1], y='Catergory of Peace Index', data=new_data, whis="range", palette="vlag",
                          ax=axes[s // 2, s % 2],
                          order=['[1,1.25)', '[1.25,1.5)','[1.5,1.75)','[1.75,2)',
                                 '[2,2.25)','[2.25,2.5)','[2.5,2.75)','[2.75,3)','[3,3.5)','3.5+'])
        #rescale boxplot x-axis with log
        axes[s // 2, s % 2].set_title('Box Plot for Data of year '+ item[s][1][-4:])

        fig.subplots_adjust(wspace=.4)


## Part 3: Analysis of level 3-4, Belonging-Esteem by World Happiness and freedom dataset


def analysis_happiness_Freedom_level(happiness: pd.DataFrame, df_free: pd.DataFrame) -> (list, list, list):
    """

    :param happiness:
    :param df_free:
    :return:

    >>> happiness = Data().get_happiness()
    >>> happiness['2017.csv'] = happiness['2017.csv'][['Country', 'Happiness.Score']]
    >>> happiness['2017.csv'].columns = ['Country', 'Happiness Score']
    >>> freedom = Data().get_freedom()
    >>> df_free_data = pd.concat([freedom['year'], freedom['countries'], freedom['hf_score']], axis=1)
    >>> df_free_data.columns = ['Year', 'Country', 'Human_Freedom_Score']
    >>> x_list_h_f, y_list_h_f, h_f_list = analysis_happiness_Freedom_level(happiness, df_free_data)
    >>> type(x_list_h_f)
    <class 'list'>
    """
    h_f_list = []
    for i in range(2):
        string2 = str(2015+i)+'.csv'
        df = happiness[string2][['Country','Happiness Score']]
        df_f = df_free[df_free['Year']==(2015+i)]
        df_h_f = pd.merge(df, df_f, on = 'Country', how='inner')
        h_f_list.append(df_h_f)
    x_list = []
    y_list = []
    for s in range(2):
        df = h_f_list[s]
        dd = df.sort_values(by=['Happiness Score'], ascending=True)
        x = np.asarray(dd['Happiness Score'])
        y = np.asarray(dd['Human_Freedom_Score'])
        index_list = []
        for j in range(x.shape[0]):
            if math.isnan(x[j]) == True or math.isnan(y[j]) == True:
                index_list.append(j)
        new_x = np.delete(x,index_list)
        new_y = np.delete(y,index_list)
        x_list.append(new_x)
        y_list.append(new_y)
    return x_list, y_list, h_f_list


def plot_level_h_f(x_list: list, y_list: list):
    plt.figure(figsize = (30,15), dpi=100)
    marker = ['.','*','>','<','1','2','s','3','4']
    color = ['#E11B00', '#1E90FF','#7EFF33','#33F4FF','#D433FF','#3351FF','#D433FF']
    for f in range(2):
        plt.plot(x_list[f],y_list[f],label = 'data of year '+ str(2015+f), marker = marker[f],color = color[f])
    plt.xlabel('Happiness Score')
    plt.ylabel('Human_Freedom_Score')
    plt.xticks(fontsize = 8, horizontalalignment = 'center', alpha = .7)
    plt.yticks(fontsize = 12, alpha = .7)
    plt.grid(axis='both',alpha = .3)
    plt.legend()
    plt.show()


def plot_cat_hf(x_list: list, y_list: list):
    plt.figure(figsize = (30,20), dpi=100)
    x_item = ['[2.5,3)','[3,3.5)','[3.5,4)','[4,4.5)','[4.5,5)','[5,5.5)',
              '[5.5,6)','[6,6.5)','[6.5,7)','7+']
    marker = ['.','*','>','<','1','2','s']
    color = ['#E11B00', '#1E90FF','#FFE333','#7EFF33','#33F4FF','#D433FF']
    y_new_list = []
    for a in range(len(x_list)):
        cc = x_list[a]
        cy = y_list[a]
        y_item = np.zeros((10,2))
        for b in range(len(cc)):
            if cc[b] >= 2.5 and cc[b]<3:
                y_item[0][0] += cy[b]
                y_item[0][1] += 1
            if cc[b] >= 3 and cc[b]<3.5:
                y_item[1][0] += cy[b]
                y_item[1][1] += 1
            if cc[b] >= 3.5 and cc[b]<4:
                y_item[2][0] += cy[b]
                y_item[2][1] += 1
            if cc[b] >= 4 and cc[b]<4.5:
                y_item[3][0] += cy[b]
                y_item[3][1] += 1
            if cc[b] >= 4.5 and cc[b]<5:
                y_item[4][0] += cy[b]
                y_item[4][1] += 1
            if cc[b] >= 5 and cc[b]<5.5:
                y_item[5][0] += cy[b]
                y_item[5][1] += 1
            if cc[b] >= 5.5 and cc[b]<6:
                y_item[6][0] += cy[b]
                y_item[6][1] += 1
            if cc[b] >= 6 and cc[b]<6.5:
                y_item[7][0] += cy[b]
                y_item[7][1] += 1
            if cc[b] >= 6.5 and cc[b]<7:
                y_item[8][0] += cy[b]
                y_item[8][1] += 1
            if cc[b] >= 7:
                y_item[9][0] += cy[b]
                y_item[9][1] += 1
        y_new = np.zeros(y_item.shape[0])
        for c in range(y_item.shape[0]):
            if y_item[c][1] == 0:
                y_new[c] = math.nan
            else:
                y_new[c] = y_item[c][0]/y_item[c][1]
        y_new_list.append(y_new)
    for s in range(len(y_new_list)):
        plt.plot(x_item,y_new_list[s],label = 'data of year '+str(2015+s), marker = marker[s],color = color[s])
    plt.xlabel('Peacefulness Index')
    plt.ylabel('Happiness Score')
    #plt.ylim(1.6,2.8)
    plt.xticks(fontsize = 8, horizontalalignment = 'center', alpha = .7)
    plt.yticks(fontsize = 12, alpha = .7)
    plt.grid(axis='both',alpha = .3)
    plt.legend()
    plt.show()


def box_plot_level_hf(h_f_list: list):
    """
    
    Required:
    import seaborn as sns
    
    :param h_f_list: 
    :return: 
    
    """
    fig, axes = plt.subplots(2,1, figsize=(50,40))
    #ax_list = [[0,0],[1,0]]
    for s in range(2):
        cat_list = []
        data = h_f_list[s]
        cc = data['Happiness Score']
        for b in range(data.iloc[:,0].size):
            if math.isnan(cc[b]) == True:
                cat_list.append(math.nan)
            if cc[b] >= 2.5 and cc[b]<3:
                cat_list.append('[2.5,3)')
            if cc[b] >= 3 and cc[b]<3.5:
                cat_list.append('[3,3.5)')
            if cc[b] >= 3.5 and cc[b]<4:
                cat_list.append('[3.5,4)')
            if cc[b] >= 4 and cc[b]<4.5:
                cat_list.append('[4,4.5)')
            if cc[b] >= 4.5 and cc[b]<5:
                cat_list.append('[4.5,5)')
            if cc[b] >= 5 and cc[b]<5.5:
                cat_list.append('[5,5.5)')
            if cc[b] >= 5.5 and cc[b]<6:
                cat_list.append('[5.5,6)')
            if cc[b] >= 6 and cc[b]<6.5:
                cat_list.append('[6,6.5)')
            if cc[b] >= 6.5 and cc[b]<7:
                cat_list.append('[6.5,7)')
            if cc[b] >= 7:
                cat_list.append('7+')
        cat_col = pd.DataFrame(cat_list)
        new_data = pd.concat([data,cat_col],axis=1)
        new_data.columns = ['Country', 'Happiness Score', 'year', 'Human_Freedom_Score', 'Range of Happiness Score']
        box = sns.boxplot(x='Human_Freedom_Score', y='Range of Happiness Score', data=new_data, whis="range", palette="vlag",
                          ax=axes[s % 2], 
                          order=['[2.5,3)','[3,3.5)','[3.5,4)','[4,4.5)','[4.5,5)','[5,5.5)','[5.5,6)','[6,6.5)','[6.5,7)','7+'])
        axes[s % 2].set_title('Box Plot for Data of year '+ str(2015+s))

        fig.subplots_adjust(wspace=.4)


## Part 4: Analysis of level 2-4, Safety-Esteem by peace and freedom dataset


def analysis_two_fourth_level(peace: pd.DataFrame, df_free: pd.DataFrame):
    level24_list = []
    for i in range(6):
        df = df_free[df_free['Year']==(2010+i)]
        string = 'pi_'+str(2010+i)
        p1 = peace['Country']
        p2 = peace[string]   
        p = pd.concat([p1, p2],axis = 1)
        df_level24 = pd.merge(df, p, on = 'Country', how='inner')
        df_level24 = df_level24.drop_duplicates(keep='first', inplace=False)
        level24_list.append(df_level24)
    x_list = []
    y_list = []
    pi_list = ['pi_2010','pi_2011','pi_2012','pi_2013','pi_2014','pi_2015','pi_2016']
    for s in range(6):
        df = level24_list[s]
        dd = df.sort_values(by=[pi_list[s]], ascending=True)
        x = np.asarray(dd[pi_list[s]])
        y = np.asarray(dd['Human_Freedom_Score'])
        index_list = []
        for j in range(x.shape[0]):
            if math.isnan(x[j]) == True or math.isnan(y[j]) == True:
                index_list.append(j)
        new_x = np.delete(x,index_list)
        new_y = np.delete(y,index_list)
        x_list.append(new_x)
        y_list.append(new_y)
    return x_list, y_list, level24_list


def plot_level_24(x_list: list, y_list: list):
    plt.figure(figsize = (30,15), dpi=100)
    marker = ['.','*','>','<','1','2','s']
    color = ['#E11B00', '#1E90FF','#FF4233','#FFE333','#7EFF33','#33F4FF','#D433FF']
    pi_list = ['pi_2010','pi_2011','pi_2012','pi_2013','pi_2014','pi_2015','pi_2016']
    for f in range(6):
        plt.plot(x_list[f],y_list[f],label = 'data of year '+pi_list[f][-4:], marker = marker[f],color = color[f])
    plt.xlabel('Peacefulness Index')
    plt.ylabel('Marriage rate')
    plt.ylim(4,9)
    plt.xlim(1,3.125)
    plt.xticks(fontsize = 8, horizontalalignment = 'center', alpha = .7)
    plt.yticks(fontsize = 12, alpha = .7)
    plt.grid(axis='both',alpha = .3)
    plt.legend()
    plt.gca().invert_xaxis()
    plt.show()


def plot_cat24(x_list: list, y_list: list):
    plt.figure(figsize = (30,20), dpi=100)
    pi_list = ['pi_2010','pi_2011','pi_2012','pi_2013','pi_2014','pi_2015','pi_2016']
    x_item = ['[1,1.25)','[1.25,1.5)','[1.5,1.75)','[1.75,2)','[2,2.25)','[2.25,2.5)',
              '[2.5,2.75)','[2.75,3)','3+']
    marker = ['.','*','>','<','1','2','s']
    color = ['#E11B00', '#1E90FF','#FF4233','#FFE333','#7EFF33','#33F4FF','#D433FF']
    y_new_list = []
    for a in range(len(x_list)):
        cc = x_list[a]
        cy = y_list[a]
        y_item = np.zeros((9,2))
        for b in range(len(cc)):
            if cc[b] >= 1 and cc[b]<1.25:
                y_item[0][0] += cy[b]
                y_item[0][1] += 1
            if cc[b] >= 1.25 and cc[b]<1.5:
                y_item[1][0] += cy[b]
                y_item[1][1] += 1
            if cc[b] >= 1.5 and cc[b]<1.75:
                y_item[2][0] += cy[b]
                y_item[2][1] += 1
            if cc[b] >= 1.75 and cc[b]<2:
                y_item[3][0] += cy[b]
                y_item[3][1] += 1
            if cc[b] >= 2 and cc[b]<2.25:
                y_item[4][0] += cy[b]
                y_item[4][1] += 1
            if cc[b] >= 2.25 and cc[b]<2.5:
                y_item[5][0] += cy[b]
                y_item[5][1] += 1
            if cc[b] >= 2.5 and cc[b]<2.75:
                y_item[6][0] += cy[b]
                y_item[6][1] += 1
            if cc[b] >= 2.75 and cc[b]<3:
                y_item[7][0] += cy[b]
                y_item[7][1] += 1
            if cc[b] >= 3:
                y_item[8][0] += cy[b]
                y_item[8][1] += 1
        y_new = np.zeros(y_item.shape[0])
        for c in range(y_item.shape[0]):
            if y_item[c][1] == 0:
                y_new[c] = math.nan
            else:
                y_new[c] = y_item[c][0]/y_item[c][1]
        y_new_list.append(y_new)
    for s in range(len(y_new_list)):
        plt.plot(x_item,y_new_list[s],label = 'data of year '+pi_list[s][1][-4:], marker = marker[s],color = color[s])
    plt.xlabel('Peacefulness Index')
    plt.ylabel('Human Freedom Score')
    #plt.ylim(1.6,2.8)
    plt.xticks(fontsize = 8, horizontalalignment = 'center', alpha = .7)
    plt.yticks(fontsize = 12, alpha = .7)
    plt.grid(axis='both',alpha = .3)
    plt.legend()
    plt.gca().invert_xaxis()
    plt.show()


def box_plot_level24(level_list24: list):
    """
    
    Required:
    import seaborn as sns
    
    :param level_list24: 
    :return: 
    """
    fig, axes = plt.subplots(3, 2, figsize=(50,40))
    item = [['Human_Freedom_Score','pi_2010'],['Human_Freedom_Score','pi_2011'],
                  ['Human_Freedom_Score','pi_2012'],['Human_Freedom_Score','pi_2013'],
                  ['Human_Freedom_Score','pi_2014'],['Human_Freedom_Score','pi_2015'],]
    ax_list = [[0,0],[0,1],[1,0],[1,1],[2,0],[2,1]]
    for s in range(6):
        cat_list = []
        data = level_list24[s]
        cc = data[item[s][1]]
        for b in range(data.iloc[:,0].size):
            if math.isnan(cc[b]) == True:
                cat_list.append(math.nan)
            if cc[b] >= 1 and cc[b]<1.25:
                cat_list.append('[1,1.25)')
            if cc[b] >= 1.25 and cc[b]<1.5:
                cat_list.append('[1.25,1.5)')
            if cc[b] >= 1.5 and cc[b]<1.75:
                cat_list.append('[1.5,1.75)')
            if cc[b] >= 1.75 and cc[b]<2:
                cat_list.append('[1.75,2)')
            if cc[b] >= 2 and cc[b]<2.25:
                cat_list.append('[2,2.25)')
            if cc[b] >= 2.25 and cc[b]<2.5:
                cat_list.append('[2.25,2.5)')
            if cc[b] >= 2.5 and cc[b]<2.75:
                cat_list.append('[2.5,2.75)')
            if cc[b] >= 2.75 and cc[b]<3:
                cat_list.append('[2.75,3)')
            if cc[b] >= 3 :
                cat_list.append('3+')
        cat_col = pd.DataFrame(cat_list)
        new_data = pd.concat([data,cat_col],axis=1)
        new_data.columns = ['Year', 'Country', item[s][0], item[s][1], 'Catergory of Peace Index']
        box = sns.boxplot(x=item[s][0], y='Catergory of Peace Index', data=new_data, whis="range", palette="vlag",
                          ax=axes[ax_list[s][0], ax_list[s][1]], 
                          order=['[1,1.25)', '[1.25,1.5)','[1.5,1.75)','[1.75,2)',
                                 '[2,2.25)','[2.25,2.5)','[2.5,2.75)','[2.75,3)','3+'])
        #rescale boxplot x-axis with log
        axes[ax_list[s][0], ax_list[s][1]].set_title('Box Plot for Data of year '+ item[s][1][-4:])

        fig.subplots_adjust(wspace=.4)


## Part 5: Analysis of level 4-5, Esteem-Self Actualization by freedom and innovation dataset


def analysis_level45(inno_list: list, free_list: list):
    level_45_list = []
    for i in range(4):
        df_level45 = pd.merge(inno_list[i], free_list[i], on = 'Country', how='inner')
        df_level45 = df_level45.drop_duplicates(keep='first', inplace=False)
        level_45_list.append(df_level45)
    x_list = []
    y_list = []
    item = ['Score2013', 'Score2014', 'Score2015', 'Score2016']
    for s in range(4):
        df = level_45_list[s]
        dd = df.sort_values(by='hf_score', ascending=True)
        x = np.asarray(dd['hf_score'])
        y = np.asarray(dd[item[s]])
        index_list = []
        for j in range(x.shape[0]):
            if math.isnan(x[j]) == True or math.isnan(y[j]) == True:
                index_list.append(j)
        new_x = np.delete(x,index_list)
        new_y = np.delete(y,index_list)
        x_list.append(new_x)
        y_list.append(new_y)
    return x_list, y_list, level_45_list


def plot45(x_list: list, y_list: list):
    plt.figure(figsize = (30,15), dpi=100)
    item = ['Score2013', 'Score2014', 'Score2015', 'Score2016']
    marker = ['.','*','>','<','1','2','s']
    color = ['#E11B00', '#1E90FF','#FF4233','#FFE333','#7EFF33','#33F4FF','#D433FF']
    for f in range(len(x_list)):
        plt.plot(x_list[f],y_list[f],label = 'data of year '+item[f][-4:], marker = marker[f])#,color = color[f])
    plt.xlabel('Freedom Index')
    plt.ylabel('Innovation Index')
    plt.xticks(fontsize = 8, horizontalalignment = 'center', alpha = .7)
    plt.yticks(fontsize = 12, alpha = .7)
    plt.grid(axis='both',alpha = .3)
    plt.legend()#prop={'size': 30})
    plt.show()


def plot45_cat(x_list: list, y_list: list):
    plt.figure(figsize = (30,20), dpi=100)
    item = ['Score2013', 'Score2014', 'Score2015', 'Score2016']
    start = 4.5
    end = 9
    range_interval = 9
    interval = (end-start)/range_interval
    x_item = []
    for j in range(range_interval):
        x_item.append('[%s,%s)' %(start+(interval*j), start+(interval*(j+1))))
    marker = ['.','*','>','<','1','2','s']
    color = ['#E11B00', '#1E90FF','#FF4233','#FFE333','#7EFF33','#33F4FF','#D433FF']
    y_new_list = []
    for a in range(len(x_list)):
        cc = x_list[a]
        cy = y_list[a]
        y_item = np.zeros((range_interval,2))
        for b in range(len(cc)):
            for k in range(10):
                if cc[b] >= (start+(interval*k)) and cc[b] < (start+(interval*(k+1))):
                    y_item[k][0] += cy[b]
                    y_item[k][1] += 1
        y_new = np.zeros(y_item.shape[0])
        for c in range(y_item.shape[0]):
            if y_item[c][1] == 0:
                y_new[c] = math.nan
            else:
                y_new[c] = y_item[c][0]/y_item[c][1]
        y_new_list.append(y_new)
    for s in range(len(y_new_list)):
        plt.plot(x_item,y_new_list[s],label = 'data of year '+item[s][-4:], marker = marker[s],color = color[s])
    plt.xlabel('Freedom Index')
    plt.ylabel('Innovation Index')
    plt.xticks(fontsize = 8, horizontalalignment = 'center', alpha = .7)
    plt.yticks(fontsize = 12, alpha = .7)
    plt.grid(axis='both',alpha = .3)
    plt.legend()#prop={'size': 30})
    plt.show()


def box_plot_45(level_45_list: list):
    fig, axes = plt.subplots(2, 2, figsize=(50,40))
    item = [['hf_score','Score2013'], ['hf_score','Score2014'], ['hf_score','Score2015'], ['hf_score','Score2016']]
    free_item = 'Human_Freedom_Score'
    ax_list = [[0,0],[0,1],[1,0],[1,1]]
    for s in range(4):
        cat_list = []
        data = level_45_list[s]
        cc = data[item[s][0]]
        for b in range(data.iloc[:,0].size):
            if math.isnan(cc[b]) == True:
                cat_list.append(math.nan)
            if cc[b] >= 4.5 and cc[b]<5.0:
                cat_list.append('[4.5,5.0)')
            if cc[b] >= 5.0 and cc[b]<5.5:
                cat_list.append('[5.0,5.5)')
            if cc[b] >= 5.5 and cc[b]<6.0:
                cat_list.append('[5.5,6.0)')
            if cc[b] >= 6.0 and cc[b]<6.5:
                cat_list.append('[6.0,6.5)')
            if cc[b] >= 6.5 and cc[b]<7.0:
                cat_list.append('[6.5,7.0)')
            if cc[b] >= 7.0 and cc[b]<7.5:
                cat_list.append('[7.0,7.5)')
            if cc[b] >= 7.5 and cc[b]<8.0:
                cat_list.append('[7.5,8.0)')
            if cc[b] >= 8.0 and cc[b]<8.5:
                cat_list.append('[8.0,8.5)')
            if cc[b] >= 8.5 and cc[b]<9:
                cat_list.append('[8.5,9.0)')
        cat_col = pd.DataFrame(cat_list)
        new_data = pd.concat([data,cat_col],axis=1)
        new_data.columns = ['Country', item[s][1], 'year', free_item, 'Catergory of Human Freedom Index']
        box = sns.boxplot(x=free_item, y='Catergory of Human Freedom Index', data=new_data, whis="range", palette="vlag",
                          ax=axes[ax_list[s][0], ax_list[s][1]], 
                          order=['[4.5,5.0)','[5.0,5.5)','[5.5,6.0)','[6.0,6.5)',
                                 '[6.5,7.0)','[7.0,7.5)','[7.5,8.0)','[8.0,8.5)','[8.5,9.0)'])
        #rescale boxplot x-axis with log
        axes[ax_list[s][0], ax_list[s][1]].set_title('Box Plot for Data of year '+ item[s][1][-4:])

        fig.subplots_adjust(wspace=.4)


## Part 6: Analysis of level 1-4, Belonging-Esteem by hunger + freedom index dataset


def analysis_first_fourth_level(hunger: pd.DataFrame, df_free: pd.DataFrame):
    level14_list = []
    for i in range(7):
        df = df_free[df_free['Year']==(2010+i)]
        string = 'undernourishment_rate_'+str(2010+i)
        p1 = hunger['Country']
        p2 = hunger[string]   
        p = pd.concat([p1, p2],axis = 1)
        df_level14 = pd.merge(df, p, on = 'Country', how='inner')
        df_level14 = df_level14.drop_duplicates(keep='first', inplace=False)
        level14_list.append(df_level14)
    x_list = []
    y_list = []
    hunger_list = ['undernourishment_rate_2010','undernourishment_rate_2011','undernourishment_rate_2012',
                   'undernourishment_rate_2013','undernourishment_rate_2014','undernourishment_rate_2015',
                   'undernourishment_rate_2016']
    for s in range(7):
        df = level14_list[s]
        dd = df.sort_values(by=[hunger_list[s]], ascending=True)
        x = np.asarray(dd[hunger_list[s]])
        y = np.asarray(dd['Human_Freedom_Score'])
        index_list = []
        for j in range(x.shape[0]):
            if math.isnan(x[j]) == True or math.isnan(y[j]) == True:
                index_list.append(j)
        new_x = np.delete(x,index_list)
        new_y = np.delete(y,index_list)
        x_list.append(new_x)
        y_list.append(new_y)
    return x_list, y_list, level14_list


def plot_14(x_list: list, y_list: list):
    plt.figure(figsize = (30,15), dpi=100)
    item = [['undernourishment_rate_2010','Human_Freedom_Score'],['undernourishment_rate_2011','Human_Freedom_Score'],
            ['undernourishment_rate_2012','Human_Freedom_Score'],['undernourishment_rate_2013','Human_Freedom_Score'],
            ['undernourishment_rate_2014','Human_Freedom_Score'],['undernourishment_rate_2015','Human_Freedom_Score'],
            ['undernourishment_rate_2016','Human_Freedom_Score']]
    marker = ['.','*','>','<','1','2','s']
    color = ['#E11B00', '#1E90FF','#FF4233','#FFE333','#7EFF33','#33F4FF','#D433FF']
    for f in range(len(x_list)):
        plt.plot(x_list[f],y_list[f],label = 'data of year '+item[f][0][-4:], marker = marker[f],color = color[f])
    plt.xlabel('undernourishment rate')
    plt.ylabel('Human_Freedom_Score')
    #plt.ylim(1,4)
    plt.xticks(fontsize = 8, horizontalalignment = 'center', alpha = .7)
    plt.yticks(fontsize = 12, alpha = .7)
    plt.grid(axis='both',alpha = .3)
    plt.legend()
    plt.gca().invert_xaxis()
    plt.show()


def plot_cat_level14(x_list: list, y_list: list):
    plt.figure(figsize = (30,20), dpi=100)
    item = [['undernourishment_rate_2010','Human_Freedom_Score'],['undernourishment_rate_2011','Human_Freedom_Score'],
            ['undernourishment_rate_2012','Human_Freedom_Score'],['undernourishment_rate_2013','Human_Freedom_Score'],
            ['undernourishment_rate_2014','Human_Freedom_Score'],['undernourishment_rate_2015','Human_Freedom_Score'],
            ['undernourishment_rate_2016','Human_Freedom_Score']]
    x_item = ['[0,5)','[5,10)','[10,15)','[15,20)','[20,25)','[25,30)','[30,35)','[35,40)','[40,45)',
             '[45,50)']#,'[50+']
    marker = ['.','*','>','<','1','2','s']
    color = ['#E11B00', '#1E90FF','#FF4233','#FFE333','#7EFF33','#33F4FF','#D433FF']
    y_new_list = []
    for a in range(len(x_list)):
        cc = x_list[a]
        cy = y_list[a]
        y_item = np.zeros((10,2))
        for b in range(len(cc)):
            if cc[b] >= 0 and cc[b]<5:
                y_item[0][0] += cy[b]
                y_item[0][1] += 1
            if cc[b] >= 5 and cc[b]<10:
                y_item[1][0] += cy[b]
                y_item[1][1] += 1
            if cc[b] >= 10 and cc[b]<15:
                y_item[2][0] += cy[b]
                y_item[2][1] += 1
            if cc[b] >= 15 and cc[b]<20:
                y_item[3][0] += cy[b]
                y_item[3][1] += 1
            if cc[b] >= 20 and cc[b]<25:
                y_item[4][0] += cy[b]
                y_item[4][1] += 1
            if cc[b] >= 25 and cc[b]<30:
                y_item[5][0] += cy[b]
                y_item[5][1] += 1
            if cc[b] >= 30 and cc[b]<35:
                y_item[6][0] += cy[b]
                y_item[6][1] += 1
            if cc[b] >= 35 and cc[b]<40:
                y_item[7][0] += cy[b]
                y_item[7][1] += 1
            if cc[b] >= 40 and cc[b]<45:
                y_item[8][0] += cy[b]
                y_item[8][1] += 1
            if cc[b] >= 45 and cc[b]<50:
                y_item[9][0] += cy[b]
                y_item[9][1] += 1
#             if cc[b] >= 50:
#                 y_item[10][0] += cy[b]
#                 y_item[10][1] += 1
        y_new = np.zeros(y_item.shape[0])
        for c in range(y_item.shape[0]):
            if y_item[c][1] == 0:
                y_new[c] = math.nan
            else:
                y_new[c] = y_item[c][0]/y_item[c][1]
        y_new_list.append(y_new)
    for s in range(len(y_new_list)):
        plt.plot(x_item,y_new_list[s],label = 'data of year '+item[s][0][-4:], marker = marker[s],color = color[s])
    plt.xlabel('undernourishment rate')
    plt.ylabel('Freedom Score')
    #plt.ylim(1.6,2.8)
    plt.xticks(fontsize = 8, horizontalalignment = 'center', alpha = .7)
    plt.yticks(fontsize = 12, alpha = .7)
    plt.grid(axis='both',alpha = .3)
    plt.legend()
    plt.gca().invert_xaxis()
    plt.show()


def box_plot_level14(level14_list: list):
    """
    
    Required:
    import seaborn as sns
    
    :param level14_list: 
    :return: 
    """
    fig, axes = plt.subplots(3, 3, figsize=(60,40))
    item = [['undernourishment_rate_2010','Human_Freedom_Score'],['undernourishment_rate_2011','Human_Freedom_Score'],
            ['undernourishment_rate_2012','Human_Freedom_Score'],['undernourishment_rate_2013','Human_Freedom_Score'],
            ['undernourishment_rate_2014','Human_Freedom_Score'],['undernourishment_rate_2015','Human_Freedom_Score'],
            ['undernourishment_rate_2016','Human_Freedom_Score']]
    for s in range(7):
        cat_list = []
        data = level14_list[s]
        cc = data[item[s][0]]
        for b in range(data.iloc[:,0].size):
            if math.isnan(cc[b]) == True:
                cat_list.append(math.nan)
            if cc[b] >= 0 and cc[b]<5:
                cat_list.append('[0,5)')
            if cc[b] >= 5 and cc[b]<10:
                cat_list.append('[5,10)')
            if cc[b] >= 10 and cc[b]<15:
                cat_list.append('[10,15)')
            if cc[b] >= 15 and cc[b]<20:
                cat_list.append('[15,20)')
            if cc[b] >= 20 and cc[b]<25:
                cat_list.append('[20,25)')
            if cc[b] >= 25 and cc[b]<30:
                cat_list.append('[25,30)')
            if cc[b] >= 30 and cc[b]<35:
                cat_list.append('[30,35)')
            if cc[b] >= 35 and cc[b]<40:
                cat_list.append('[35,40)')
            if cc[b] >= 40 and cc[b]<45:
                cat_list.append('[40,45)')
            if cc[b] >= 45 and cc[b]<50:
                cat_list.append('[45,50)')
        cat_col = pd.DataFrame(cat_list)
        new_data = pd.concat([data,cat_col],axis=1)
        new_data.columns = ['Year', 'Country', item[s][1], item[s][0], 'Catergory of Hunger']
        box = sns.boxplot(x=item[s][1], y='Catergory of Hunger', data=new_data, whis="range", palette="vlag",
                          ax=axes[s // 3, s % 3], 
                          order=['[0,5)','[5,10)','[10,15)','[15,20)','[20,25)','[25,30)','[30,35)','[35,40)','[40,45)'])
        #rescale boxplot x-axis with log
        axes[s // 3, s % 3].set_title('Box Plot for Data of year '+ item[s][0][-4:])

        fig.subplots_adjust(wspace=.4)


## Part 7: Analysis of level 1-5, Physiological-Esteem by hunger + Innovation index dataset


def analysis_level15(hunger: list, inno_list: list):
    level_15_list = []
    for i in range(4):
        string = 'undernourishment_rate_'+str(2013+i)
        p1 = hunger['Country']
        p2 = hunger[string]   
        p = pd.concat([p1, p2],axis = 1)
        df_level15 = pd.merge(p, inno_list[i], on = 'Country', how='inner')
        df_level15 = df_level15.drop_duplicates(keep='first', inplace=False)
        level_15_list.append(df_level15)
    x_list = []
    y_list = []
    item = [['undernourishment_rate_2013','Score2013'], ['undernourishment_rate_2014','Score2014'],
            ['undernourishment_rate_2015','Score2015'], ['undernourishment_rate_2016','Score2016']]
    for s in range(4):
        df = level_15_list[s]
        dd = df.sort_values(by=[item[s][0]], ascending=True)
        x = np.asarray(dd[item[s][0]])
        y = np.asarray(dd[item[s][1]])
        index_list = []
        for j in range(x.shape[0]):
            if math.isnan(x[j]) == True or math.isnan(y[j]) == True:
                index_list.append(j)
        new_x = np.delete(x,index_list)
        new_y = np.delete(y,index_list)
        x_list.append(new_x)
        y_list.append(new_y)
    return x_list, y_list, level_15_list


def plot_15(x_list: list, y_list: list):
    plt.figure(figsize = (30,15), dpi=100)
    item = [['undernourishment_rate_2013','Score2013'], ['undernourishment_rate_2014','Score2014'],
            ['undernourishment_rate_2015','Score2015'], ['undernourishment_rate_2016','Score2016']]
    marker = ['.','*','>','<','1','2','s']
    color = ['#E11B00', '#1E90FF','#FF4233','#FFE333','#7EFF33','#33F4FF','#D433FF']
    for f in range(len(x_list)):
        plt.plot(x_list[f],y_list[f],label = 'data of year '+item[f][0][-4:], marker = marker[f],color = color[f])
    plt.xlabel('undernourishment rate')
    plt.ylabel('Human_Innovation_Index')
    #plt.ylim(1,4)
    plt.xticks(fontsize = 8, horizontalalignment = 'center', alpha = .7)
    plt.yticks(fontsize = 12, alpha = .7)
    plt.grid(axis='both',alpha = .3)
    plt.legend()
    plt.gca().invert_xaxis()
    plt.show()


def plot_cat_level15(x_list: list, y_list: list):
    plt.figure(figsize = (30,20), dpi=100)
    item = [['undernourishment_rate_2013','Score2013'], ['undernourishment_rate_2014','Score2014'],
            ['undernourishment_rate_2015','Score2015'], ['undernourishment_rate_2016','Score2016']]
    x_item = ['[0,5)','[5,10)','[10,15)','[15,20)','[20,25)','[25,30)','[30,35)','[35,40)','[40,45)',
             '[45,50)']#,'[50+']
    marker = ['.','*','>','<','1','2','s']
    color = ['#E11B00', '#1E90FF','#FF4233','#FFE333','#7EFF33','#33F4FF','#D433FF']
    y_new_list = []
    for a in range(len(x_list)):
        cc = x_list[a]
        cy = y_list[a]
        y_item = np.zeros((10,2))
        for b in range(len(cc)):
            if cc[b] >= 0 and cc[b]<5:
                y_item[0][0] += cy[b]
                y_item[0][1] += 1
            if cc[b] >= 5 and cc[b]<10:
                y_item[1][0] += cy[b]
                y_item[1][1] += 1
            if cc[b] >= 10 and cc[b]<15:
                y_item[2][0] += cy[b]
                y_item[2][1] += 1
            if cc[b] >= 15 and cc[b]<20:
                y_item[3][0] += cy[b]
                y_item[3][1] += 1
            if cc[b] >= 20 and cc[b]<25:
                y_item[4][0] += cy[b]
                y_item[4][1] += 1
            if cc[b] >= 25 and cc[b]<30:
                y_item[5][0] += cy[b]
                y_item[5][1] += 1
            if cc[b] >= 30 and cc[b]<35:
                y_item[6][0] += cy[b]
                y_item[6][1] += 1
            if cc[b] >= 35 and cc[b]<40:
                y_item[7][0] += cy[b]
                y_item[7][1] += 1
            if cc[b] >= 40 and cc[b]<45:
                y_item[8][0] += cy[b]
                y_item[8][1] += 1
            if cc[b] >= 45 and cc[b]<50:
                y_item[9][0] += cy[b]
                y_item[9][1] += 1
#             if cc[b] >= 50:
#                 y_item[10][0] += cy[b]
#                 y_item[10][1] += 1
        y_new = np.zeros(y_item.shape[0])
        for c in range(y_item.shape[0]):
            if y_item[c][1] == 0:
                y_new[c] = math.nan
            else:
                y_new[c] = y_item[c][0]/y_item[c][1]
        y_new_list.append(y_new)
    for s in range(len(y_new_list)):
        plt.plot(x_item,y_new_list[s],label = 'data of year '+item[s][0][-4:], marker = marker[s],color = color[s])
    plt.xlabel('undernourishment rate')
    plt.ylabel('Innovation Index Score')
    #plt.ylim(1.6,2.8)
    plt.xticks(fontsize = 8, horizontalalignment = 'center', alpha = .7)
    plt.yticks(fontsize = 12, alpha = .7)
    plt.grid(axis='both',alpha = .3)
    plt.legend()
    plt.gca().invert_xaxis()
    plt.show()


def box_plot_level15(level_15_list: list):
    """

    Required:
    import seaborn as sns

    :param level_15_list:
    :return:
    """
    fig, axes = plt.subplots(2, 2, figsize=(60,40))
    item = [['undernourishment_rate_2013','Score2013'], ['undernourishment_rate_2014','Score2014'],
            ['undernourishment_rate_2015','Score2015'], ['undernourishment_rate_2016','Score2016']]
    inno_item = ['Innovation index score of year 2013','Innovation index score of year 2014',
                 'Innovation index score of year 2015','Innovation index score of year 2016']
    for s in range(4):
        cat_list = []
        data = level_15_list[s]
        cc = data[item[s][0]]
        for b in range(data.iloc[:,0].size):
            if math.isnan(cc[b]) == True:
                cat_list.append(math.nan)
            if cc[b] >= 0 and cc[b]<5:
                cat_list.append('[0,5)')
            if cc[b] >= 5 and cc[b]<10:
                cat_list.append('[5,10)')
            if cc[b] >= 10 and cc[b]<15:
                cat_list.append('[10,15)')
            if cc[b] >= 15 and cc[b]<20:
                cat_list.append('[15,20)')
            if cc[b] >= 20 and cc[b]<25:
                cat_list.append('[20,25)')
            if cc[b] >= 25 and cc[b]<30:
                cat_list.append('[25,30)')
            if cc[b] >= 30 and cc[b]<35:
                cat_list.append('[30,35)')
            if cc[b] >= 35 and cc[b]<40:
                cat_list.append('[35,40)')
            if cc[b] >= 40 and cc[b]<45:
                cat_list.append('[40,45)')
            if cc[b] >= 45 and cc[b]<50:
                cat_list.append('[45,50)')
        cat_col = pd.DataFrame(cat_list)
        new_data = pd.concat([data,cat_col],axis=1)
        new_data.columns = ['Country', item[s][0], inno_item[s], 'Percentage Range of Hunger']
        box = sns.boxplot(x=inno_item[s], y='Percentage Range of Hunger', data=new_data, whis="range", palette="vlag",
                          ax=axes[s // 2, s % 2], 
                          order=['[0,5)','[5,10)','[10,15)','[15,20)','[20,25)','[25,30)','[30,35)','[35,40)','[40,45)'])
        #rescale boxplot x-axis with log
        axes[s // 2, s % 2].set_title('Box Plot for Data of year '+ item[s][0][-4:])

        fig.subplots_adjust(wspace=.4)


