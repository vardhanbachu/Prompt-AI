"""
PromptForge AI
A professional Streamlit application that transforms simple ideas
into optimized AI prompts using Ollama (Llama 3).
"""

import streamlit as st
import requests
import json

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Prompt AI",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# CSS — Soft, academic, professional
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600&family=Source+Sans+3:wght@300;400;500;600&display=swap');

:root {
  --bg:        #F5F7FA;
  --white:     #FFFFFF;
  --primary:   #2C3E50;
  --secondary: #34495E;
  --accent:    #2980B9;
  --border:    #DCDDE1;
  --muted:     #7F8C8D;
  --success:   #27AE60;
  --error-bg:  #FDEDEC;
  --error-bd:  #E74C3C;
  --radius:    6px;
  --shadow:    0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
}

html, body, [class*="css"] {
  font-family: 'Source Sans 3', sans-serif;
  background-color: var(--bg) !important;
  color: var(--primary);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
  max-width: 780px !important;
  padding: 2.5rem 2rem 5rem !important;
}

/* ── Header ── */
.pf-header {
  text-align: center;
  padding: 2.5rem 0 2rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 2.5rem;
}
.pf-title {
  font-family: 'Lora', serif;
  font-size: 2.2rem;
  font-weight: 600;
  color: var(--primary);
  letter-spacing: -0.3px;
  margin-bottom: 0.35rem;
}
.pf-title span { color: var(--accent); }
.pf-subtitle {
  font-size: 0.95rem;
  font-weight: 300;
  color: var(--muted);
}
.pf-rule {
  width: 40px;
  height: 2px;
  background: var(--accent);
  margin: 1rem auto 0;
  border-radius: 2px;
}

/* ── Labels ── */
.field-label {
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  color: var(--secondary);
  margin-bottom: 0.45rem;
}

/* ── Streamlit overrides ── */
div[data-testid="stTextArea"] textarea {
  background: var(--white) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--primary) !important;
  font-family: 'Source Sans 3', sans-serif !important;
  font-size: 0.95rem !important;
  line-height: 1.65 !important;
  padding: 0.75rem 1rem !important;
  box-shadow: var(--shadow) !important;
  transition: border-color 0.2s !important;
  resize: vertical !important;
}
div[data-testid="stTextArea"] textarea:focus {
  border-color: var(--accent) !important;
  outline: none !important;
  box-shadow: 0 0 0 3px rgba(41,128,185,0.1) !important;
}
div[data-testid="stTextArea"] textarea::placeholder {
  color: #B2BEC3 !important;
  font-style: italic;
}


/* Primary button */
div[data-testid="stButton"] > button[kind="primary"] {
  background: var(--primary) !important;
  border: none !important;
  border-radius: var(--radius) !important;
  color: white !important;
  font-family: 'Source Sans 3', sans-serif !important;
  font-size: 0.92rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.4px !important;
  padding: 0.6rem 2rem !important;
  width: 100% !important;
  transition: background 0.2s !important;
  box-shadow: var(--shadow) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
  background: var(--secondary) !important;
}

/* Secondary buttons */
div[data-testid="stButton"] > button:not([kind="primary"]) {
  background: var(--white) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--secondary) !important;
  font-family: 'Source Sans 3', sans-serif !important;
  font-size: 0.82rem !important;
  padding: 0.45rem 1rem !important;
  transition: border-color 0.2s, color 0.2s !important;
  box-shadow: var(--shadow) !important;
}
div[data-testid="stButton"] > button:not([kind="primary"]):hover {
  border-color: var(--accent) !important;
  color: var(--accent) !important;
}

div[data-testid="stDownloadButton"] > button {
  background: var(--white) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--secondary) !important;
  font-family: 'Source Sans 3', sans-serif !important;
  font-size: 0.82rem !important;
  box-shadow: var(--shadow) !important;
}
div[data-testid="stDownloadButton"] > button:hover {
  border-color: var(--accent) !important;
  color: var(--accent) !important;
}

