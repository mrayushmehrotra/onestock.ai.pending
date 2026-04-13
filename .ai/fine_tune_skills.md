Great constraint — here's the full breakdown of free, open-source options you can fine-tune locally:

---

## Best Models for Indian Stock Market Fine-tuning (Free & Open Source)

### 🥇 Top Recommendation: **FinGPT + Qwen2.5-Finance**

For your use case (predicting which stock will boom), you actually need **two different model types** working together:

---

## Type 1 — Sentiment / News Understanding (LLM-based)

These understand financial language, news, and fundamentals:

| Model | Size | Why it's good | Fine-tune on |
|---|---|---|---|
| **FinGPT (Llama-3.1-8B base)** | 8B | Purpose-built for finance, already trained on earnings calls, SEC filings, financial news | Your scraped Moneycontrol/ET headlines |
| **Qwen2.5-7B-Finance** | 7B | Alibaba's finance-specific model, strong on Asian markets | Indian company news, BSE announcements |
| **Mistral-7B-v0.3** | 7B | Best base model for fine-tuning at 7B, very efficient | Financial sentiment datasets |
| **Phi-3.5-mini** | 3.8B | Runs on a basic laptop, surprisingly capable | If you have limited RAM (< 8GB) |

**What to fine-tune it on:**
- NSE/BSE company announcements (free from nseindia.com)
- Moneycontrol news headlines + price movement labels
- `FinancialPhraseBank` dataset (free on HuggingFace)
- `FLARE-FinQA`, `FLARE-Headlines` benchmarks (free)

---

## Type 2 — Price Prediction (Classical ML / Time-Series)

For the actual boom prediction from feature vectors — **no LLM needed here**:

| Model | Library | Why |
|---|---|---|
| **XGBoost** | `xgboost` | Best on tabular stock data, interpretable, fast |
| **LightGBM** | `lightgbm` | 3x faster than XGBoost, lower RAM |
| **TimesNet / PatchTST** | HuggingFace `time-series-transformers` | State-of-the-art time-series transformer, free |
| **TiDE** | `pytorch` | Google's time-series model, outperforms LSTM |

---

## The Ideal Free Stack for Your System

```
News/Announcements
       │
       ▼
  FinGPT (Qwen2.5-7B fine-tuned)   ← sentiment score
       │
       ▼
  Feature Vector (technical + fundamental + sentiment)
       │
       ▼
  LightGBM / XGBoost                ← boom probability score
       │
       ▼
  Top stock picks
```

---

## Free Data Sources (replacing paid APIs)

| What you need | Free source | How |
|---|---|---|
| NSE OHLCV daily | `yfinance` (`.NS` suffix) | `yf.Ticker("RELIANCE.NS")` |
| BSE data | `yfinance` (`.BO` suffix) | `yf.Ticker("500325.BO")` |
| NSE historical bulk download | nseindia.com bhav copy | Daily CSV, free |
| Fundamentals | `Screener.in` scraping | `requests` + `BeautifulSoup` |
| Company announcements | NSE XBRL API | Free, official |
| News headlines | ET / Moneycontrol scraping | `httpx` + `BeautifulSoup` |
| FII/DII data | NSE website free endpoint | JSON API, no key needed |
| Options chain | NSE website free endpoint | `https://www.nseindia.com/api/option-chain-indices` |

---

## Fine-tuning FinGPT Locally — Minimum Setup

```python
# Fine-tune Mistral-7B or Llama-3.1-8B on financial sentiment
# Uses QLoRA — runs on a single GPU with 8GB VRAM, or CPU (slow)

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer
import torch

model_name = "mistralai/Mistral-7B-v0.3"  # free on HuggingFace

# QLoRA config — 4-bit quantization so it fits in 8GB GPU
from transformers import BitsAndBytesConfig
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto"
)

lora_config = LoraConfig(
    r=16, lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# Your training data format:
# {"text": "TATAPOWER Q3 profit jumps 40%, promoter buying. [LABEL: BULLISH]"}
# {"text": "ADANI GROUP faces SEBI probe, FIIs selling. [LABEL: BEARISH]"}
```

**If you don't have a GPU:** Use **Google Colab free tier** (T4 GPU, 15GB VRAM) for fine-tuning, then download and run inference locally on CPU.

---

## Honest Recommendation for Your Stage

Given you're building this as a portfolio/side project right now, I'd suggest this order:

1. **Start with LightGBM + VADER** (zero GPU needed, runs in minutes, gives you a working system fast)
2. **Replace VADER with FinGPT/Mistral fine-tuned** once the pipeline is solid
3. **Swap LightGBM for PatchTST** if you want to push accuracy further later
