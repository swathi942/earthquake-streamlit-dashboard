import streamlit as st
import pandas as pd
import pymysql
from sqlalchemy import create_engine

# MySQL connection

host="localhost"
user="root"
password="12345"
database="seismic_db"

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")



queries = {
    
" 1. Top 10 strongest earthquakes":"""
select * from earthquakes
order by mag desc
limit 10;
""",

"2. Top 10 deepest earthquakes (depth_km)":"""
SELECT * FROM earthquakes
ORDER BY depth_km DESC
LIMIT 10;
""",


 "3. Shallow earthquakes < 50 km and mag > 7.5":"""
SELECT * FROM earthquakes
WHERE depth_km < 50 AND mag > 7.5;
""",


 "5. Average magnitude per magnitude type (magType)":"""
SELECT magType, AVG(mag) AS avg_mag 
FROM earthquakes
GROUP BY magType;
""",


"6. Year with most earthquakes":"""
SELECT YEAR(time) AS year, COUNT(*) AS total
FROM earthquakes
GROUP BY year(time)
ORDER BY total DESC
LIMIT 1;
""",

 "7. Month with highest number of earthquakes":"""
SELECT Month(time) AS Month , COUNT(*) AS total
FROM earthquakes
GROUP BY Month(time)
ORDER BY total DESC
LIMIT 1;
""",


"8. Day of week with most earthquakes":"""
SELECT Dayname(time) AS Day , COUNT(*) AS total
FROM earthquakes
GROUP BY Dayname(time)
ORDER BY total DESC;
""",

"9. Count of earthquakes per hour of day":"""
SELECT hour(time) AS hour , COUNT(*) AS total
FROM earthquakes
GROUP BY hour(time)
ORDER BY hour;
""",


"10. Most active reporting network (net)":"""
SELECT net , COUNT(*) AS total
FROM earthquakes
GROUP BY net
ORDER BY total Desc;
""",


"11.  Top 5 places with highest casualties":"""
SELECT place, Max(felt) AS casualties
FROM earthquakes
GROUP BY place
ORDER BY casualties DESC
LIMIT 5;
""",

"13.  Average economic loss by alert level":"""
SELECT alert,COUNT(*) AS total
FROM earthquakes
GROUP BY alert;
""",

"14.  Count of reviewed vs automatic earthquakes (status)":"""
SELECT status,COUNT(*) AS total
FROM earthquakes
GROUP BY status;
""",


"15.  Count by earthquake type (type)":"""
SELECT type,COUNT(*) AS total
FROM earthquakes
GROUP BY type;
""",

 "16.  Number of earthquakes by data type (types)":"""
SELECT types,COUNT(*) AS total
FROM earthquakes
GROUP BY types;
""",


"18.  Events with high station coverage (nst > threshold)":"""
SELECT * FROM earthquakes
WHERE nst > 50;
""",


"19.  Number of tsunamis triggered per year":"""
SELECT YEAR(time) AS year, COUNT(*) AS tsunamis
FROM earthquakes
WHERE tsunami = 1
GROUP BY year(time);
""",


"20.  Count earthquakes by alert levels (red, orange, etc.)":"""
SELECT alert,COUNT(*) AS total
FROM earthquakes
GROUP BY alert;
""",


"21. Top 5 countries – highest avg mag":"""
SELECT country, AVG(mag) as avg_mag
FROM earthquakes
GROUP BY country
ORDER BY avg_mag DESC
LIMIT 5;
""",

"22. Same month shallow & deep earthquakes":"""
SELECT country, YEAR(time) AS year, MONTH(time) AS month
FROM earthquakes
GROUP BY country, year(time), month(time)
HAVING 
SUM( depth_km < 70 ) > 0
AND
SUM(depth_km > 300) > 0;
""",

 "23. Year-over-Year growthrate": """
SELECT year,
       total,
       LAG(total) OVER (ORDER BY year) AS growth
FROM (
    SELECT YEAR(time) AS year, COUNT(*) AS total
    FROM earthquakes
    GROUP BY year(time)
) t;
""",

 "24.  3 most seismically active regions":"""
 SELECT place as region,
       COUNT(*) AS freq, AVG(mag) AS avg_mag
FROM earthquakes
GROUP BY region
ORDER BY freq DESC, avg_mag DESC
LIMIT 3;
""",


"25. average depth of earthquakes within ±5° latitude range of the equator":"""
SELECT country, AVG(depth_km) AS avg_depth
FROM earthquakes
WHERE latitude BETWEEN -5 AND 5
GROUP BY country;
""",


"26. highest ratio of shallow to deep earthquakes":"""
SELECT country,
SUM(depth_km < 70) /
SUM(depth_km > 300) AS ratio
FROM earthquakes
GROUP BY country;
""",


"27. average magnitude difference between earthquakes with tsunami alerts ":"""
SELECT 
    (SELECT AVG(mag) FROM earthquakes WHERE tsunami = 1)
  - (SELECT AVG(mag) FROM earthquakes WHERE tsunami = 0) 
    AS avg_magnitude_difference;
""",
    
    
"28. Lowest data reliability (high rms & gap)":"""
SELECT place, mag, rms, gap
FROM earthquakes
ORDER BY rms DESC, gap DESC
LIMIT 10;
""",

"30. Regions with most deep-focus earthquakes (>300km)":"""
SELECT country, COUNT(*) AS deep_count
FROM earthquakes
WHERE depth_km > 300
GROUP BY country
ORDER BY deep_count DESC;
"""
}


#-------------------------------
# Streamlit UI
#-------------------------------
st.title("Earthquake Data Analysis Dashboard")

#Dropdown
task = st.selectbox("Choose Query Number",list(queries.keys()))

# Run button
if st.button("Run Query"):
    query= queries[task]
    df = pd.read_sql(query,engine)

    st.subheader(f"Results for:{task}")
    st.dataframe(df,use_container_width=True)