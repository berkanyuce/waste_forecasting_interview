#Dependencies
    # Streamlit (pip install streamlit)
    # Pandas
    # Plotly (pip install plotly==5.4.0)
    # Statsmodels (pip install statsmodels)
    # fbprophet (install -c conda-forge prophet.)
    # Seaborn
    
import streamlit as st #Streamlit is a library for developing ML projects on the web.
                        #open terminal to run code and write it:
                            # %streamlit run /code_location/interview.py
import pandas as pd
st.set_option('deprecation.showPyplotGlobalUse', False) #Use PyPlot on Streamlit

def general_visualizations(df):    
    #Distirbution Graph
    import plotly.figure_factory as ff
    st.subheader('Distirbution Graph')
    
    value_data = [df['% Paper'], df['% Plastic']] #X axis
    type_labels = ['Paper', 'Plastic'] #Y axes
    fig = ff.create_distplot(value_data, type_labels, bin_size=.1)
    st.plotly_chart(fig)
    
    #Violin Graph
    import plotly.graph_objects as go
    st.subheader('Violin Graph')

    fig = go.Figure()
    fig.add_trace(go.Violin(y=df['% Paper'],
                            x=df['SPID'],
                            legendgroup='Paper', scalegroup='Plastic', name='Paper',
                            side='negative',
                            line_color='blue')
                 )
    fig.add_trace(go.Violin(y=df['% Plastic'],
                            x=df['SPID'],
                            legendgroup='Plastic', scalegroup='Paper', name='Plastic',
                            side='positive',
                            line_color='orange')
                 )
    fig.update_traces(meanline_visible=True) #Show meanline graph inside the violin.
    fig.update_layout(violingap=0.5, violinmode='overlay') #Violin's layout.
    st.plotly_chart(fig)
 
    #Average Fullnes by Month
    import plotly.express as px

    st.subheader('Average Fullnes by Month')
    
    df['% Total'] = df['% Paper'] + df['% Plastic'] #Set total percentage of both of wastes.
    df =df.groupby(['year','month']).mean() #Group the df by firstly year and then month.
                                            #Take mean for line chart.
    df = df.reset_index()
    df['VisitDate'] = df['year'].astype(str) +'-'+ df['month'].astype(str)
    fig = px.line(df, x='VisitDate', y=['% Plastic','% Paper', '% Total'])
    st.plotly_chart(fig)

def auto_correlation(df):
    ######Autocorrelation
    from statsmodels.graphics.tsaplots import plot_acf
    
    st.header('Autocorrelation')
        
    df['% Total'] = df['% Paper'] + df['% Plastic']
    df['VisitDate'] = pd.to_datetime(df['VisitDate']) #Convert VisitDate column's type to Datetype.
    df['VisitDay'] = df['VisitDate'].apply(lambda x: x.date()) #Delete hours from VisitDate column.
    df = df.groupby('VisitDay').sum() #Sum total percentage by day.
    
    #Autocorrelation Plot
    st.pyplot(plot_acf(x=df['% Total'], lags=40, title='Daily All Wastes'))

def seasonality(df):
        
    #####Seasonality
    #Sum datas by month.
    df['VisitDate'] = pd.to_datetime(df['VisitDate']) #Convert VisitDate column's type to Datetype.
    df["VisitDate"] = df["VisitDate"].dt.strftime("%Y-%m") #Convert date format to year-month
    df = df.groupby('VisitDate', as_index=False).sum() #Group
    df['% Total'] = df['% Paper'] + df['% Plastic']
    
    from statsmodels.tsa.seasonal import seasonal_decompose
    
    df_seasonality = df[['VisitDate','% Total']].copy() #Working only date and total percentage columns.
    df_seasonality['VisitDate'] = pd.to_datetime(df_seasonality['VisitDate']) #Convert column data type to datetime.
    df_seasonality = df_seasonality.set_index('VisitDate') 
    
    decompose_result_mult = seasonal_decompose(df_seasonality, model="multiplicative", period=int(len(df_seasonality)/2))
    
    st.pyplot(decompose_result_mult.plot())

def forecasting(df):
        
    #Forecasting - Prophet
    from fbprophet import Prophet
    df['% Total'] = df['% Paper'] + df['% Plastic'] #Set total percentage of both of wastes.
    df['VisitDay'] = df['VisitDate'].apply(lambda x: x.date()) #Delete hours from VisitDate column.

    df = df.loc[:, ["VisitDay", "% Total"]] #Select all rows of visitday and % total columns.
    df['VisitDay'] = pd.DatetimeIndex(df['VisitDay']) #Convert datatype to datetime
    
    df = df.rename(columns={'VisitDay': 'ds', 
                            '% Total': 'y'}) #Prepare df for create Prophet model.
    my_model = Prophet()
    my_model.fit(df)
    
    future_dates = my_model.make_future_dataframe(periods=365) #Selecting model's future predict period.
    forecast =my_model.predict(future_dates)
   
    st.pyplot(my_model.plot(forecast))
    st.pyplot(my_model.plot_components(forecast))

