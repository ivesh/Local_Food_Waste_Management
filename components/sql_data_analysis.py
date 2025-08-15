# STEP 4: SQL QUERY DEVELOPMENT & ANALYSIS
print("STEP 4: SQL QUERY DEVELOPMENT & ANALYSIS")
print("="*60)

import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('food_waste_management.db')
cursor = conn.cursor()

print("\n🔍 EXECUTING ALL 15 REQUIRED SQL QUERIES")
print("="*60)

# Query 1: How many food providers and receivers are there in each city?
print("\n1. PROVIDERS AND RECEIVERS COUNT BY CITY")
print("-" * 50)

query1_sql = """
SELECT 
    City,
    COUNT(*) as Total_Providers
FROM providers 
GROUP BY City
ORDER BY Total_Providers DESC;
"""

cursor.execute(query1_sql)
result1 = cursor.fetchall()
print("PROVIDERS BY CITY:")
for row in result1:
    print(f"  {row[0]}: {row[1]} providers")

query1b_sql = """
SELECT 
    City,
    COUNT(*) as Total_Receivers
FROM receivers 
GROUP BY City
ORDER BY Total_Receivers DESC;
"""

cursor.execute(query1b_sql)
result1b = cursor.fetchall()
print("\nRECEIVERS BY CITY:")
for row in result1b:
    print(f"  {row[0]}: {row[1]} receivers")

# Query 2: Which type of food provider contributes the most food?
print("\n2. PROVIDER TYPE CONTRIBUTIONS")
print("-" * 50)

query2_sql = """
SELECT 
    p.Type as Provider_Type,
    COUNT(f.Food_ID) as Total_Food_Items,
    SUM(f.Quantity) as Total_Quantity
FROM providers p
JOIN food_listings f ON p.Provider_ID = f.Provider_ID
GROUP BY p.Type
ORDER BY Total_Quantity DESC;
"""

cursor.execute(query2_sql)
result2 = cursor.fetchall()
print("CONTRIBUTIONS BY PROVIDER TYPE:")
for row in result2:
    print(f"  {row[0]}: {row[1]} items, {row[2]} total quantity")

# Query 3: Contact information of food providers in a specific city (Mumbai)
print("\n3. PROVIDER CONTACTS IN MUMBAI")
print("-" * 50)

query3_sql = """
SELECT Provider_ID, Name, Type, Contact
FROM providers 
WHERE City = 'Mumbai'
ORDER BY Name
LIMIT 5;
"""

cursor.execute(query3_sql)
result3 = cursor.fetchall()
print("MUMBAI PROVIDERS CONTACT INFO:")
for row in result3:
    print(f"  ID: {row[0]}, {row[1]} ({row[2]}) - {row[3]}")

# Query 4: Which receivers have claimed the most food?
print("\n4. TOP RECEIVERS BY CLAIMS")
print("-" * 50)

query4_sql = """
SELECT 
    r.Receiver_ID,
    r.Name,
    r.Type,
    r.City,
    COUNT(c.Claim_ID) as Total_Claims
FROM receivers r
JOIN claims c ON r.Receiver_ID = c.Receiver_ID
GROUP BY r.Receiver_ID, r.Name, r.Type, r.City
ORDER BY Total_Claims DESC
LIMIT 5;
"""

cursor.execute(query4_sql)
result4 = cursor.fetchall()
print("TOP RECEIVERS:")
for row in result4:
    print(f"  {row[1]} ({row[2]}, {row[3]}): {row[4]} claims")

# Query 5: Total quantity of food available from all providers
print("\n5. TOTAL AVAILABLE FOOD QUANTITY")
print("-" * 50)

query5_sql = """
SELECT 
    COUNT(Food_ID) as Total_Food_Items,
    SUM(Quantity) as Total_Quantity
FROM food_listings;
"""

cursor.execute(query5_sql)
result5 = cursor.fetchone()
print(f"Total Food Items: {result5[0]}")
print(f"Total Quantity: {result5[1]} units")

# Query 6: Which city has the highest number of food listings?
print("\n6. CITIES WITH MOST FOOD LISTINGS")
print("-" * 50)

