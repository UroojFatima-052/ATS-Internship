# Task 2: Model Interpretation and Business Report

## Objective
Interpret the model selected in Task 1 using feature importance, then translate the technical
findings into a short business report covering key drivers, risks, limitations and recommended
actions.

## Project Structure
```
Task 02/
├── Model Interpretation.ipynb   # Main notebook (fully executed)
├── data/
│   └── sales_data.csv           # Same dataset as Task 1
├── screenshots/                 # Exported chart images (evidence of outputs)
│   ├── 01_feature_importance.png
│   ├── 02_importance_by_group.png
│   ├── 03_shipping_ratio_effect.png
│   ├── 04_loss_rate_by_subcategory.png
│   └── 05_loss_rate_by_segment.png
├── Report.docx                  # Written report, includes the full business report
└── README.md                    # This file
```

## Tools & Libraries Used
- Python 3
- pandas, numpy for data handling
- matplotlib, seaborn for data visualization
- scikit-learn for rebuilding the model and reading feature importances
- Jupyter Notebook

## How to Run
1. Install the required libraries:
   ```
   pip install pandas numpy matplotlib seaborn scikit-learn jupyter
   ```
2. Open a terminal in this folder and run:
   ```
   jupyter notebook "Model Interpretation.ipynb"
   ```
3. Run all cells from top to bottom.
4. Generated charts are saved automatically into the `screenshots/` folder.

The notebook rebuilds the Random Forest from Task 1 with the same settings and the same
`random_state=42`, then confirms the accuracy and ROC-AUC match Task 1 before interpreting it.

## Approach
A model that predicts well but cannot be explained is hard to trust and hard to act on. Two
questions are answered here:

1. **Which factors does the model rely on?** Answered with Random Forest's built-in feature
   importance.
2. **Which direction does each factor push?** Importance alone does not say whether high values are
   good or bad, so the top driver was split into five bands and the actual profit rate was measured
   in each band.

The interpretation was then checked by shuffling the top feature and measuring how much the model
got worse.

## Key Steps Performed
1. Rebuilt the Random Forest from Task 1 and confirmed the scores match (0.9458 accuracy,
   0.9888 ROC-AUC).
2. Extracted and plotted feature importances.
3. Grouped the importances into engineered features vs original columns.
4. Split `Shipping Cost Ratio` into five bands and measured the real profit rate and average profit
   in each.
5. Profiled loss rates across product sub-category, customer segment and ship mode.
6. Validated the interpretation by shuffling the top feature and a weak feature and comparing the
   damage.
7. Wrote the business report for a non-technical reader.

## Key Results

### Feature importance, top drivers
| Feature | Importance |
|---|---|
| **Shipping Cost Ratio** | **0.2334** |
| Shipping Cost | 0.1023 |
| Product Base Margin | 0.0925 |
| Order Quantity | 0.0853 |
| Sales | 0.0824 |
| Revenue Per Unit | 0.0716 |
| Unit Price | 0.0641 |
| Discount Value | 0.0419 |

`Shipping Cost Ratio` is more than twice as important as the next feature. It is one of the five
features created in Task 1, so the feature engineering did not just improve the score, it produced
the model's single most useful input.

### Importance by feature group
| Group | Total importance |
|---|---|
| Original numeric | 44.5% |
| Engineered (new) | 37.3% |
| Original categorical | 18.2% |

The five new features account for over a third of the model's decision making.

### Direction of the top driver
| Shipping Cost Ratio band | Orders | Profit rate | Average profit |
|---|---|---|---|
| Very Low | 1,680 | 90.4% | 1,106.74 |
| Low | 1,680 | 78.3% | 166.29 |
| Medium | 1,679 | 49.1% | -103.45 |
| High | 1,680 | 20.6% | -148.11 |
| Very High | 1,680 | 7.7% | -115.72 |

The pattern is clear and large. When shipping is a small share of the sale, 90% of orders make
money. When it is a large share, only 8% do.

### Riskiest sub-categories
| Sub-Category | Orders | Loss rate | Total profit |
|---|---|---|---|
| Bookcases | 189 | 78.3% | -33,582 |
| Scissors, Rulers and Trimmers | 144 | 76.4% | -7,799 |
| Tables | 361 | 71.5% | -99,062 |
| Storage & Organization | 546 | 69.4% | 6,664 |
| Paper | 1,225 | 59.3% | 45,263 |

### Validating the interpretation
| Condition | ROC-AUC |
|---|---|
| Normal | 0.9888 |
| After shuffling Shipping Cost Ratio | 0.8716 |
| After shuffling Order Month (a weak feature) | 0.9887 |

Scrambling the top feature costs 0.1172 of ROC-AUC. Scrambling a weak feature costs 0.0001. The
importance ranking is describing something real.

## Reflection
**What I learned**
- Feature importance only tells half the story. It says a feature matters, not whether high values
  are good or bad. Splitting the top feature into bands is what made the finding usable.
- The most important feature in the model was one created in Task 1, not one that came with the
  dataset.
- Shuffling a feature to test its importance was a simple check that made the conclusion far more
  convincing than a bar chart on its own.

**Limitations of this interpretation**
- Random Forest's built-in importance tends to favour numeric features with many possible values
  over categorical ones, so the ranking may slightly understate the categorical columns.
- Each feature was looked at on its own, so any effects that depend on combinations of features are
  not visible here.
- The analysis explains what the model does, which is not the same as explaining what actually
  causes profit in the business.

**Next steps**
1. Use permutation importance as a second opinion, since it is measured on test data and is less
   prone to the bias above.
2. Look at pairs of features together rather than one at a time.
3. Attach real money figures to the model's decisions so recommendations can be stated as an
   expected saving.
4. Re-check the model on newer orders after a few months, since business conditions change.
