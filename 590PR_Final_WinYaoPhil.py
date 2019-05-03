


from PR_Final_WinYaoPhil_functions import *

Data = Data()


def finish_it():
    """

    :return:

    >>> finish_it()

    """

    # coding: utf-8

    # 1-2 -ok
    #
    # 1-3
    #
    # 1-4
    #
    # 1-5
    #
    # 2-3 -ok
    #
    # 2-4 -ok
    #
    # 2-5
    #
    # 3-4
    #
    # 3-5
    #
    # 4-5 -ok

    # # World-living-quality-analysis
    #
    # ### Title:
    # Make Maslow Great Again ...or not
    # ——A Statistical Methodology/Model/Proof/Falsification of Maslow's Pyramid
    #
    # ### Team members:
    # Worawich (Win) Chaiyakunapruk,
    # Phil Zhe Wang,
    # Yao Xiao,
    #
    # ### Summary:
    # Maslow's hierarchy of needs, or the so-called Maslow pyramid, is a famous theory when we talk about human being's self-satisfaction. Raised in 1943, the book A Theory of Human Motivation, it describes people's psychological motivation in different developing periods.
    # However famous, the doubts it received has never been reduced. You will get over 20000 results in google scholar after typing in keywords like "Maslow's hierarchy of needs criticism".
    # But most of the criticisms are built from the point of Psychology, which makes them not that strong on my opinion.
    # This time, we will build the hierarchy model with real data, and try to prove if he is right or wrong.
    # Maslow used to be a great psychologist, but our slogan is:
    # Make Maslow Great Again! (or not, if possible, because in that situation is most likely to publish a paper)
    #
    # ### Hypotheses:
    # 1. Maslow's theory is right in all!
    # 2. Maslow's theory is right to some extent!
    # 3. Maslow's theory has a scope: it works for developing contries but not developed contries!
    #
    # ### Datasets:
    # - World get_happiness Report [https://www.kaggle.com/unsdsn/world-happiness]
    # - The Human get_freedom Index [https://www.kaggle.com/gsutters/the-human-freedom-index]
    # - UNODC Global Criminal Justice Statistics [https://data.world/unodc/b4aa5785-7a33-4c07-af15-0f15d95a121f] I already registered and download this one.
    # - get_poverty And Equity Database [https://datacatalog.worldbank.org/dataset/poverty-and-equity-database]
    # - IBRD Statement Of Loans - Historical Data [https://finances.worldbank.org/Loans-and-Credits/IBRD-Statement-Of-Loans-Historical-Data/zucq-nrc3]
    # - World Integrated get_trade Solution get_trade Stats [https://datacatalog.worldbank.org/dataset/world-integrated-trade-solution-trade-stats]
    # - Economic Fitness [https://datacatalog.worldbank.org/dataset/economic-fitness]
    # - get_suicide Rates Overview 1985 to 2016 [https://www.kaggle.com/russellyates88/suicide-rates-overview-1985-to-2016]
    # - World Bank: Education Data [https://www.kaggle.com/theworldbank/world-bank-intl-education]
    #
    # ### Mapping
    # - Physiological ——> get_hunger/living data
    # - Safety ——> Criminal data
    # - Love/belonging ——> Marriage/Children/Family data
    # - Esteem ——> Position/Class data
    # - Self-actualization ——> Job satisfaction/get_happiness data
    #
    # ### Git:
    # https://github.com/winwowin/World-living-quality-analysis
    #

    # ## Getting data




    ## Part 1: Analysis of level 1-2, Physiological-Safety by hunger+peace index dataset

    hunger_data = Data.get_hunger()
    peace_data = Data.get_peace()

    x_list, y_list, df_level1 = analysis_first_two_level(hunger_data, peace_data)
    plot12(x_list, y_list)
    plot_cat12(x_list, y_list)
    box_plot_level12(df_level1)

    ## Part 2: Analysis of level 2-3, Safety-Belonging by Peace Index and Marriage data

    married = Data.get_marital()
    married = married.astype({"Year": int}, copy=False)

    percent_married = get_marriage_rate(married)
    x_list_level2, y_list_level2, df_level2 = analysis_two_third_level(peace_data, percent_married)
    plot_level_23(x_list_level2, y_list_level2)

    ## Part 2-2: Analysis of level 2-3, Safety-Belonging by Peace Index and Happiness data

    happiness = Data.get_happiness()
    happiness['2017.csv'] = happiness['2017.csv'][['Country', 'Happiness.Score']]
    happiness['2017.csv'].columns = ['Country', 'Happiness Score']

    x_list_p_h, y_list_p_h, p_h_list = analysis_peace_happiness_level(peace_data, happiness)
    plot_level_p_h(x_list_p_h, y_list_p_h)
    plot_cat_ph(x_list_p_h, y_list_p_h)
    box_plot_level_ph(p_h_list)

    ## Part 3: Analysis of level 3-4, Belonging-Esteem by World Happiness and freedom dataset

    freedom = Data.get_freedom()
    df_free_data = pd.concat([freedom['year'], freedom['countries'], freedom['hf_score']], axis=1)
    df_free_data.columns = ['Year', 'Country', 'Human_Freedom_Score']

    x_list_h_f, y_list_h_f, h_f_list = analysis_happiness_Freedom_level(happiness, df_free_data)
    plot_level_h_f(x_list_h_f, y_list_h_f)
    plot_cat_hf(x_list_h_f, y_list_h_f)
    box_plot_level_hf(h_f_list)

    ## Part 4: Analysis of level 2-4, Safety-Esteem by peace and freedom dataset

    x_list_level24, y_list_level24, level24_list = analysis_two_fourth_level(peace_data, df_free_data)
    level24_list[0].head(20)

    plot_level_24(x_list_level24, y_list_level24)
    plot_cat24(x_list_level24, y_list_level24)
    box_plot_level24(level24_list)

    ## Part 5: Analysis of level 4-5, Esteem-Self Actualization by freedom and innovation dataset

    free_list = prep_freedom()
    inno_list = prep_innovation()
    x_list_45, y_list_45, level_45_list = analysis_level45(inno_list, free_list)

    plot45(x_list_45, y_list_45)
    plot45_cat(x_list_45, y_list_45)
    level_45_list[0].head(20)
    box_plot_45(level_45_list)

    ## Part 6: Analysis of level 1-4, Belonging-Esteem by hunger + freedom index dataset

    x_list_14, y_list_14, level14_list = analysis_first_fourth_level(hunger_data, df_free_data)
    plot_14(x_list_14, y_list_14)
    plot_cat_level14(x_list_14, y_list_14)
    box_plot_level14(level14_list)

    ## Part 7: Analysis of level 1-5, Physiological-Esteem by hunger + Innovation index dataset

    x_list_15, y_list_15, level_15_list = analysis_level15(hunger_data, inno_list)
    plot_15(x_list_15, y_list_15)
    plot_cat_level14(x_list_15, y_list_15)
    box_plot_level15(level_15_list)

    print("Result: As for result, we find that Maslow is right, and his model of Maslow's hierarchy of \
    needs, or the so-called Maslow pyramid, can apply to almost all the countries in the world. According\
     to our finding, the relationship between any lower levels and its relative higer levels satisfies our\
      proposed model. For each level, we firstly cleaned both datasets from lower level and higher level,\
       which implys the work of getting rid of Nan values and changing the corresponding name of countires.\
        Then, we ploted the corresponding relationship betwwen higher level and lower level for all the country. \
        However, from this plot, we can not see the trend or check if all kinds of countries satisfy this relationship. \
        So, we categorized the lower level needs in different ranges. By using this way, we can smooth the relationship \
        and see the corresponding trend more clearly. After we've done with this process, we'll check if the\
         relationship we got can fit the model we proposed or not. Moreover, if the trend of this data plot \
         is not clear and didn't change a lot, we would go back and check if the dataset we used has deficiency \
         and substitute with other datasets. The last step of analysis in each step is to check if the results we \
         got suits for all the kinds of countries, like poor ones, developing ones and developed ondes. So we plotted\
          the corresponding box plot to show the statistics information of corresponding datasets and check if there \
          are any outliers or if the data of each category is highly skewed. However, due to the fact that the total \
          countries' amount is not that huge, so for some categories in some analysis level, the data can be highly \
          skewed, or have outlier, or even just one or two data points. Still we tend to believe that this whole trend \
          and the model we get basically satisifies all the countries in the world. From our final project, we think \
          Maslow's hierarchy of needs is still valid nowadays, especially when the level of hierarchy goes to a higher \
          level. For example, the relationship between Innovation(Level 5) and hunger(Level 1) or Freedom(Level 4) are \
          both in a perfect shape of relation and fit our proposed model perfectly.")

finish_it()