div[data-testid="stAlert"] {
  border-radius: var(--radius) !important;
  font-size: 0.88rem !important;
  font-family: 'Source Sans 3', sans-serif !important;
}

label, .stSelectbox label {
  display: none !important;
}

/* ── Output card ── */
.output-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-top: 3px solid var(--accent);
  border-radius: var(--radius);
  padding: 1.5rem 1.6rem;
  box-shadow: var(--shadow);
  margin-bottom: 1rem;
}
.output-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border);
}
.output-card-title {
  font-family: 'Lora', serif;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--primary);
  letter-spacing: 0.2px;
}
.output-meta {
  display: flex;
  gap: 0.75rem;
}
.meta-pill {
  font-size: 0.72rem;
  font-weight: 500;
  color: var(--muted);
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 0.15rem 0.6rem;
}
.output-text {
  font-family: 'Source Sans 3', sans-serif;
  font-size: 0.93rem;
  line-height: 1.75;
  color: var(--primary);
  white-space: pre-wrap;
  word-break: break-word;
}

/* ── Empty state ── */
.empty-state {
  background: var(--white);
  border: 1px dashed var(--border);
  border-radius: var(--radius);
  padding: 3rem 2rem;
  text-align: center;
}
.empty-icon { font-size: 2rem; margin-bottom: 0.5rem; }
.empty-title {
  font-family: 'Lora', serif;
  font-size: 0.95rem;
  color: var(--secondary);
  margin-bottom: 0.3rem;
}
.empty-sub { font-size: 0.82rem; color: var(--muted); }

/* ── Word range row ── */
.range-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0.75rem 1rem;
  box-shadow: var(--shadow);
  margin-bottom: 0.5rem;
}
.range-label {
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.6px;
  text-transform: uppercase;
  color: var(--secondary);
  white-space: nowrap;
}
.range-value {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--accent);
  white-space: nowrap;
  margin-left: auto;
}
.range-hint {
  font-size: 0.75rem;
  color: var(--muted);
  margin-top: 0.15rem;
}

/* Slider track */
div[data-testid="stSlider"] > div > div > div {
  background: var(--accent) !important;
}
div[data-testid="stSlider"] [role="slider"] {
  background: var(--primary) !important;
  border: 2px solid var(--accent) !important;
  box-shadow: none !important;
}
div[data-testid="stSlider"] p {
  font-family: 'Source Sans 3', sans-serif !important;
  font-size: 0.75rem !important;
  color: var(--muted) !important;
}

/* ── Divider ── */
.pf-divider {
  border: none;
  border-top: 1px solid var(--border);
  margin: 1.5rem 0;
}

/* ── Footer ── */
.pf-footer {
  text-align: center;
  margin-top: 3rem;
  padding-top: 1.2rem;
  border-top: 1px solid var(--border);
  font-size: 0.75rem;
  color: var(--muted);
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────
OLLAMA_BASE  = "http://localhost:11434"
OLLAMA_MODEL = "llama3"



# ─────────────────────────────────────────────────────────────
# FUNCTIONS
# ─────────────────────────────────────────────────────────────

def get_model_name() -> str:
    """
    Query Ollama for installed models and return the best match.
    Falls back to the configured model name if unavailable.
    """
    try:
        resp = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=5)
        resp.raise_for_status()
        models = [m["name"] for m in resp.json().get("models", [])]
        if not models:
            return OLLAMA_MODEL
        for name in models:
            if OLLAMA_MODEL in name:
                return name
        return models[0]
    except Exception:
        return OLLAMA_MODEL


