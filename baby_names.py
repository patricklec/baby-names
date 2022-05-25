import pandas as pd 
import plotly.express as px 
import streamlit as st


# Prepare Dataframe
df = pd.read_csv("baby_names.csv")

df["Sex"].replace("F","Female", inplace=True)
df["Sex"].replace("M", "Male", inplace=True)


#Set Streamlit Basic Layout
st.set_page_config(page_title="Names Dashboard",
                    page_icon = ":chart_with_upwards_trend:")
             

#Display Original Dataframe?
#st.dataframe(df)


# Sidebar
st.sidebar.header("Please Filter Here:")
name = st.sidebar.text_input("Type the Name", value="")


gender= st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Sex"].unique(),
    default=df["Sex"].unique()
)

years_included = st.sidebar.slider("Select years to be included:",
    min_value= 1910, max_value=2021, value=(1910,2021), step=1)

min_year = years_included[0]
max_year = years_included[1]

state = st.sidebar.multiselect(
    "Select which US States you want to include:",
    options=df["State"].unique(),
    default=df["State"].unique()
)



# Set new selection and display the selected part of df
df_selection = df.query(
    "Name == @name & Sex == @gender & State == @state & Year >= @min_year & Year <= @max_year" 
)


total_named = df_selection["Count"].sum()

year_max = 0
if name != "":
    try:
        year_max = df_selection.loc[df_selection["Count"].idxmax()]["Year"]
    except: 
        pass
  
left_column, right_column = st.columns(2)
with left_column:
    if name != "":
        st.subheader(f":baby: Total number of babies that were named {name}: {total_named}")

with right_column:
    if name != "" or year_max != 0:
        st.subheader(f":date: Your name was most common in {year_max}.")

st.markdown("---")



# Graph 

name_by_year = df_selection

fig = px.line(name_by_year, x="Year", y="Count", color="State",
title = f"Number of Babies named {name} by Year", 
template ="plotly_white")

if name != "":
    st.plotly_chart(fig)



hide_st_style = """ 
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)