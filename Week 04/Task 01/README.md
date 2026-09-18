# Final Task 1: End-to-End Machine Learning Project

## Objective
Complete an end-to-end machine learning project from problem definition and data validation through
EDA, feature engineering, train/validation/test design, baseline modeling, model comparison,
evaluation, interpretation and a final recommendation.

## Project Structure
```
Task 01/
├── End-to-End ML Project.ipynb   # Main notebook (fully executed)
├── data/
│   └── sales_data.csv            # Dataset (8,399 rows, 21 columns)
├── screenshots/                  # Exported chart images (evidence of outputs)
│   ├── 01_eda_overview.png
│   ├── 02_correlation.png
│   ├── 03_feature_check.png
│   ├── 04_model_comparison.png
│   ├── 05_final_test_evaluation.png
│   └── 06_feature_importance.png
├── Report.docx                   # Final written report
└── README.md                     # This file
```

## Tools & Libraries Used
- Python 3
- pandas, numpy for data handling
- matplotlib, seaborn for visualization
- scikit-learn for preprocessing, modeling and evaluation
- Jupyter Notebook

## How to Run
1. Install the required libraries:
   ```
   pip install pandas numpy matplotlib seaborn scikit-learn jupyter
   ```
2. Open a terminal in this folder and run:
   ```
   jupyter notebook "End-to-End ML Project.ipynb"
   ```
3. Run all cells from top to bottom.
4. Charts are saved automatically into `screenshots/`.

## The Problem
**Business problem:** just over half of all order lines lose money. Sales look healthy while profit
does not. The business needs to know which orders are risky before they are fulfilled.

**ML problem:** binary classification. Predict `Profitable = 1` if the order made money, `0` if not.

**Why classification and not regression:** predicting the exact profit amount is harder and less
reliable, and a manager mainly needs to know whether to look at an order more closely, which is a
yes or no question.

**Success criteria, set before any modeling:**

| Criterion | Target | Result | Status |
|---|---|---|---|
| Beats majority-class guessing | Above 50.8% | 95.4% | PASS |
| Useful enough to act on | At least 85% accuracy | 95.4% | PASS |
| Balanced errors | Precision above 0.80 | 0.965 | PASS |
| Balanced errors | Recall above 0.80 | 0.940 | PASS |
| Explainable | Drivers can be named | Yes | PASS |

Setting these first matters, otherwise it is too easy to look at whatever score comes out and
declare it good.

## Key Steps Performed
1. **Data validation.** Six checks: duplicates, missing values, negative/zero sales, negative/zero
   quantity, discount out of range, and orders shipped before they were placed. Five passed. The
   only issue was 63 missing `Product Base Margin` values (0.75%).
2. **Missing value handling.** Filled with the median margin of the same product category, which is
   more accurate than one global median and keeps every sale in the dataset.
3. **EDA.** Only the findings that changed a modeling decision were kept.
4. **Feature engineering.** Five new features, each tied to an EDA finding.
5. **Three-way split.** Train 60% / validation 20% / test 20%, all stratified.
6. **Baseline.** A dummy classifier that always guesses the majority class, scoring 50.8%.
7. **Model comparison.** Four models compared on the validation set.
8. **Final evaluation.** The test set opened once, at the end.
9. **Interpretation.** Feature importance plus a band analysis showing direction.
10. **Recommendation.**

## Why a Three-Way Split
Weeks 2 and 3 used a simple train/test split. That has a problem: if you compare several models on
the test set and pick the winner, you have used the test set to make a decision, so its score is no
longer a fair estimate. The winner was partly selected by luck on those specific rows.

The fix is three sets, each with one job:

| Set | Size | Job |
|---|---|---|
| Training | 60% (5,039 rows) | The models learn from this |
| Validation | 20% (1,680 rows) | Models are compared here, and the winner chosen |
| Test | 20% (1,680 rows) | Opened once at the end, never used to decide anything |

