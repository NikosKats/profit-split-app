import math
import streamlit as st

st.set_page_config(page_title="Prop Split + Reverse (Dubai • Cyprus • Bulgaria)", page_icon="📈", layout="centered")

st.title("📈 Prop Split + Reverse (Dubai • Cyprus • Bulgaria)")
st.caption("Profit split quick math + reverse after-tax calculators (Dubai, Cyprus, Bulgaria).")

# ---------- Shared split
st.divider()
your_split = st.number_input(
    "Your split (%)",
    min_value=0.0, max_value=100.0, value=80.0, step=1.0,
    help="Example: 80 means you keep 80% of the gross PnL."
)
s = your_split / 100.0

# ---------- Tabs
tab_ps_req, tab_ps_take, tab_reverse_ae, tab_reverse_cy, tab_reverse_bg = st.tabs([
    "Profit Split → Required Gross",
    "Profit Split ← Your Take-Home",
    "Reverse (Dubai)",
    "Reverse (Cyprus)",
    "Reverse (Bulgaria)",
])

# =========================
# Profit Split — Required Gross
# =========================
with tab_ps_req:
    st.subheader("Required Gross → Target Take-Home (pre-tax)")
    target = st.number_input("Target take-home (pre-tax)", min_value=0.0, value=1000.0, step=100.0, format="%.2f")
    if s <= 0:
        st.error("Your split must be greater than 0%.")
    else:
        required_gross = target / s
        st.metric("Required gross PnL", f"{required_gross:,.2f}")
        with st.expander("Formula"):
            st.code("Required Gross = Target / (Your Split)")

# =========================
# Profit Split — Your Take-Home
# =========================
with tab_ps_take:
    st.subheader("Your Take-Home ← Gross PnL (pre-tax)")
    gross = st.number_input("Gross PnL", value=1250.0, step=100.0, format="%.2f")
    take_home = gross * s
    st.metric("Your take-home (pre-tax)", f"{take_home:,.2f}")
    with st.expander("Formula"):
        st.code("Take-Home = Gross PnL × (Your Split)")

# =========================
# Helper for allowance + flat %
# =========================
def reverse_with_threshold(target_after_tax: float, threshold: float, flat_rate: float):
    """
    Simple 'allowance + flat % above' model:
    Net = min(T, threshold) + (T - threshold)*(1 - r) if T > threshold.
    Inversion:
      if Net <= threshold → T = Net
      else T = threshold + (Net - threshold)/(1 - r)
    """
    r = flat_rate / 100.0
    if r >= 1.0:
        return 0.0
    if target_after_tax <= threshold:
        return target_after_tax
    return threshold + (target_after_tax - threshold) / (1.0 - r)

# =========================
# Reverse (Dubai)
# =========================
with tab_reverse_ae:
    st.subheader("🕌 Reverse (Dubai): Target After-Tax → Required Gross")

    target_after_tax_ae = st.number_input("Target after-tax net (Dubai)", min_value=0.0, value=1000.0, step=100.0, format="%.2f")
    ae_regime = st.radio(
        "Treatment (Dubai)",
        ["Individual (0% personal income tax)", "Company (apply corporate tax %)"],
        index=0
    )

    if ae_regime == "Individual (0% personal income tax)":
        required_take_home_ae = target_after_tax_ae
    else:
        corp_rate = st.number_input("Corporate tax rate (%)", min_value=0.0, max_value=100.0, value=9.0, step=0.5)
        if (1 - corp_rate/100.0) <= 0:
            st.error("Invalid corporate tax rate (must be < 100%).")
            required_take_home_ae = 0.0
        else:
            required_take_home_ae = target_after_tax_ae / (1 - corp_rate/100.0) if target_after_tax_ae > 0 else 0.0

    if s <= 0:
        st.error("Your split must be greater than 0% to compute required gross.")
    else:
        required_gross_ae = required_take_home_ae / s
        st.metric("Required pre-tax take-home (Dubai)", f"{required_take_home_ae:,.2f}")
        st.metric("Required gross PnL (given your split)", f"{required_gross_ae:,.2f}")

