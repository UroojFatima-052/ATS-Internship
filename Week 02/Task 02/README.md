# Task 2: Baseline Predictive Model on the Superstore Sales Dataset

## Objective
Build a baseline supervised-learning model on the same sales dataset used in Task 1, following
standard practice: define the problem, split the data correctly, preprocess the features, train a
baseline model, evaluate it with appropriate metrics, and explain its limitations.

## Problem Framing
Task 1 found that **50.8% of all order lines lose money**. So the useful question is not "how much
will this order sell for" but **"will this order line be profitable or not"**.

That makes this a **binary classification** problem, with the target `Profitable` = 1 when
`Profit > 0`, else 0.

## Project Structure
```
Task 02/
├── Profit Prediction.ipynb  # Main Jupyter Notebook (source file, fully executed)
├── data/
│   └── sales_data.csv       # Dataset used (8,399 rows, 21 columns)
├── screenshots/             # Exported chart images (evidence of outputs)
│   ├── 01_target_distribution.png
│   ├── 02_confusion_matrix.png
│   ├── 03_roc_curve.png
│   ├── 04_model_comparison.png
│   └── 05_feature_importance.png
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
   jupyter notebook "Profit Prediction.ipynb"
   ```
4. Run all cells from top to bottom.
5. Generated charts are saved automatically into the `screenshots/` folder.

## Dataset and Features
The same Superstore Sales dataset as Task 1 (8,399 rows, 21 columns). The cleaning steps from Task
1 are repeated at the top of this notebook so it runs standalone.

**Target:** `Profitable` (1 if `Profit > 0`, else 0). Class balance is 49.2% profitable against
50.8% not, so the classes are almost even and no resampling is needed.

**Numeric features (7):** `Order Quantity`, `Sales`, `Discount`, `Unit Price`, `Shipping Cost`,
`Product Base Margin`, `Shipping Delay`

**Categorical features (7):** `Order Priority`, `Ship Mode`, `Region`, `Customer Segment`,
`Product Category`, `Product Sub-Category`, `Product Container`

**Dropped on purpose:** `Profit` (the target is derived from it, keeping it would leak the answer),
`Row ID`, `Order ID`, `Customer Name`, `Product Name`, `Province`, `Order Date`, `Ship Date`.

After one-hot encoding, 14 input columns become 54 model columns.

## Key Steps Performed
1. Loaded and re-applied the Task 1 cleaning steps.
2. Created the binary target and checked class balance.
3. Selected features and removed leaking, ID and free-text columns.
4. Split 80/20 with `stratify=y` and a fixed `random_state=42`.
5. Built a `ColumnTransformer` pipeline: `StandardScaler` on numeric columns, `OneHotEncoder` on
   categorical columns, wrapped in a `Pipeline` so preprocessing is fitted on training data only
   and nothing leaks into the test set.
6. Trained the baseline model, Logistic Regression.
7. Evaluated with accuracy, precision, recall, F1, ROC-AUC, a classification report and a confusion
   matrix, plus an ROC curve.
8. Trained a shallow Decision Tree (`max_depth=5`) on the same pipeline as a comparison.
9. Ran 5-fold cross-validation on both models to confirm the scores are stable.
10. Inspected logistic regression coefficients to see which features drive the prediction.
11. Tested the trained model on two new, unseen orders.
12. Documented limitations and next steps.


## Key Results
| Metric | Logistic Regression (baseline) | Decision Tree (depth 5) |
|---|---|---|
| Accuracy | 0.7929 | **0.8685** |
| Precision | 0.8028 | **0.8704** |
| Recall | 0.7678 | **0.8609** |
| F1 Score | 0.7849 | **0.8657** |
| ROC-AUC | 0.8657 | **0.9296** |

**Majority-class baseline for comparison: 50.8% accuracy.** Both models beat it comfortably.

5-fold cross-validation on the training set:

| Model | Mean Accuracy | Std Dev |
|---|---|---|
| Logistic Regression | 0.7875 | 0.0070 |
| Decision Tree (depth 5) | 0.8464 | 0.0130 |

Confusion matrix for the baseline model on 1,680 test rows: 697 true negatives, 635 true positives,
156 false positives, 192 false negatives.

**Interpretation:** the Decision Tree beats the linear baseline on every metric, which says the
relationship between the features and profitability is not linear. The strongest coefficients in
the logistic model are `Sales` (pushes towards profitable), `Shipping Cost` and
`Product Base Margin` (push towards a loss), with a lot of the remaining signal carried by
`Product Sub-Category`, which matches the Task 1 finding that profitability is very uneven across
sub-categories.

## Limitations
1. **No cost-of-goods data**, so profitability can only be inferred from price, discount and
   shipping. That is a hard ceiling on accuracy.
2. **Row-level, not order-level.** Lines from the same order can end up on opposite sides of the
   train/test split, which is a mild form of leakage.
3. **Random split ignores time.** Real forecasting would train on earlier years and test on later
   ones.
4. **No hyperparameter tuning.** Defaults throughout, apart from capping tree depth. Deliberate for
   a baseline, but neither model is at its best.
5. **Fixed 0.5 decision threshold**, even though approving a losing order and rejecting a good one
   almost certainly cost the business different amounts.
6. **Linear model on a non-linear problem**, which is exactly why the shallow tree wins.

## Key Lessons and Improvements for the Next Iteration
- Group the split by `Order ID` using `GroupShuffleSplit` so no order is spread across train and
  test.
- Try a time-based split, training on 2009 to 2011 and testing on 2012, which matches how the model
  would actually be used.
- Add engineered features such as revenue per unit, shipping cost as a share of sales, and order
  month.
- Tune the decision threshold against a real cost matrix instead of leaving it at 0.5.
- Once the baseline is solid, move to an ensemble such as Random Forest or Gradient Boosting and
  compare it fairly against these numbers.
- Log every experiment's metrics in one table so improvements are measurable rather than assumed.
