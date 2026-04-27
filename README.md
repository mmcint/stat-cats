# 🐾 Stat Cats

**K-State Wildcats Historical Comparison Dashboard**

## Structure

```
stat-cats/
├── Home.py                        ← Landing page (Stat Cats)
├── pages/
│   ├── 1_🏈_Football.py          ← Football dashboard
│   └── 2_🏀_Basketball.py        ← Basketball dashboard
├── utils.py                       ← Shared API helpers, charts, styles
├── .streamlit/
│   ├── config.toml                ← Purple theme + layout config
│   └── secrets.toml               ← API keys (DO NOT COMMIT)
└── requirements.txt
```

## Setup

```bash
git clone https://github.com/mmcint/stat-cats
cd stat-cats
pip install -r requirements.txt
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
# Add your API keys to secrets.toml
streamlit run Home.py
```

## API Keys

| API | URL | Cost |
|-----|-----|------|
| CollegeFootballData.com | collegefootballdata.com/key | Free |
| CollegeBasketballData.com | collegebasketballdata.com | Free tier |

## Deploy to Streamlit Community Cloud

1. Push to `github.com/mmcint/stat-cats`
2. Go to share.streamlit.io → New app
3. Set **Main file path** to `Home.py`
4. Add API keys under **Advanced settings → Secrets**
