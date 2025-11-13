# 🧠 FinMar — Financial Data Pipeline for Moroccan Market

**FinMar** is an end-to-end data engineering project designed to collect, process, and visualize financial data from Moroccan online platforms.  
It mimics an enterprise-grade architecture built on **AWS**, using scalable cloud components and modern data engineering tools.

---

## 🚀 Project Overview

FinMar automates the entire lifecycle of financial data:

1. **Scraping** financial data from Moroccan public and private websites (e.g. exchange rates, market indexes, investment news).
2. **Storing** raw data securely in **AWS S3**.
3. **Processing** and cleaning data using **Apache Spark** on a **Kubernetes cluster (K8s)** deployed on **EC2** instances.
4. **Loading** processed data into **Amazon Redshift** (for analysis) or back into S3 (for data lake storage).
5. **Visualizing** results through **Metabase dashboards** for insights on trends and performance indicators.

---

## 🏗️ Architecture

![FinMar Architecture](A_README.md_file_for_the_"FinMar"_project_showcase.png)

> ⚙️ The pipeline is orchestrated with **Apache Airflow** for flexibility and transparency.  
> Alternatively, **AWS Step Functions** or **MWAA** could be used for a fully managed cloud setup.

---

## 🧰 Tech Stack

| Layer                     | Tools & Services                                    |
| ------------------------- | --------------------------------------------------- |
| **Scraping**              | BeautifulSoup, Requests                             |
| **Storage**               | AWS S3                                              |
| **Processing**            | Apache Spark, Kubernetes (K8s)                      |
| **Orchestration**         | Apache Airflow                                      |
| **Data Warehouse**        | Amazon Redshift                                     |
| **Visualization**         | Metabase _(recommended for interactive dashboards)_ |
| **Deployment**            | AWS EC2, ECS _(beyond free tier)_                   |
| **Monitoring (optional)** | Prometheus + Grafana                                |

---

## ⚡ Key Features

- Automated **data collection** from multiple Moroccan financial sources.
- **Scalable Spark cluster** running on Kubernetes for distributed data processing.
- Cloud-native **data pipeline** leveraging AWS for storage, compute, and analytics.
- **Interactive dashboards** for real-time financial insights.
- Modular architecture for future extensions (e.g., predictive models, alerting).

---

## 🧩 Setup & Installation (Local Simulation)

> You can start locally before deploying to AWS.

```bash
# 1️⃣ Clone the repository
git clone https://github.com/your-username/finmar.git
cd finmar

# 2️⃣ Create your environment
python3 -m venv venv
source venv/bin/activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Run the local scraper
python src/scraper/main.py

# 5️⃣ Launch Airflow locally (optional)
airflow standalone
```
