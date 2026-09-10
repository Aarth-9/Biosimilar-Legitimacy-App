from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Biosimilar Legitimacy Dashboard", layout="wide")

BASE = Path(__file__).resolve().parent / "outputs"


@st.cache_data
def load_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(BASE / name)


main_df = load_csv("biosimilar_legitimacy_dataset.csv")
comparison = load_csv("comparability_summary.csv")
safety = load_csv("safety_summary.csv")
regulatory = load_csv("regulatory_legitimacy.csv")
biologic_comparison = load_csv("biologic_comparison.csv")

if main_df.empty:
    st.error("No biosimilar legitimacy dataset found in outputs/. Run the dataset generator first.")
    st.stop()

candidate_df = main_df[main_df["product_type"] == "candidate"].copy()
if candidate_df.empty:
    st.error("No candidate biosimilar records were found.")
    st.stop()

sidebar = st.sidebar
sidebar.title("Filters")
selected_product = sidebar.selectbox(
    "Select biosimilar candidate",
    candidate_df["product_name"].tolist(),
)

selected_row = candidate_df[candidate_df["product_name"] == selected_product].iloc[0]
peer_group = main_df[
    (main_df["molecule"] == selected_row["molecule"]) |
    (main_df["reference_product"] == selected_row["reference_product"])
].sort_values("overall_legitimacy_score", ascending=False)

st.title("Biosimilar Legitimacy & Comparative Quality Dashboard")
st.caption("Synthetic evidence-based evaluation of biosimilar quality, safety, comparability, and regulatory legitimacy.")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Overall legitimacy", f"{selected_row['overall_legitimacy_score']:.1f}/100")
with col2:
    st.metric("Quality score", f"{selected_row['quality_score']:.1f}/100")
with col3:
    st.metric("Safety score", f"{selected_row['safety_score']:.1f}/100")
with col4:
    st.metric("Regulatory score", f"{selected_row['regulatory_score']:.1f}/100")
with col5:
    st.metric("PK/PD similarity", f"{selected_row['pk_pd_similarity_pct']:.1f}%")

overview_tab, safety_tab, regulatory_tab, comparison_tab = st.tabs([
    "Overview",
    "Safety & Side Effects",
    "Regulatory Legitimacy",
    "Compare with Originator / Similar Biologics",
])

