import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# LOAD DATA
# =========================================================

flights = pd.read_excel(
    'Airline_Operations_Analytics_Dataset.xlsx',
    sheet_name='Flights'
)

# =========================================================
# FEATURE ENGINEERING
# =========================================================

flights['route'] = (

    flights['source_city']
    + ' → ' +
    flights['destination_city']

)

# TOTAL DELAY
flights['total_delay'] = (

    flights['arrival_delay']
    + flights['departure_delay']

)

# TOTAL REVENUE
flights['total_revenue'] = (

    flights['passengers']
    * flights['ticket_price']

)

# OCCUPANCY RATE
flights['occupancy_rate'] = (

    flights['passengers']
    * 100.0
    / flights['capacity']

)

# REVENUE PER PASSENGER
flights['revenue_per_passenger'] = (

    flights['total_revenue']
    / flights['passengers']

)

# FUEL EFFICIENCY
flights['fuel_efficiency'] = (

    flights['total_revenue']
    / flights['fuel_cost']

)

# =========================================================
# ROUTE STRATEGIC ANALYSIS
# =========================================================

route_analysis = flights.groupby('route').agg(

    Total_Flights = ('flight_id', 'count'),

    Total_Passengers = ('passengers', 'sum'),

    Total_Revenue = ('total_revenue', 'sum'),

    Average_Delay = ('total_delay', 'mean'),

    Average_Occupancy = ('occupancy_rate', 'mean'),

    Average_Fuel_Efficiency = (
        'fuel_efficiency',
        'mean'
    ),

    Revenue_Per_Passenger = (
        'revenue_per_passenger',
        'mean'
    ),

    Cancelled_Flights = (
        'flight_status',
        lambda x: (x == 'Cancelled').sum()
    )

).reset_index()

# =========================================================
# CANCELLATION RATE
# =========================================================

route_analysis['Cancellation_Rate'] = (

    route_analysis['Cancelled_Flights']
    * 100.0
    / route_analysis['Total_Flights']

)

# =========================================================
# NORMALIZED BUSINESS SCORES
# =========================================================

# DEMAND SCORE
route_analysis['Demand_Score'] = (

    route_analysis['Total_Passengers']
    * 100
    / route_analysis['Total_Passengers'].max()

)

# PROFITABILITY SCORE
route_analysis['Profitability_Score'] = (

    route_analysis['Total_Revenue']
    * 100
    / route_analysis['Total_Revenue'].max()

)

# OPERATIONAL SCORE
route_analysis['Operational_Score'] = (

    100
    -
    route_analysis['Average_Delay']

)

# CUSTOMER EXPERIENCE SCORE
route_analysis['Customer_Experience_Score'] = (

    route_analysis['Average_Occupancy']
    -
    route_analysis['Cancellation_Rate']
    -
    (route_analysis['Average_Delay'] / 2)

)

# =========================================================
# FINAL STRATEGIC SCORE
# =========================================================

route_analysis['Strategic_Route_Score'] = (

    route_analysis['Demand_Score'] * 0.30

    +

    route_analysis['Profitability_Score'] * 0.30

    +

    route_analysis['Operational_Score'] * 0.20

    +

    route_analysis['Customer_Experience_Score'] * 0.20

)

# =========================================================
# STRATEGIC RECOMMENDATION ENGINE
# =========================================================

conditions = [

    (
        route_analysis['Strategic_Route_Score'] >= 85
    ),

    (
        route_analysis['Strategic_Route_Score']
        .between(70,84)
    ),

    (
        route_analysis['Strategic_Route_Score']
        .between(55,69)
    ),

    (
        route_analysis['Strategic_Route_Score'] < 55
    )

]

recommendations = [

    'Expand Route',

    'Maintain Route',

    'Improve Operations',

    'Consider Discontinuing'

]

route_analysis['Strategic_Recommendation'] = (

    np.select(
        conditions,
        recommendations,
        default='Unknown'
    )

)

# =========================================================
# RANKING
# =========================================================

route_analysis = route_analysis.sort_values(

    by='Strategic_Route_Score',

    ascending=False

)

