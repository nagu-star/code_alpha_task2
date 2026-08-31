import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('books_scraped_data_complete.csv')

# 1. Fix the price encoding issue (Â£ -> £) and convert to float
for col in ['Price', 'Price (excl. tax)', 'Price (incl. tax)', 'Tax']:
    df[col] = (df[col]
               .str.replace('Â£', '', regex=False)
               .str.replace('£', '', regex=False)
               .astype(float))

# 2. Convert Rating from words to numbers
rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
df['Rating'] = df['Rating'].map(rating_map)
print(df['Rating'].unique())

# 3. Drop columns with no variation (useless for analysis)
df = df.drop(columns=['Availability', 'Product Type'])

# 4. Handle missing Description (2 missing) - fill with placeholder
df['Description'] = df['Description'].fillna('No description available')

# 5. Check for the duplicate title
print(df[df.duplicated(subset='Title', keep=False)])

# 6. Confirm everything looks right now
print(df.dtypes)
print(df.head())
print(df.isnull().sum())
print(df[['Price', 'Rating', 'Number of Reviews']].describe())

#

fig, axes = plt.subplots(1, 2, figsize=(12, 4))


df['Price'].hist(bins=20, ax=axes[0], edgecolor='black')
axes[0].set_title('Price Distribution')
axes[0].set_xlabel('Price (£)')
axes[0].set_ylabel('Number of Books')

df['Rating'].value_counts().sort_index().plot(kind='bar', ax=axes[1], edgecolor='black')
axes[1].set_title('Rating Distribution')
axes[1].set_xlabel('Rating (stars)')
axes[1].set_ylabel('Number of Books')

plt.tight_layout()
plt.show()

df.boxplot(column='Price', by='Rating', figsize=(8,5))
plt.title('Price by Rating')
plt.suptitle('')
plt.xlabel('Rating (stars)')
plt.ylabel('Price (£)')
plt.show()


# Calculate IQR (Interquartile Range) for Price
Q1 = df['Price'].quantile(0.25)
Q3 = df['Price'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print(f"Q1: £{Q1:.2f}, Q3: £{Q3:.2f}, IQR: £{IQR:.2f}")
print(f"Normal range: £{lower_bound:.2f} to £{upper_bound:.2f}")

# Find actual outliers
outliers = df[(df['Price'] < lower_bound) | (df['Price'] > upper_bound)]
print(f"\nNumber of outlier books: {len(outliers)}")
print(outliers[['Title', 'Price', 'Rating']])

# Also just look at the extremes directly
print("\n--- 5 cheapest books ---")
print(df.nsmallest(5, 'Price')[['Title', 'Price', 'Rating']])

print("\n--- 5 most expensive books ---")
print(df.nlargest(5, 'Price')[['Title', 'Price', 'Rating']])
