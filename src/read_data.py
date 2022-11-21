import duckdb

con = duckdb.connect(database=":memory:")
con.execute(
    "CREATE VIEW 'gas_prices' AS SELECT * FROM '"+datapath+"';"
)
con.execute("DESCRIBE SELECT * FROM 'gas_prices';").fetchall()

# stmt = """
#     SELECT *
#     FROM 'gas_prices'
#     WHERE '2021-01-01' < date AND date < '2021-02-01' AND province_name == 'MADRID'
# """

stmt = """
    SELECT *
    FROM 'gas_prices'
    WHERE municipality_name == 'Madrid' AND '2021-01-01' < date AND date < '2023-02-01'
"""
#WHERE 'province_name' == 'MADRID'
# Create DataFrame with the selected data

df = con.execute(stmt).fetchdf()

df['date']=df['date'].dt.strftime('%d%m%Y')

# Initial data analysis and null values filling
print('     ')
print('#########################################################')
print('     DATA TYPE, NON-NULL VARIABLES AND MEMORY USAGE')
print('#########################################################')
print('     ')
print(df['province_name'].unique())
print(df.info())
print('     ')
print('---------- Filling NaN ...')
df= df.fillna(0)
print('---------- NaN remaining:', df.isnull().sum().sum())
print('     ')

# Download selected dataset into .csv

df.to_csv('datos.csv')