# =========================================================
# DISPLAY RESULTS
# =========================================================

print("\n STRATEGIC ROUTE OPTIMIZATION ANALYSIS \n")

print(route_analysis)

# =========================================================
# TOP STRATEGIC ROUTES
# =========================================================

top_routes = route_analysis.head(10)

print("\n TOP STRATEGIC ROUTES \n")

print(top_routes)

# =========================================================
# WORST ROUTES
# =========================================================

worst_routes = route_analysis.tail(10)

print("\n LOWEST STRATEGIC ROUTES \n")

print(worst_routes)

# =========================================================
# RECOMMENDATION DISTRIBUTION
# =========================================================

recommendation_summary = (

    route_analysis[
        'Strategic_Recommendation'
    ].value_counts()

)

print("\n STRATEGIC DISTRIBUTION \n")

print(recommendation_summary)

# =========================================================
# CORRELATION ANALYSIS
# =========================================================

correlation = route_analysis[[

    'Demand_Score',

    'Profitability_Score',

    'Operational_Score',

    'Customer_Experience_Score',

    'Strategic_Route_Score'

]].corr()

print("\n CORRELATION MATRIX \n")

print(correlation)

# =========================================================
# VISUALIZATION 1
# TOP STRATEGIC ROUTES
# =========================================================

plt.figure(figsize=(12,6))

plt.bar(

    top_routes['route'],

    top_routes['Strategic_Route_Score']

)

plt.title('Top Strategic Airline Routes')

plt.xlabel('Route')

plt.ylabel('Strategic Route Score')

plt.xticks(rotation=75)

plt.savefig(
    "top_strategic_routes.png",
    bbox_inches='tight'
)

plt.show()

# =========================================================
# VISUALIZATION 2
# RECOMMENDATION DISTRIBUTION
# =========================================================

plt.figure(figsize=(8,5))

plt.pie(

    recommendation_summary.values,

    labels=recommendation_summary.index,

    autopct='%1.1f%%'

)

plt.title('Strategic Recommendation Distribution')

plt.savefig(
    "strategic_distribution.png",
    bbox_inches='tight'
)

plt.show()

# =========================================================
# VISUALIZATION 3
# BUBBLE CHART
# =========================================================

plt.figure(figsize=(10,6))

plt.scatter(

    route_analysis['Average_Delay'],

    route_analysis['Total_Revenue'],

    s = route_analysis['Total_Passengers'] / 50

)

plt.title(
    'Revenue vs Delay vs Passenger Demand'
)

plt.xlabel('Average Delay')

plt.ylabel('Total Revenue')

plt.savefig(
    "strategic_bubble_chart.png",
    bbox_inches='tight'
)

plt.show()

# =========================================================
# VISUALIZATION 4
# STRATEGIC SCORE DISTRIBUTION
# =========================================================

plt.figure(figsize=(10,6))

plt.hist(
    route_analysis['Strategic_Route_Score'],
    bins=10
)

plt.title('Strategic Route Score Distribution')

plt.xlabel('Strategic Score')

plt.ylabel('Number of Routes')

plt.savefig(
    "strategic_score_distribution.png",
    bbox_inches='tight'
)

plt.show()

# =========================================================
# FINAL EXECUTIVE INSIGHTS
# =========================================================

best_route = route_analysis.iloc[0]

worst_route = route_analysis.iloc[-1]

print("\n FINAL EXECUTIVE INSIGHTS \n")

print(
    f"1. Best strategic route is "
    f"{best_route['route']} "
    f"with score "
    f"{best_route['Strategic_Route_Score']:.2f}"
)

print(
    f"2. Weakest route is "
    f"{worst_route['route']} "
    f"with score "
    f"{worst_route['Strategic_Route_Score']:.2f}"
)

print(
    "3. Routes with high passenger demand "
    "and lower delays consistently "
    "perform better strategically."
)

print(
    "4. Some routes generate high revenue "
    "but suffer operational instability."
)

print(
    "5. Strategic route optimization helps "
    "management prioritize network expansion."
)
