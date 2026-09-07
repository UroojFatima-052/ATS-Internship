# Task 1: Exploratory Data Analysis (EDA) on the Superstore Sales Dataset

## Objective
Perform industry-style Exploratory Data Analysis on a real sales dataset, covering data cleaning,
missing-value analysis, descriptive statistics, outlier checks, correlation analysis and
informative visualizations, then summarize the main business findings.

## Project Structure
```
Task 01/
├── Sales EDA.ipynb          # Main Jupyter Notebook (source file, fully executed)
├── data/
│   └── sales_data.csv       # Dataset used (8,399 rows, 21 columns)
├── screenshots/             # Exported chart images (evidence of outputs)
│   ├── 01_missing_values_map.png
│   ├── 02_outlier_boxplots.png
│   ├── 03_sales_profit_distribution.png
│   ├── 04_sales_profit_by_category_region.png
│   ├── 05_profit_by_subcategory.png
│   ├── 06_discount_vs_profit.png
│   ├── 07_correlation_heatmap.png
│   └── 08_monthly_sales_trend.png
├── Report.docx              # Written report summarizing methodology & findings
└── README.md                # This file
```

## Tools & Libraries Used
- Python 3
- pandas, numpy for data handling and cleaning
- matplotlib, seaborn for data visualization
- Jupyter Notebook

## How to Run
1. Make sure Python 3 and Jupyter are installed.
2. Install the required libraries:
   ```
   pip install pandas numpy matplotlib seaborn jupyter
   ```
3. Open a terminal in this folder and run:
   ```
   jupyter notebook "Sales EDA.ipynb"
   ```
4. Run all cells from top to bottom.
5. Generated charts are saved automatically into the `screenshots/` folder.

## Dataset
Superstore Sales, **8,399 rows and 21 columns** covering four years of trading (January 2009 to
December 2012). Each row is one product line inside a customer order, so the 8,399 rows belong to
5,496 unique orders placed by 795 customers across 1,263 products.

Main columns: `Order Date`, `Ship Date`, `Order Priority`, `Order Quantity`, `Sales`, `Discount`,
`Ship Mode`, `Profit`, `Unit Price`, `Shipping Cost`, `Region`, `Customer Segment`,
`Product Category`, `Product Sub-Category`, `Product Container`, `Product Base Margin`.

## Key Steps Performed
1. Loaded and inspected the dataset (shape, dtypes, duplicates, unique counts).
2. Cleaned the data: parsed `Order Date` and `Ship Date` into real dates, derived a
   `Shipping Delay` column, and validated that no record has negative delays, zero sales or zero
   quantity.
3. Ran a missing-value analysis (count, percentage and a missing-value map) and filled the only
   affected column, `Product Base Margin`, using the median of its product category.
4. Produced descriptive statistics for every numeric column and value counts for every categorical
   column.
5. Detected outliers with the IQR rule across eight numeric columns and documented the decision to
   keep them.
6. Univariate analysis: distribution of `Sales` and `Profit`.
7. Bivariate analysis: sales and profit by product category and region, profit by sub-category,
   discount against profit.
8. Correlation analysis using a heatmap of all numeric features.
9. Time-series view of monthly sales and profit across the four-year period.
10. Summarized findings and listed improvements for the next iteration.


## Key Findings
| Finding | Detail |
|---|---|
| Data quality | Only `Product Base Margin` had gaps: 63 values, 0.75% of the dataset. No duplicate rows. |
| Total sales | 14,915,601 across four years |
| Total profit | 1,521,768 |
| Loss-making order lines | **4,264 rows, 50.8% of the dataset** |
| Most profitable category | Technology (886,314 profit from 5,984,248 sales) |
| Weakest category | Furniture (117,433 profit from 5,178,591 sales) |
| Worst sub-category | Tables, at a loss of 99,062 |
| Sales to Profit correlation | 0.58, only moderate |
| Discount effect | Average profit falls from 231 in the lowest discount band to negative in the highest, and the loss rate climbs from 47% to 56% |

- **Roughly half of all order lines lose money.** This is the headline finding and it is what
  Task 2 goes on to model.
- Money columns are heavily right-skewed with many statistical outliers. These were **kept**, since
  a 10,000 sale or a 14,000 loss is a genuine business event and removing them would hide exactly
  the transactions worth understanding.
- Revenue does not imply profit. Furniture sells almost as much as Technology but returns roughly a
  seventh of the profit.
- Sales and profit are volatile month to month with no clear seasonality, and profit stays close to
  break-even across the whole four-year period.

## Key Lessons and Improvements for the Next Iteration
- Filling missing margins with a category median is quick but crude. Filling at the sub-category or
  product level would be more accurate.
- Keeping outliers is right for a business report, but a modelling task should also test a capped
  or log-transformed version of `Sales`.
- The analysis runs at the order-line level. Rolling it up to whole orders or to customers would
  answer different questions, such as which customers are unprofitable overall.
- The dataset has no cost-of-goods column, so the cause of each loss can only be inferred. Adding
  cost data would make the profit analysis conclusive.
