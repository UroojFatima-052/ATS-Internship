# Task 1: Feature Engineering and Model Comparison

## Objective
Prepare the sales dataset for predictive modeling, create meaningful new features, handle missing
and categorical data, train more than one model, compare them using appropriate evaluation metrics,
and explain which model is preferable and why.

## Project Structure
```
Task 01/
├── Feature Engineering and Model Comparison.ipynb  # Main notebook (fully executed)
├── data/
│   └── sales_data.csv       # Dataset used (8,399 rows, 21 columns)
├── screenshots/             # Exported chart images (evidence of outputs)
│   ├── 01_new_features_check.png
│   ├── 02_model_comparison.png
│   ├── 03_roc_curves.png
│   └── 04_confusion_matrix.png
├── Report.docx              # Written report summarizing methodology & results
└── README.md                # This file
```

## Tools & Libraries Used
- Python 3
- pandas, numpy for data handling
- matplotlib, seaborn for data visualization
- scikit-learn for preprocessing, model training and evaluation
- Jupyter Notebook

## How to Run
1. Make sure Python 3 and Jupyter are installed.
2. Install the required libraries:
   ```
   pip install pandas numpy matplotlib seaborn scikit-learn jupyter
   ```
3. Open a terminal in this folder and run:
   ```
   jupyter notebook "Feature Engineering and Model Comparison.ipynb"
   ```
4. Run all cells from top to bottom.
5. Generated charts are saved automatically into the `screenshots/` folder.

## Dataset
The same Superstore Sales dataset used in Week 2, 8,399 rows and 21 columns, so this week's results
can be compared directly against last week's baseline.

**Target:** `Profitable` (1 if `Profit > 0`, else 0), with a class balance of about 49% to 51%.

## The Five New Features
| Feature | Formula | Why it was created |
|---|---|---|
| Shipping Delay | Ship Date - Order Date | A slow shipment may point to a bulky or awkward product |
| Revenue Per Unit | Sales / Order Quantity | Separates cheap bulk orders from expensive small ones |
| Shipping Cost Ratio | Shipping Cost / Sales | Week 2 showed shipping eats margin, this measures it directly |
| Discount Value | Sales x Discount | 10% off a 5,000 order is very different from 10% off a 50 order |
| Order Month | Month of Order Date | Lets the model pick up any seasonal pattern |

## Key Steps Performed
1. Loaded the dataset and filled the 63 missing `Product Base Margin` values with the median of
   each product category.
2. Created the five new features listed above.
3. Created the binary target and checked the class balance.
4. Checked with boxplots whether the new features actually separate profitable from unprofitable
   orders, before training anything.
5. Selected 11 numeric and 7 categorical features, dropping `Profit` (which would leak the answer),
   ID columns and free-text names.
6. Split the data 80/20 with `stratify=y` and a fixed `random_state=42`.
7. Built a `ColumnTransformer` pipeline: scaling for numeric columns, one-hot encoding for
   categorical ones, all inside a `Pipeline` so nothing leaks into the test set.
8. Trained three models: Logistic Regression, Decision Tree and Random Forest.
9. Compared them on accuracy, precision, recall, F1 and ROC-AUC, plus ROC curves.
10. Ran 5-fold cross-validation to confirm the scores are stable.
11. Retrained all three models on the original columns only, to prove the new features made a
    difference.
12. Evaluated the best model in detail and tested it on a new unseen order.

## Key Results

Test set, 1,680 rows:

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression | 0.8732 | 0.8595 | 0.8875 | 0.8733 | 0.9364 |
| Decision Tree | 0.9310 | 0.9309 | 0.9287 | 0.9298 | 0.9561 |
| **Random Forest** | **0.9458** | **0.9600** | **0.9287** | **0.9441** | **0.9888** |

5-fold cross-validation on the training set:

| Model | Mean Accuracy | Std Dev |
|---|---|---|
| Logistic Regression | 0.8695 | 0.0058 |
| Decision Tree | 0.9143 | 0.0061 |
| Random Forest | 0.9351 | 0.0082 |

Did the new features help? All three models were retrained on the original columns only:

| Model | Original features only | With new features | Improvement |
|---|---|---|---|
| Logistic Regression | 0.7917 | 0.8732 | +0.0815 |
| Decision Tree | 0.9071 | 0.9310 | +0.0239 |
| Random Forest | 0.9405 | 0.9458 | +0.0053 |

Compared to Week 2:

| | Accuracy | ROC-AUC |
|---|---|---|
| Week 2 best (Decision Tree, raw columns) | 0.8685 | 0.9296 |
| Week 3 best (Random Forest, new features) | 0.9458 | 0.9888 |

Confusion matrix for Random Forest: 821 true negatives, 768 true positives, 32 false positives,
59 false negatives.

## Which Model Is Better, and Why
**Random Forest** was chosen, based on three things rather than accuracy alone:

1. **Scores.** It has the highest accuracy, precision, F1 and ROC-AUC of the three.
2. **Stability.** Its cross-validation standard deviation is 0.0082, small enough that the score is
   not swinging between folds.
3. **Usefulness for Task 2.** It reports feature importances, which Task 2 needs to explain what
   drives the predictions.

Logistic Regression is the easiest model to explain but it is clearly the weakest here, which
matches the Week 2 conclusion that this problem is not linear. The trade-off with Random Forest is
that 200 trees are harder to explain than a single tree, and Task 2 addresses that using feature
importance.

## Reflection
**What I learned**
- Feature engineering made more difference than changing the algorithm. The same three models
  scored higher purely because they were given better inputs.
- The improvement was biggest for Logistic Regression (+0.0815) and smallest for Random Forest
  (+0.0053). That makes sense: a linear model depends heavily on being handed good features, while
  Random Forest can already find some of those patterns by combining raw columns itself.
- `Shipping Cost Ratio` came directly from an observation made during the Week 2 analysis, which
  showed that looking at the data properly first genuinely pays off.
- Retraining on the original columns was the only way to prove the improvement was real rather than
  assumed.

**Limitations**
- No cost-of-goods column exists in the data, so profitability can only be estimated.
- The split is random, so two lines from the same order can end up on opposite sides.
- No hyperparameter tuning was done, so none of the models are at their best.
- The decision threshold is left at the default 0.5.

**Next steps**
1. Split the data by `Order ID` instead of randomly, so a whole order stays on one side.
2. Try tuning the Random Forest with `GridSearchCV`.
3. Add customer-level features such as how many orders a customer has placed before.
4. Try a time-based split, training on earlier years and testing on later ones.