with overview_tab:
    st.subheader(f"{selected_product} quality snapshot")
    score_cols = [
        "quality_score",
        "comparability_score",
        "safety_score",
        "efficacy_score",
        "regulatory_score",
    ]
    score_values = [selected_row[col] for col in score_cols]
    score_chart = pd.DataFrame({
        "Metric": [
            "Quality",
            "Comparability",
            "Safety",
            "Efficacy",
            "Regulatory",
        ],
        "Score": score_values,
    })

    fig = px.bar(
        score_chart,
        x="Metric",
        y="Score",
        color="Score",
        color_continuous_scale="Viridis",
        title="Core legitimacy dimensions",
    )
    fig.update_yaxes(range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

    evidence_cols = [
        "pk_pd_similarity_pct",
        "structural_similarity_pct",
        "analytical_similarity_pct",
        "clinical_equivalence_pct",
        "batch_consistency_pct",
    ]
    evidence_labels = [
        "PK/PD similarity",
        "Structural similarity",
        "Analytical similarity",
        "Clinical equivalence",
        "Batch consistency",
    ]
    evidence_df = pd.DataFrame({
        "Evidence area": evidence_labels,
        "Value": [selected_row[col] for col in evidence_cols],
    })

    fig2 = px.bar(
        evidence_df,
        x="Evidence area",
        y="Value",
        color="Value",
        color_continuous_scale="Cividis",
        title="Comparability and analytical evidence",
    )
    fig2.update_yaxes(range=[0, 100])
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Key evidence summary")
    summary = pd.DataFrame([
        {"Field": "Reference product", "Value": selected_row["reference_product"]},
        {"Field": "Therapeutic area", "Value": selected_row["therapeutic_area"]},
        {"Field": "Manufacturer", "Value": selected_row["manufacturer"]},
        {"Field": "Approval status", "Value": selected_row["approval_status"]},
        {"Field": "Interchangeability", "Value": selected_row["interchangeability_status"]},
        {"Field": "Adverse event rate / 1000", "Value": f"{selected_row['adverse_event_rate_per_1000']:.1f}"},
        {"Field": "Serious AE rate / 1000", "Value": f"{selected_row['serious_ae_rate_per_1000']:.1f}"},
        {"Field": "Discontinuation rate %", "Value": f"{selected_row['discontinuation_rate_pct']:.1f}"},
        {"Field": "Immunogenicity rate %", "Value": f"{selected_row['immunogenicity_rate_pct']:.1f}"},
    ])
    st.dataframe(summary, hide_index=True, use_container_width=True)

with safety_tab:
    st.subheader("Safety and side-effect profile")
    safety_plot = safety.sort_values("adverse_event_rate_per_1000", ascending=False)
    fig = px.bar(
        safety_plot,
        x="product_name",
        y="adverse_event_rate_per_1000",
        color="product_type",
        title="Adverse-event rate by product",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        safety[safety["product_name"].isin([selected_product] + peer_group["product_name"].tolist())][[
            "product_name",
            "product_type",
            "adverse_event_rate_per_1000",
            "serious_ae_rate_per_1000",
            "discontinuation_rate_pct",
            "immunogenicity_rate_pct",
            "side_effect_profile",
            "overall_legitimacy_score",
        ]].sort_values("overall_legitimacy_score", ascending=False),
        hide_index=True,
        use_container_width=True,
    )

with regulatory_tab:
    st.subheader("Regulatory legitimacy and approval status")
    fig = px.bar(
        regulatory.sort_values("overall_legitimacy_score", ascending=False),
        x="product_name",
        y="regulatory_score",
        color="approval_status",
        title="Regulatory legitimacy score by product",
    )
    fig.update_yaxes(range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        regulatory[regulatory["product_name"].isin([selected_product] + peer_group["product_name"].tolist())][[
            "product_name",
            "product_type",
            "approval_status",
            "interchangeability_status",
            "quality_score",
            "comparability_score",
            "regulatory_score",
            "overall_legitimacy_score",
        ]].sort_values("overall_legitimacy_score", ascending=False),
        hide_index=True,
        use_container_width=True,
    )

with comparison_tab:
    st.subheader("Candidate against originator and similar biologics")
    comparison_plot = peer_group[[
        "product_name",
        "product_type",
        "overall_legitimacy_score",
        "quality_score",
        "safety_score",
        "comparability_score",
    ]].copy()

    fig = px.bar(
        comparison_plot,
        x="product_name",
        y="overall_legitimacy_score",
        color="product_type",
        title="Overall legitimacy comparison across molecules and peers",
    )
    fig.update_yaxes(range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

    comparison_scatter = peer_group[[
        "product_name",
        "product_type",
        "overall_legitimacy_score",
        "safety_score",
        "comparability_score",
    ]].copy()
    scatter_fig = px.scatter(
        comparison_scatter,
        x="safety_score",
        y="overall_legitimacy_score",
        color="product_type",
        hover_name="product_name",
        title="Safety vs overall legitimacy",
        size="comparability_score",
    )
    st.plotly_chart(scatter_fig, use_container_width=True)

    st.dataframe(
        peer_group[[
            "product_name",
            "product_type",
            "reference_product",
            "overall_legitimacy_score",
            "quality_score",
            "comparability_score",
            "safety_score",
            "regulatory_score",
            "approval_status",
        ]].sort_values("overall_legitimacy_score", ascending=False),
        hide_index=True,
        use_container_width=True,
    )

st.sidebar.markdown("---")
st.sidebar.caption("Synthetic dataset created for scientific and regulatory biosimilar evaluation.")
