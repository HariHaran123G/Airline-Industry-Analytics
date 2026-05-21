import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
flights=pd.read_excel( 'Airline_Operations_Analytics_Dataset.xlsx',sheet_name='Flights')

# Feature engineering

flights['route']=(flights['source_city']+'→'+ flights['destination_city'])
flights['revenue']=(flights['passengers']* flights['ticket_price'])
flights['Total_delay']=(flights['arrival_delay']+flights['departure_delay'])
flights['fuel_efficiency']=(flights['revenue']/flights['fuel_cost']
flights['revenue_per_passenger']=(flights['revenue']/flights['passengers'])

# Route analysis
route_analysis=flights.groupby('route').agg(
  Total_flights=('flight_id', 'count'),
  Total_passengers=('passengers','sum'),
    Total_revenue=('revenue','sum')
  Average_delay=('Total_delay','mean')
Average_fuel_efficiency=('fuel_efficiency','mean')
Average_revenue_per_passenger=('revenue_per_passenger','mean')).reset_index()

# ROUTE PERFORMANCE SCORE
route_analysis['Route_analysis_score']=(
  route_analysis['Average_Fuel_Efficiency'] * 10 +route_analysis['Revenue_Per_Passenger']  / 100  - route_analysis['Average_Total_Delay'])
route_analysis= route_analysis.sort_values(by='Route_analysis_score',ascending=False)

# DISPLAY RESULTS

print("\n ROUTE PERFORMANCE ANALYSIS \n")
print(route_analysis)

best_route=route_analysis.iloc[0]
print("\n BEST PERFORMING ROUTE \n")
print(
  f"{best_route['route']}"
  f"has the best operational-business performance "
   f"with score of "
    f"{best_route['Route_Performance_Score']:.2f}")


# TOP 10 ROUTES
top_routes = route_analysis.head(10)
print("\n TOP 10 ROUTES \n")
print(top_routes)

# VISUALIZATION 1
# TOP ROUTE PERFORMANCE
plt.figure=(figsize=(12,6))
plt.bar(top_routes['route'],top_routes['Route_analysis_score'])
plt.xlabel('Route')
plt.ylabel('Route Performance Score')
plt.xticks(rotation=75)
plt.show()

# VISUALIZATION 2
# REVENUE VS DELAY
plt.figure(figsize=(10,6))
plt.scatter(
    route_analysis['Average_Total_Delay'],
    route_analysis['Total_Revenue'])
plt.title('Route Revenue vs Delay')
plt.xlabel('Average Total Delay')
plt.ylabel('Total Revenue')
plt.show()

# VISUALIZATION 3
# PASSENGERS VS REVENUE
plt.figure(figsize=(10,6))
plt.scatter(route_analysis['Total_Passengers'], route_analysis['Total_Revenue'])
plt.title( 'Passenger Volume vs Revenue')
plt.xlabel('Total Passengers')
plt.ylabel('Total Revenue')
plt.show()

# CORRELATION ANALYSIS
correlation=route.analysis[['Total_Passengers','Total_Revenue','Average_Total_Delay', 'Average_Fuel_Efficiency','Revenue_Per_Passenger']].corr()
print("\n Correlation matrix \n")
print(correlation)



                               
