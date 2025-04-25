# 🌐 Localyst – Smart Local Insights from Google Maps

### Final Project
**Project Title**: Leveraging Google Technologies for Community Impact  
**Author**: Aswanth V 
**Technologies Used**: Streamlit, Playwright, Google Maps  

---

## 📌 Overview

**Localyst** is a lightweight, user-friendly web application that helps entrepreneurs, small business owners, NGOs, and community planners collect real-time business listing data from **Google Maps**.

With just a search query and a click, users can extract essential business insights like names, addresses, contact details, review metrics, and geo-coordinates — all exportable in CSV or Excel formats.

BoostLocal leverages the power of **Google Maps** via automated web scraping to democratize access to location intelligence and community insights.

---

## 🎯 Problem Statement

Local business stakeholders often struggle with:

- Identifying competitors or collaborators in their region
- Conducting location-based market research
- Mapping essential services in underserved communities

Manual methods are time-consuming and inconsistent. There’s a strong need for a simple, scalable tool to extract this data in real-time.

---

## 💡 Solution

Localyst bridges the gap by:

- Automating business discovery using **Google Maps**
- Providing easy access to structured data
- Enabling export to common formats for planning, outreach, or analytics

This tool empowers users to make **data-driven decisions** and promotes smarter community building and entrepreneurship.

---

## 🔧 Features

- 🔍 Search for any business type (e.g., "dermatologists in Pune")
- 🗺️ Extract name, address, website, phone number, reviews, and coordinates
- 📊 Download results as CSV or Excel
- ⏱️ Fast performance using headless Chromium (Playwright)
- 🖥️ Clean Streamlit interface with progress feedback

---

## 🌐 Google Technologies Used

| Technology       | Purpose                                             |
|------------------|-----------------------------------------------------|
| Google Maps      | Primary data source via automated scraping         |
| Streamlit        | Front-end UI for interaction                       |
| Playwright       | Automating Google Maps interaction                 |
| (Optional) Firebase / Google Sheets API | Storing scraped results for future retrieval |

---

## 🧰 Installation & Setup

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/boostlocal.git
cd boostlocal
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run app.py
```

---

## ✅ Requirements

- **Python**: 3.8+
- **Google Chrome**: Installed
- **Internet connection**
- **OS**: Windows, macOS, or Linux

---

## 📈 Potential Impact

Localyst can be used by:

- 📍 **Small business owners** conducting competitor research
- 🏥 **NGOs** mapping health/education infrastructure
- 📊 **Local governments** analyzing service coverage
- 📚 **Students** working on geography or entrepreneurship projects

It’s fast, accessible, and easy to scale.

---

## 🚀 Future Enhancements

- Integrate with **Firebase** to store data history
- Use **Google Maps API (official)** for a scalable backend
- Add **user authentication** (Google Sign-In)
- Schedule scraping jobs via **Google Cloud Functions**
- Map results visually with **Google Maps JS API**