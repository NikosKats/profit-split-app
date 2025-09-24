import math
import streamlit as st

st.set_page_config(page_title="Prop Split + Reverse", page_icon="📈", layout="centered")

# ---------- Language dictionaries
translations = {
    "en": {
        "title": "📈 Prop Split + Reverse (Dubai • Cyprus • Bulgaria)",
        "subtitle": "Profit split quick math + reverse after-tax calculators.",
        "split_label": "Your split (%)",
        "split_help": "Example: 80 means you keep 80% of the gross PnL.",
        "ps_req": "Profit Split → Required Gross",
        "ps_take": "Profit Split ← Your Take-Home",
        "rev_ae": "Reverse (Dubai)",
        "rev_cy": "Reverse (Cyprus)",
        "rev_bg": "Reverse (Bulgaria)",
        "req_gross_title": "Required Gross → Target Take-Home (pre-tax)",
        "req_take_title": "Your Take-Home ← Gross PnL (pre-tax)",
        "target_take": "Target take-home (pre-tax)",
        "gross_pnl": "Gross PnL",
        "take_home": "Your take-home (pre-tax)",
        "req_gross": "Required gross PnL",
        "formula": "Formula",
        "ae_subtitle": "🕌 Reverse (Dubai): Target After-Tax → Required Gross",
        "cy_subtitle": "🇨🇾 Reverse (Cyprus): Target After-Tax → Required Gross",
        "bg_subtitle": "🇧🇬 Reverse (Bulgaria): Target After-Tax → Required Gross",
        "target_after_tax": "Target after-tax net",
        "treatment": "Treatment",
        "ae_opts": ["Individual (0% personal income tax)", "Company (apply corporate tax %)"],
        "cy_opts": ["Individual (allowance + flat % above)", "Company (apply corporate tax %)"],
        "bg_opts": ["Individual (flat % with optional allowance)", "Company (apply corporate tax %)"],
        "corp_rate": "Corporate tax rate (%)",
        "allowance": "Tax-free allowance (annual)",
        "flat_rate": "Flat rate (%)",
        "flat_personal_rate": "Flat personal tax rate (%)",
        "req_take_home": "Required pre-tax take-home",
        "req_gross_final": "Required gross PnL (given your split)",
        "notes": "General notes",
        "notes_text": (
            "- Profit Split tabs are **pre-tax** quick math.\n"
            "- Reverse tabs use **simple, editable models**:\n"
            "  - Dubai: Individuals 0% personal tax; Company = single-rate.\n"
            "  - Cyprus: allowance + flat rate above it; Company = single-rate.\n"
            "  - Bulgaria: flat % (optional allowance); Company = single-rate.\n"
            "- Results are estimates only — not tax advice."
        ),
    },
    "el": {
        "title": "📈 Διαχωρισμός Κερδών + Αντίστροφος Υπολογισμός (Ντουμπάι • Κύπρος • Βουλγαρία)",
        "subtitle": "Γρήγοροι υπολογισμοί διαχωρισμού + αντίστροφος φόρου μετά φόρων.",
        "split_label": "Το ποσοστό σας (%)",
        "split_help": "Παράδειγμα: 80 σημαίνει ότι κρατάτε το 80% των κερδών.",
        "ps_req": "Διαχωρισμός → Απαιτούμενο Μικτό",
        "ps_take": "Διαχωρισμός ← Καθαρά Κέρδη Σας",
        "rev_ae": "Αντίστροφος (Ντουμπάι)",
        "rev_cy": "Αντίστροφος (Κύπρος)",
        "rev_bg": "Αντίστροφος (Βουλγαρία)",
        "req_gross_title": "Απαιτούμενο Μικτό → Στόχος Καθαρών (προ φόρων)",
        "req_take_title": "Καθαρά Κέρδη Σας ← Μικτό PnL (προ φόρων)",
        "target_take": "Στόχος καθαρού κέρδους (προ φόρων)",
        "gross_pnl": "Μικτό PnL",
        "take_home": "Καθαρά κέρδη σας (προ φόρων)",
        "req_gross": "Απαιτούμενο μικτό PnL",
        "formula": "Τύπος",
        "ae_subtitle": "🕌 Αντίστροφος (Ντουμπάι): Στόχος Μετά Φόρων → Απαιτούμενο Μικτό",
        "cy_subtitle": "🇨🇾 Αντίστροφος (Κύπρος): Στόχος Μετά Φόρων → Απαιτούμενο Μικτό",
        "bg_subtitle": "🇧🇬 Αντίστροφος (Βουλγαρία): Στόχος Μετά Φόρων → Απαιτούμενο Μικτό",
        "target_after_tax": "Στόχος καθαρού μετά φόρων",
        "treatment": "Καθεστώς",
        "ae_opts": ["Ιδιώτης (0% φόρος)", "Εταιρεία (εταιρικός φόρος %)"],
        "cy_opts": ["Ιδιώτης (αφορολόγητο + ποσοστό πάνω)", "Εταιρεία (εταιρικός φόρος %)"],
        "bg_opts": ["Ιδιώτης (σταθερό % με προαιρετικό αφορολόγητο)", "Εταιρεία (εταιρικός φόρος %)"],
        "corp_rate": "Εταιρικός φόρος (%)",
        "allowance": "Αφορολόγητο (ετήσιο)",
        "flat_rate": "Σταθερό ποσοστό (%)",
        "flat_personal_rate": "Σταθερός φόρος εισοδήματος (%)",
        "req_take_home": "Απαιτούμενο καθαρό προ φόρων",
        "req_gross_final": "Απαιτούμενο μικτό PnL (με το ποσοστό σας)",
        "notes": "Σημειώσεις",
        "notes_text": (
            "- Οι καρτέλες διαχωρισμού είναι υπολογισμοί **προ φόρων**.\n"
            "- Οι αντίστροφες καρτέλες βασίζονται σε **απλά μοντέλα**:\n"
            "  - Ντουμπάι: Ιδιώτες 0% φόρος, Εταιρεία = απλό ποσοστό.\n"
            "  - Κύπρος: αφορολόγητο + ποσοστό, Εταιρεία = απλό ποσοστό.\n"
            "  - Βουλγαρία: σταθερό % (προαιρετικό αφορολόγητο), Εταιρεία = απλό ποσοστό.\n"
            "- Οι υπολογισμοί είναι ενδεικτικοί — όχι φορολογική συμβουλή."
        ),
    }
}