def heatmap_viz(waste_forecasting,location):
    import seaborn as sns

    df = pd.merge(waste_forecasting,location, how='inner') #Join two csv file in same SPID
    df['SP_total'] = df['% Paper'] * df['# Paper'] + df['% Plastic'] * df['# Plastic'] #Total waste = Number of Bin * Percentage of Fullnes
    df['VisitDate'] = pd.to_datetime(df['VisitDate'],format='%Y-%m-%d') #COnverting dateformat to Year-Month-Day
    df['VisitDay'] = df['VisitDate'].apply(lambda x: x.date()) #Delete hours
    
    df.drop(['% Paper','# Paper','# Plastic','% Plastic','VisitDate'],axis=1,inplace=True) #Delete unnecessery columns
    
    col1, col2 = st.columns(2)
    start_date = col1.date_input('Select Start Date',min(df['VisitDay']) ,min_value=min(df['VisitDay']), max_value=max(df['VisitDay'])) #Take date input from user.
    end_date = col2.date_input('Select End Date', max(df['VisitDay']) ,min_value=min(df['VisitDay']), max_value=max(df['VisitDay']))

    if start_date > end_date: #Check
        temp = start_date
        start_date = end_date
        end_date = temp
        
    df = df[(df['VisitDay'] < end_date) & (df['VisitDay'] > start_date)] #Select datas between choosed dates
    df.drop('VisitDay', axis=1, inplace=True)
    df_grouped = df.groupby(['Latitude', 'Longitude']).sum() #Group Service Points and sum their wastes.

    st.pyplot(sns.jointplot(x = df['Latitude'], y = df['Longitude'],
              kind = "hex", data = df_grouped))
 
#CSV to dataframe
#Write your own csv file locations
waste_forecasting = pd.read_csv('https://raw.githubusercontent.com/berkanyuce/waste_forecasting_interview/main/waste_forecasting_anonym.csv', index_col=0)
location = pd.read_csv('https://raw.githubusercontent.com/berkanyuce/waste_forecasting_interview/main/location_data_anonym.csv', index_col=0)

#User chooses analyze type
analyze_type = st.sidebar.selectbox('Select Analyze Type', ["Single Service Point", "Service Points' Heatmap", "Project Process and Opinions"])

if analyze_type == 'Single Service Point':
    #Get all service points that are included in both datasets.
    data = pd.merge(waste_forecasting,location,on='SPID',how='inner')
    
    #Deleting service points with id 15184 and 16193. They don't have enough data.
    spid_list = data['SPID'].unique()
    spid_list.sort()
    spid_list = spid_list[(spid_list != 15184) & (spid_list != 16193)]
    
    #User chooses Service Point ID
    sp_id_selected = st.sidebar.selectbox('Select Service Point ID', spid_list)
    
    #Group service points by their SPID.
    #Seperate date by day,month,year. It will used for visualizations.
    sp = pd.merge(waste_forecasting,location,on='SPID',how='left')
    sp = waste_forecasting.groupby('SPID')
    sp_selected = sp.get_group(sp_id_selected)
    sp_selected['VisitDate'] = pd.to_datetime(sp_selected['VisitDate'],format='%Y-%m-%d')
    sp_selected['year']= sp_selected['VisitDate'].dt.year
    sp_selected['month']= sp_selected['VisitDate'].dt.month
    sp_selected['day']= sp_selected['VisitDate'].dt.day
    
    #Seperate wastes by paper and plastic ;) 
    #Choose their fullnes by date
    paper = sp_selected[['SPID','VisitDate', '% Paper','year','month','day']]
    plastic = sp_selected[['SPID','VisitDate', '% Plastic','year','month','day']]
    df = pd.merge(plastic, paper, how='inner')

    sp_id_selected = st.sidebar.selectbox('Select Visualization', ['General Visualizations','Autocorrelation', 'Seasonality', 'Forecasting'])
    if sp_id_selected == 'General Visualizations':
        general_visualizations(df)
    elif sp_id_selected == 'Autocorrelation':
        auto_correlation(df)
    elif sp_id_selected == 'Seasonality': 
        seasonality(df)
    else:
        forecasting(df)
elif analyze_type == "Service Points' Heatmap":
    heatmap_viz(waste_forecasting,location)
else:
    '''
    ### Project Process
    Firstly, I loaded csv files. I grouped all service point by their id. Then, I looked inside the groups by using this code: \n
              for key, item in sp:
                  print(sp.get_group(key))
                  
    I realize missing datas. The service point which id's is **15769**. There is one record about this service point. 
    But there is no any location data in our location.csv. However, I did nothing to this record. \n
    
    When comparing locations and wastes records, there is a service point with id **10222** in location data. 
    However, there is no data on this service point in wastes data.
    That's why I used a join to avoid this problem. \n
    
    Two service points with id **15184** and **16193**. They don't have enough data for analyze. So I discard these service points.\n
    
    After the manupulation, I started to visualazing. \n
    
    When I look at some service points' visualizations, the percentage of wastes is increasing by the month.
    It means, we need more bins for these service points. \n
    
    I understand that the waste collection rates of service points increase and decrease on different days and months.
    It means, we need to a specific approach to the waste collection problem. For example, we chan choose different route for spring and autumn.        
    '''