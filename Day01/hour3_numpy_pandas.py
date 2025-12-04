# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: ai_mastery
#     language: python
#     name: python3
# ---

# %%
import pandas as pd

url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
df = pd.read_csv(url)
df.head()
df.info()
df.describe(include='all')

# %%
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 120)


# %%
url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
df = pd.read_csv(url)
df.shape

# %%
# Missing counts and percent
missing = df.isnull().sum().sort_values(ascending=False)
missing_pct = (df.isnull().mean()*100).sort_values(ascending=False)
pd.concat([missing, missing_pct], axis=1, keys=['missing','pct']).head(20)


# %%
# Example repair for TotalCharges (string -> numeric), then fill
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
print("Missing before fill:", df['TotalCharges'].isnull().sum())
df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)
print("Missing after fill:", df['TotalCharges'].isnull().sum())


# %%
# Identify categorical columns and cardinality
cat_cols = df.select_dtypes(include=['object']).columns.tolist()
card = {c: df[c].nunique() for c in cat_cols}
card


# %%
# Example: drop customerID and encode obvious low-cardinality cols
df = df.drop(columns=['customerID'])
low_card_cols = [c for c, n in card.items() if n <= 6 and c!='customerID']
df = pd.get_dummies(df, columns=low_card_cols, drop_first=True)
# For remaining object columns with >6 categories, encode with simple label encoding for now
from sklearn.preprocessing import OrdinalEncoder
high_card_cols = [c for c in df.select_dtypes(include=['object']).columns.tolist()]
if high_card_cols:
    oe = OrdinalEncoder()
    df[high_card_cols] = oe.fit_transform(df[high_card_cols])
    
df.shape



# %%
# Tenure group buckets + AvgMonthlyCharge
df['TenureGroup'] = pd.cut(df['tenure'], bins=[-1, 12, 24, 48, 72], labels=['0-12','12-24','24-48','48-72'])
df['AvgMonthlyCharge'] = df['TotalCharges'] / (df['tenure'] + 1)    # +1 to avoid div0

# Show value counts and basic stats
print(df['TenureGroup'].value_counts())
df[['AvgMonthlyCharge','MonthlyCharges']].describe().T


# %%
agg = df.groupby('TenureGroup').agg({
    'AvgMonthlyCharge':'mean',
    'MonthlyCharges':'median',
    # if Churn exists as numeric after encoding, use mean; else decode original before drop
})
agg


# %%
from sklearn.base import BaseEstimator, TransformerMixin

def load_and_preprocess(url):
    df = pd.read_csv(url)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)
    df = df.drop(columns=['customerID'])
    low_card_cols = [c for c in df.select_dtypes(include=['object']).columns.tolist() if df[c].nunique() <= 6]
    df = pd.get_dummies(df, columns=low_card_cols, drop_first=True)
    # encode remaining object columns if any
    rem_obj = df.select_dtypes(include=['object']).columns.tolist()
    if rem_obj:
        from sklearn.preprocessing import OrdinalEncoder
        oe = OrdinalEncoder()
        df[rem_obj] = oe.fit_transform(df[rem_obj])
    df['TenureGroup'] = pd.cut(df['tenure'], bins=[-1,12,24,48,72], labels=['0-12','12-24','24-48','48-72'])
    df['AvgMonthlyCharge'] = df['TotalCharges'] / (df['tenure'] + 1)
    return df

clean_df = load_and_preprocess(url)
clean_df.shape