def build_system_prompt(min_words: int, max_words: int) -> str:
    """Construct the meta-prompt that instructs the LLM how to forge a prompt."""
    return f"""You are Prompt AI, an expert AI prompt engineer.

Your task: receive a rough user idea and transform it into a single, detailed, optimized AI prompt.

Rules:
1. Output ONLY the final prompt — no preamble, no explanation, no labels, no markdown fences.
2. The prompt MUST be between {min_words} and {max_words} words. Count carefully. This is non-negotiable.
3. Begin with a role assignment: "Act as an experienced [relevant expert]."
4. Add clear objectives, context, constraints, expected output format, and tone.
5. Make the prompt immediately usable with ChatGPT, Claude, Gemini, or Llama — no extra editing needed.
6. Do NOT include phrases like "Here is your prompt:" or "Sure!" — return only the prompt itself.
"""


def generate_prompt(user_input: str, min_words: int, max_words: int) -> str:
    """
    Send the user idea to Ollama /api/generate and return the optimized prompt.
    Raises descriptive exceptions on failure.
    """
    model = get_model_name()
    system_prompt = build_system_prompt(min_words, max_words)

    # Scale num_predict: ~1.4 tokens per word, add 20% headroom
    num_predict = int(max_words * 1.4 * 1.2)

    payload = {
        "model":  model,
        "prompt": f"{system_prompt}\n\nUser idea: {user_input.strip()}",
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p":       0.9,
            "num_predict": num_predict,
        },
    }

    try:
        response = requests.post(
            f"{OLLAMA_BASE}/api/generate",
            json=payload,
            timeout=120,
        )
        response.raise_for_status()
        result = response.json().get("response", "").strip()
        if not result:
            raise ValueError("Ollama returned an empty response. Please try again.")
        return result

    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "Unable to connect to Ollama.\n"
            "Make sure Ollama is running:  ollama serve"
        )
    except requests.exceptions.Timeout:
        raise TimeoutError(
            "Ollama took too long to respond. "
            "The model may still be loading — wait a moment and try again."
        )
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response else "?"
        if status == 404:
            raise RuntimeError(
                f"Model '{OLLAMA_MODEL}' not found in Ollama.\n"
                f"Install it with:  ollama pull {OLLAMA_MODEL}"
            )
        raise RuntimeError(f"Ollama returned HTTP {status}: {e}")


# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
for k, v in [("result", ""), ("user_input", ""), ("word_range", (150, 300))]:
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="pf-header">
  <div class="pf-title">Prompt <span>AI</span></div>
  <div class="pf-subtitle">Transform simple ideas into optimized AI prompts.</div>
  <div class="pf-rule"></div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# INPUT SECTION
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="field-label">Your Idea</div>', unsafe_allow_html=True)

user_input = st.text_area(
    label="idea",
    label_visibility="hidden",
    value=st.session_state.user_input,
    placeholder=(
        'Examples:\n'
        '"Create a website for a gym"\n'
        '"Write a blog about artificial intelligence"\n'
        '"Design a portfolio website for a software engineer"'
    ),
    height=160,
    key="idea_box",
)

st.markdown("<div style='height:0.25rem'></div>", unsafe_allow_html=True)

# ── Word Range Slider ──
st.markdown('<div class="field-label" style="margin-top:1rem;">Prompt Length — Word Range</div>', unsafe_allow_html=True)

word_range = st.slider(
    label="word_range_slider",
    label_visibility="hidden",
    min_value=100,
    max_value=10000,
    value=st.session_state.word_range,
    step=50,
    key="word_slider",
)

min_w, max_w = word_range

# Show range description
if max_w <= 300:
    length_hint = "Short — concise, punchy prompt"
elif max_w <= 600:
    length_hint = "Medium — balanced detail"
elif max_w <= 1500:
    length_hint = "Long — rich context and structure"
elif max_w <= 4000:
    length_hint = "Extended — comprehensive and detailed"
else:
    length_hint = "Deep — exhaustive, multi-section prompt"

st.markdown(
    f'<div class="range-hint">📝 &nbsp;{min_w} – {max_w} words &nbsp;·&nbsp; {length_hint}</div>',
    unsafe_allow_html=True,
)