## The Five Engineered Features
| Feature | Formula | Reason |
|---|---|---|
| Shipping Delay | Ship Date - Order Date | A slow shipment can point to a bulky or awkward product |
| Revenue Per Unit | Sales / Order Quantity | Separates cheap bulk orders from expensive small ones |
| Shipping Cost Ratio | Shipping Cost / Sales | EDA showed sales does not equal profit; this measures what shipping eats |
| Discount Value | Sales x Discount | 10% off a 5,000 order differs from 10% off a 50 order |
| Order Month | Month of Order Date | Allows the model to pick up seasonality |

## Key Results

Model comparison on the **validation** set:

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression | 0.8720 | 0.8600 | 0.8839 | 0.8718 | 0.9333 |
| Decision Tree | 0.9065 | 0.9026 | 0.9081 | 0.9054 | 0.9373 |
| Random Forest | 0.9327 | 0.9429 | 0.9190 | 0.9308 | 0.9824 |
| **Gradient Boosting** | **0.9345** | **0.9487** | 0.9166 | **0.9323** | **0.9841** |

Baseline (always guess majority class): 0.5077

Final evaluation of Gradient Boosting on the **held-out test set**:

| Metric | Validation | Test (final) |
|---|---|---|
| Accuracy | 0.9345 | 0.9536 |
| Precision | 0.9487 | 0.9652 |
| Recall | 0.9166 | 0.9395 |
| F1 | 0.9323 | 0.9522 |
| ROC-AUC | 0.9841 | 0.9886 |

Confusion matrix on the test set: 825 true negatives, 777 true positives, 28 false positives,
50 false negatives.

The test score came out slightly higher than validation. That is normal variation for two 1,680-row
sets drawn randomly. What matters is that they are close. A test score far *below* validation would
mean the model had been over-fitted to the validation set during selection.

### Top drivers
| Feature | Importance |
|---|---|
| **Shipping Cost Ratio** | **0.5887** |
| Product Base Margin | 0.1776 |
| Order Quantity | 0.1285 |
| Shipping Cost | 0.0207 |

Direction, from splitting `Shipping Cost Ratio` into five bands:

| Band | Orders | Profit rate | Average profit |
|---|---|---|---|
| Very Low | 1,680 | 90.4% | 1,106.74 |
| Low | 1,680 | 78.3% | 166.29 |
| Medium | 1,679 | 49.1% | -103.45 |
| High | 1,680 | 20.6% | -148.11 |
| Very High | 1,680 | 7.7% | -115.72 |

## Final Recommendation
**Adopt the model as a warning system, not as an automatic gatekeeper.** It should flag high-risk
orders for a person to review rather than reject them on its own. The reason is in the confusion
matrix: it makes mistakes in both directions, so automatic rejection would turn away 50 genuinely
profitable orders out of every 1,680.

**The most valuable business action does not need the model at all.** Shipping cost as a share of
the sale is the dominant driver, so reviewing shipping on cheap, bulky products is the highest-value
step available.

## Challenges
- **Outliers.** Sales and Profit contain many statistical outliers, but a 10,000 order or a large
  loss is a real business event, not a data error. Removing them would hide exactly the transactions
  the business needs to see, so they were kept.
- **Avoiding accidental cheating.** `Profit` had to be dropped from the features since the target is
  derived from it. Leaving it in would have produced a near-perfect score that meant nothing.
- **Trusting the score.** Comparing four models on a test set and reporting that score would have
  been optimistic. The validation set solved this, at the cost of a smaller training set.

## Limitations
1. No cost-of-goods column, which is a hard ceiling on accuracy.
2. Predictions are per order line, not per customer, so a loss-leader that wins a valuable account
   looks like a plain failure.
3. Random split, so two lines from the same order can land in different sets.
4. No hyperparameter tuning, so the model is probably not at its best.
5. Threshold fixed at 0.5, which assumes a wrong approval costs the same as a wrong rejection.
6. Trained on four-year-old historical data.

## Future Improvements
1. Add cost-of-goods data. Every other limitation is smaller than this one.
2. Split by `Order ID` so a whole order stays in one set.
3. Tune the chosen model with `GridSearchCV`.
4. Add customer-level features, such as how many orders a customer has placed before.
5. Set the decision threshold from real business costs instead of leaving it at 0.5.
6. Deploy it and monitor it, which is what Final Task 2 covers.