# =========================
# Reverse (Cyprus)
# =========================
with tab_reverse_cy:
    st.subheader("🇨🇾 Reverse (Cyprus): Target After-Tax → Required Gross")

    target_after_tax_cy = st.number_input("Target after-tax net (Cyprus)", min_value=0.0, value=1000.0, step=100.0, format="%.2f")
    cy_regime = st.radio(
        "Treatment (Cyprus)",
        ["Individual (allowance + flat % above)", "Company (apply corporate tax %)"],
        index=0
    )

    if cy_regime == "Individual (allowance + flat % above)":
        cy_allowance = st.number_input("Tax-free allowance (annual)", min_value=0.0, value=19_500.0, step=100.0)
        cy_rate = st.number_input("Flat rate above allowance (%)", min_value=0.0, max_value=100.0, value=20.0, step=0.5)
        required_take_home_cy = reverse_with_threshold(target_after_tax_cy, cy_allowance, cy_rate)
    else:
        cy_corp = st.number_input("Corporate tax rate (%)", min_value=0.0, max_value=100.0, value=12.5, step=0.5)
        if (1 - cy_corp/100.0) <= 0:
            st.error("Invalid corporate tax rate (must be < 100%).")
            required_take_home_cy = 0.0
        else:
            required_take_home_cy = target_after_tax_cy / (1 - cy_corp/100.0) if target_after_tax_cy > 0 else 0.0

    if s <= 0:
        st.error("Your split must be greater than 0% to compute required gross.")
    else:
        required_gross_cy = required_take_home_cy / s
        st.metric("Required pre-tax take-home (Cyprus)", f"{required_take_home_cy:,.2f}")
        st.metric("Required gross PnL (given your split)", f"{required_gross_cy:,.2f}")

# =========================
# Reverse (Bulgaria)
# =========================
with tab_reverse_bg:
    st.subheader("🇧🇬 Reverse (Bulgaria): Target After-Tax → Required Gross")

    target_after_tax_bg = st.number_input("Target after-tax net (Bulgaria)", min_value=0.0, value=1000.0, step=100.0, format="%.2f")
    bg_regime = st.radio(
        "Treatment (Bulgaria)",
        ["Individual (flat % with optional allowance)", "Company (apply corporate tax %)"],
        index=0
    )

    if bg_regime == "Individual (flat % with optional allowance)":
        bg_allowance = st.number_input("Tax-free allowance (annual)", min_value=0.0, value=0.0, step=100.0)
        bg_rate = st.number_input("Flat personal tax rate (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
        required_take_home_bg = reverse_with_threshold(target_after_tax_bg, bg_allowance, bg_rate)
    else:
        bg_corp = st.number_input("Corporate tax rate (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
        if (1 - bg_corp/100.0) <= 0:
            st.error("Invalid corporate tax rate (must be < 100%).")
            required_take_home_bg = 0.0
        else:
            required_take_home_bg = target_after_tax_bg / (1 - bg_corp/100.0) if target_after_tax_bg > 0 else 0.0

    if s <= 0:
        st.error("Your split must be greater than 0% to compute required gross.")
    else:
        required_gross_bg = required_take_home_bg / s
        st.metric("Required pre-tax take-home (Bulgaria)", f"{required_take_home_bg:,.2f}")
        st.metric("Required gross PnL (given your split)", f"{required_gross_bg:,.2f}")

# ---------- Footer
with st.expander("General notes"):
    st.markdown(
        "- Profit Split tabs are **pre-tax** quick math.\n"
        "- Reverse tabs use **simple, editable models**:\n"
        "  - **Dubai:** Individuals 0% personal tax; Company = single-rate model.\n"
        "  - **Cyprus:** allowance + flat rate above it (editable); Company = single corporate rate.\n"
        "  - **Bulgaria:** flat % (optional allowance); Company = single corporate rate.\n"
        "- Results are estimates only — not tax advice."
    )

st.caption("Built for prop traders: fast split math + reverse after-tax estimates (Dubai, Cyprus, Bulgaria).")
