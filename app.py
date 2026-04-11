import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="IEEE_Results", page_icon="⚡", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

* { font-family: 'Cairo', sans-serif !important; box-sizing: border-box; }

.stApp {
    background: linear-gradient(135deg, #080c14 0%, #0d1526 100%);
    color: #e0e8ff;
}

/* عنوان */
.title {
    font-size: clamp(1.8em, 5vw, 2.8em);
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #00d4ff, #7b61ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
    line-height: 1.2;
}
.subtitle {
    text-align: center;
    color: #8899cc;
    font-size: clamp(0.9em, 3vw, 1.1em);
    margin-bottom: 20px;
}

/* كارد السؤال */
.q-card {
    background: #111827;
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: clamp(16px, 4vw, 28px);
    margin: 12px 0;
}
.q-text {
    font-size: clamp(1em, 3.5vw, 1.25em);
    font-weight: 700;
    color: #e0e8ff;
    margin-bottom: 16px;
    line-height: 1.5;
}

/* نتيجة */
.result-card {
    background: linear-gradient(135deg, #0d1f3c, #1a2d4a);
    border: 2px solid #00d4ff;
    border-radius: 20px;
    padding: clamp(20px, 5vw, 40px);
    text-align: center;
    margin: 16px 0;
    box-shadow: 0 0 40px rgba(0,212,255,0.1);
}
.result-name { color: #8899cc; font-size: clamp(0.9em, 3vw, 1.1em); margin-bottom: 6px; }
.result-team { font-size: clamp(1.5em, 6vw, 2.5em); font-weight: 900; margin: 8px 0; }
.result-desc { color: #c0d0f0; font-size: clamp(0.9em, 3vw, 1.05em); margin: 12px 0; line-height: 1.6; }
.result-rec {
    background: rgba(0,212,255,0.07);
    border-radius: 10px;
    padding: clamp(10px, 3vw, 15px);
    margin-top: 16px;
    font-size: clamp(0.85em, 2.5vw, 1em);
    font-weight: 700;
    line-height: 1.6;
}

/* insight */
.insight-box {
    background: #111827;
    border-left: 4px solid #00d4ff;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
    color: #c0d0f0;
    font-size: clamp(0.85em, 2.5vw, 1em);
    line-height: 1.6;
}

/* metric */
.metric-box {
    background: #111827;
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: clamp(12px, 3vw, 20px);
    text-align: center;
    height: 100%;
}
.metric-num {
    font-size: clamp(1.5em, 5vw, 2.5em);
    font-weight: 900;
    color: #00d4ff;
    line-height: 1.2;
}
.metric-lbl { color: #8899cc; font-size: clamp(0.75em, 2vw, 0.9em); margin-top: 4px; }

/* زرار */
.stButton > button {
    background: linear-gradient(135deg, #00d4ff, #7b61ff) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 20px !important;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 700 !important;
    font-size: clamp(0.95em, 3vw, 1.05em) !important;
    width: 100% !important;
    margin-top: 8px !important;
}

/* radio */
div[data-testid="stRadio"] label {
    color: #c0d0f0 !important;
    font-size: clamp(0.9em, 2.8vw, 1.05em) !important;
    line-height: 1.6 !important;
    padding: 6px 0 !important;
}
div[data-testid="stRadio"] > div {
    gap: 8px !important;
}

/* input */
.stTextInput > div > div > input {
    background: #111827 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 10px !important;
    color: #e0e8ff !important;
    font-size: clamp(0.95em, 3vw, 1.05em) !important;
    padding: 12px !important;
}

/* progress */
.stProgress > div > div {
    background: linear-gradient(90deg, #00d4ff, #7b61ff) !important;
    border-radius: 10px !important;
}

/* nav */
div[data-testid="stRadio"][data-baseweb="radio"] label {
    font-size: clamp(0.9em, 2.8vw, 1em) !important;
}

hr { border-color: #1e3a5f !important; }
</style>
""", unsafe_allow_html=True)

# ============================================
# Teams
# ============================================
TEAMS = {
    "Data & AI 📊": {
        "color": "#00d4ff",
        "وصف": "بتحب الأرقام والتحليل واكتشاف patterns مخفية في البيانات",
        "ابدأ بـ": "Python ← SQL ← Machine Learning ← Data Visualization"
    },
    "Frontend 💻": {
        "color": "#ff6b6b",
        "وصف": "بتحب تصميم واجهات جميلة وتخلي تجربة المستخدم مميزة",
        "ابدأ بـ": "HTML & CSS ← JavaScript ← React ← Figma"
    },
    "Backend ⚙️": {
        "color": "#7b61ff",
        "وصف": "بتحب بناء الأنظمة اللي بتشتغل من ورا الكواليس وتخلي كل حاجة تمشي",
        "ابدأ بـ": "Python ← APIs ← Databases ← Server Management"
    },
    "Security 🔒": {
        "color": "#ff4757",
        "وصف": "بتحب تكتشف الثغرات وتحمي الأنظمة من الهجمات",
        "ابدأ بـ": "Networking ← Linux ← Ethical Hacking ← Cybersecurity"
    },
    "Marketing 📣": {
        "color": "#ffa502",
        "وصف": "بتحب توصل الأفكار للناس وتخلي أكبر عدد يعرف عن IEEE",
        "ابدأ بـ": "Content Creation ← Social Media ← Graphic Design ← Analytics"
    },
    "HR 🤝": {
        "color": "#2ed573",
        "وصف": "بتحب تطور الناس وتبني فريق قوي ومترابط",
        "ابدأ بـ": "People Management ← Recruitment ← Training ← Team Building"
    },
    "PR 🎙️": {
        "color": "#ff6b81",
        "وصف": "بتحب تتكلم وتمثل IEEE وتبني علاقات قوية مع الجميع",
        "ابدأ بـ": "Public Speaking ← Writing ← Event Management ← Networking"
    },
    "PM 📋": {
        "color": "#eccc68",
        "وصف": "بتحب تنظم المشاريع وتقود الفرق وتوصل للهدف في الوقت الصح",
        "ابدأ بـ": "Agile ← Scrum ← Project Planning ← Leadership"
    },
    "Logistics 🚚": {
        "color": "#a29bfe",
        "وصف": "بتحب تنفذ وتنسق وتخلي كل تفصيلة في مكانها الصح",
        "ابدأ بـ": "Operations ← Event Coordination ← Planning ← Resource Management"
    },
}

# ============================================
# Questions
# ============================================
QUESTIONS = [
    {
        "سؤال": "🤔 لما بتواجه مشكلة، أول حاجة بتعملها إيه؟",
        "اختيارات": {
            "بجمع معلومات وأحلل الأرقام قبل ما أحكم": {"Data & AI 📊": 3, "Backend ⚙️": 2},
            "بفكر في حل إبداعي وأجرب أفكار جديدة": {"Frontend 💻": 3, "Marketing 📣": 2},
            "بتكلم مع الناس وأسمع وجهات نظر مختلفة": {"HR 🤝": 3, "PR 🎙️": 2},
            "بعمل خطة واضحة وأقسم المشكلة لخطوات صغيرة": {"PM 📋": 3, "Logistics 🚚": 2},
        }
    },
    {
        "سؤال": "💡 إيه اللي بيوصفك أكتر في الشغل؟",
        "اختيارات": {
            "بحب الأرقام والكود وحل المشاكل المعقدة": {"Data & AI 📊": 3, "Backend ⚙️": 2, "Security 🔒": 1},
            "بحب الشكل والجماليات وأعمل حاجات تبان حلوة": {"Frontend 💻": 3, "Marketing 📣": 2},
            "بحب أتكلم مع الناس وأفهمهم وأساعدهم": {"HR 🤝": 3, "PR 🎙️": 2},
            "بحب أنظم وأخطط وأتأكد إن كل حاجة ماشية صح": {"PM 📋": 3, "Logistics 🚚": 2},
        }
    },
    {
        "سؤال": "🎯 لو اتديتلك مشروع IEEE كامل، هتختار تعمل إيه؟",
        "اختيارات": {
            "أحلل البيانات أو أبني الـ technical solution": {"Data & AI 📊": 3, "Backend ⚙️": 2, "Security 🔒": 1},
            "أصمم الـ website أو أعمل الـ marketing campaign": {"Frontend 💻": 3, "Marketing 📣": 2},
            "أتواصل مع الناس وأمثل الفريق وأبني العلاقات": {"PR 🎙️": 3, "HR 🤝": 2},
            "أنظم الفريق والمواعيد وأتأكد إن كل حاجة بتتنفذ": {"PM 📋": 3, "Logistics 🚚": 2},
        }
    },
    {
        "سؤال": "📱 إيه المحتوى اللي بتستهلكه أكتر على النت؟",
        "اختيارات": {
            "مقالات تكنولوجيا وـ tutorials وأخبار AI": {"Data & AI 📊": 3, "Backend ⚙️": 1, "Security 🔒": 2},
            "محتوى تصميم وـ UI/UX وـ branding وـ trends": {"Frontend 💻": 3, "Marketing 📣": 2},
            "بودكاست تطوير ذات وقيادة وعلاقات إنسانية": {"HR 🤝": 3, "PR 🎙️": 2},
            "محتوى إنتاجية وتنظيم وقت وـ project management": {"PM 📋": 3, "Logistics 🚚": 2},
        }
    },
    {
        "سؤال": "😤 إيه أكتر حاجة بتضايقك في الـ teamwork؟",
        "اختيارات": {
            "لما بيتاخد قرارات من غير data أو تحليل": {"Data & AI 📊": 3, "Backend ⚙️": 1},
            "لما الشكل والـ design يبقى مش professional": {"Frontend 💻": 3, "Marketing 📣": 2},
            "لما التواصل بين الناس يبقى ضعيف ومفيش وضوح": {"HR 🤝": 3, "PR 🎙️": 2},
            "لما مفيش خطة واضحة أو deadlines محددة": {"PM 📋": 3, "Logistics 🚚": 2},
        }
    }
]

# ============================================
# Session State
# ============================================
for key, val in [
    ("responses", []),
    ("q_index", 0),
    ("answers", []),
    ("name", ""),
    ("show_result", False)
]:
    if key not in st.session_state:
        st.session_state[key] = val

# ============================================
# حساب النتيجة
# ============================================
def calculate_team(answers):
    scores = {team: 0 for team in TEAMS}
    for answer in answers:
        for team, points in answer.items():
            if team in scores:
                scores[team] += points
    return max(scores, key=scores.get), scores

# ============================================
# Header
# ============================================
st.markdown('<div class="title">⚡ IEEE Team Finder</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">اكتشف انت مناسب لأي team في IEEE</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    mode = st.radio("", ["🎯 Quiz", "📊 Dashboard"], horizontal=True, label_visibility="collapsed")

st.markdown("---")

# ============================================
# QUIZ
# ============================================
if mode == "🎯 Quiz":

    # نتيجة
    if st.session_state.show_result:
        team, scores = calculate_team(st.session_state.answers)
        info = TEAMS[team]
        color = info["color"]

        st.markdown(f"""
        <div class="result-card">
            <p class="result-name">🎉 {st.session_state.name}، انت مناسب لـ</p>
            <div class="result-team" style="color:{color};">{team}</div>
            <p class="result-desc">{info['وصف']}</p>
            <div class="result-rec" style="color:{color};">
                💡 مسارك:<br>{info['ابدأ بـ']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📊 نقاطك على كل الـ teams")
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        fig = go.Figure(go.Bar(
            x=[s for _, s in sorted_scores],
            y=[t for t, _ in sorted_scores],
            orientation="h",
            marker=dict(color=[TEAMS[t]["color"] for t, _ in sorted_scores]),
            text=[s for _, s in sorted_scores],
            textposition="outside"
        ))
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            height=350,
            margin=dict(l=10, r=50, t=10, b=10),
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, tickfont=dict(size=11))
        )
        st.plotly_chart(fig, use_container_width=True)

        if st.button("🔄 جرب تاني"):
            st.session_state.q_index = 0
            st.session_state.answers = []
            st.session_state.name = ""
            st.session_state.show_result = False
            st.rerun()

    # اسم
    elif st.session_state.name == "":
        st.markdown('<div class="q-card"><p class="q-text">👋 أهلاً! اكتب اسمك الأول</p></div>', unsafe_allow_html=True)
        name = st.text_input("", placeholder="اسمك هنا...", label_visibility="collapsed")
        if st.button("ابدأ الاختبار ⚡"):
            if name.strip():
                st.session_state.name = name.strip()
                st.rerun()
            else:
                st.error("⚠️ اكتب اسمك الأول!")

    # أسئلة
    elif st.session_state.q_index < len(QUESTIONS):
        q = QUESTIONS[st.session_state.q_index]

        st.progress(st.session_state.q_index / len(QUESTIONS))
        st.markdown(f"<p style='color:#8899cc; font-size:0.9em; margin:4px 0;'>سؤال {st.session_state.q_index + 1} من {len(QUESTIONS)}</p>", unsafe_allow_html=True)

        st.markdown(f'<div class="q-card"><p class="q-text">{q["سؤال"]}</p></div>', unsafe_allow_html=True)

        choice = st.radio(
            "",
            list(q["اختيارات"].keys()),
            label_visibility="collapsed",
            key=f"q_{st.session_state.q_index}"
        )

        if st.button("التالي ←"):
            st.session_state.answers.append(q["اختيارات"][choice])
            st.session_state.q_index += 1
            if st.session_state.q_index == len(QUESTIONS):
                team, scores = calculate_team(st.session_state.answers)
                st.session_state.responses.append({
                    "الاسم": st.session_state.name,
                    "Team": team,
                    "الوقت": datetime.now().strftime("%H:%M:%S")
                })
                st.session_state.show_result = True
            st.rerun()

# ============================================
# DASHBOARD
# ============================================
else:
    if not st.session_state.responses:
        st.warning("⏳ لسه مفيش إجابات! قولهم يجاوبوا على الـ Quiz")
    else:
        df = pd.DataFrame(st.session_state.responses)
        total = len(df)
        top_team = df["Team"].value_counts().index[0]
        top_pct = df["Team"].value_counts().iloc[0] / total * 100

        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="metric-box"><div class="metric-num">{total}</div><div class="metric-lbl">👥 المشاركين</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-box"><div class="metric-num" style="font-size:1.1em; word-break:break-word;">{top_team}</div><div class="metric-lbl">🏆 أكتر team</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-box"><div class="metric-num">{top_pct:.0f}%</div><div class="metric-lbl">📊 نسبتهم</div></div>', unsafe_allow_html=True)

        st.markdown("---")

        # Charts
        col1, col2 = st.columns(2)
        with col1:
            tc = df["Team"].value_counts().reset_index()
            tc.columns = ["Team", "عدد"]
            fig1 = px.bar(tc, x="عدد", y="Team", orientation="h",
                         title="توزيع الـ Teams 🏆", color="Team",
                         color_discrete_map={t: TEAMS[t]["color"] for t in TEAMS}, text="عدد")
            fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              font_color="white", showlegend=False, height=380,
                              margin=dict(l=5, r=40, t=40, b=5))
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fig2 = px.pie(df, names="Team", title="النسب المئوية 📊", color="Team",
                         color_discrete_map={t: TEAMS[t]["color"] for t in TEAMS}, hole=0.4)
            fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              font_color="white", height=380,
                              margin=dict(l=5, r=5, t=40, b=5))
            st.plotly_chart(fig2, use_container_width=True)

        # Insights
        st.markdown("---")
        st.markdown("### 💡 التحليل الإحصائي")

        tech = ["Data & AI 📊", "Frontend 💻", "Backend ⚙️", "Security 🔒"]
        people = ["HR 🤝", "PR 🎙️", "Marketing 📣", "PM 📋", "Logistics 🚚"]
        tc = df["Team"].isin(tech).sum()
        pc = df["Team"].isin(people).sum()

        for i in [
            f"👥 {total} شخص خدوا الاختبار لحد دلوقتي",
            f"🏆 {top_pct:.0f}% من الحضور مناسبين لـ {top_team}",
            f"💻 Technical profiles: {tc/total*100:.0f}%  |  🤝 People-oriented: {pc/total*100:.0f}%",
            f"🔥 أغلبية واضحة في {top_team}!" if top_pct > 40 else "⚖️ التوزيع متوازن بين الـ teams!",
            "📌 IEEE بتاعتكم Technical بشكل واضح!" if tc > pc else "📌 IEEE بتاعتكم People-oriented بشكل واضح!"
        ]:
            st.markdown(f'<div class="insight-box">{i}</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📋 نتائج الكل")
        st.dataframe(df[["الاسم", "Team", "الوقت"]], use_container_width=True, hide_index=True)

        csv = df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button("⬇️ نزل الداتا CSV", data=csv.encode("utf-8-sig"),
                          file_name="ieee_results.csv", mime="text/csv")

        st.caption(f"🔄 آخر تحديث: {datetime.now().strftime('%H:%M:%S')}")