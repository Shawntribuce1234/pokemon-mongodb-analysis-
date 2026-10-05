# pokemon-mongodb-analysis-
# Pokémon Analysis with MongoDB

A Python and MongoDB project exploring the first 151 Pokémon through API collection, nested document modeling, database queries, and visualization. Completed by **Shawn Tribuce** for **DS4300 — Homework 3**.

The project collects Pokémon, species, and evolution-chain data from PokeAPI, saves a JSON snapshot, imports the documents into MongoDB, and uses queries and aggregation pipelines to explore types, abilities, physical attributes, and base stats.

## Repository Structure

```text
pokemon-mongodb-analysis/
├── README.md
├── src/
│   ├── fetch_pokemon.py
│   ├── import_mongodb.py
│   └── plot_type_distribution.py
├── data/
│   └── pokemon.json
├── queries/
│   └── query_examples.txt
└── report/
    └── pokemon_analysis_abstract.pdf
```

The scripts were renamed from `step1.py`, `step2.py`, and `step4.py` to describe their roles. `query_examples.txt` preserves the original `step3.txt` commands and recorded outputs. The report is the original `Extended_Abstract.pdf`. Script contents are unchanged.

## Dataset and Document Model

The included `pokemon.json` is a JSON array containing **151 documents**, with unique Pokémon IDs covering **1–151**. Each document contains:

- Identifiers and attributes: `pokemon_id`, `name`, `base_experience`, `height`, and `weight`.
- A `types` array.
- An `abilities` array of objects containing `name` and `is_hidden`.
- A `stats` object containing HP, attack, defense, special attack, special defense, and speed.
- A sprite URL.
- Species metadata: generation, legendary and mythical flags, habitat, growth rate, and capture rate.
- A nested `evolution_chain` containing species names and recursive `evolves_to` arrays.

All documents are stored together in the `pokemon` collection of the `ds4300_pokemon` database. Arrays and embedded objects allow queries against types, abilities, and individual stats within each document.

The first 151 IDs define the selected Pokémon, but the snapshot includes later type assignments such as Fairy and Steel. It is not a reconstruction of the original games' historical typing. Evolution chains are copied recursively from the API without filtering their members to IDs 1–151. Height and weight are retained in the API's raw numeric representation; the code does not convert units.

## Workflow

### 1. Collect and transform API responses

`fetch_pokemon.py` loops over IDs 1–151. For each ID it retrieves a Pokémon response, a species response, and the evolution chain referenced by the species response. It selects the fields used by the project and recursively simplifies evolution chains to species names and child branches.

Successfully built documents are accumulated and written to `pokemon.json` in the current working directory. The script pauses for 0.1 seconds after each successful Pokémon. HTTP errors are printed and the affected Pokémon is skipped; the script does not retry failed requests or enforce a complete 151-document output.

### 2. Import into MongoDB

`import_mongodb.py` reads `pokemon.json` from the current working directory and connects to `mongodb://localhost:27017/`. It selects `ds4300_pokemon.pokemon`, drops the existing collection, and inserts the loaded documents in one batch. It then prints one sample document without MongoDB's `_id` field.

**Running the importer replaces the existing `pokemon` collection in `ds4300_pokemon`.** Use that database for this project only if its existing contents can be replaced.

### 3. Explore with queries

The query transcript contains ten examples with recorded outputs:

| Question | Main operations |
|---|---|
| Which Pokémon are Fire type? | Array membership and projection |
| Which have attack greater than 100? | Nested-field comparison and descending sort |
| Which are the ten heaviest? | Sort and limit |
| What are their names, types, and stats? | Projection, limited to five examples |
| Which have exactly two types? | `$size`, limited to five examples |
| Which have a hidden ability? | Nested array-field matching, limited to five examples |
| What is average HP by habitat? | `$match`, `$group`, `$avg`, and `$sort` |
| Which have the highest base experience? | Aggregation sort, limit, and projection |
| Which types are most common? | `$unwind`, `$group`, and `$sort` |
| How do legendary and other Pokémon compare? | Grouping by `is_legendary` and averaging attack, defense, and HP |

