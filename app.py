import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime

st.set_page_config(
    page_title="Sales Intelligence Agent",
    page_icon="🤝",
    layout="wide"
)

st.markdown("""
<style>
    .stButton > button {
        background: linear-gradient(135deg, #e94560, #0f3460);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
    }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background:linear-gradient(135deg,#1a1a2e,#0f3460);padding:2rem;border-radius:12px;margin-bottom:2rem;text-align:center;'>
    <h1 style='color:#e94560;margin:0;'>🤝 Sales Intelligence Agent</h1>
    <p style='color:#a8b2d8;margin:0.5rem 0 0;'>AI-powered account insights for smarter sales conversations</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    api_key = st.text_input("Groq API Key (FREE)", type="password", placeholder="Enter your Groq API key")
    model_choice = st.selectbox("AI Model", [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama-3.1-70b-versatile"
    ])
    st.markdown("---")
    st.markdown("**💡 Why Groq?**")
    st.markdown("✅ Completely FREE\n\n✅ No credit card needed\n\n✅ Very fast\n\n✅ Powered by Llama 3")

def scrape_url(url, max_chars=3000):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; SalesAgent/1.0)"}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        text = " ".join(text.split())
        return text[:max_chars]
    except Exception as e:
        return f"[Could not fetch {url}: {str(e)}]"

def call_groq(prompt, api_key, model):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a sales intelligence analyst. Your ONLY job is to help "
                    "sales representatives understand prospective accounts. You analyze "
                    "company strategies, competitors, and leadership. You do NOT answer "
                    "unrelated questions."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 1800
    }
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60
    )
    if response.status_code != 200:
        raise Exception(f"Groq API error {response.status_code}: {response.text}")
    return response.json()["choices"][0]["message"]["content"]

def build_insights_prompt(inputs, company_text, competitor_texts):
    competitor_data = ""
    for i, (url, text) in enumerate(competitor_texts):
        competitor_data += f"\nCompetitor {i+1} ({url}):\n{text[:800]}\n"

    return f"""
You are preparing a sales intelligence one-pager for a sales representative.

=== SALES REP'S PRODUCT ===
Product Name: {inputs['product_name']}
Product Category: {inputs['product_category']}
Value Proposition: {inputs['value_proposition']}
Target Contact: {inputs['target_customer']}

=== PROSPECT COMPANY DATA (scraped from {inputs['company_url']}) ===
{company_text}

=== COMPETITOR DATA ===
{competitor_data if competitor_data else "No competitor URLs provided."}

=== YOUR TASK ===
Generate a structured sales intelligence report with EXACTLY these 5 sections.
Use markdown formatting. Be specific, concise, and actionable.

## 🏢 Company Strategy
Summarize the company's strategy as it relates to {inputs['product_category']}.
What problems might they have that {inputs['product_name']} could solve?

## ⚔️ Competitor Landscape
Identify any competitors mentioned in the company data.
Compare the competitors listed ({inputs.get('competitors', 'none provided')}) to {inputs['product_name']}.

## 👥 Key Leadership
Identify decision-makers relevant to purchasing {inputs['product_category']}.
What are their likely priorities?

## 📊 Strategic Signals
List 3-5 specific signals that suggest this company might need {inputs['product_name']}.
Format as bullet points with clear reasoning.

## 💬 Suggested Talking Points for {inputs['target_customer']}
Give 3 specific conversation starters connecting company pain points to {inputs['product_name']} benefits.

---
End with a brief Next Steps recommendation (2-3 sentences).
"""

st.markdown("## 📝 Account Details")

with st.form("sales_form"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🛍️ Your Product")
        product_name = st.text_input("Product Name *", placeholder="e.g. Snowflake Data Cloud")
        product_category = st.text_input("Product Category *", placeholder="e.g. Cloud Data Warehousing")
        value_proposition = st.text_area("Value Proposition *", height=100,
            placeholder="e.g. Enables companies to unify and analyze data across cloud platforms.")

    with col2:
        st.markdown("#### 🎯 Target Account")
        company_url = st.text_input("Prospect Company URL *", placeholder="e.g. https://www.nike.com")
        target_customer = st.text_input("Target Contact / Role *", placeholder="e.g. Chief Data Officer")
        competitors_raw = st.text_area("Competitor URLs (one per line)", height=100,
            placeholder="https://www.databricks.com")

    uploaded_file = st.file_uploader("📎 Optional: Upload Product Overview (PDF or TXT)", type=["pdf", "txt"])
    submitted = st.form_submit_button("🚀 Generate Account Insights")

if submitted:
    if not api_key:
        st.error("⚠️ Please enter your Groq API key in the sidebar.")
        st.stop()
    if not all([product_name, product_category, value_proposition, company_url, target_customer]):
        st.error("⚠️ Please fill in all required fields (marked with *).")
        st.stop()

    competitor_urls = [u.strip() for u in competitors_raw.strip().split("\n") if u.strip()]
    inputs = {
        "product_name": product_name,
        "product_category": product_category,
        "value_proposition": value_proposition,
        "company_url": company_url,
        "target_customer": target_customer,
        "competitors": ", ".join(competitor_urls)
    }

    progress = st.progress(0)
    status = st.empty()

    status.info("🌐 Step 1/4 — Fetching prospect company website...")
    company_text = scrape_url(company_url)
    progress.progress(25)

    status.info("🔍 Step 2/4 — Fetching competitor websites...")
    competitor_texts = []
    for url in competitor_urls[:3]:
        competitor_texts.append((url, scrape_url(url)))
    progress.progress(50)

    extra_product_context = ""
    if uploaded_file:
        status.info("📄 Step 3/4 — Reading uploaded document...")
        if uploaded_file.type == "text/plain":
            extra_product_context = uploaded_file.read().decode("utf-8")[:2000]
    progress.progress(65)

    status.info("🤖 Step 4/4 — AI is generating insights...")
    prompt = build_insights_prompt(inputs, company_text, competitor_texts)
    if extra_product_context:
        prompt += f"\n\n=== ADDITIONAL PRODUCT CONTEXT ===\n{extra_product_context}"

    try:
        insights = call_groq(prompt, api_key, model_choice)
        progress.progress(100)
        status.success("✅ Insights generated successfully!")
    except Exception as e:
        status.error(f"❌ Error: {str(e)}")
        st.stop()

    st.markdown("---")
    st.markdown(f"""
    <div style='background:#1a1a2e;color:white;padding:1.2rem 1.5rem;border-radius:10px;margin-bottom:1.5rem;'>
        <h2 style='margin:0;color:#e94560;'>📋 Account Intelligence Report</h2>
        <p style='margin:0.3rem 0 0;color:#a8b2d8;'>
            {product_name} → {company_url} | Contact: {target_customer} |
            Generated: {datetime.now().strftime("%B %d, %Y %I:%M %p")}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(insights)

    st.markdown("---")
    report_text = f"""SALES INTELLIGENCE REPORT
Generated: {datetime.now().strftime("%B %d, %Y")}
Product: {product_name}
Prospect: {company_url}
Target Contact: {target_customer}
Model Used: {model_choice}

{'='*60}

{insights}

{'='*60}
SOURCES SCRAPED:
- Prospect: {company_url}
{chr(10).join(f'- Competitor: {u}' for u in competitor_urls)}
"""
    st.download_button(
        label="⬇️ Download Report as .txt",
        data=report_text,
        file_name=f"sales_intel_{urllib.parse.urlparse(company_url).netloc}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )

    with st.expander("🔗 Data Sources Used"):
        st.markdown(f"- **Prospect:** [{company_url}]({company_url})")
        for url in competitor_urls:
            st.markdown(f"- **Competitor:** [{url}]({url})")
        st.markdown(f"- **AI Model:** {model_choice}")

else:
    st.markdown("""
    <div style='text-align:center;padding:2rem;color:#888;'>
        <h3>👆 Fill in the form above and click Generate Account Insights</h3>
        <p>The agent will research the prospect company and generate a tailored one-pager.</p>
    </div>
    """, unsafe_allow_html=True)