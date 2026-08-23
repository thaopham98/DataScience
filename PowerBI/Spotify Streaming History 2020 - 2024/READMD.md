# Spotify Streaming History - Power BI Report

## 📌 Overview
This Power BI report provides insights into Spotify streaming history, analyzing user listening behavior, platform preferences, and track engagement. The report consists of two pages with interactive visualizations and slicers for dynamic exploration.

## 📢 Notes
- The dataset contains cleaned Spotify streaming data across multiple time periods.
- **Datasets Used:**
  - `Streaming_History_Audio_2020-2023_0`
  - `Streaming_History_Audio_2023-2024_1`
  - `Streaming_History_Audio_2024_2`
  - `Streaming_History_Video_2022-2024`
- Data is linked via `master_metadata_track_name` with many-to-many relationships.
- The dataset contains cleaned Spotify streaming data across multiple time periods.
- Data is linked via `master_metadata_track_name` with many-to-many relationships.

## 📊 Report Structure

### **1️⃣ Overview Page**
Contains key metrics, slicers, and high-level visualizations:
- **Metric Cards:**
  - Total Unique Tracks Played
  - Total Listening Time (Hours)
  - Total Play Sessions
  - Most Played Track
  - Most Popular Artist
  - Total Unique Number of Artists
- **Slicers:**
  - Artist Name
  - Platform
  - Album Name
  - Year
  - Month
- **Visualizations:**
  - **Total Listening Hours by Day** (Line Chart)
  - **Track Count by Track Name** (Bar Chart)
  - **Top Artists by Listening Time** (Bar Chart)

![Spotify Dashboard 1](/images/spotify_dashboard1.png)

### **2️⃣ Listening Behavior & Engagement Page**
Focuses on user behavior across different platforms and engagement with tracks.
- **Slicers:**
  - Artist Name
  - Platform
  - Album Name
  - Year
  - Month
- **Visualizations:**
  - **Total Listening Hours by Platform** (Stacked Bar Chart)
  - **Skip vs. Completion Rate by Track** (Stacked Column Chart)

![Spotify Dashboard 2](/images/spotify_dashboard2.png)

## 📈 Future Enhancements
- Additional trend analysis (year-over-year comparisons)
- Deeper insights into skipping behavior
- Interactive drill-through pages for artist and album details

## 🛠️ How to Use
1. **Filter Data Using Slicers**: Select specific years, months, artists, or platforms to refine insights.
2. **Hover Over Visuals**: Tooltips provide additional details on data points.
3. **Drill Through Analysis** *(Future Enhancement)*: Click on specific elements to navigate deeper into track and artist trends.


## View the Report in Power BI
- [Power BI](https://app.powerbi.com/groups/me/reports/270144f8-fc54-4402-af84-c2da0cdf0200/b608adbee4739a5e52cd?experience=power-bi)
---
**Author:** Thao Pham  
**Last Updated:** 8/22/2026