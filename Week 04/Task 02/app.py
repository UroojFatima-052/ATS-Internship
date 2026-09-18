"""
Order Profitability Checker
---------------------------
A small Streamlit app that loads the trained model and predicts whether a
sales order will make money or lose money.

Run it with:
    streamlit run app.py
"""

import joblib
import pandas as pd
import streamlit as st

MODEL_PATH = "model/profit_model.joblib"
INFO_PATH = "model/model_info.joblib"

st.set_page_config(page_title="Order Profitability Checker", page_icon="📦",
                   layout="centered")


@st.cache_resource
def load_model():
    """Load the model once and keep it in memory."""
    return joblib.load(MODEL_PATH), joblib.load(INFO_PATH)


def validate_input(quantity, sales, discount, unit_price, shipping_cost,
                   margin, shipping_delay):
    """Check the inputs make sense before sending them to the model.

    Returns a list of error messages. An empty list means the input is fine.
    """
    errors = []

    if quantity <= 0:
        errors.append("Order quantity must be greater than 0.")
    if sales <= 0:
        errors.append("Sales must be greater than 0.")
    if unit_price <= 0:
        errors.append("Unit price must be greater than 0.")
    if not 0 <= discount <= 1:
        errors.append("Discount must be between 0 and 1.")
    if not 0 <= margin <= 1:
        errors.append("Product base margin must be between 0 and 1.")
    if shipping_cost < 0:
        errors.append("Shipping cost cannot be negative.")
    if shipping_delay < 0:
        errors.append("Shipping delay cannot be negative.")
    if shipping_cost > sales:
        errors.append("Shipping cost is higher than the sale value. Please check the numbers.")

    return errors


def build_features(quantity, sales, discount, unit_price, shipping_cost,
                   margin, shipping_delay, month, priority, ship_mode,
                   region, segment, category, sub_category, container):
    """Turn the form inputs into the exact row layout the model expects."""
    return pd.DataFrame([{
        "Order Quantity": quantity,
        "Sales": sales,
        "Discount": discount,
        "Unit Price": unit_price,
        "Shipping Cost": shipping_cost,
        "Product Base Margin": margin,
        "Shipping Delay": shipping_delay,
        "Revenue Per Unit": sales / quantity,
        "Shipping Cost Ratio": shipping_cost / sales,
        "Discount Value": sales * discount,
        "Order Month": month,
        "Order Priority": priority,
        "Ship Mode": ship_mode,
        "Region": region,
        "Customer Segment": segment,
        "Product Category": category,
        "Product Sub-Category": sub_category,
        "Product Container": container,
    }])


model, info = load_model()

st.title("📦 Order Profitability Checker")
st.write(
    "Enter the details of a sales order and the model will predict whether it is "
    "likely to make money or lose money."
)

with st.expander("About this model"):
    st.write(f"**Model type:** {info['model_name']}")
    st.write(f"**Test accuracy:** {info['test_accuracy']:.1%}")
    st.write(f"**Trained on:** {info['training_rows']:,} order lines")
    st.write(
        "**Important:** this is a decision support tool, not an automatic approval system. "
        "It makes mistakes in both directions, so a flagged order should be reviewed by a "
        "person rather than rejected outright."
    )

st.subheader("Order details")

col1, col2 = st.columns(2)

with col1:
    quantity = st.number_input("Order quantity", min_value=1, value=10, step=1)
    sales = st.number_input("Sales value", min_value=0.01, value=500.00, step=10.0)
    unit_price = st.number_input("Unit price", min_value=0.01, value=50.00, step=1.0)
    discount = st.slider("Discount", 0.0, 0.5, 0.05, 0.01)

with col2:
    shipping_cost = st.number_input("Shipping cost", min_value=0.0, value=15.00, step=1.0)
    margin = st.slider("Product base margin", 0.0, 1.0, 0.50, 0.01)
    shipping_delay = st.number_input("Shipping delay (days)", min_value=0, value=3, step=1)
    month = st.selectbox("Order month", list(range(1, 13)), index=5)

st.subheader("Product and customer")

col3, col4 = st.columns(2)

with col3:
    category = st.selectbox("Product category", info["categories"]["Product Category"])
    sub_category = st.selectbox("Product sub-category", info["categories"]["Product Sub-Category"])
    container = st.selectbox("Product container", info["categories"]["Product Container"])
    priority = st.selectbox("Order priority", info["categories"]["Order Priority"])

with col4:
    region = st.selectbox("Region", info["categories"]["Region"])
    segment = st.selectbox("Customer segment", info["categories"]["Customer Segment"])
    ship_mode = st.selectbox("Ship mode", info["categories"]["Ship Mode"])

st.write("")

if st.button("Check this order", type="primary", use_container_width=True):

    errors = validate_input(quantity, sales, discount, unit_price,
                            shipping_cost, margin, shipping_delay)

    if errors:
        st.error("Please fix the following before checking:")
        for e in errors:
            st.write("- " + e)
    else:
        row = build_features(quantity, sales, discount, unit_price, shipping_cost,
                             margin, shipping_delay, month, priority, ship_mode,
                             region, segment, category, sub_category, container)

        prediction = model.predict(row)[0]
        probability = model.predict_proba(row)[0, 1]

        st.write("---")

        if prediction == 1:
            st.success(f"### Likely PROFITABLE\nProbability of profit: **{probability:.1%}**")
        else:
            st.error(f"### Likely to LOSE MONEY\nProbability of profit: **{probability:.1%}**")

        if 0.40 <= probability <= 0.60:
            st.warning(
                "This order sits close to the borderline, so the model is not confident "
                "either way. Worth a closer look by a person."
            )

        st.write("**Why:**")
        ratio = shipping_cost / sales
        st.write(f"- Shipping is **{ratio:.1%}** of the sale value "
                 f"({'high, this is the main risk factor' if ratio > 0.05 else 'low, which is good'})")
        st.write(f"- Revenue per unit is **{sales / quantity:,.2f}** "
                 f"({'low, cheap items are riskier' if sales / quantity < 50 else 'healthy'})")
        st.write(f"- Discount gives away **{sales * discount:,.2f}**")

st.write("---")
st.caption(
    "Shipping cost as a share of the sale is the strongest driver in this model. "
    "Orders where shipping takes a small share make money about 90% of the time; "
    "orders where it takes a large share make money less than 10% of the time."
)
