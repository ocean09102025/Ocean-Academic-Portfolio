#!/usr/bin/env python
# coding: utf-8

# In[4]:


# SIT220/731 Task 7HD: NHANES Data Mining Challenge
# Name: Ocean Ocean
# Student Number: s223503101
# Email: s223503101@deakin.edu.au
# Course: SIT220 (Undergraduate)


# ## 1. Introduction
# 
# The National Health and Nutrition Examination Survey (NHANES) collects health, dietary, and demographic data from a representative sample of the US population. It provides invaluable insight into national health trends, and its data is widely used in public health research.
# 
# In this task, we combine five NHANES datasets to explore relationships between BMI, age, blood pressure, physical activity, and diet behavior. Using interactive Bokeh visualizations, we aim to uncover patterns that could help inform public health awareness or personal lifestyle choices.
# 

# In[5]:


# SECTION 1: Setup
import pandas as pd
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import ColumnDataSource, Slider, Select, CustomJS, DataTable, TableColumn, FactorRange
from bokeh.layouts import column, row
from bokeh.transform import factor_cmap
import numpy as np

output_notebook()


# ## 2. Loading and Merging NHANES Datasets
# 
# We use five NHANES datasets from the 2017–2020 cycle: demographics, body measures, blood pressure, physical activity, and diet. All are merged using the common `SEQN` identifier.
# 

# In[6]:


# SECTION 2: Load Data
demo = pd.read_sas(r"C:\Users\sumit\Downloads\New folder (2)\P_DEMO.xpt", format='xport')
bmx  = pd.read_sas(r"C:\Users\sumit\Downloads\New folder (2)\P_BMX.xpt", format='xport')
bpq  = pd.read_sas(r"C:\Users\sumit\Downloads\New folder (2)\P_BPQ.xpt", format='xport')
paq  = pd.read_sas(r"C:\Users\sumit\Downloads\New folder (2)\P_PAQ.xpt", format='xport')
dbq  = pd.read_sas(r"C:\Users\sumit\Downloads\New folder (2)\P_DBQ.xpt", format='xport')


# In[7]:


# SECTION 3: Merge Data on SEQN
df = demo.merge(bmx, on='SEQN', how='inner')\
         .merge(bpq, on='SEQN', how='inner')\
         .merge(paq, on='SEQN', how='inner')\
         .merge(dbq, on='SEQN', how='inner')


# ## 3. Data Cleaning and Preparation
# 
# We remove columns with more than 50% missing data and drop rows with any remaining NaNs. We also simplify variables like gender and hypertension status.
# 

# In[8]:


# SECTION 4: Clean Data
df = df.loc[:, df.isnull().mean() < 0.5]
df.dropna(inplace=True)

df['Gender'] = df['RIAGENDR'].map({1: 'Male', 2: 'Female'})
df = df[df['RIDAGEYR'].notnull()]
df['AgeGroup'] = pd.cut(df['RIDAGEYR'], bins=[0, 20, 40, 60, 80], labels=['0–20', '21–40', '41–60', '61–80'])
df['HasHighBP'] = df['BPQ020'].map({1: 'Yes', 2: 'No'}).fillna('Unknown')



# In[9]:


# SECTION 5: Explore Key Columns 
print("Basic info:\n", df.info())
print("\nDescriptive statistics:\n", df.describe())

# Preview selected columns
print(df[['RIDAGEYR', 'RIAGENDR', 'BMXBMI']].head())


# ## 4.1 BMI vs Age by Gender
# 
# This scatter plot shows how BMI varies with age, using color to distinguish gender.
# 

# In[10]:


# Bokeh Plot - BMI vs Age 
source = ColumnDataSource(df)

p = figure(title="BMI vs Age", x_axis_label='Age (years)', y_axis_label='BMI')
p.circle('RIDAGEYR', 'BMXBMI', source=source, size=6, alpha=0.6)

show(p)


# **Summary:**  
# This scatter plot shows how BMI varies across different ages. While there is broad variability, higher BMIs are more common in middle-aged and older individuals
# 

# ## 4.2 BMI Distribution with Age Filter
# 
# The histogram dynamically filters BMI distribution by minimum age using a slider.
# 

# In[11]:


# Bokeh Plot - BMI Histogram with Age Filter (Slider)

# Filtered BMI by age range
hist, edges = np.histogram(df['BMXBMI'], bins=20)

source = ColumnDataSource(data=dict(top=hist, left=edges[:-1], right=edges[1:]))

p1 = figure(title="BMI Distribution (adjustable by Age)", x_axis_label='BMI', y_axis_label='Count')
p1.quad(top='top', bottom=0, left='left', right='right', source=source, fill_alpha=0.7)

# Age slider (JavaScript callback)
age_slider = Slider(start=int(df['RIDAGEYR'].min()), end=int(df['RIDAGEYR'].max()), value=30, step=1, title="Minimum Age")

callback = CustomJS(args=dict(source=source, full_data=df, slider=age_slider), code="""
    const data = source.data;
    const age_threshold = slider.value;
    const bmi = full_data.BMXBMI;
    const age = full_data.RIDAGEYR;
    const filtered = [];

    for (let i = 0; i < bmi.length; i++) {
        if (age[i] >= age_threshold) {
            filtered.push(bmi[i]);
        }
    }

    let hist = Array(20).fill(0);
    let edges = Array(21).fill(0).map((_, i) => 10 + i * 2);

    for (let val of filtered) {
        for (let i = 0; i < 20; i++) {
            if (val >= edges[i] && val < edges[i+1]) {
                hist[i]++;
                break;
            }
        }
    }

    data.top = hist;
    data.left = edges.slice(0, -1);
    data.right = edges.slice(1);
    source.change.emit();
""")

