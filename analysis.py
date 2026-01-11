
import pandas as pd

df = pd.read_csv("customer_shopping_behavior.csv")
print(df.head())



# %%
df.info()

# %%
df.describe(include='all')

# %%
df.isnull().sum()

# %%
df['Review Rating'] = pd.to_numeric(df['Review Rating'], errors='coerce')


# %%
df['Review Rating'] = (
    df.groupby('Category')['Review Rating']
      .transform(lambda x: x.fillna(x.median()))
)

# %%
df.isnull().sum()


# %%
df.columns = (
    df.columns
      .str.lower()
      .str.replace(r'[^\w]+', '_', regex=True)
      .str.strip('_')
)


# %%
df.columns

# %%
# new column: age_group
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels = labels)

# %%
df[['age','age_group']].head(10)

# %%
# new column : purchase_frequency_days
frequency_mapping = {
    'Weekly': 7,
    'Bi-Weekly': 14,
    'Fortnightly': 14,
    'Monthly': 30,
    'Quarterly': 90,
    'Every 3 Months': 90,
    'Annually': 365,   
}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)

# %%
df[['purchase_frequency_days', 'frequency_of_purchases']].head(10)

# %%
df[['discount_applied', 'promo_code_used']].head(10)

# %%
(df['discount_applied'] == df['promo_code_used']).all()

# %%
df.drop(columns=['promo_code_used'], inplace=True)

# %%
df.columns


# %%
from sqlalchemy import create_engine
from urllib.parse import quote_plus

username = "postgres"
password = quote_plus("Your_Password")
host = "localhost"
port = "5432"
database = "customer_behaviour"   

engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)

table_name = "customer"
df.to_sql(table_name, engine, if_exists="replace", index=False)

print("✅ Data successfully loaded into PostgreSQL")



