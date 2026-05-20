# weather impact analysis
# Load data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

flights=pd.read_excel('Airline_Operations_Analytics_Dataset.xlsx',sheet_name='Flights')
flights['Total_delay']=(flights['arrival_delay']+flights['departure_delay'])
flights['cancelled']=np.where(flights['cancellation_status']=='Yes',1,0)
flights['estimated_revenue']=(flights['passengers']*flights['ticket_price'])

# WEATHER LEVEL ANALYSIS
weather_analysis=flights.groupby('weather_condition').agg(
  Total_flights=('flight_id','count'),
  Average_departure_delay=('departure_delay','mean'),
  Average_arrival_delay=('arrival_delay','mean'),
  Average_total_delay=('Total_delay','mean'),
  cancellation_count=('Cancelled','sum'),
  Total_passengers=('passengers','sum'),
  Estimated_revenue=('estimated_revenue','sum')).reset_index()

weather_analysis['cancellation_rate%']=(weather_analysis['cancellation_count']*100.0/weather_analysis['Total_flights'])

# Weather disruption score
weather_analysis['Weather_disruption_score']=(weather_analysis['cancellation_rate%']+weather_analysis['Average_total_delay'])
weather_analysis=weather_analysis.sort_values(by='Weather_disruption_score',ascending= False)

#Display results
print("\n Weather impact analysis \n")
print(weather_analysis)

# Most disruptive weather
worst_weather=weather_analysis.iloc[0]
print("\n Most disruptive weather is \n")
print( f"{worst_weather['weather_condition']}"
        f" causes the worst weather disruption"
        f" with score of"
        f"{weather_analysis['Weather_disruption_score']:.2f}"
# Visualisation 1
plt.figure(figsize=(12,6))
plt.bar(weather_analysis['weather_condition'],weather_analysis['Average_total_delay'])
plt.title( 'Average Flight Delay by Weather Condition')
plt.xlabel('Weather Condition')
plt.ylabel('Average Total Delay')
plt.show()

# VISUALIZATION 2
# CANCELLATION RATE ANALYSIS
plt.figure(figsize=(12,6))
plt.plot(weather_analysis['weather_condition'], weather_analysis['Cancellation_Rate_%'], marker='o')
plt.title('Cancellation Rate by Weather Condition')
plt.xlabel('Weather Condition')
plt.ylabel('Cancellation Rate %')
plt.grid(True)
plt.show()

# VISUALIZATION 3
# PASSENGER IMPACT ANALYSIS
plt.figure(figsize=(10,6))
plt.scatter(weather_analysis['Average_Total_Delay'], weather_analysis['Total_Passengers'])
for i in range(len(weather_analysis)):
    plt.text( weather_analysis['Average_total_delay'].iloc[i],weather_analysis['Total_passengers'].iloc[i],
        weather_analysis['weather_condition'].iloc[i])
plt.title('Passenger Impact vs Flight Delay')
plt.xlabel('Average Total Delay')
plt.ylabel('Affected Passengers')
plt.show()

# CORRELATION ANALYSIS
correlation= flights[[
    'departure_delay',
    'arrival_delay',
    'passengers',
    'fuel_cost',
    'flight_duration']].corr()
print("\n CORRELATION MATRIX \n")
print(correlation)




      
