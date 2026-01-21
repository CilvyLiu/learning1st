import streamlit as st
import pandas as pd
import random
import os
base_path = os.path.dirname(__file__)

def get_path(file_name):
    """获取文件的绝对路径"""
    return os.path.join(base_path, file_name)
# =====================================================
# 页面配置（必须置于首行）
# =====================================================
st.set_page_config(
    page_title="探险家英语词汇工坊",
    page_icon="🎒",
    layout="wide"
)

# 自定义 CSS 让界面更美观
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; font-weight: bold; }
    .stProgress > div > div > div > div { background-color: #4CAF50; }
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# 1. 词库数据 (全量 47 个单词)
# =====================================================
DATA = [
    {"id": 1, "word": "travel", "pos": "动词、名词", "cn": "旅行，游历；长途行走", "example": "I love to travel around the world."},
    {"id": 2, "word": "trip", "pos": "名词、动词", "cn": "旅行，旅游；绊倒", "example": "We're planning a trip to the mountains next month."},
    {"id": 3, "word": "tour", "pos": "名词、动词", "cn": "旅行，观光；巡回演出", "example": "The band is on a world tour."},
    {"id": 4, "word": "journey", "pos": "名词、动词", "cn": "（尤指长途）旅行，旅程", "example": "The journey by train is very scenic."},
    {"id": 5, "word": "voyage", "pos": "名词、动词", "cn": "航行，航海；航天", "example": "The Titanic's maiden voyage was tragic."},
    {"id": 6, "word": "vacation", "pos": "名词、动词", "cn": "假期，休假", "example": "We're going on vacation to the beach this summer."},
    {"id": 7, "word": "prepare", "pos": "动词", "cn": "准备，筹备", "example": "She is preparing for the exam."},
    {"id": 8, "word": "passport", "pos": "名词", "cn": "护照；途径", "example": "You need a valid passport to travel abroad."},
    {"id": 9, "word": "embassy", "pos": "名词", "cn": "大使馆", "example": "He works at the embassy."},
    {"id": 10, "word": "exit", "pos": "名词、动词", "cn": "出口；退场", "example": "Please use the emergency exit in case of fire."},
    {"id": 11, "word": "entry", "pos": "名词", "cn": "进入；入口；参赛作品", "example": "Entry to the museum is free."},
    {"id": 12, "word": "administration", "pos": "名词", "cn": "管理；行政；政府", "example": "The new administration has implemented reforms."},
    {"id": 13, "word": "ministry", "pos": "名词", "cn": "（政府的）部；神职", "example": "He works in the Ministry of Education."},
    {"id": 14, "word": "security", "pos": "名词、形容词", "cn": "安全；保安部门", "example": "Security is very important when traveling."},
    {"id": 15, "word": "visa", "pos": "名词、动词", "cn": "签证", "example": "I need to apply for a visa."},
    {"id": 16, "word": "apply", "pos": "动词", "cn": "申请；适用；应用", "example": "He applied for a job in the company."},
    {"id": 17, "word": "issue", "pos": "名词、动词", "cn": "问题；发行", "example": "The government will issue new policies."},
    {"id": 18, "word": "authority", "pos": "名词", "cn": "权力；权威；当局", "example": "The local authorities are responsible for order."},
    {"id": 19, "word": "luggage", "pos": "名词", "cn": "行李", "example": "He left his luggage at the airport."},
    {"id": 20, "word": "baggage", "pos": "名词", "cn": "行李；负担", "example": "How much baggage can I take on the plane?"},
    {"id": 21, "word": "agency", "pos": "名词", "cn": "代理机构", "example": "I booked the hotel through a travel agency."},
    {"id": 22, "word": "reserve", "pos": "动词、名词", "cn": "预订；保留", "example": "We reserved a table at the restaurant."},
    {"id": 23, "word": "inn", "pos": "名词", "cn": "小旅馆；客栈", "example": "We stayed at a cozy inn in the mountains."},
    {"id": 24, "word": "accommodation", "pos": "名词", "cn": "住处；住宿", "example": "The accommodation is very comfortable."},
    {"id": 25, "word": "dormitory", "pos": "名词", "cn": "集体宿舍", "example": "The dormitory is equipped with modern facilities."},
    {"id": 26, "word": "residence", "pos": "名词", "cn": "住宅；住所", "example": "He has a beautiful residence in the countryside."},
    {"id": 27, "word": "escalator", "pos": "名词", "cn": "自动扶梯", "example": "Take the escalator to the second floor."},
    {"id": 28, "word": "elevator", "pos": "名词", "cn": "电梯；升降机", "example": "The elevator is out of order."},
    {"id": 29, "word": "lobby", "pos": "名词", "cn": "大厅；游说", "example": "We met in the lobby of the hotel."},
    {"id": 30, "word": "reception", "pos": "名词", "cn": "接待；接待处", "example": "The reception at the hotel was very warm."},
    {"id": 31, "word": "laundry", "pos": "名词", "cn": "洗衣房", "example": "I need to take my laundry to the laundry."},
    {"id": 32, "word": "departure", "pos": "名词", "cn": "离开；出发", "example": "The departure time is 9 o'clock."},
    {"id": 33, "word": "check", "pos": "动词、名词", "cn": "检查；核实", "example": "Please check your luggage before you leave."},
    {"id": 34, "word": "destination", "pos": "名词", "cn": "目的地；终点", "example": "Our destination is a small town by the sea."},
    {"id": 35, "word": "attraction", "pos": "名词", "cn": "吸引力；景点", "example": "The Great Wall is a major tourist attraction."},
    {"id": 36, "word": "heritage", "pos": "名词", "cn": "遗产；继承物", "example": "We should protect our cultural heritage."},
    {"id": 37, "word": "museum", "pos": "名词", "cn": "博物馆", "example": "We visited the history museum last weekend."},
    {"id": 38, "word": "gallery", "pos": "名词", "cn": "画廊；美术馆", "example": "There is an exhibition in the gallery."},
    {"id": 39, "word": "cathedral", "pos": "名词", "cn": "大教堂", "example": "The cathedral is a magnificent building."},
    {"id": 40, "word": "souvenir", "pos": "名词", "cn": "纪念品", "example": "I bought a lot of souvenirs during my trip."},
    {"id": 41, "word": "scenic", "pos": "形容词", "cn": "风景优美的", "example": "We took a drive along the scenic route."},
    {"id": 42, "word": "pleasant", "pos": "形容词", "cn": "令人愉快的", "example": "It was a pleasant trip."},
    {"id": 43, "word": "attractive", "pos": "形容词", "cn": "有吸引力的", "example": "The city has many attractive places."},
    {"id": 44, "word": "fascinating", "pos": "形容词", "cn": "极有吸引力的", "example": "The story is really fascinating."},
    {"id": 45, "word": "marvelous", "pos": "形容词", "cn": "极好的；非凡的", "example": "The view from the top is marvelous."},
    {"id": 46, "word": "picturesque", "pos": "形容词", "cn": "风景如画的", "example": "The village is really picturesque."},
    {"id": 47, "word": "magnificent", "pos": "形容词", "cn": "壮丽的；宏伟的", "example": "The palace is magnificent."}
]

df = pd.DataFrame(DATA)

# =====================================================
# 2. 侧边栏 (Logo & 导航)
# =====================================================
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_container_width=True)
else:
    st.sidebar.title("🌍 Explorer English")

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
        st.image("mindmap.png", use_container_width=True, caption="探险单词脑图逻辑")
    

    col1, col2 = st.columns(2)
    with col1:
        st.info("**First: Prepare（准备）**\n\n办 `passport` 和 `visa`，去 `embassy` 申请。")
        st.success("**Next: Pass & Stay（抵达）**\n\n过 `security`，带好 `luggage`，入住 `accommodation`。")
    with col2:
        st.warning("**Finally: Enjoy（享受）**\n\n去 `museum` 看 `heritage`，欣赏 `scenic` 的风景。")

    st.divider()
    word_search = st.selectbox("🔍 搜索单词深挖详情", df["word"].tolist())
    row = df[df["word"] == word_search].iloc[0]
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"### ✨ {row['word']} [{row['pos']}]")
    with c2:
        st.markdown(f"> **中文解释：** {row['cn']}")
        st.markdown(f"> **地道例句：** {row['example']}")

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
        if os.path.exists("medal.png"):
            st.image("medal.png", width=150)
        st.success("🏆 太了不起了！你完成了所有 47 个单词挑战！")
        if st.button("重新开启新一轮"):
            st.session_state.used_idx.clear()
            st.rerun()
    else:
        if "quiz_idx" not in st.session_state or st.session_state.quiz_idx not in available:
            st.session_state.quiz_idx = random.choice(available)

        row = df.iloc[st.session_state.quiz_idx]
        
        # 进度条
        progress_val = len(st.session_state.used_idx) / len(df)
        st.progress(progress_val)
        st.write(f"目前进度: {len(st.session_state.used_idx)} / {len(df)}")

        st.info(f"#### 这里的中文是：**“{row['cn']}”**")
        user_ans = st.text_input("✍️ 请输入对应的英文单词", key="quiz_input").strip().lower()

        if st.button("检查答案"):
            if user_ans == row["word"].lower():
                st.success("✅ Bingo! 完全正确！")
                st.balloons()
                st.session_state.used_idx.add(st.session_state.quiz_idx)
                st.button("进入下一个单词")
            else:
                st.error("❌ 差一点点，再试一次！提示：注意拼写或语义场。")

# =====================================================
# 6. 模式三：完整词汇表
# =====================================================
elif mode == "完整词汇表":
    st.subheader("📖 探险家词汇秘籍")
    st.table(df[["word", "pos", "cn"]]) 

    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("⬇️ 下载复习表 (CSV)", csv, "explorer_vocab.csv", "text/csv")

# =====================================================
# 页脚
# =====================================================
st.divider()
st.caption("“理解是记忆之父，重复是记忆之母。” —— Nova Liu 教学工坊 (ESL 50年经验)")
