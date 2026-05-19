import pandas as pd
import numpy as py
import matplotlib.pyplot as plt

flights=pd.read_excel(Data/'Airline_Operations_Analytics_Dataset.xlsx',sheet_name='Flights')
print("\n Sample data: \n")
print(flights.head())
print("\n Data information: \n")
print(flights.info())
print("\n Statistical info\n")
print(flights.describe())

#Revenue per flight
flights['revenue']=(flights['passengers']*flights['ticket_price'])-flights['fuel_cost']
flights['fuel_efficiency']=(flights['revenue']/flights['fuel_cost'])
flights['total_delay']=(flights['departure_delay']+flights['arrival_delay'])
flights['cancelled']=np.where(flights['cancellation_status']=='Yes',1,0)

#Airline level analysis
airline_analysis=flights.groupby('airline').agg(
Total_flights =('flight_id','count'),
Total_passengers=('passengers','sum'),
Average_departure_delay=('departure_delay','mean'),
Average_Arrival_Delay = ('arrival_delay', 'mean'),
Average_Total_Delay = ('total_delay','mean'),
Total_revenue=('revenue','sum'),
Average_fuel_effiency=('fuel_efficiency','mean'),
cancellation_count=('cancelled','sum')).reset_index()

# Cancellation rate
airline_analysis['cancellation_%']= (airline_analysis['cancellation_count']*100.0/airline_analysis['Total_flights'])

# operational efficiency score
airline_analysis['Efficiency_score']=(airline_analysis['Average_Fuel_Efficiency']*10- airline_analysis['Average_Total_Delay'] -airline_analysis['cancellation_%'])

#Rank best airlines
airline_analysis = airline_analysis.sort_values(by='Efficiency_score',ascending = False)
print("\n Ranking best airlines in terms of operational efficiency:\n")
print(airline_analysis)

top_airline=airline_analysis.iloc[0]
print("\n BEST OPERATING AIRLINE \n")
print(
  f"{top_airline['airline']}"
f" with operational efficiency score of "
f"{top_airline['Efficiency_score']:.2f}" )

# Visualisation 1:
# Operational score comparison
plt.figure(figsize=(12,6))
plt.bar(airline_analysis['airline'], airline_analysis['Operational_Efficiency_Score'])
plt.title('Airline Operational Efficiency Comparison')
plt.xlabel('Airlines')
plt.ylabel('Operational_Efficiency_Score')
plt.xticks(rotation=45)
plt.show()

# VISUALIZATION 2
# DELAY COMPARISON
plt.figure(figsize=(12,6))
plt.plot(airline_analysis['airline'], airline_analysis['Average_Departure_Delay'], marker ='o', label='Departure delay')
plt.plot(airline_analysis['airline'], airline_analysis['Average_Arrival_Delay'], marker ='o', label='Arrival delay')
plt.title('Average Flight Delays by Airline')
plt.xlabel('Airlines')
plt.ylabel('Delay (Minutes)')
plt.legend()
plt.grid(True)
plt.show()

# VISUALIZATION 3
# REVENUE VS DELAY
plt.figure(figsize=(10,6))
plt.scatter(airline_analysis['Average_Total_Delay'],airline_analysis['Total_Revenue'])
for i in range(len(airline_analysis)):
  plt.text(airline_analysis['Average_Total_Delay'].iloc[i], airline_analysis['Total_Revenue'].iloc[i], airline_analysis['airline'].iloc[i])
plt.title('Revenue vs Average Delay')
plt.xlabel('Average Total Delay')
plt.ylabel('Total Revenue')
plt.show()






















