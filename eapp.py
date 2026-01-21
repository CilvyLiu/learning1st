import streamlit as st
import pandas as pd
import random
import os

# =====================================================
# 页面配置（必须最前）
# =====================================================
st.set_page_config(
    page_title="探险家英语词汇工坊",
    layout="wide"
)

# 自定义 CSS 让界面更美观
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# 1. 词库数据 (包含全部47个单词)
# =====================================================
DATA = [
    {"id": 1, "word": "travel", "pos": "动词、名词", "cn": "旅行，游历", "example": "I love to travel around the world."},
    {"id": 2, "word": "trip", "pos": "名词、动词", "cn": "旅行，旅游", "example": "We're planning a trip to the mountains."},
    {"id": 3, "word": "tour", "pos": "名词、动词", "cn": "观光，巡回", "example": "The band is on a world tour."},
    {"id": 4, "word": "journey", "pos": "名词、动词", "cn": "旅程", "example": "The journey by train is very scenic."},
    {"id": 5, "word": "voyage", "pos": "名词、动词", "cn": "航海，航行", "example": "The Titanic's maiden voyage was tragic."},
    {"id": 6, "word": "vacation", "pos": "名词", "cn": "假期，休假", "example": "We're going on vacation to the beach."},
    {"id": 7, "word": "prepare", "pos": "动词", "cn": "准备", "example": "She is preparing for the exam."},
    {"id": 8, "word": "passport", "pos": "名词", "cn": "护照", "example": "You need a valid passport to travel."},
    {"id": 9, "word": "embassy", "pos": "名词", "cn": "大使馆", "example": "He works at the embassy."},
    {"id": 10, "word": "exit", "pos": "名词、动词", "cn": "出口", "example": "Use the emergency exit in case of fire."},
    {"id": 11, "word": "entry", "pos": "名词", "cn": "入口", "example": "Entry to the museum is free."},
    {"id": 12, "word": "administration", "pos": "名词", "cn": "管理，行政", "example": "The new administration implemented reforms."},
    {"id": 13, "word": "ministry", "pos": "名词", "cn": "（政府的）部", "example": "He works in the Ministry of Education."},
    {"id": 14, "word": "security", "pos": "名词", "cn": "安全，保安", "example": "Pay attention to security when traveling."},
    {"id": 15, "word": "visa", "pos": "名词", "cn": "签证", "example": "I need to apply for a visa."},
    {"id": 16, "word": "apply", "pos": "动词", "cn": "申请", "example": "He applied for a job."},
    {"id": 17, "word": "issue", "pos": "名词、动词", "cn": "发行，发布", "example": "The government will issue new policies."},
    {"id": 18, "word": "authority", "pos": "名词", "cn": "权力，当局", "example": "The local authorities maintain order."},
    {"id": 19, "word": "luggage", "pos": "名词", "cn": "行李", "example": "He left his luggage at the airport."},
    {"id": 20, "word": "baggage", "pos": "名词", "cn": "行李", "example": "How much baggage can I take?"},
    {"id": 21, "word": "agency", "pos": "名词", "cn": "代理机构", "example": "I booked via a travel agency."},
    {"id": 22, "word": "reserve", "pos": "动词", "cn": "预订", "example": "We reserved a table at the restaurant."},
    {"id": 23, "word": "inn", "pos": "名词", "cn": "小旅馆", "example": "We stayed at a cozy inn."},
    {"id": 24, "word": "accommodation", "pos": "名词", "cn": "住处", "example": "The accommodation is very comfortable."},
    {"id": 25, "word": "dormitory", "pos": "名词", "cn": "宿舍", "example": "The dormitory has modern facilities."},
    {"id": 26, "word": "residence", "pos": "名词", "cn": "住宅", "example": "He has a residence in the countryside."},
    {"id": 27, "word": "escalator", "pos": "名词", "cn": "自动扶梯", "example": "Take the escalator to the 2nd floor."},
    {"id": 28, "word": "elevator", "pos": "名词", "cn": "电梯", "example": "The elevator is out of order."},
    {"id": 29, "word": "lobby", "pos": "名词", "cn": "大厅", "example": "We met in the hotel lobby."},
    {"id": 30, "word": "reception", "pos": "名词", "cn": "接待处", "example": "The reception was very warm."},
    {"id": 31, "word": "laundry", "pos": "名词", "cn": "洗衣房", "example": "I need to take my laundry."},
    {"id": 32, "word": "departure", "pos": "名词", "cn": "离开，起程", "example": "Departure time is 9 o'clock."},
    {"id": 33, "word": "check", "动词", "cn": "检查", "example": "Check your luggage before leaving."},
    {"id": 34, "word": "destination", "名词", "cn": "目的地", "example": "Our destination is a small town."},
    {"id": 35, "word": "attraction", "名词", "cn": "景点", "example": "The Great Wall is a major attraction."},
    {"id": 36, "word": "heritage", "名词", "cn": "遗产", "example": "Protect our cultural heritage."},
    {"id": 37, "word": "museum", "名词", "cn": "博物馆", "example": "We visited the museum."},
    {"id": 38, "word": "gallery", "名词", "cn": "画廊", "example": "There is an exhibition in the gallery."},
    {"id": 39, "word": "cathedral", "名词", "cn": "大教堂", "example": "The cathedral is magnificent."},
    {"id": 40, "word": "souvenir", "名词", "cn": "纪念品", "example": "I bought souvenirs during my trip."},
    {"id": 41, "word": "scenic", "形容词", "cn": "风景优美的", "example": "We took the scenic route."},
    {"id": 42, "word": "pleasant", "形容词", "cn": "愉快的", "example": "It was a pleasant trip."},
    {"id": 43, "word": "attractive", "形容词", "cn": "有吸引力的", "example": "The city has attractive places."},
    {"id": 44, "word": "fascinating", "形容词", "cn": "迷人的", "example": "The story is fascinating."},
    {"id": 45, "word": "marvelous", "形容词", "cn": "极好的", "example": "The view is marvelous."},
    {"id": 46, "word": "picturesque", "形容词", "cn": "风景如画的", "example": "The village is picturesque."},
    {"id": 47, "word": "magnificent", "形容词", "cn": "壮丽的", "example": "The palace is magnificent."}
]
]
# 注意：DATA列表可以根据你的全量单词继续添加...

