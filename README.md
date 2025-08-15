# Local Food Wastage Management System

A comprehensive web application built with Streamlit to manage food donations and reduce food wastage by connecting food providers with receivers.

## Features

- **Dashboard**: Overview of key metrics and statistics
- **Food Listings**: Browse and filter available food items
- **Claims Management**: Submit, view, and update food claims
- **Provider Directory**: Contact information for food providers
- **Analytics**: Data visualization and insights
- **SQL Queries**: Execute predefined analytical queries
- **Reports**: Generate wastage and performance reports

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

## Technologies Used

- Python
- Streamlit
- SQLite
- Pandas
- Plotly

## Project Structure

```
├── app.py                 # Main Streamlit application
├── food_waste_management.db # SQLite database
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```
