# Customer Experience & Operational Risk Analysis
import pandas as pd
import numpy as py
import matplotlib.pyplot as plt

# 1. LOAD DATA & QUICK PREVIEW
flights=pd.read_excel('Airline_Operations_Analytics_Dataset.xlsx',sheet_name=print("\n Data preview \n", flights.head()))

flights['route'] = flights['source_city'] + ' → ' + flights['destination_city']
flights['total_delay'] = flights['arrival_delay'] + flights['departure_delay']
flights['total_revenue'] = flights['passengers'] * flights['ticket_price']
flights['occupancy_rate'] = (flights['passengers'] * 100.0) / flights['capacity']
flights['revenue_per_seat'] = flights['total_revenue'] / flights['capacity']
flights['fuel_efficiency'] = flights['total_revenue'] / flights['fuel_cost']

flights['is_cancelled']=flights['flight_status']=='Cancelled'

# UNIFIED AGGREGATION & ROUTE METRICS
route_analysis=flights.groupby('route').agg(
  Total_flights=('flightid','count')
  Total_Cancellations=('is_cancelled', 'sum'),
  Average_Occupancy_Rate=('occupancy_rate', 'mean'),
  Average_Passengers=('passengers', 'mean'),
  Average_Capacity=('capacity', 'mean'),
  Total_Revenue=('total_revenue', 'sum'),
  Average_Revenue_Per_Seat=('revenue_per_seat', 'mean'),
  Average_Fuel_Efficiency=('fuel_efficiency', 'mean')).reset_index()

# Calculate cancellation rate directly on aggregated numbers
route_analysis['Cancellation_rate']=route_analysis['Total_cancellations']*100.0/route_analysis['Total_flights']

# SCALED CUSTOMER EXPERIENCE SCORE
def min_max_scale(series):
  if series.max()== series.min():
    return 0.0
  return(series - series(min))/(series.max()-series.min())

norm_occupancy=min_max_series(route_analysis[' Average_Occupancy_Rate'])
norm_fuel = min_max_scale(route_analysis['Average_Fuel_Efficiency'])
norm_rev_seat = min_max_scale(route_analysis['Average_Revenue_Per_Seat'])
norm_delay = min_max_scale(route_analysis['Average_Total_Delay'])
norm_cancel = min_max_scale(route_analysis['Cancellation_Rate'])

route_analysis['Customer_Experience_Score']=((norm_occupancy*0.3)+(norm_fuel * 0.40) + (norm_rev_seat * 0.30) -  (norm_delay * 0.25) - (norm_cancel * 0.35))
route_analysis['Risk_category']=pd.qcut(route_analysis['Customer_Experience_Score'],q=[0, 0.33, 0.66, 1.0], labels=['High Risk', 'Moderate Risk', 'Low Risk'])

route_analysis=route_analysis.sort_values(by='Customer_Experience_Score', ascending= False)
top10=route_analysis.head(10)
worst10=route_analysis.tail(10)

pivot_summary = route_analysis.pivot_table(values=['Customer_Experience_Score', 'Average_Total_Delay', 'Cancellation_Rate'],
                                           index='Risk_category',
                                           aggfunc='mean')
print("\n Pivot summary: \n", pivot_summary )
correlation = route_analysis[['Average_Total_Delay', 'Cancellation_Rate', 'Average_Occupancy_Rate', 'Total_Revenue', 'Customer_Experience_Score']].corr()
print("\n Pivot summary: \n", pivot_summary )

# VISUALIZATIONS
# Plot 1: Top Routes
plt.figure(figsize=(12,6))
plt.bar(top10['route'], top_routes['Customer_Experience_Score'])
plt.title('Top Airline Routes by Customer Experience')
plt.xlabel('Route')
plt.ylabel('Customer Experience Score')
plt.xticks(rotation=75)
plt.savefig("top_customer_routes.png", bbox_inches='tight')
plt.close()


# Plot 2: Worst Routes
plt.figure(figsize=(12, 6))
plt.barh(worst10['route'], worst_routes['Customer_Experience_Score'])
plt.title('Worst Performing Airline Routes')
plt.xlabel('Customer Experience Score')
plt.ylabel('Route')
plt.savefig("worst_routes.png", bbox_inches='tight')
plt.close()

# Plot 3: Bubble Chart
plt.figure(figsize=(12,6))
plt.scatter( route_analysis['Average_Total_Delay'], route_analysis['Total_Revenue'], s=route_analysis['Average_Occupancy_Rate'] * 5, alpha=0.6)
plt.title('Revenue vs Delay vs Occupancy')
plt.xlabel('Average Total Delay')
plt.ylabel('Total Revenue')
plt.savefig("revenue_delay_occupancy.png", bbox_inches='tight')
plt.close()

# Plot 4: Pie Chart
risk_counts=route_analysis['risk_category'].value_counts()
plt.figure(figsize=(8, 5))
plt.pie(risk_counts.values, labels=risk_counts.index, autopct='%1.1f%%')
plt.title('Operational Risk Distribution')
plt.savefig("risk_distribution.png", bbox_inches='tight')
plt.close()