query6_sql = """
SELECT 
    Location as City,
    COUNT(Food_ID) as Total_Listings,
    SUM(Quantity) as Total_Quantity
FROM food_listings
GROUP BY Location
ORDER BY Total_Listings DESC;
"""

cursor.execute(query6_sql)
result6 = cursor.fetchall()
print("FOOD LISTINGS BY CITY:")
for row in result6:
    print(f"  {row[0]}: {row[1]} listings, {row[2]} total quantity")

# Query 7: Most commonly available food types
print("\n7. MOST COMMON FOOD TYPES")
print("-" * 50)

query7_sql = """
SELECT 
    Food_Type,
    COUNT(Food_ID) as Food_Count,
    SUM(Quantity) as Total_Quantity
FROM food_listings
GROUP BY Food_Type
ORDER BY Food_Count DESC;
"""

cursor.execute(query7_sql)
result7 = cursor.fetchall()
print("FOOD TYPES DISTRIBUTION:")
for row in result7:
    print(f"  {row[0]}: {row[1]} items, {row[2]} total quantity")

conn.close()

print(f"\n✓ First 7 queries executed successfully!")
print("Continuing with remaining queries...")

# Continue with remaining SQL queries (8-15)
print("CONTINUING WITH QUERIES 8-15")
print("="*60)

# Connect to the database
conn = sqlite3.connect('food_waste_management.db')
cursor = conn.cursor()

# Query 8: How many food claims have been made for each food item?
print("\n8. CLAIMS PER FOOD ITEM (TOP 10)")
print("-" * 50)

query8_sql = """
SELECT 
    f.Food_ID,
    f.Food_Name,
    f.Food_Type,
    f.Meal_Type,
    COUNT(c.Claim_ID) as Total_Claims
FROM food_listings f
LEFT JOIN claims c ON f.Food_ID = c.Food_ID
GROUP BY f.Food_ID, f.Food_Name, f.Food_Type, f.Meal_Type
ORDER BY Total_Claims DESC
LIMIT 10;
"""

cursor.execute(query8_sql)
result8 = cursor.fetchall()
print("MOST CLAIMED FOOD ITEMS:")
for row in result8:
    print(f"  {row[1]} (ID: {row[0]}): {row[4]} claims")

# Query 9: Which provider has had the highest number of successful food claims?
print("\n9. PROVIDERS WITH MOST SUCCESSFUL CLAIMS")
print("-" * 50)

query9_sql = """
SELECT 
    p.Provider_ID,
    p.Name,
    p.Type,
    p.City,
    COUNT(c.Claim_ID) as Successful_Claims
FROM providers p
JOIN food_listings f ON p.Provider_ID = f.Provider_ID
JOIN claims c ON f.Food_ID = c.Food_ID
WHERE c.Status = 'Completed'
GROUP BY p.Provider_ID, p.Name, p.Type, p.City
ORDER BY Successful_Claims DESC
LIMIT 5;
"""

cursor.execute(query9_sql)
result9 = cursor.fetchall()
print("TOP PROVIDERS BY SUCCESSFUL CLAIMS:")
for row in result9:
    print(f"  {row[1]} ({row[2]}, {row[3]}): {row[4]} completed claims")

# Query 10: What percentage of food claims are completed vs. pending vs. canceled?
print("\n10. CLAIM STATUS DISTRIBUTION")
print("-" * 50)

query10_sql = """
SELECT 
    Status,
    COUNT(Claim_ID) as Count,
    ROUND((COUNT(Claim_ID) * 100.0) / (SELECT COUNT(*) FROM claims), 2) as Percentage
FROM claims
GROUP BY Status
ORDER BY Count DESC;
"""

cursor.execute(query10_sql)
result10 = cursor.fetchall()
print("CLAIM STATUS BREAKDOWN:")
for row in result10:
    print(f"  {row[0]}: {row[1]} claims ({row[2]}%)")

# Query 11: What is the average quantity of food claimed per receiver?
print("\n11. AVERAGE FOOD QUANTITY PER RECEIVER")
print("-" * 50)

