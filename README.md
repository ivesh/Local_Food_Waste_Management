# Local Food Wastage Management System

## Project Overview

### Problem Statement
Food wastage is a critical social and environmental problem where surplus food from restaurants, hotels, and other establishments ends up being discarded while many individuals and communities suffer from food insecurity. This project addresses this challenge by building a comprehensive Local Food Wastage Management System. It facilitates the efficient redistribution of excess food from providers like hotels, resorts, and apartments to NGOs and individuals in need, thereby reducing wastage and promoting social good.

The system empowers food providers and receivers with real-time tracking, geographical filtering, claim management, and insightful data analysis. This solution is vital to businesses in the hospitality industry wishing to reduce environmental footprint, contribute to social welfare, and optimize their operational efficiency regarding food surplus management.

---

## Dataset Description

The system utilizes four key datasets representing the ecosystem participants and transactions:

- **Providers Dataset (`providers_data.csv`)**
  - Contains information about food providers such as restaurants, grocery stores, supermarkets, hotels, resorts, and apartments.
  - Fields: Provider_ID, Name, Type, Address, City, Contact.

- **Receivers Dataset (`receivers_data.csv`)**
  - Lists individuals and organizations claiming surplus food.
  - Fields: Receiver_ID, Name, Type (NGO, Community Center, Individual), City, Contact.

- **Food Listings Dataset (`food_listings_data.csv`)**
  - Details surplus food items available for claim.
  - Fields: Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location (city), Food_Type (Vegetarian/Non-Vegetarian/Vegan), Meal_Type (Breakfast, Lunch, Dinner, Snacks).

- **Claims Dataset (`claims_data.csv`)**
  - Tracks the claiming of food items by receivers.
  - Fields: Claim_ID, Food_ID, Receiver_ID, Status (Pending, Completed, Canceled), Timestamp.

## Project Structure

```
Local_Food_Waste_Management/
│
├── data/
│ ├── providers_data.csv # Provider information dataset
│ ├── receivers_data.csv # Receiver information dataset
│ ├── food_listings_data.csv # Food surplus details dataset
│ ├── claims_data.csv # Food claim transaction dataset
│
├── food_waste_management.db # SQLite database storing all processed data
│
├── app.py # Streamlit dashboard application for interaction, visualization, and management
├── requirements.txt # Python package dependencies required to run the app
├── README.md # This file - project documentation
└── test.ipynb # Jupyter notebook used for initial data exploration and data cleaning
```

## Technologies Used

- Python
- Streamlit
- SQLite
- Pandas
- Plotly


## Features

- **Dashboard**: Overview of key metrics and statistics
- **Food Listings**: Browse and filter available food items
- **Claims Management**: Submit, view, and update food claims
- **Provider Directory**: Contact information for food providers
- **Analytics**: Data visualization and insights
- **SQL Queries**: Execute predefined analytical queries
- **Reports**: Generate wastage and performance reports

## Streamlit Application Features

The application offers a user-friendly interface with comprehensive functionalities designed for all stakeholders in hospitality and food redistribution:

- **Dashboard Overview**
![alt text](<Screenshot 2025-09-14 162448.png>)
- Key metrics including total providers, receivers, food items, and successful claims.
- Interactive pie charts and bar charts visualizing claim statuses and food listings by city.

- **Food Listings**
![alt text](<Screenshot 2025-09-14 162507.png>)
- Dynamic filtering by city, food type, and meal type.
- View detailed listings with provider contact info for coordination.

- **Claims Management**
![alt text](<Screenshot 2025-09-14 162521.png>)
- Submit new food claims via simple forms.
- Update claim status (Pending, Completed, Cancelled).
- View and manage all existing claims.

- **Provider and Receiver Directory**
![alt text](<Screenshot 2025-09-14 162547.png>)
- Searchable listings categorized by type.
- Easy access to contact information to facilitate coordination.

- **Analytics**
![alt text](<Screenshot 2025-09-14 162602.png>)
![alt text](<Screenshot 2025-09-14 162637.png>)
- Visualizations showing distribution of food types, meal types, wastage statistics, and provider contributions.
- Insights from 15+ SQL analytical queries incorporated directly into the UI.

- **Report Generation**
![alt text](<Screenshot 2025-09-14 162654.png>)
![alt text](<Screenshot 2025-09-14 162704.png>)
- Generate food wastage and provider performance reports with one-click access.

---

## Advantages of Visuals in the Dashboard

- **Real-time Insights**: Stakeholders can monitor live data trends, claim statuses, and food availability helping with proactive decision-making.
- **Geographical Analysis**: City-wise charts pinpoint high-demand and high-wastage areas enabling targeted redistribution efforts.
- **Actionable Metrics**: Metrics like claim success rate, provider contributions, and expiring food warnings empower effective operational management.
- **User Engagement**: Intuitive, interactive visuals enhance user experience, boosting faster coordination between providers and receivers.

---

## Strategic Business Decisions Enabled

- **Waste Reduction**: Hotels and resorts can minimize unnecessary discard by timely listing and tracing surplus food.
- **Cost Optimization**: Reduce costs related to waste disposal and improve food resource management.
- **Social Responsibility**: Demonstrate corporate social responsibility by linking surplus donations directly to needy communities.
- **Operational Efficiency**: Quickly identify and prioritize food donations nearing expiry and allocate resources efficiently.
- **Market Intelligence**: Use data analytics to understand demand patterns, optimize meal preparation, and forecast surplus needs.
- **Reputation Enhancement**: Position your hospitality business as an environmentally and socially committed leader – a strong selling point for guests and investors alike.


## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

## Database Structure

The application uses SQLite database with four main tables:
- **providers**: Food providers information
- **receivers**: Food receivers information  
- **food_listings**: Available food items
- **claims**: Food claim records

## Usage

1. Navigate through different sections using the sidebar
2. Use filters to find specific food items or providers
3. Submit new claims through the Claims Management interface
4. View analytics and generate reports for insights