The transcript is a reference document, not an executable query script: commands are interspersed with prose and outputs. Some recorded lists are incomplete. For example, the attack query matches **22 documents** in the supplied JSON, while its recorded output lists eleven. Equal-value ties are not explicitly ordered by a secondary key.

### 4. Visualize type distribution

`plot_type_distribution.py` connects to the same MongoDB collection and runs an aggregation that expands the `types` array, counts each type, and sorts counts in descending order.

Matplotlib displays a red bar chart with a label above each bar. The script uses `plt.show()` and does not automatically export an image. A chart is included in the project report.

## Verified Findings

Recounting the saved JSON reproduces the report's leading type counts:

| Type | Pokémon count |
|---|---:|
| Poison | 33 |
| Water | 32 |
| Normal | 22 |
| Flying | 19 |
| Grass | 14 |
| Ground | 14 |
| Psychic | 14 |

The snapshot has **17 represented types**, **67 dual-type Pokémon**, and **218 total type memberships**. Each dual-type Pokémon contributes to two bars, so the chart's counts sum to more than 151. Poison ranks first by type membership in this snapshot.

The `is_legendary` flag identifies Articuno, Zapdos, Moltres, and Mewtwo. Mew is marked mythical and is included in the `is_legendary: false` group by the comparison query. That query groups solely by the legendary flag; it does not exclude mythical Pokémon.

## Running the Project

### Requirements

- Python 3.
- A MongoDB server accessible at `mongodb://localhost:27017/` for import, queries, and plotting.
- A graphical environment for the interactive chart.
- Internet access only if refreshing the data from PokeAPI.

Install the Python dependencies:

```bash
python3 -m pip install requests pymongo matplotlib
```

### Use the included snapshot

From the repository root, change to `data/` so the unchanged scripts resolve `pokemon.json` correctly:

```bash
cd data
python3 ../src/import_mongodb.py
python3 ../src/plot_type_distribution.py
```

The importer replaces the collection as described above. The plotting script requires that collection to have been populated.

The original queries were run using MongoDB Compass. To reproduce them, select the `ds4300_pokemon` database in a MongoDB shell and run individual commands from `queries/query_examples.txt`, excluding the prose and recorded outputs.

### Refresh from PokeAPI

From the repository root:

```bash
cd data
python3 ../src/fetch_pokemon.py
```

This overwrites `data/pokemon.json` when collection finishes. Review the resulting document count before importing it, because HTTP failures can leave a partial dataset. Re-run the importer if you want the database to reflect the refreshed snapshot.

## Outputs

- **JSON snapshot:** the selected and transformed API data.
- **MongoDB collection:** imported Pokémon documents in `ds4300_pokemon.pokemon`.
- **Console sample:** one document printed after import.
- **Query transcript:** saved commands and results from the original coursework.
- **Interactive chart:** type counts generated from the database.
- **[Extended abstract](report/pokemon_analysis_abstract.pdf):** project discussion and the type-distribution visualization.

## Verification and Limitations

During repository preparation, the JSON was parsed, IDs were checked for complete unique coverage of 1–151, type memberships were recounted, legendary/mythical flags were inspected, and all three Python files passed syntax parsing.

No automated test suite is included. Live API calls and MongoDB operations were not rerun during this review. The sample printed by the importer is a manual inspection aid, not an automated correctness test.

The collector has no request timeout, retries, or evolution-chain cache. It catches HTTP errors but does not handle every possible connection or decoding failure. The importer does not validate the schema, create custom indexes, or perform incremental updates. Connection settings are hard-coded, and collection and plotting scripts require a running local MongoDB server.

This is an exploratory document-database project. The type counts describe the selected snapshot; they do not establish why particular game-design decisions were made.

## Author and Coursework

**Shawn Tribuce**  
**DS4300 — Homework 3**