query11_sql = """
SELECT 
    r.Receiver_ID,
    r.Name,
    r.Type,
    COUNT(c.Claim_ID) as Total_Claims,
    ROUND(AVG(f.Quantity), 2) as Avg_Quantity_Per_Claim
FROM receivers r
JOIN claims c ON r.Receiver_ID = c.Receiver_ID
JOIN food_listings f ON c.Food_ID = f.Food_ID
WHERE c.Status = 'Completed'
GROUP BY r.Receiver_ID, r.Name, r.Type
ORDER BY Avg_Quantity_Per_Claim DESC
LIMIT 5;
"""

cursor.execute(query11_sql)
result11 = cursor.fetchall()
print("TOP RECEIVERS BY AVERAGE QUANTITY:")
for row in result11:
    print(f"  {row[1]} ({row[2]}): {row[4]} avg qty per claim ({row[3]} claims)")

# Query 12: Which meal type is claimed the most?
print("\n12. MOST CLAIMED MEAL TYPES")
print("-" * 50)

query12_sql = """
SELECT 
    f.Meal_Type,
    COUNT(c.Claim_ID) as Total_Claims,
    SUM(f.Quantity) as Total_Quantity_Claimed
FROM food_listings f
JOIN claims c ON f.Food_ID = c.Food_ID
GROUP BY f.Meal_Type
ORDER BY Total_Claims DESC;
"""

cursor.execute(query12_sql)
result12 = cursor.fetchall()
print("MEAL TYPE CLAIM STATISTICS:")
for row in result12:
    print(f"  {row[0]}: {row[1]} claims, {row[2]} total quantity")

# Query 13: What is the total quantity of food donated by each provider?
print("\n13. TOTAL DONATIONS BY PROVIDER (TOP 10)")
print("-" * 50)

query13_sql = """
SELECT 
    p.Provider_ID,
    p.Name,
    p.Type,
    p.City,
    COUNT(f.Food_ID) as Total_Items,
    SUM(f.Quantity) as Total_Quantity_Donated
FROM providers p
JOIN food_listings f ON p.Provider_ID = f.Provider_ID
GROUP BY p.Provider_ID, p.Name, p.Type, p.City
ORDER BY Total_Quantity_Donated DESC
LIMIT 10;
"""

cursor.execute(query13_sql)
result13 = cursor.fetchall()
print("TOP DONORS BY QUANTITY:")
for row in result13:
    print(f"  {row[1]} ({row[2]}, {row[3]}): {row[5]} units ({row[4]} items)")

print(f"\n✓ Queries 8-13 executed successfully!")
print("Continuing with final queries...")

# Final queries (14-15)
print("FINAL QUERIES 14-15")
print("="*60)

# Connect to the database
conn = sqlite3.connect('food_waste_management.db')
cursor = conn.cursor()

# Query 14: What are the upcoming food items that will expire in the next 7 days?
print("\n14. FOOD ITEMS EXPIRING IN NEXT 7 DAYS")
print("-" * 50)

query14_sql = """
SELECT 
    f.Food_ID,
    f.Food_Name,
    f.Quantity,
    f.Expiry_Date,
    f.Location,
    p.Name as Provider_Name,
    p.Contact as Provider_Contact
FROM food_listings f
JOIN providers p ON f.Provider_ID = p.Provider_ID
WHERE date(f.Expiry_Date) BETWEEN date('now') AND date('now', '+7 days')
ORDER BY f.Expiry_Date
LIMIT 10;
"""

cursor.execute(query14_sql)
result14 = cursor.fetchall()
print("EXPIRING SOON (Next 7 days):")
if result14:
    for row in result14:
        print(f"  {row[1]} (ID: {row[0]}) - Qty: {row[2]}, Expires: {row[3]}")
        print(f"    Location: {row[4]}, Provider: {row[5]}, Contact: {row[6]}")
else:
    print("  No food items expiring in the next 7 days")

# Alternative query for current date context (since our data is future-dated)
print("\n14b. FOOD ITEMS EXPIRING EARLIEST (First 10)")
print("-" * 50)

