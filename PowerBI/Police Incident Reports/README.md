# Police Incident Reports - Power BI Dashboard

## 📌 Overview
This Power BI report visualizes **police incident reports** to analyze crime trends, district-wise incidents, and temporal crime patterns. The goal is to provide actionable insights for law enforcement, policymakers, and the public.

## 📂 Dataset
The dataset used in this report contains police incident records, including:
- **Incident Date**: The date when the incident occurred.
- **Police District**: The district where the incident was reported.
- **Incident Type**: The category of the reported crime.
- **Resolution**: The outcome of the incident (e.g., Arrest, Unresolved, etc.).

## 📊 Features
The dashboard includes **multiple interactive charts** across three pages, providing a comprehensive analysis of police incident reports. Below is a breakdown of the visualizations and their purpose:

---

### **Page 1: ![Overview](https://github.com/thaopham98/DataScience/blob/main/images/Police%20Incident%20Reports%20-%20Overview.png)**
1. **Number of Incidents by Day of Week** 📅  
   - A bar chart showing the distribution of incidents across days of the week to identify peak crime days.

2. **Incidents by Police District** 📍  
   - A map bubble visualization displaying the number of incidents reported in each police district.

3. **Top 5 Incident Categories** 🔍  
   - A bar chart highlighting the most frequent types of incidents reported, with **Larceny Theft** as the most common category.

4. **Number of Incidents by Year** 📈  
   - A bar chart tracking the trend of incidents over the years to identify increasing or decreasing crime rates.

5. **Incident Resolution** ✅  
   - A funnel chart showing the outcomes of reported incidents (e.g., Arrest, Unresolved, etc.) to analyze resolution rates.

6. **Report Online Filing Insights** 🖥️  
   - A donut chart displaying the proportion of incidents filed online versus offline.

---

### **Page 2: ![Incident Details](https://github.com/thaopham98/DataScience/blob/main/images/Police%20Incident%20Reports%20-%20Incident%20Details.png)**
1. **Count of Incident Number** 🔢  
   - A card visualization showing the total number of incidents.

2. **Incidents by Police District** 📊  
   - A treemap visualization providing an alternative view of incident distribution by police district.

3. **Violent vs. Non-violent Incidents** ⚖️  
   - A bar chart comparing the number of violent, non-violent, and other incident types.

4. **Incidents by Year, Quarter, and Month** 📅  
   - A line chart showing trends in incidents over time, broken down by year, quarter, and month.

5. **Subcategories of Larceny Theft** 🥧  
   - A pie chart displaying the subcategories of **Larceny Theft**, the most frequent incident type.

---

### **Page 3: ![Advanced Analysis](https://github.com/thaopham98/DataScience/blob/main/images/Police%20Incident%20Reports%20-%20Advanced%20Analysis.png)**
1. **Filters** 🔍  
   - A dropdown slicer for filtering data by **Year** and **Police District**.

2. **Correlation Between Incident Type, Resolution, and File Online** 🔗  
   - A heatmap visualizing the relationship between incident types, resolutions, and whether the incident was filed online.

---

### **Key Insights**
- The dashboard provides a clear overview of crime trends, incident types, and resolution rates.
- Users can drill down into specific details, such as subcategories of **Larceny Theft** or temporal patterns in incidents.
- Advanced visualizations like the heatmap and stacked area chart enable deeper analysis of correlations and trends.

---

### **Future Enhancements**
- Add a **slicer for Incident Category** to allow users to filter the pie chart and other visualizations by incident type.
- Include **dynamic titles** for visualizations to reflect user selections (e.g., "Subcategories for [Selected Incident Category]").
- Enhance interactivity with **bookmarks** to save default views (e.g., Larceny Theft as the default category).

## 🛠 Installation & Usage
### **1. Clone the Repository**
```bash
git clone https://github.com/thaopham98/DataScience.git
cd DataScience
```

### **2. Open the Report in Power BI**
- Install **[Power BI Desktop](https://powerbi.microsoft.com/)** if not already installed.
- Open the `Police Incident Reports.pbix` file in Power BI.
- [Power BI](https://app.powerbi.com/groups/me/reports/cb3ab8b2-c1e6-428d-a78b-03833c7b1f93/9f99b2d38dae1b46d930?experience=power-bi) 

### **3. Explore the Dashboard**
- Interact with filters to analyze specific districts, dates, and crime types.
- Modify or extend the report as needed.


## 📝 Contributing
Contributions are welcome! Feel free to submit pull requests or open issues for enhancements and bug fixes.

## 📜 License
This project is licensed under the **MIT License**.

## 📩 Contact
For questions or suggestions, feel free to reach out!