# ---------- Language selector
lang = st.sidebar.selectbox("Language / Γλώσσα", ["English", "Ελληνικά"])
lang_code = "en" if lang == "English" else "el"
t = lambda key: translations[lang_code][key]

# ---------- Title
st.title(t("title"))
st.caption(t("subtitle"))

# ---------- Split input
st.divider()
your_split = st.number_input(
    t("split_label"),
    min_value=0.0, max_value=100.0, value=80.0, step=1.0,
    help=t("split_help")
)
s = your_split / 100.0

# ---------- Tabs
tab_ps_req, tab_ps_take, tab_reverse_ae, tab_reverse_cy, tab_reverse_bg = st.tabs([
    t("ps_req"), t("ps_take"), t("rev_ae"), t("rev_cy"), t("rev_bg")
])

# =========================
# Profit Split — Required Gross
# =========================
with tab_ps_req:
    st.subheader(t("req_gross_title"))
    target = st.number_input(t("target_take"), min_value=0.0, value=1000.0, step=100.0, format="%.2f")
    if s <= 0:
        st.error("Split must be >0%.")
    else:
        required_gross = target / s
        st.metric(t("req_gross"), f"{required_gross:,.2f}")
        with st.expander(t("formula")):
            st.code("Required Gross = Target / (Your Split)")

# =========================
# Profit Split — Your Take-Home
# =========================
with tab_ps_take:
    st.subheader(t("req_take_title"))
    gross = st.number_input(t("gross_pnl"), value=1250.0, step=100.0, format="%.2f")
    take_home = gross * s
    st.metric(t("take_home"), f"{take_home:,.2f}")
    with st.expander(t("formula")):
        st.code("Take-Home = Gross PnL × (Your Split)")

