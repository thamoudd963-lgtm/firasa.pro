import streamlit as st
import anthropic
import re

st.set_page_config(page_title="فِراسة AI", page_icon="👁️", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Tajawal:wght@300;400;500;700&family=DM+Mono:wght@400;500&display=swap');

:root {
    --black: #0a0a0a;
    --white: #ffffff;
    --gray-50: #f9f9f9;
    --gray-100: #f2f2f2;
    --gray-200: #e5e5e5;
    --gray-400: #a0a0a0;
    --gray-600: #666666;
    --gray-800: #222222;
}

* { -webkit-font-smoothing: antialiased; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: var(--gray-50) !important;
    font-family: 'Tajawal', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ── HERO ── */
.hero {
    background: var(--black);
    margin: -1rem -1rem 2.5rem -1rem;
    padding: 64px 32px 56px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(255,255,255,0.04) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 10px; letter-spacing: 6px;
    color: #444; text-transform: uppercase;
    margin-bottom: 28px;
}
.hero-eye {
    margin-bottom: 20px;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(52px, 10vw, 88px);
    font-weight: 400; color: var(--white);
    letter-spacing: -3px; line-height: 0.95;
    margin-bottom: 4px;
}
.hero-title em {
    font-style: italic;
    color: #555;
}
.hero-divider {
    width: 1px; height: 32px;
    background: #333;
    margin: 24px auto;
}
.hero-sub {
    font-family: 'Tajawal', sans-serif;
    font-size: 15px; font-weight: 300;
    color: #555; direction: rtl;
    letter-spacing: 0.3px;
    line-height: 1.6;
}

/* ── INPUT ── */
.field-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px; letter-spacing: 4px;
    color: var(--gray-400); text-transform: uppercase;
    text-align: right; margin-bottom: 8px;
}

[data-testid="stTextArea"] textarea {
    background: var(--white) !important;
    color: var(--black) !important;
    font-family: 'Tajawal', sans-serif !important;
    font-size: 16px !important; font-weight: 400 !important;
    line-height: 1.85 !important;
    border: 1px solid var(--gray-200) !important;
    border-radius: 12px !important;
    padding: 18px !important;
    direction: rtl; text-align: right;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--black) !important;
    box-shadow: 0 0 0 3px rgba(0,0,0,0.06) !important;
}
[data-testid="stTextArea"] textarea::placeholder {
    color: #ccc !important;
}

/* ── BUTTON ── */
[data-testid="stButton"] > button {
    width: 100% !important;
    background: var(--black) !important;
    color: var(--white) !important;
    font-family: 'Tajawal', sans-serif !important;
    font-size: 16px !important; font-weight: 500 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 16px !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
}
[data-testid="stButton"] > button:hover {
    background: #1a1a1a !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── REPORT HEADER ── */
.report-header {
    display: flex; justify-content: space-between;
    align-items: center; direction: rtl;
    padding-bottom: 16px;
    border-bottom: 1.5px solid var(--black);
    margin-bottom: 40px;
}
.report-title {
    font-family: 'DM Serif Display', serif;
    font-size: 24px; color: var(--black);
    letter-spacing: -0.5px;
}
.report-badge {
    font-family: 'DM Mono', monospace;
    font-size: 8px; letter-spacing: 3px;
    color: var(--white); background: var(--black);
    padding: 5px 12px; border-radius: 4px;
    text-transform: uppercase;
}

/* ── SECTION ── */
.section-header {
    display: flex; align-items: center;
    gap: 12px; direction: rtl;
    margin-bottom: 20px; margin-top: 36px;
}
.section-num {
    font-family: 'DM Mono', monospace;
    font-size: 9px; color: var(--gray-400);
    letter-spacing: 2px;
    border: 1px solid var(--gray-200);
    padding: 3px 8px; border-radius: 4px;
}
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 18px; color: var(--black);
    letter-spacing: -0.3px;
}

