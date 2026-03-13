# 🤝 Sales Intelligence Agent
### Per Scholas AP 931 — Capstone Project
**Student:** Thanuja sandra
**GitHub:** thanusandra29-glitch
**Date:** March 2026

---

## 📌 Project Overview
The Sales Intelligence Agent is an AI-powered web application that helps sales representatives research prospect companies and generate actionable insights. Instead of spending hours manually researching a company, a sales rep can enter a company URL and get a complete intelligence report in seconds.

---

## 🎯 What Problem Does It Solve?
Sales reps waste hours researching companies before meetings. This tool automates that research using AI, giving reps a competitive edge by understanding the prospect's strategy, leadership, and pain points before the first conversation.

---

## 🚀 Features
- 🌐 Automatically scrapes prospect company websites
- 🔍 Analyzes up to 3 competitor websites
- 🤖 Generates a 5-section AI-powered intelligence report
- 📄 Supports optional product overview file upload (PDF or TXT)
- ⬇️ Download the report as a .txt file
- 🎨 Clean, professional UI built with Streamlit

---

## 📋 The 5-Section Report
1. **Company Strategy** — What is the company focused on?
2. **Competitor Landscape** — How do competitors compare?
3. **Key Leadership** — Who are the decision makers?
4. **Strategic Signals** — Why might they need your product?
5. **Talking Points** — What to say in the sales meeting?

---

## 🛠️ Tech Stack
| Tool | Purpose |
|------|---------|
| Python | Core programming language |
| Streamlit | Web application framework |
| Groq API | Free AI inference (Llama 3) |
| BeautifulSoup4 | Web scraping |
| Requests | HTTP requests |
| uv | Fast Python package manager |

---

## ⚙️ How To Run

### Step 1: Clone the repo
### Step 2: Install dependencies
### Step 3: Get a free Groq API key
- Go to https://console.groq.com
- Sign up for free
- Create an API key

### Step 4: Run the app
### Step 5: Use the app
- Enter your Groq API key in the sidebar
- Fill in your product details
- Enter the prospect company URL
- Click Generate Account Insights

---

## 🧪 Test I Ran
- **Product:** Salesforce CRM
- **Prospect Company:** https://www.nike.com
- **Competitor:** https://www.hubspot.com
- **Target Contact:** Chief Sales Officer
- **Result:** Successfully generated a complete 5-section intelligence report

---

## 📁 Project Structure
---

## 🔐 Security Note
The Groq API key is entered by the user in the sidebar at runtime.
It is never stored in the code or committed to GitHub.

---

## 💡 What I Learned
- Building AI-powered applications with LLMs
- Web scraping with BeautifulSoup
- Prompt engineering for structured outputs
- Building user interfaces with Streamlit
- Managing API keys securely
- Version control with Git and GitHub
