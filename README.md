# 'Put your money where your mouth (Twitter) is'

The objective of this project to showcase any correlations between Twitter activity of Donald Trump and Hillary Clinton with the stock market and the 2016 Presidential elections polls.
![image](https://user-images.githubusercontent.com/76560772/159755218-b4f67c81-1d9a-488e-b149-cf3bb29a617f.png)
![image](https://user-images.githubusercontent.com/76560772/159755306-c880c63f-e1e1-4ef7-83ae-0164f880e1b6.png)

In order to achieve such analysis, multiple data sources were used - these are in the respective files explained below. 


- Yahoo Finance Web Scrapping using Selenium
- Donald Trump Tweets CSV obtained from Kaggle
- Hilary Trump Tweets CSV obtained from Kaggle
- Election polls CSV obtained from Kaggle
- Companies and their ticker JSON obtained from SEC.gov website
- Indexes, Commodities and Crypto CSV manually inputted

The initial step was the cleaning of the data can be found in the cleaning folder of the document:
- Clinton_Cleaning
- Companies_json_cleaning
- Trump_Tweets_CVS_cleaning
- Presi_Polls_Cleaning
- Join_CSV_cleaning

The Scrapping of the Yahoo Finance is in the Notebook folder. 

Preparing the data for analysis - The data after being obtained from different sources, the cleaning was followed the respective objectives:

- Tweets files - Produce a sum() per day for the cumulative count for Tweets. We need to bring all into a "day" in order to compare with stock market. 
- Presidential polls - the weight of the individual poll was averaged per day and an overall index was given calculated by the (weight of the poll * number of voters)
- Stock market scrapping - make sure the table rows are by day and eliminating where the stock has paid dividends / split stock. 
- Create an 'election' analysis by extracting the tweets where Clinton has no input, in order to compare both candidates fairly. 

Functions - the functions are located under the src folder. Main functions found:
- Scrapping
- Scrapping file cleaning 
- Clean of JSON company ticker file
- Visualization

Notebook and Analysis file:

Analysis 1 file consists of the union of the different databases ready for analysis.
For the purposes of the excersize, the S&P 500 Index has been chosen. 
Initial conclusions for the election tweets:

- Donald Trump on July 2016 showcases a significant lower tweet count than Clinton:
![image](https://user-images.githubusercontent.com/76560772/159754586-3177b175-453b-4579-8a85-dff9798bfd29.png)

- However, his engagement with the people, measured by Retweets, is higher:
![image](https://user-images.githubusercontent.com/76560772/159754702-4105c3a7-d66b-4b20-a699-42405fbf31bc.png)

- Which led me to think if there is a correlation between the S&P 500 avg price per month and Trump´s retweet - and there is: 
![image](https://user-images.githubusercontent.com/76560772/159754836-555d8d6e-5d49-4f49-9fbb-e2d2b4807558.png)

- BUT, when the volume of the stock decreases, is where Trump has the most influence, or retweets. is his mouth scaring people away? specially in July 2016. 
![image](https://user-images.githubusercontent.com/76560772/159784194-0973e312-8964-45a9-8dd9-fd18ce4cc942.png)

The intention is to carry over the analysis to the second project to nurture the visualizations and hypothesis analysis. 


BONUS - USER Interaction Scrapping. 

The user will have the opportunity to input the desired stock to analyze, and automatically using the functions, the file will be ready for analysis with the other variables. 

![image](https://user-images.githubusercontent.com/76560772/159755085-1cd89928-e701-43b4-9865-a8d66587777f.png)




