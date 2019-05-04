# World-living-quality-analysis
# Proposal
### Title:
Make Maslow Great Again ...or not
——A Statistical Methodology/Model/Proof/Falsification of Maslow's Pyramid

### Team members:
Worawich (Win) Chaiyakunapruk,
Phil Zhe Wang, 
Yao Xiao,  

### Summary: 
Maslow's hierarchy of needs, or the so-called Maslow pyramid, is a famous theory when we talk about human being's self-satisfaction. Raised in 1943, the book A Theory of Human Motivation, it describes people's psychological motivation in different developing periods.
However famous, the doubts it received has never been reduced. You will get over 20000 results in google scholar after typing in keywords like "Maslow's hierarchy of needs criticism".
But most of the criticisms are built from the point of Psychology, which makes them not that strong on my opinion.
This time, we will build the hierarchy model with real data, and try to prove if he is right or wrong.
Maslow used to be a great psychologist, but our slogan is:
Make Maslow Great Again! (or not, if possible, because in that situation is most likely to publish a paper)

### Hypotheses: 
1. Maslow's theory is right in all!
2. Maslow's theory is right to some extent!
3. Maslow's theory has a scope: it works for developing contries but not developed contries!

### Datasets:	
- World Happiness Report [https://www.kaggle.com/unsdsn/world-happiness]
- The Human Freedom Index [https://www.kaggle.com/gsutters/the-human-freedom-index]
- UNODC Global Criminal Justice Statistics [https://data.world/unodc/b4aa5785-7a33-4c07-af15-0f15d95a121f] I already registered and download this one.
- Poverty And Equity Database [https://datacatalog.worldbank.org/dataset/poverty-and-equity-database]
- IBRD Statement Of Loans - Historical Data [https://finances.worldbank.org/Loans-and-Credits/IBRD-Statement-Of-Loans-Historical-Data/zucq-nrc3]
- World Integrated Trade Solution Trade Stats [https://datacatalog.worldbank.org/dataset/world-integrated-trade-solution-trade-stats]
- Economic Fitness [https://datacatalog.worldbank.org/dataset/economic-fitness]
- Suicide Rates Overview 1985 to 2016 [https://www.kaggle.com/russellyates88/suicide-rates-overview-1985-to-2016]
- World Bank: Education Data [https://www.kaggle.com/theworldbank/world-bank-intl-education]

### Mapping
- Physiological ——> Hunger/living data
- Safety ——> Criminal data
- Love/belonging ——> Marriage/Children/Family data
- Esteem ——> Position/Class data
- Self-actualization ——> Job satisfaction/Happiness data

# Final Report
## Introduction
![image](https://github.com/winwowin/World-living-quality-analysis/blob/master/images/Pyramid1.PNG)
<Br/>Maslow’s hierarchy of needs is a theory in psychology proposed by Abraham Maslow in his 1943 paper "A Theory of Human Motivation" in Psychological Review. 
Maslow's hierarchy of needs is used to study how humans intrinsically partake in behavioral motivation. Maslow used the terms "physiological", "safety", "belonging and love", "social needs" or "esteem", and "self-actualization" to describe the pattern through which human motivations generally move.
This means that in order for motivation to occur at the next level, each level must be satisfied within the individual themselves.
Although the criticism never stops, the theory has a widespread influence all over the world.
## Aims & Hypothesis
The purpose of our experiment is to validate whether Maslow’s model for the hierarchy of needs makes sense in the real world. In other words, we are exploring if there indeed is a sequence for people to satisfy their needs. For example, do most people really put survival in the first place compared to other needs like respect and freedom.
We are trying to put real data that can represent one or two factors in his pyramid to simulate the conceptual model. So we have to quantify the needs at all levels and try to find their relations.
- Maslow’s pyramids do make sense in the real world
- Maslow’s pyramids have some preconditions to be correct
![image](https://github.com/winwowin/World-living-quality-analysis/blob/master/images/MMGA.PNG)
## Methodology & Modeling
The original hierarchy states that a lower level must be completely satisfied and fulfilled before moving onto a higher pursuit. 
![image](https://github.com/winwowin/World-living-quality-analysis/blob/master/images/model.PNG)
## Abstract Model
Based on the description of Maslow’s original words, we can extract the information to create a logical model like this:
- When lower level needs are not satisfied, higher level needs are zero
- when lower level needs are met, higher level needs start increasing
- The increasing rate of higher level needs should be larger than the lower level needs because people move onto the next level
![image](https://github.com/winwowin/World-living-quality-analysis/blob/master/images/Formula.PNG)
## Dataset Mapping
In order to quantify the psychological concepts in the pyramid, we have to pick data from the real world to represent each level. Since we did not find an accurate description of what exactly each level means, we have to pick the data according to our own understanding and trying to be objective in this process.
![image](https://github.com/winwowin/World-living-quality-analysis/blob/master/images/DataMapping.PNG)

## Plotting Strategies
The most difficult part of our project is to draw the plot that can show the relationship between lower levels and higher levels. The ways of processing the data and smoothing the curve matter a lot. Our early attempt to draw the plot failed because it’s too skewed and the dots are too many to see the relationship. So we decided to take the following strategies to improve it:
- divide the lower level data into 10 categories of the same range
- calculate the mean value of the higher level data that falls into the same range
- plot the data, so that we only get 10 dots, which is clear
![image](https://github.com/winwowin/World-living-quality-analysis/blob/master/images/PlottingStrategies.PNG)
## Results
results:<Br/>
![image](https://github.com/winwowin/World-living-quality-analysis/blob/master/images/results1.PNG)
![image](https://github.com/winwowin/World-living-quality-analysis/blob/master/images/results2.PNG)
![image](https://github.com/winwowin/World-living-quality-analysis/blob/master/images/results-box1.PNG)
![image](https://github.com/winwowin/World-living-quality-analysis/blob/master/images/results-box2.PNG)
<Br/>As for result, we find that Maslow is right, and his model of Maslow's hierarchy of needs, or the so-called Maslow pyramid, can apply to almost all the countries in the world. According to our finding, the relationship between any lower levels and its relative higer levels satisfies our proposed model. For each level, we firstly cleaned both datasets from lower level and higher level, which implys the work of getting rid of Nan values and changing the corresponding name of countires. Then, we ploted the corresponding relationship betwwen higher level and lower level for all the country. However, from this plot, we can not see the trend or check if all kinds of countries satisfy this relationship. So, we categorized the lower level needs in different ranges. By using this way, we can smooth the relationship and see the corresponding trend more clearly. After we've done with this process, we'll check if the relationship we got can fit the model we proposed or not. Moreover, if the trend of this data plot is not clear and didn't change a lot, we would go back and check if the dataset we used has deficiency and substitute with other datasets. The last step of analysis in each step is to check if the results we got suits for all the kinds of countries, like poor ones, developing ones and developed ondes. So we plotted the corresponding box plot to show the statistics information of corresponding datasets and check if there are any outliers or if the data of each category is highly skewed. However, due to the fact that the total countries' amount is not that huge, so for some categories in some analysis level, the data can be highly skewed, or have outlier, or even just one or two data points. Still we tend to believe that this whole trend and the model we get basically satisifies all the countries in the world. From our final project, we think Maslow's hierarchy of needs is still valid nowadays, especially when the level of hierarchy goes to a higher level. For example, the relationship between Innovation(Level 5) and hunger(Level 1) or Freedom(Level 4) are both in a perfect shape of relation and fit our proposed model perfectly.

## Conclusion & Discussion
As we can see from the results of our experiments, most of the results correspond to the expected deduction from the original theory. However, some are different, and we can make some assumptions about the reasons behind the scene.
Take the first plot as an example: it reveals the relationship between hunger and safety. When the undernourishment index value is low, the peace index value is low as well. It means as people going far away from hunger, their environment gets safer too. This is the same as part of the theory. However, things get different when people are not able to fulfill their needs for food. In areas where people suffer hunger, the peace index value goes into two opposing extremes: very safe or very dangerous. It shows us two different hells: people in dangerous areas take all risks trying to get food, while people in safe areas are too hungry to commit any crimes. However different, both pathetic. 
![image](https://github.com/winwowin/World-living-quality-analysis/blob/master/images/Discussion.PNG)
## Future Research
Split the dataset and try to find some scope of the theory. For example, split the data of developed and deloping countries to see their differences.
Modify the dataset to make it more suitable for the level it presents. For example, combine the poverty and undernourishment data to represent the first level need.
Try to do more quantified social science theory analytics with more real-world data.
## Reference
1. McLeod, S. (2007). Maslow's hierarchy of needs. Simply psychology, 1.
2. Kaur, A. (2013). Maslow’s need hierarchy theory: Applications and criticisms. Global Journal of Management and Business Studies, 3(10), 1061-1064.
3. World Happiness Report [https://www.kaggle.com/unsdsn/world-happiness]
4. The Human Freedom Index [https://www.kaggle.com/gsutters/the-human-freedom-index] 
5. Poverty And Equity Database [https://datacatalog.worldbank.org/dataset/poverty-and-equity-database]
6. Global peace index [http://visionofhumanity.org/indexes/global-peace-index/]
7. Hunger and Undernourishment, Max Roser and Hannah Ritchie, [https://ourworldindata.org/hunger-and-undernourishment]
8. Global Innovation Index [https://www.globalinnovationindex.org/analysis-indicator]
9. population by marital status,  Demographic Statistics Database, [http://data.un.org/Data.aspx?d=POP&f=tableCode%3A23]