st.markdown("<div style='height:0.25rem'></div>", unsafe_allow_html=True)

# Buttons
col1, col2 = st.columns([3, 1])
with col1:
    generate_clicked = st.button("Generate Prompt", type="primary", use_container_width=True)
with col2:
    clear_clicked = st.button("Clear", use_container_width=True)

st.markdown('<hr class="pf-divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# OUTPUT SECTION
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="field-label">Generated Prompt</div>', unsafe_allow_html=True)

if st.session_state.result:
    gp    = st.session_state.result
    words = len(gp.split())
    chars = len(gp)

    st.markdown(f"""
    <div class="output-card">
      <div class="output-card-header">
        <div class="output-card-title">✦ Forged Prompt</div>
        <div class="output-meta">
          <span class="meta-pill">{words} words</span>
          <span class="meta-pill">{chars} chars</span>
          <span class="meta-pill">target {st.session_state.word_range[0]}–{st.session_state.word_range[1]}w</span>
        </div>
      </div>
      <div class="output-text">{gp}</div>
    </div>
    """, unsafe_allow_html=True)

    # Action buttons
    a1, a2, a3 = st.columns(3)
    with a1:
        if st.button("📋  Copy Prompt", use_container_width=True):
            st.toast("Copied to clipboard!", icon="✅")
            st.markdown(
                f"<script>navigator.clipboard.writeText({json.dumps(gp)});</script>",
                unsafe_allow_html=True,
            )
    with a2:
        st.download_button(
            label="⬇  Download .TXT",
            data=gp,
            file_name="promptforge_output.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with a3:
        if st.button("↺  Regenerate", use_container_width=True):
            generate_clicked = True

else:
    st.markdown("""
    <div class="empty-state">
      <div class="empty-icon">✦</div>
      <div class="empty-title">Your prompt will appear here</div>
      <div class="empty-sub">Enter an idea above and click Generate Prompt</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# GENERATION LOGIC
# ─────────────────────────────────────────────────────────────
if generate_clicked:
    if not user_input.strip():
        st.error("⚠ Please enter your idea before generating a prompt.")
    else:
        st.session_state.user_input = user_input
        st.session_state.word_range = word_range
        with st.spinner(f"Generating your {min_w}–{max_w} word prompt via Ollama…"):
            try:
                output = generate_prompt(user_input, min_w, max_w)
                st.session_state.result = output
                st.rerun()
            except ConnectionError as e:
                st.error(f"🔌 Connection Error\n\n{e}")
            except TimeoutError as e:
                st.warning(f"⏱ Timeout\n\n{e}")
            except RuntimeError as e:
                st.error(f"🚫 Error\n\n{e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

# Clear logic
if clear_clicked:
    st.session_state.result     = ""
    st.session_state.user_input = ""
    st.session_state.word_range = (150, 300)
    st.rerun()


# ─────────────────────────────────────────────────────────────
# SIDEBAR — How It Works
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✦ Prompt AI")
    st.markdown("---")
    st.markdown("""
**How it works**

1. Type a rough idea in plain English
2. Set your desired word range (100–10,000)
3. Click **Generate Prompt**
4. Copy or download the result

---

**Word Range Guide**

| Range | Type |
|-------|------|
| 100–300 | Short & punchy |
| 300–600 | Balanced |
| 600–1500 | Detailed |
| 1500–4000 | Extended |
| 4000–10000 | Exhaustive |

---

**Setup**

```bash
ollama serve
ollama pull llama3
streamlit run app.py
```
""")
    st.caption("Prompt AI · Streamlit + Ollama")


# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="pf-footer">
  Prompt AI &nbsp;·&nbsp; Powered by Ollama + Llama 3 &nbsp;·&nbsp; Built with Streamlit
</div>
""", unsafe_allow_html=True)