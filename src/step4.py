"""
DS4300 Homework 3 - Step 4
Shawn Tribuce

Ploting a bar chart of the distribution of Pokemon types across the first 151 Pokemon using matplotlib.
"""

import pymongo
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Connecting to MongoDB and getting the collection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db     = client["ds4300_pokemon"]
col    = db["pokemon"]

# Group by type and count number of Pokemon for each type
Count_type = [
    { "$unwind": "$types" },
    { "$group": {
        "_id":   "$types",
        "count": { "$sum": 1 }
    }},
    { "$sort": { "count": -1 } }
]

results = list(col.aggregate(Count_type)) # Convert the aggregation to a list of results
client.close()

# Separate the types and counts into two lists for plotting
types  = [r["_id"] for r in results]
counts = [r["count"] for r in results]


# Add value labels on top of each bar for clarity and customize the plot with titles and axis labels
fig, ax = plt.subplots(figsize=(12, 6)) # Set the figure size for better readability
bars = ax.bar(types, counts, color="red", linewidth=0.6)
for bar, count in zip(bars, counts): # Add the count value on top of each bar
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        str(count),
        ha="center", va="bottom",
        fontsize=9, color="#333333"
    )
ax.set_title("Type Distribution Across Generation 1 Pokémon (151 total)", fontsize=14)
ax.set_xlabel("Type", fontsize=11)
ax.set_ylabel("Number of Pokemon", fontsize=11)
plt.show()