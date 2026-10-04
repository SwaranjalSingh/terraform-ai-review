import streamlit as st
from parser import parse_plan
from ai import generate_review


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Terraform AI Plan Review",
    page_icon="🔧",
    layout="wide"
)


# -----------------------------
# Custom Styling
# -----------------------------
st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 17px;
    color: #666;
    margin-bottom: 30px;
}

.section-title {
    font-size: 25px;
    font-weight: 600;
    margin-top: 30px;
    margin-bottom: 15px;
}

.risk-high {
    padding: 15px;
    border-radius: 8px;
    background-color: #ffe5e5;
    color: #b00020;
    font-weight: 600;
    margin-bottom: 15px;
}

.risk-low {
    padding: 15px;
    border-radius: 8px;
    background-color: #e5f7e9;
    color: #137333;
    font-weight: 600;
    margin-bottom: 15px;
}

.review-box {
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 10px;
    background-color: #fafafa;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="main-title">Terraform AI Plan Review</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload a Terraform plan JSON file to analyze infrastructure changes, '
    'risks, and potential destructive operations.'
    '</div>',
    unsafe_allow_html=True
)


# -----------------------------
# Upload
# -----------------------------
st.markdown("### Upload Terraform Plan")

uploaded_file = st.file_uploader(
    "Upload Terraform Plan JSON",
    type=["json"],
    help="Upload the JSON output generated using terraform show -json"
)


# -----------------------------
# Analyze
# -----------------------------
if uploaded_file:

    st.success(f"Uploaded: {uploaded_file.name}")

    analyze_button = st.button(
        "🔍 Analyze Terraform Plan",
        type="primary"
    )

    if analyze_button:

        try:

            # Read uploaded JSON
            plan_data = uploaded_file.read()

            # Parse Terraform plan
            resources = parse_plan(plan_data)

            # -----------------------------
            # Calculate change counts
            # -----------------------------
            create_count = 0
            update_count = 0
            delete_count = 0
            replace_count = 0

            for resource in resources:

                action = str(resource.get("action", "")).lower()

                if action == "create":
                    create_count += 1

                elif action == "update":
                    update_count += 1

                elif action == "delete":
                    delete_count += 1

                elif action == "replace":
                    replace_count += 1

            total_changes = len(resources)

            # -----------------------------
            # Overview
            # -----------------------------
            st.markdown(
                '<div class="section-title">Terraform Plan Overview</div>',
                unsafe_allow_html=True
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Create", create_count)

            with col2:
                st.metric("Update", update_count)

            with col3:
                st.metric("Delete", delete_count)

            with col4:
                st.metric("Replace", replace_count)

            # -----------------------------
            # Risk Assessment
            # -----------------------------
            st.markdown(
                '<div class="section-title">Risk Assessment</div>',
                unsafe_allow_html=True
            )

            if delete_count > 0 or replace_count > 0:

                st.markdown(
                    '<div class="risk-high">'
                    '🔴 HIGH RISK — Plan contains DELETE and/or REPLACE operations.'
                    '</div>',
                    unsafe_allow_html=True
                )

                st.warning(
                    "Manual review is required before applying this Terraform plan."
                )

            elif create_count > 0 or update_count > 0:

                st.markdown(
                    '<div class="risk-low">'
                    '🟢 LOW / MEDIUM RISK — No destructive operations detected.'
                    '</div>',
                    unsafe_allow_html=True
                )

            else:

                st.info("No infrastructure changes detected.")

            # -----------------------------
            # AI Review
            # -----------------------------
            st.markdown(
                '<div class="section-title">AI Terraform Review</div>',
                unsafe_allow_html=True
            )

            with st.spinner("AI is reviewing the Terraform plan..."):

                review = generate_review(resources)

            st.markdown(
                '<div class="review-box">',
                unsafe_allow_html=True
            )

            st.markdown(review)

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

            # -----------------------------
            # Affected Resources
            # -----------------------------
            st.markdown(
                '<div class="section-title">Affected Resources</div>',
                unsafe_allow_html=True
            )

            for resource in resources:

                resource_name = resource.get(
                    "address",
                    resource.get("name", "Unknown resource")
                )

                action = resource.get(
                    "action",
                    "unknown"
                ).upper()

                if action == "CREATE":
                    icon = "🟢"

                elif action == "UPDATE":
                    icon = "🟡"

                elif action == "DELETE":
                    icon = "🔴"

                elif action == "REPLACE":
                    icon = "🟠"

                else:
                    icon = "⚪"

                st.markdown(
                    f"{icon} **{resource_name}** — `{action}`"
                )

        except Exception as e:

            st.error(
                "Unable to analyze the Terraform plan."
            )

            st.exception(e)

else:

    st.info(
        "Upload a Terraform plan JSON file to begin the review."
    )