/* ── PERCENT BARS ── */
.bar-wrap {
    background: var(--white);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 10px;
    border: 1px solid var(--gray-100);
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
}
.bar-row {
    display: flex; justify-content: space-between;
    align-items: center; direction: rtl;
    margin-bottom: 10px;
}
.bar-label {
    font-family: 'Tajawal', sans-serif;
    font-size: 14px; font-weight: 500; color: var(--black);
}
.bar-val {
    font-family: 'DM Mono', monospace;
    font-size: 13px; font-weight: 500; color: var(--black);
}
.bar-track {
    height: 4px; background: var(--gray-100);
    border-radius: 99px; overflow: hidden;
}
.bar-fill {
    height: 4px; background: var(--black);
    border-radius: 99px;
    transition: width 1s ease;
}

/* ── HIDDEN BLOCK ── */
.hidden-block {
    background: var(--white);
    border-radius: 12px;
    border: 1px solid var(--gray-100);
    border-right: 3px solid var(--black);
    padding: 20px 22px;
    font-family: 'Tajawal', sans-serif;
    font-size: 15px; font-weight: 400;
    line-height: 1.9; color: #333;
    direction: rtl; text-align: right;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
}

/* ── REPLY CARDS ── */
.reply-light {
    background: var(--white);
    border: 1px solid var(--gray-200);
    border-radius: 12px;
    padding: 20px 22px; margin-bottom: 10px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.reply-dark {
    background: var(--black);
    border-radius: 12px;
    padding: 20px 22px; margin-bottom: 10px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.15);
}
.reply-type-light {
    font-family: 'DM Mono', monospace;
    font-size: 9px; letter-spacing: 3px;
    color: var(--gray-400); text-transform: uppercase;
    text-align: right; margin-bottom: 10px;
}
.reply-type-dark {
    font-family: 'DM Mono', monospace;
    font-size: 9px; letter-spacing: 3px;
    color: #555; text-transform: uppercase;
    text-align: right; margin-bottom: 10px;
}
.reply-text-light {
    font-family: 'Tajawal', sans-serif;
    font-size: 15px; line-height: 1.9;
    color: #333; direction: rtl; text-align: right;
}
.reply-text-dark {
    font-family: 'Tajawal', sans-serif;
    font-size: 15px; line-height: 1.9;
    color: #bbb; direction: rtl; text-align: right;
}

/* ── ADVICE ── */
.advice-block {
    background: var(--black);
    border-radius: 16px;
    padding: 32px;
    direction: rtl; text-align: right;
    box-shadow: 0 4px 24px rgba(0,0,0,0.15);
}
.advice-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 9px; letter-spacing: 4px;
    color: #444; text-transform: uppercase;
    margin-bottom: 14px;
}
.advice-text {
    font-family: 'DM Serif Display', serif;
    font-size: 17px; font-style: italic;
    color: #ccc; line-height: 1.85;
}