df = pd.DataFrame(DATA)

# =====================================================
# 2. 侧边栏 (Logo & 导航)
# =====================================================
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_container_width=True)
else:
    st.sidebar.title("🌍 Explorer")

st.sidebar.header("📚 学习导航")
mode = st.sidebar.radio("选择模式", ["思维脑图学习", "单词大闯关", "完整词汇表"])

# =====================================================
# 3. 主界面顶部 Banner
# =====================================================
if os.path.exists("banner.jpg"):
    st.image("banner.jpg", use_container_width=True)

st.title("🎒 少年探险家词汇课")
st.markdown("### 🧠 记忆公式：**First (准备) → Next (出发) → Finally (享受)**")

# =====================================================
# 4. 模式一：思维脑图学习
# =====================================================
if mode == "思维脑图学习":
    st.subheader("🌟 用故事建立记忆链接")
    
    if os.path.exists("mindmap.png"):
        st.image("mindmap.png", use_container_width=True, caption="探险单词脑图")
    

    col1, col2 = st.columns(2)
    with col1:
        st.info("**First: Prepare（准备）**\n\n办 `passport` 和 `visa`，去 `embassy` 申请。")
        st.success("**Next: Pass & Stay（抵达）**\n\n过 `security`，带好 `luggage`，入住 `accommodation`。")
    with col2:
        st.warning("**Finally: Enjoy（享受）**\n\n去 `museum` 看 `heritage`，欣赏 `scenic` 的风景。")

    word = st.selectbox("🔍 搜索单词深挖", df["word"].tolist())
    row = df[df["word"] == word].iloc[0]
    st.markdown(f"### ✨ {row['word']} [{row['pos']}]")
    st.markdown(f"> **中文：** {row['cn']}")
    st.markdown(f"> **例句：** {row['example']}")

# =====================================================
# 5. 模式二：单词大闯关
# =====================================================
elif mode == "单词大闯关":
    st.subheader("🎯 勇敢者的挑战")

    if "used_idx" not in st.session_state:
        st.session_state.used_idx = set()

    available = list(set(range(len(df))) - st.session_state.used_idx)
    
    if not available:
        st.balloons()
        st.success("🏆 太了不起了！你完成了所有单词挑战！")
        if st.button("重新开启下一轮"):
            st.session_state.used_idx.clear()
            st.rerun()
    else:
        if "quiz_idx" not in st.session_state or st.session_state.quiz_idx not in available:
            st.session_state.quiz_idx = random.choice(available)

        row = df.iloc[st.session_state.quiz_idx]
        
        # 进度条
        progress = len(st.session_state.used_idx) / len(df)
        st.progress(progress)
        st.write(f"目前进度: {len(st.session_state.used_idx)} / {len(df)}")

        st.info(f"#### 这里的中文是：**“{row['cn']}”**")
        user_ans = st.text_input("✍️ 请输入对应的英文单词", key="quiz_input").strip().lower()

        if st.button("检查答案"):
            if user_ans == row["word"].lower():
                # 答对了显示奖牌
                if os.path.exists("medal.png"):
                    st.image("medal.png", width=120)
                st.success("✅ Bingo! 完全正确！")
                st.balloons()
                st.session_state.used_idx.add(st.session_state.quiz_idx)
                # 停留一秒让孩子看清楚
                st.button("进入下一题")
            else:
                st.error("❌ 差一点点，再试一次！提示：注意拼写哦。")

# =====================================================
# 6. 模式三：完整词汇表
# =====================================================
elif mode == "完整词汇表":
    st.subheader("📖 探险家词汇秘籍")
    st.table(df[["word", "pos", "cn"]]) # 使用table展示更清晰

    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("⬇️ 点击下载课后复习表 (CSV)", csv, "vocab.csv", "text/csv")

# 页脚
st.divider()
st.caption("“理解是记忆之父，重复是记忆之母。” —— Nova Liu 教学工坊 (ESL 50年经验)")
