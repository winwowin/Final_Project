import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from pandas import read_excel
import logging
import zipfile


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

    def get_innovation(self: object, sheet: str = None) -> dict:
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
        # file_path = "590PR_final_datasets"
        file_name = "Innovation.zip"
        zf = zipfile.ZipFile(self.file_path + '/' + file_name)
        inv = {}
        for name in zipfile.ZipFile.infolist(zf):
            inv[name.filename] = pd.read_csv(zf.open(name.filename))
        if not sheet == None:
            return inv[sheet]
        else:
            return inv

    def prep_freedom(self):
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

    # def prep_innovation(self):
    #     inno_list = []
    #     for i in range(6):
    #         df = Data.get_innovation('get_innovation-201%s.csv' % (i + 3))
    #         df.rename({'Economy': 'Country', 'Score': 'Score201%s' % (i + 3)}, axis='columns', inplace=True)
    #         inno_list.append(df[['Country', 'Score201%s' % (i + 3)]])
    #     return inno_list

# freedom = Data().get_freedom()
# # gdelt = Data().get_GDELT("2016 10 15", "2016 10 16")
# happiness = Data().get_happiness()
# print(type(Data().get_happiness()['2015.csv']))
# hunger = Data().get_hunger()
# # married = Data().get_married_UNPD('CURRENTLY MARRIED')
# peace = Data().get_peace()
# print(peace)

# # print(Data().get_poverty().keys())
# Data().get_poverty("PovStatsData.csv")
# poverty = Data().get_poverty()
# suicide = Data().get_suicide
# trade = Data().get_trade
# # crime = Data().get_UNODC_crime()
# burglary = Data().get_UNODC_crime('Burglary')

# unemploy = Data().get_unemployment()
#
# # free_list = PREP_DATA.freedom()
# # inno_list = PREP_DATA.innovation()



print(Data().get_innovation())