query14b_sql = """
SELECT 
    f.Food_ID,
    f.Food_Name,
    f.Quantity,
    f.Expiry_Date,
    f.Location,
    p.Name as Provider_Name,
    f.Food_Type,
    f.Meal_Type
FROM food_listings f
JOIN providers p ON f.Provider_ID = p.Provider_ID
ORDER BY f.Expiry_Date ASC
LIMIT 10;
"""

cursor.execute(query14b_sql)
result14b = cursor.fetchall()
print("EARLIEST EXPIRING ITEMS:")
for row in result14b:
    print(f"  {row[1]} ({row[6]} {row[7]}) - Qty: {row[2]}, Expires: {row[3]}")
    print(f"    Location: {row[4]}, Provider: {row[5]}")

# Query 15: Which locations have the highest food wastage (unclaimed expired food)?
print("\n15. LOCATIONS WITH HIGHEST FOOD WASTAGE")
print("-" * 50)

query15_sql = """
SELECT 
    f.Location,
    COUNT(f.Food_ID) as Unclaimed_Items,
    SUM(f.Quantity) as Wasted_Quantity,
    AVG(f.Quantity) as Avg_Waste_Per_Item
FROM food_listings f
LEFT JOIN claims c ON f.Food_ID = c.Food_ID
WHERE c.Food_ID IS NULL  -- No claims made
   OR (c.Status = 'Cancelled')  -- Cancelled claims
GROUP BY f.Location
ORDER BY Wasted_Quantity DESC;
"""

cursor.execute(query15_sql)
result15 = cursor.fetchall()
print("FOOD WASTAGE BY LOCATION:")
for row in result15:
    print(f"  {row[0]}: {row[1]} unclaimed items, {row[2]} units wasted")
    print(f"    Average waste per item: {row[3]:.1f} units")

# Additional analysis - Overall wastage statistics
print("\n15b. OVERALL WASTAGE ANALYSIS")
print("-" * 50)

query15b_sql = """
SELECT 
    'Total Food Listed' as Metric,
    COUNT(f.Food_ID) as Count,
    SUM(f.Quantity) as Total_Quantity
FROM food_listings f
UNION ALL
SELECT 
    'Successfully Claimed' as Metric,
    COUNT(DISTINCT c.Food_ID) as Count,
    SUM(f.Quantity) as Total_Quantity
FROM claims c
JOIN food_listings f ON c.Food_ID = f.Food_ID
WHERE c.Status = 'Completed'
UNION ALL
SELECT 
    'Unclaimed/Wasted' as Metric,
    COUNT(f.Food_ID) as Count,
    SUM(f.Quantity) as Total_Quantity
FROM food_listings f
LEFT JOIN claims c ON f.Food_ID = c.Food_ID AND c.Status = 'Completed'
WHERE c.Food_ID IS NULL;
"""

cursor.execute(query15b_sql)
result15b = cursor.fetchall()
print("OVERALL STATISTICS:")
for row in result15b:
    print(f"  {row[0]}: {row[1]} items, {row[2]} total quantity")

conn.close()

print(f"\n✅ ALL 15 SQL QUERIES COMPLETED SUCCESSFULLY!")
print("="*60)
print("\nQUERY SUMMARY:")
print("1. ✓ Providers and receivers count by city")
print("2. ✓ Provider type contributions")
print("3. ✓ Provider contacts by city")
print("4. ✓ Top receivers by claims")
print("5. ✓ Total available food quantity")
print("6. ✓ Cities with most food listings")
print("7. ✓ Most common food types")
print("8. ✓ Claims per food item")
print("9. ✓ Providers with most successful claims")
print("10. ✓ Claim status distribution")
print("11. ✓ Average quantity per receiver")
print("12. ✓ Most claimed meal types")
print("13. ✓ Total donations by provider")
print("14. ✓ Food items expiring soon")
print("15. ✓ Locations with highest wastage")

print(f"\n🎉 PHASE 3 COMPLETE: SQL Query Development & Analysis")
print("Ready to proceed to Phase 4: Exploratory Data Analysis (EDA)")