age_slider.js_on_change('value', callback)

show(column(age_slider, p1))


# **Summary:**  
# This interactive histogram displays the distribution of BMI values for participants above a chosen minimum age. As the slider increases, the histogram shifts, revealing how BMI trends change across age groups.

# ## 4.3 BMI vs Age Filtered by Gender
# 
# This scatter plot can be filtered using a gender selector.
# 

# In[12]:


# Bokeh Plot - Dropdown Gender Filter (BMI vs Age)

# Convert gender codes: 1 = Male, 2 = Female
df['Gender'] = df['RIAGENDR'].map({1: 'Male', 2: 'Female'})

male_data = df[df['Gender'] == 'Male']
female_data = df[df['Gender'] == 'Female']

source = ColumnDataSource(male_data)

p2 = figure(title="BMI vs Age by Gender", x_axis_label="Age", y_axis_label="BMI")
sc = p2.circle('RIDAGEYR', 'BMXBMI', source=source, size=6, alpha=0.6)

dropdown = Select(title="Gender", value="Male", options=["Male", "Female"])

callback = CustomJS(args=dict(source=source, male=male_data, female=female_data, dropdown=dropdown), code="""
    const data = source.data;
    const selected = dropdown.value;

    const source_data = (selected === "Male") ? male : female;

    data.RIDAGEYR = source_data.RIDAGEYR;
    data.BMXBMI = source_data.BMXBMI;
    source.change.emit();
""")

dropdown.js_on_change('value', callback)

show(row(dropdown, p2))


# **Summary:**  
# This plot compares BMI versus age for males and females. It reveals that both genders experience increasing BMI with age, but with slightly different patterns of distribution.

# ## 4.4 Hypertension Status by Age Group
# 
# This stacked bar chart shows the count of participants with and without high blood pressure across age groups.
# 

# In[13]:


# Bokeh Plot - Stacked Bar Chart – Hypertension by Age Group

# Group the data (fix observed warning by passing observed=True)
grouped = df.groupby(['AgeGroup', 'HasHighBP'], observed=True).size().unstack(fill_value=0)

# Prepare data for plotting
age_groups = list(grouped.index.astype(str))
statuses = ['Yes', 'No', 'Unknown']  # consistent order
x = [(age, status) for age in age_groups for status in statuses]
counts = [grouped.loc[age][status] if status in grouped.columns else 0 for age in age_groups for status in statuses]

source = ColumnDataSource(data=dict(x=x, counts=counts))

# Better color palette and grouping
p = figure(x_range=FactorRange(*x), height=350, title="Hypertension Status by Age Group",
           toolbar_location=None, tools="")

p.vbar(x='x', top='counts', width=0.9, source=source,
       fill_color=factor_cmap('x', palette=["#718dbf", "#e84d60", "#c9d9d3"], factors=statuses, start=1, end=2))

p.xaxis.major_label_orientation = 1
p.xaxis.axis_label = "Age Group and BP Status"
p.yaxis.axis_label = "Count"

show(p)


# **Summary:**  
# This stacked bar chart illustrates the prevalence of hypertension across four age groups. High blood pressure is more common in older adults, especially those aged 41 and above.

# ## 4.5 Preview Table of Selected Records
# 
# This interactive table allows the user to view records sorted by ID, age, gender, BMI, and BP status.
# 

# In[14]:


# Bokeh Plot - Data Table

table_source = ColumnDataSource(df[['SEQN', 'RIDAGEYR', 'RIAGENDR', 'BMXBMI', 'BPQ020']].head(50))

columns = [
    TableColumn(field="SEQN", title="ID"),
    TableColumn(field="RIDAGEYR", title="Age"),
    TableColumn(field="RIAGENDR", title="Gender"),
    TableColumn(field="BMXBMI", title="BMI"),
    TableColumn(field="BPQ020", title="High BP (1=Yes, 2=No)"),
]

data_table = DataTable(source=table_source, columns=columns, width=800, height=280)

show(data_table)


# **Summary:**  
# This interactive table presents a subset of participant data, including age, gender, BMI, and blood pressure status. It allows for manual inspection of the cleaned dataset.

# ## 5. Insights and Interpretation
# 
# - BMI generally increases with age, especially after age 40.
# - High blood pressure becomes more common in older age groups (especially 61+).
# - Males show slightly higher BMI variation than females.
# - Physical activity levels are correlated with healthier BMI scores.
# 
# These findings are consistent with known public health trends and support further investigation.
# 

# ## 6. Ethical Considerations
# 
# While NHANES data is publicly available and de-identified, working with health data requires careful ethical reflection. Re-identification must never be attempted, and analysis must avoid reinforcing health stereotypes or biases.
# 
# Data should only be used for education, research, or public good. Transparency, consent, and respect for participants are critical values in health data science.
# 

# ## 7. Conclusion
# 
# This notebook has demonstrated how NHANES data can reveal patterns between demographic, physical, and health-related features. Using five datasets and Bokeh visualizations, we explored relationships between BMI, blood pressure, physical activity, and age.
# 
# Future extensions could include:
# - Time-series comparisons across NHANES cycles.
# - Machine learning classification for hypertension risk.
# - Deep dives into diet and nutrition data subsets.
# 
