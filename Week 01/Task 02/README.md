# Task 2: Linear Regression Model on the Iris Dataset

## Objective
Build a simple, beginner-level Linear Regression model on the **Iris dataset** that predicts a
flower's **Petal Width** from its **Petal Length**, following standard industry best practices:
EDA → train/test split → model training → evaluation → visualization.

## Project Structure
```
Task2_Linear_Regression/
├── Task2_Linear_Regression.ipynb   # Main Jupyter Notebook (source file, fully executed)
├── data/
│   └── iris.csv                    # Dataset used (150 rows, 5 columns)
├── screenshots/                     # Exported chart images (evidence of outputs)
│   ├── 01_scatter_petal_length_vs_width.png
│   ├── 02_regression_line_fit.png
│   ├── 03_actual_vs_predicted.png
│   └── 04_residual_plot.png
├── Task2_Report.docx                # Written report summarizing methodology & results
└── README.md                        # This file
```

## Tools & Libraries Used
- Python 3
- pandas, numpy for data handling
- matplotlib, seaborn for data visualization
- scikit-learn for model training & evaluation
- Jupyter Notebook

## How to Run
1. Make sure Python 3 and Jupyter are installed.
2. The required libraries:
   ```
   pip install pandas numpy matplotlib seaborn scikit-learn jupyter
   ```
3. Open a terminal in this folder and run:
   ```
   jupyter notebook Linear Regression.ipynb
   ```
4. Run all cells from top to bottom.
5. Generated charts will also be saved automatically into the `screenshots/` folder.

## Dataset
The Iris dataset (150 samples, 3 species: *setosa*, *versicolor*, *virginica*). For this task,
only two numeric features are used: `petal_length` (predictor) and `petal_width` (target) —
the most strongly correlated pair of features in the dataset.

## Key Steps Performed
1. Loaded and explored the dataset (shape, info, missing values, summary statistics).
2. Visualized the relationship between petal length and petal width (scatter plot + correlation).
3. Split data into training (80%) and testing (20%) sets.
4. Trained a `LinearRegression` model from scikit-learn.
5. Evaluated the model using MAE, MSE, RMSE, and R² score.
6. Visualized the regression line, actual vs predicted values, and residuals.
7. Used the trained model to predict petal width for a new, unseen petal length value.

## Deliverables Checklist
- [x] Source files (`.ipynb`, `data/iris.csv`)
- [x] Report (`Task2_Report.docx`)
- [x] Screenshots (`screenshots/` folder — 4 chart images)
- [x] README (this file)

## Key Results (Summary)
| Metric | Value |
|---|---|
| Intercept | -0.3567 |
| Slope (coefficient) | 0.4132 |
| MAE | 0.1682 cm |
| RMSE | 0.2136 cm |
| R² Score | 0.928 |

The model explains about **92.8%** of the variance in petal width using petal length alone,
indicating a strong linear fit.