# =========================
# Reverse (Dubai)
# =========================
with tab_reverse_ae:
    st.subheader(t("ae_subtitle"))
    target_after_tax_ae = st.number_input(f"{t('target_after_tax')} (Dubai)", min_value=0.0, value=1000.0, step=100.0, format="%.2f")
    ae_regime = st.radio(t("treatment"), t("ae_opts"), index=0)

    if ae_regime == t("ae_opts")[0]:
        required_take_home_ae = target_after_tax_ae
    else:
        corp_rate = st.number_input(t("corp_rate"), min_value=0.0, max_value=100.0, value=9.0, step=0.5)
        if (1 - corp_rate/100.0) <= 0:
            st.error("Invalid corporate tax rate.")
            required_take_home_ae = 0.0
        else:
            required_take_home_ae = target_after_tax_ae / (1 - corp_rate/100.0)

    if s > 0:
        required_gross_ae = required_take_home_ae / s
        st.metric(t("req_take_home"), f"{required_take_home_ae:,.2f}")
        st.metric(t("req_gross_final"), f"{required_gross_ae:,.2f}")

# =========================
# Reverse (Cyprus)
# =========================
with tab_reverse_cy:
    st.subheader(t("cy_subtitle"))
    target_after_tax_cy = st.number_input(f"{t('target_after_tax')} (Cyprus)", min_value=0.0, value=1000.0, step=100.0, format="%.2f")
    cy_regime = st.radio(t("treatment"), t("cy_opts"), index=0)

    def reverse_with_threshold(target, threshold, rate):
        r = rate / 100.0
        if r >= 1.0: return 0.0
        if target <= threshold: return target
        return threshold + (target - threshold) / (1 - r)

    if cy_regime == t("cy_opts")[0]:
        cy_allowance = st.number_input(t("allowance"), min_value=0.0, value=19_500.0, step=100.0)
        cy_rate = st.number_input(t("flat_rate"), min_value=0.0, max_value=100.0, value=20.0, step=0.5)
        required_take_home_cy = reverse_with_threshold(target_after_tax_cy, cy_allowance, cy_rate)
    else:
        cy_corp = st.number_input(t("corp_rate"), min_value=0.0, max_value=100.0, value=12.5, step=0.5)
        required_take_home_cy = target_after_tax_cy / (1 - cy_corp/100.0) if (1 - cy_corp/100.0) > 0 else 0.0

    if s > 0:
        required_gross_cy = required_take_home_cy / s
        st.metric(t("req_take_home"), f"{required_take_home_cy:,.2f}")
        st.metric(t("req_gross_final"), f"{required_gross_cy:,.2f}")

# =========================
# Reverse (Bulgaria)
# =========================
with tab_reverse_bg:
    st.subheader(t("bg_subtitle"))
    target_after_tax_bg = st.number_input(f"{t('target_after_tax')} (Bulgaria)", min_value=0.0, value=1000.0, step=100.0, format="%.2f")
    bg_regime = st.radio(t("treatment"), t("bg_opts"), index=0)

    if bg_regime == t("bg_opts")[0]:
        bg_allowance = st.number_input(t("allowance"), min_value=0.0, value=0.0, step=100.0)
        bg_rate = st.number_input(t("flat_personal_rate"), min_value=0.0, max_value=100.0, value=10.0, step=0.5)
        required_take_home_bg = reverse_with_threshold(target_after_tax_bg, bg_allowance, bg_rate)
    else:
        bg_corp = st.number_input(t("corp_rate"), min_value=0.0, max_value=100.0, value=10.0, step=0.5)
        required_take_home_bg = target_after_tax_bg / (1 - bg_corp/100.0) if (1 - bg_corp/100.0) > 0 else 0.0

    if s > 0:
        required_gross_bg = required_take_home_bg / s
        st.metric(t("req_take_home"), f"{required_take_home_bg:,.2f}")
        st.metric(t("req_gross_final"), f"{required_gross_bg:,.2f}")

# ---------- Footer
with st.expander(t("notes")):
    st.markdown(t("notes_text"))
