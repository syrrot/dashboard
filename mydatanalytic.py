import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
st.set_page_config(layout="wide")

st.image("header2.jpg",use_container_width=True)
st.title("⛓ US Crime Analyzation Dashboard ⛓")

df = pd.read_csv("clean_data_crime.csv")

disposition_options = ["All"] + sorted(df["Disposition"].dropna().unique().tolist())
selected_disposition = st.selectbox("Select Disposition", options=disposition_options)

category_options = ["All"] + sorted(df["Category"].dropna().unique().tolist())
selected_category = st.selectbox("Select Category", options=category_options)

filtered_df = df.copy()

if selected_disposition != "All":
    filtered_df = filtered_df[filtered_df["Disposition"] == selected_disposition]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]
     
# Split into 3 columns
col1, col2, col3, col4 = st.columns((4, 4, 3,4), gap='medium')
     
with col1:
    st.subheader("Offender Age")
    if "Offender_Age" in filtered_df.columns:
        fig_hist = px.histogram(
        filtered_df,
        x="Offender_Age",
        nbins=20,  
        title="Distribution of Crime Cases by Offender Age",
        color_discrete_sequence=["pink"])
        fig_hist.update_layout(xaxis_title="Offender Age", yaxis_title="Number of Cases")
        fig_hist.update_traces( marker = {"color":"pink", "line":{"color":"black","width":2}})
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.warning("Column 'Offender_Age' not found in the data.")

    st.subheader("Victim Age")
    if "Victim_Age" in filtered_df.columns:
        fig_hist = px.histogram(
        filtered_df,
        x="Offender_Age",
        nbins=20,  
        title="Distribution of Crime Cases by Victim Age",
        color_discrete_sequence=["lightblue"])
        fig_hist.update_layout(xaxis_title="Victim Age", yaxis_title="Number of Cases")
        fig_hist.update_traces( marker = {"color":"lightblue", "line":{"color":"black","width":2}})
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.warning("Column 'Victim_Age' not found in the data.")
    
with col2:
    st.subheader("Offender Race")
    if "Offender_Race" in filtered_df.columns:
        bar_data = filtered_df["Offender_Race"].value_counts().reset_index()
        bar_data.columns = ["Offender_Race", "Count"]
        fig_bar = px.bar(bar_data, x="Offender_Race", y="Count", color="Offender_Race",color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("Column 'Offender_Race' not found in data.")
        
    st.subheader("Victim Race")
    if "Victim_Race" in filtered_df.columns:
        bar_data = filtered_df["Victim_Race"].value_counts().reset_index()
        bar_data.columns = ["Victim_Race", "Count"]
        fig_bar = px.bar(bar_data, x="Victim_Race", y="Count", color="Victim_Race",color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("Column 'Victim_Race' not found in data.")


with col3:
    st.subheader("Offender Gender")
    if "Offender_Gender" in filtered_df.columns:
        pie_data = filtered_df["Offender_Gender"].value_counts().nlargest(10).reset_index()
        pie_data.columns = ["Offender_Gender", "Count"]
        fig_pie = px.pie(pie_data, names="Offender_Gender", values="Count", color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("Column 'Offender_Gender' not found in data.")

    st.subheader("Victim Gender")
    if "Victim_Gender" in filtered_df.columns:
        pie_data = filtered_df["Victim_Gender"].value_counts().nlargest(10).reset_index()
        pie_data.columns = ["Victim_Gender", "Count"]
        fig_pie = px.pie(pie_data, names="Victim_Gender", values="Count", color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("Column 'Victim_Gender' not found in data.")

with col4:
    st.subheader("Report Type Breakdown")
    # Calculate counts and percentages
    total = len(filtered_df)
    incident_count = len(filtered_df[filtered_df["Report_Type"] == "Incident Report"])
    supplemental_count = len(filtered_df[filtered_df["Report_Type"] == "Supplemental Report"])

    incident_percent = round((incident_count / total) * 100, 1) if total else 0
    supplemental_percent = round((supplemental_count / total) * 100, 1) if total else 0

    # Combined donut chart
    fig, ax = plt.subplots()
    labels = ['Incident Report', 'Supplemental Report']
    sizes = [incident_count, supplemental_count]
    colors = ['#4CAF50', '#CD5C5C']  # Green and Red

    ax.pie(sizes, labels=labels, colors=colors, startangle=90,
       counterclock=False, wedgeprops={'width': 0.3}, autopct='%1.1f%%', textprops={'color': 'white', 'fontsize' : 13})

    # Set face colors
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    st.pyplot(fig)

    st.subheader("Victim's Injuries Status")
    # Calculate counts and percentages
    total = len(filtered_df)
    Non_fatal_count = len(filtered_df[filtered_df["Victim_Fatal_Status"] == "Non-fatal"])
    Fatal_count = len(filtered_df[filtered_df["Victim_Fatal_Status"] == "Fatal"])

    Non_fatal_percent = round((Non_fatal_count / total) * 100, 1) if total else 0
    Fatal_percent = round((Fatal_count / total) * 100, 1) if total else 0

    # Combined donut chart
    fig, ax = plt.subplots()
    labels = ['Non-fatal', 'Fatal']
    sizes = [Non_fatal_count, Fatal_count]
    colors = ['#4CAF50', '#CD5C5C']  # Green and Red

    ax.pie(sizes, labels=labels, colors=colors, startangle=90,
       counterclock=False, wedgeprops={'width': 0.3}, autopct='%1.1f%%', textprops={'color': 'white', 'fontsize' : 13})

    # Set face colors
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    st.pyplot(fig)


st.subheader("Overall Crime Categories")
category_counts = df["Category"].value_counts()
fig = px.bar(
    category_counts,
    x=category_counts.index,
    y=category_counts.values,
    labels={"x": "Category", "y": "Number of Cases"},
    title="Crime by Category"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
with st.expander("📄 Raw Data"):
    st.dataframe(df)