/* ── FOOTER ── */
.footer-wrap {
    margin-top: 64px;
    padding: 32px 0 16px;
    border-top: 1px solid var(--gray-200);
    text-align: center;
}
.footer-name {
    font-family: 'DM Serif Display', serif;
    font-size: 18px; color: var(--black);
    letter-spacing: -0.3px; margin-bottom: 4px;
}
.footer-role {
    font-family: 'DM Mono', monospace;
    font-size: 10px; letter-spacing: 3px;
    color: var(--gray-400); text-transform: uppercase;
    margin-bottom: 16px;
}
.footer-ig {
    display: inline-flex; align-items: center; gap: 6px;
    font-family: 'DM Mono', monospace;
    font-size: 11px; color: var(--gray-600);
    text-decoration: none; letter-spacing: 1px;
    border: 1px solid var(--gray-200);
    padding: 7px 16px; border-radius: 99px;
    transition: all 0.2s;
}
.footer-ig:hover {
    background: var(--black); color: var(--white);
    border-color: var(--black);
}
.footer-copy {
    font-family: 'DM Mono', monospace;
    font-size: 9px; letter-spacing: 2px;
    color: var(--gray-400); margin-top: 20px;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

# ── HERO ──
st.markdown("""
<div class="hero">
  <p class="hero-eyebrow">Digital Physiognomy Engine · v2.0</p>
  <div class="hero-eye">
    <svg width="56" height="36" viewBox="0 0 100 62" fill="none">
      <path d="M5 31 Q50 -8 95 31 Q50 70 5 31Z" stroke="white" stroke-width="1.5" fill="none"/>
      <circle cx="50" cy="31" r="14" fill="white" opacity="0.08"/>
      <circle cx="50" cy="31" r="9" stroke="white" stroke-width="1.5" fill="none"/>
      <circle cx="50" cy="31" r="3.5" fill="white"/>
      <circle cx="53.5" cy="27.5" r="1.8" fill="white" opacity="0.45"/>
    </svg>
  </div>
  <div class="hero-title">فِراسة <em>AI</em></div>
  <div class="hero-divider"></div>
  <p class="hero-sub">حلّل الشخصيات · اقرأ ما بين السطور · تصرّف بذكاء</p>
</div>
""", unsafe_allow_html=True)

# ── API ──
try:
    api_key = st.secrets["ANTHROPIC_KEY"]
    client = anthropic.Anthropic(api_key=api_key)
except Exception:
    st.error("⚠ لم يتم العثور على مفتاح API في الـ Secrets.")
    st.stop()

# ── INPUT ──
st.markdown('<p class="field-label">النص المراد تحليله</p>', unsafe_allow_html=True)
user_input = st.text_area(
    label="input",
    height=155,
    placeholder="الصق هنا رسالة، مقال، أو أي نص تودّ كشف أبعاده الخفية...",
    label_visibility="collapsed"
)

if st.button("ابدأ تحليل الفِراسة ←"):
    if not user_input.strip():
        st.warning("يرجى إدخال نص للتحليل.")
    else:
        with st.spinner("جاري التحليل..."):
            prompt = f"""أنت الآن "كبير خبراء الفِراسة الرقمية". مهمتك هي تحليل النص التالي بعمق استراتيجي وتقديم تقرير مفصل يشمل:

1. **تحليل السمات بنسب مئوية**:
   - الصدق والشفافية: [X]%
   - الثقة بالنفس: [X]%
   - التوتر أو القلق: [X]%
   - العاطفية مقابل العقلانية: [X]%

2. **قراءة ما بين السطور**:
   - ما هو الهدف الحقيقي غير المعلن للكاتب من هذا النص؟
   - هل هناك نبرة تلاعب، استعطاف، أو فرض سيطرة؟

3. **اقتراحات الرد الذكي (3 خيارات)**:
   - **الرد الدبلوماسي**: لامتصاص الموقف والحفاظ على العلاقة.
   - **الرد الحازم**: لوضع حدود واضحة وإظهار القوة.
   - **الرد الودي**: إذا كان النص يحمل نوايا طيبة ويحتاج تقارباً.

4. **نصيحة "الفِراسة" الذهبية**:
   - كيف يجب أن تتعامل مع هذه الشخصية مستقبلاً بناءً على هذا النص؟

اجعل أسلوبك فخماً، تقنياً، ومفيداً جداً.

النص المطلوب تحليله:
"{user_input}"
"""
            try:
                message = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}]
                )
                text = message.content[0].text

                # ── Parse ──
                traits = []
                for m in re.finditer(r'([^:\n*]+):\s*(\d+)%', text):
                    label = re.sub(r'[\*\-\d\.]', '', m.group(1)).strip()
                    val = int(m.group(2))
                    if 2 < len(label) < 60 and 0 <= val <= 100:
                        traits.append((label, val))

                hidden_m = re.search(r'قراءة ما بين السطور[\s\S]*?(?=\n\d\s*[\.\-]|\*\*\d|اقتراح|$)', text, re.I)
                hidden = hidden_m.group(0).replace('**','').strip()[:600] if hidden_m else ""

                dip_m  = re.search(r'الرد الدبلوماسي[^:]*:([\s\S]*?)(?=الرد الحازم|$)', text, re.I)
                firm_m = re.search(r'الرد الحازم[^:]*:([\s\S]*?)(?=الرد الودي|$)', text, re.I)
                frnd_m = re.search(r'الرد الودي[^:]*:([\s\S]*?)(?=نصيحة|###|\d\s*\.|$)', text, re.I)
                replies = []
                if dip_m:  replies.append(("🤝 &nbsp; دبلوماسي", dip_m.group(1).replace('**','').strip()[:320], "light"))
                if firm_m: replies.append(("⚡ &nbsp; حازم", firm_m.group(1).replace('**','').strip()[:320], "dark"))
                if frnd_m: replies.append(("✨ &nbsp; ودّي", frnd_m.group(1).replace('**','').strip()[:320], "light"))

                adv_m = re.search(r'نصيحة[\s\S]*?الذهبية[^:]*:([\s\S]*?)(?=$|\n\n\n)', text, re.I)
                advice = adv_m.group(1).replace('**','').strip()[:500] if adv_m else ""

                # ── Render ──
                st.markdown("""
                <div class="report-header">
                  <span class="report-title">تقرير الفِراسة</span>
                  <span class="report-badge">Classified</span>
                </div>""", unsafe_allow_html=True)

                # 01
                if traits:
                    st.markdown("""<div class="section-header">
                      <span class="section-num">01</span>
                      <span class="section-title">السمات الشخصية</span>
                    </div>""", unsafe_allow_html=True)
                    for label, val in traits:
                        st.markdown(f"""
                        <div class="bar-wrap">
                          <div class="bar-row">
                            <span class="bar-label">{label}</span>
                            <span class="bar-val">{val}%</span>
                          </div>
                          <div class="bar-track">
                            <div class="bar-fill" style="width:{val}%"></div>
                          </div>
                        </div>""", unsafe_allow_html=True)

                # 02
                if hidden:
                    st.markdown("""<div class="section-header">
                      <span class="section-num">02</span>
                      <span class="section-title">قراءة ما بين السطور</span>
                    </div>""", unsafe_allow_html=True)
                    st.markdown(f'<div class="hidden-block">{hidden}</div>', unsafe_allow_html=True)

                # 03
                if replies:
                    st.markdown("""<div class="section-header">
                      <span class="section-num">03</span>
                      <span class="section-title">اقتراحات الرد الذكي</span>
                    </div>""", unsafe_allow_html=True)
                    for rtype, rcontent, rvar in replies:
                        if rvar == "dark":
                            st.markdown(f"""
                            <div class="reply-dark">
                              <div class="reply-type-dark">{rtype}</div>
                              <div class="reply-text-dark">{rcontent}</div>
                            </div>""", unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="reply-light">
                              <div class="reply-type-light">{rtype}</div>
                              <div class="reply-text-light">{rcontent}</div>
                            </div>""", unsafe_allow_html=True)

                # 04
                if advice:
                    st.markdown("""<div class="section-header">
                      <span class="section-num">04</span>
                      <span class="section-title">نصيحة الفِراسة الذهبية</span>
                    </div>""", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="advice-block">
                      <div class="advice-eyebrow">Golden Insight</div>
                      <div class="advice-text">{advice}</div>
                    </div>""", unsafe_allow_html=True)

                if not traits and not replies:
                    st.markdown(f'<div class="hidden-block">{text}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"حدث خطأ: {e}")

# ── FOOTER ──
st.markdown("""
<div class="footer-wrap">
  <div class="footer-name">thamoud</div>
  <div class="footer-role">Developer · فِراسة AI</div>
  <a class="footer-ig" href="https://www.instagram.com/thamoudd?igsh=ZHB0bjdzbXM5dGx0" target="_blank">
    <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
    </svg>
    @thamoudd
  </a>
  <div class="footer-copy">© 2026 Firasa AI · All rights reserved</div>
</div>
""", unsafe_allow_html=True)
