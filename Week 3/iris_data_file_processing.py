from ucimlrepo import fetch_ucirepo

# 1. Fetch the dataset (Iris ID is 53)
iris = fetch_ucirepo(id=53)

# Extract features and targets into a single DataFrame for convenience
X = iris.data.features
y = iris.data.targets


# 1. Total number of records (rows)
total_records = len(X)
print(f"Total number of records: {total_records}")

# 2. Total number of different flowers (unique species)
num_unique_flowers = y["class"].nunique()
print(f"Total number of different flowers: {num_unique_flowers}")

# 3. Names of all different flowers
flower_names = y["class"].unique().tolist()
print(f"Names of different flowers: {flower_names}")