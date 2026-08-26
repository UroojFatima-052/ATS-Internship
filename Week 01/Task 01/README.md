# Task 1: Exploratory Data Analysis (EDA) on the Iris Dataset

## Objective
Perform industry-style Exploratory Data Analysis (EDA) on the classic Iris flower dataset, inspecting data quality, understanding feature distributions, and visualizing relationships between features and species.

## Project Structure
```
Task1_EDA_Iris/
├── Task1_EDA_Iris.ipynb     # Main Jupyter Notebook (source file, fully executed)
├── data/
│   └── iris.csv             # Dataset used (150 rows, 5 columns)
├── screenshots/              # Exported chart images (evidence of outputs)
│   ├── 01_feature_distributions.png
│   ├── 02_boxplots_by_species.png
│   ├── 03_petal_scatter.png
│   ├── 04_sepal_scatter.png
│   ├── 05_pairplot.png
│   ├── 06_correlation_heatmap.png
│   └── 07_species_count.png
├── Task1_Report.docx         # Written report summarizing methodology & findings
└── README.md                 # This file
```

## Tools & Libraries Used
- Python 3
- pandas, numpy for data handling
- matplotlib, seaborn for data visualization
- Jupyter Notebook

## How to Run
1. Make sure Python 3 and Jupyter are installed.
2. The required libraries:
   ```
   pip install pandas numpy matplotlib seaborn jupyter
   ```
3. Open a terminal in this folder and run:
   ```
   jupyter notebook Iris EDA.ipynb
   ```
4. Run all cells from top to bottom.
5. Generated charts will also be saved automatically into the `screenshots/` folder.

## Key Steps Performed
1. Loaded and inspected the dataset (shape, data types, missing values, duplicates).
2. Generated statistical summaries (`describe()`) and class balance checks.
3. Performed univariate analysis (histograms, boxplots).
4. Performed bivariate analysis (scatter plots, pairplot, correlation heatmap).
5. Summarized key insights about which features best separate the species.

## Deliverables Checklist
- [x] Source files (`.ipynb`, `data/iris.csv`)
- [x] Report (`Task1_Report.docx`)
- [x] Screenshots (`screenshots/` folder — 7 chart images)
- [x] README (this file)

## Key Findings 
- The dataset is clean, no missing values or duplicates, perfectly balanced (50 samples/species).
- Petal length and petal width are the strongest, most correlated features (correlation ≈ 0.96)
  and best separate the three species.
- *Setosa* is easily distinguishable from the other two species; *versicolor* and *virginica*
  overlap more.

