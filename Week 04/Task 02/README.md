# Final Task 2: Model Deployment and Responsible Reporting

## Objective
Prepare the model selected in Final Task 1 for practical use: define an inference workflow, validate
inputs, check fairness, plan monitoring, and write a stakeholder report that is honest about the
model's limitations.

## Why this matters
A model sitting in a notebook helps nobody. But a model put in front of real users without input
checks, fairness checks or a monitoring plan is worse than no model, because people will trust it
without knowing when it is wrong.

## Project Structure
```
Task 02/
├── Model Deployment and Reporting.ipynb   # Main notebook (fully executed)
├── app.py                                 # Streamlit app, the working deployment
├── model/
│   ├── profit_model.joblib                # Saved trained model
│   ├── model_info.joblib                  # Category options, scores, metadata
│   └── baseline_stats.json                # Saved training-data snapshot for drift checks
├── data/
│   └── sales_data.csv
├── screenshots/                           # Evidence of outputs
│   ├── 01_validation_tests.png            # Input validation QA results (8/8 passed)
│   ├── 02_fairness_check.png              # Accuracy by region and category
│   ├── 03_drift_check.png                 # Monitoring drift check
│   ├── 04_app_form.png                    # The running app
│   ├── 05_app_borderline.png              # A borderline prediction with the warning
│   ├── 06_app_profitable.png              # A clearly profitable prediction
│   └── 07_app_validation_error.png        # Input validation rejecting bad input
├── Report.docx                            # Final written report, includes the stakeholder report
└── README.md                              # This file
```

## Tools & Libraries Used
- Python 3
- pandas, numpy for data handling
- matplotlib, seaborn for visualization
- scikit-learn for rebuilding the model
- joblib for saving and loading the model
- streamlit for the web app
- Jupyter Notebook

## How to Run

**The notebook:**
```
pip install pandas numpy matplotlib seaborn scikit-learn joblib jupyter
jupyter notebook "Model Deployment and Reporting.ipynb"
```
Run all cells top to bottom. This trains the model and saves the three files into `model/`.

**The app** (run the notebook first, so the model files exist):
```
pip install streamlit
streamlit run app.py
```
It opens at `http://localhost:8501`.

## The Inference Workflow
```
User fills in the form in app.py
        ↓
validate_input()  →  if anything is wrong, show an error and STOP
        ↓
build_features()  →  calculate the 4 engineered features from the raw inputs
        ↓
model.predict_proba()  →  probability of profit
        ↓
Show result + the reason behind it
```

**The key design decision:** the four engineered features (`Revenue Per Unit`,
`Shipping Cost Ratio`, `Discount Value`, `Order Month`) are calculated inside the app, not asked for
on the form. A user should enter sales and shipping cost, not be asked to work out a ratio. This
creates a rule though: the app's formulas must match the notebook's exactly, or every prediction is
quietly wrong.

## Input Validation (QA Evidence)
The model will accept almost anything and return a confident number. A negative quantity, a discount
of 5.0, shipping cost higher than the sale value: none of these raise an error, they just produce
nonsense. So inputs are checked before the model sees them.

**8 test cases, 8 passed:**

| Test case | Expected | Actual | Result |
|---|---|---|---|
| Normal valid order | accept | accepted | PASS |
| Zero quantity | reject | rejected | PASS |
| Negative quantity | reject | rejected | PASS |
| Zero sales | reject | rejected | PASS |
| Discount above 1 (500%) | reject | rejected | PASS |
| Negative discount | reject | rejected | PASS |
| Negative shipping cost | reject | rejected | PASS |
| Shipping cost above sale value | reject | rejected | PASS |

The last case is the interesting one. Shipping cost higher than the sale value is not impossible in
reality, but it is unusual enough to be far more likely a typing mistake, so the app asks the user
to check rather than silently predicting on it.

## Fairness Check
A model can have good overall accuracy while working badly for one group. Accuracy was measured
separately across regions, customer segments, product categories and ship modes.

| Result | Value |
|---|---|
| Overall test accuracy | 95.4% |
| Best group | Northwest Territories, 98.8% |
| Worst group | **Furniture, 91.2%** |
| Spread | 0.076 |

Across regions and customer segments the model is very even, every group within about one point of
overall.

**The one gap worth naming is Furniture, about 4 points below overall.** That is not large enough to
call the model unfair, but it is not a coincidence either: Furniture is the category with the most
bulky, high-shipping products, which is exactly the case the model finds hardest to call. Furniture
predictions should be treated with a little more caution, and the gap should be watched after
deployment rather than assumed to stay small.

## Monitoring Plan
A model does not stay accurate on its own. The data it sees in six months will not look like the
data it was trained on, and when that happens it degrades quietly. No error appears, the predictions
just get worse.

`baseline_stats.json` saves a snapshot of the training data (mean, median, std and 5th/95th
percentiles for every numeric column, plus category shares) so future data can be compared against
it. The `check_drift()` function flags any column whose mean has moved more than 0.25 standard
deviations.

| What to track | How often | Action if it moves |
|---|---|---|
| Feature drift | Monthly | Investigate the flagged column. A pricing or shipping change is the usual cause |
| Real accuracy, once actual profit is known | Quarterly | Retrain if it falls more than 5 points below 95% |
| Share of orders predicted profitable | Monthly | A sudden swing usually means the input data changed |
| Fairness gaps across groups | Quarterly | Investigate any group 5+ points below overall |
| Rejected inputs in the app | Monthly | A spike suggests users are confused by a form field |

**The quarterly accuracy check matters most.** Everything else is a proxy. Once the real profit
figures come in, predictions can be compared against what actually happened, and that is the only
measurement that truly counts.

## Demo Evidence
Screenshots 05 and 06 are worth viewing together. The only thing changed between them is the
shipping cost, from 15 to 6 on a 500 sale, and the prediction moves from **43.5%** to **94.6%**
probability of profit. That is the model's top driver visible in the live app.

Screenshot 07 shows the validation layer rejecting a shipping cost higher than the sale value,
with a plain-language message rather than a crash or a nonsense prediction.

## Challenges
- **Where to calculate the engineered features.** The model needs `Shipping Cost Ratio`, but asking
  a user to type a ratio is bad form design and an easy place to introduce errors. Calculating it in
  the app solved this but created the matching-formulas rule above.
- **What counts as invalid input.** Shipping cost higher than the sale value is unusual but not
  impossible. Rejecting it outright would block a real case; accepting it silently would hide a
  typo. Warning the user and asking them to check was the middle option.
- **Keeping dropdown options in sync.** Hard-coding them would have worked today and broken the
  first time the data changed, so they are saved alongside the model in `model_info.joblib`.

## Limitations of this Deployment
1. **It runs locally.** Someone has to start it with `streamlit run app.py`. A real deployment needs
   hosting so people can just open a link.
2. **One order at a time.** No way to upload a spreadsheet and check a hundred orders at once, which
   is probably how it would actually get used.
3. **Nothing is logged.** Predictions are not saved, so the quarterly accuracy check would have to
   be done by hand.
4. **The drift check is manual.** It runs in the notebook rather than on a schedule.
5. **No login.** Anyone with the app can use it.

## Future Improvements
1. Host it on Streamlit Community Cloud or Hugging Face Spaces for a shareable link.
2. Add batch upload so a CSV of orders can be checked in one go.
3. Log every prediction with inputs and timestamp, making the quarterly accuracy check automatic.
4. Automate the drift check to run monthly.
5. Add cost-of-goods data and retrain. Still the highest-value improvement available.
6. Tune the decision threshold using the real cost of a wrong approval versus a wrong rejection.
