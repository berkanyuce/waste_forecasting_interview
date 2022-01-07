# Waste Forecasting

This project is developed for an interview. The data is collected from real service points, anonymised and it’s coming from a real world problem.

There are two datas. location_data_anonym.csv and waste_forecasting_anonym.csv

In location_data_anonym file includes latitude and longitude informations of each service point. In waste_forecasting_anonym file includes
visit date of each service point and these service points' fulness ratio of paper and plastic bins' and finally how many bins are there for plastic and paper. 

Expected me 4 tasks. These are:
1. Impute missing data and prepare daily time series for each service point. (you should remove outliers if you think it’s necessary)
2. Analyse the data and derive insights. (Auto Correlation, Seasonality, Required Visit Intervals for bins, etc.)
3. Use a tool/algorithm of your choice to create forecasting model. (You can aggregate waste generation of all service points into one or you can create forecasting for each service point level. You can try multiple methods/algorithms and compare them, if you would like to, this is not necessary.)
4. Visualise the results of step 2 and 3 using any tool or library you want. You are expected to visually show time series specs (auto correlation, seasonality, daily aggregated waste for each location etc.) and generate heatmaps using locations data.

There is my solution in interview.py
First of all, I looked into the data. I looked for missing values. As expected, there are some missing values in both of data. 
Then I visualized data for question 2 and for understanding data.
I googled what is forecasting in statistics and how can I develop a forecasting model. I found Facebook's (Now they changed their company name to Meta.) Prophet model and I used it for my solution. 

I used Streamlit to make the app work in the browser, Pandas to manipulate the data, Plotly to visualize, Statsmodels to find statistical results, Seaborn to make heatmap and Prophet to make forecasting.
Addition information is included to inside application. The project runs on Streamlit servers. To reach project click this link: https://share.streamlit.io/berkanyuce/waste_forecasting_interview/main/interview.py 
