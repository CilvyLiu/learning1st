import streamlit as st
import pandas as pd
import random
import os

# ---------------------------
# 0️⃣ 路径与初始化
# ---------------------------
base_path = os.path.dirname(__file__)

def get_path(file_name):
    p = os.path.join(base_path, file_name)
    return p if os.path.exists(p) else None

# 页面配置：设置 wide 模式有利于适配平板和电脑
st.set_page_config(page_title="探险家英语词汇工坊", page_icon="🎒", layout="wide")

# 全局 CSS：优化移动端体验和卡片样式
st.markdown("""
<style>
    .main { background-color: #f5f7f9; }
    /* 响应式卡片容器 */
    .flashcard-container {
        perspective: 1000px;
        margin: 20px auto;
        max-width: 350px;
        height: 220px;
        cursor: pointer;
    }
    .flashcard {
        background-color: white;
        border: 2px solid #2e7d32;
        border-radius: 15px;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .word-text { font-size: 32px; font-weight: bold; color: #2e7d32; }
    .cn-text { font-size: 24px; color: #555; }
    .stButton>button { width: 100%; border-radius: 20px; }
    
    /* 移动端适配：减小内边距 */
    @media (max-width: 600px) {
        .word-text { font-size: 26px; }
        .cn-text { font-size: 20px; }
    }
</style>
""", unsafe_allow_html=True)

# TTS 朗读函数 (JavaScript 代码实现)
def speak_word(word):
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance('{word}');
    msg.lang = 'en-US';
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)

# ---------------------------
# 1️⃣ 词库 (47个单词)
# ---------------------------
DATA = [
    {"id": 1, "word": "travel", "pos": "动词、名词", "cn": "旅行，游历", "example": "I love to travel around the world."},
    {"id": 2, "word": "trip", "pos": "名词、动词", "cn": "旅行，旅游", "example": "We're planning a trip to the mountains next month."},
    {"id": 3, "word": "tour", "pos": "名词、动词", "cn": "旅行，观光", "example": "The band is on a world tour."},
    {"id": 4, "word": "journey", "pos": "名词、动词", "cn": "长途旅行", "example": "The journey by train is very scenic."},
    {"id": 5, "word": "voyage", "pos": "名词、动词", "cn": "航行，航海", "example": "The Titanic's maiden voyage was tragic."},
    {"id": 6, "word": "vacation", "pos": "名词、动词", "cn": "假期", "example": "We're going on vacation to the beach."},
    {"id": 7, "word": "prepare", "pos": "动词", "cn": "准备", "example": "She is preparing for the exam."},
    {"id": 8, "word": "passport", "pos": "名词", "cn": "护照", "example": "You need a valid passport to travel abroad."},
    {"id": 9, "word": "embassy", "pos": "名词", "cn": "大使馆", "example": "He works at the embassy."},
    {"id": 10, "word": "exit", "pos": "名词、动词", "cn": "出口", "example": "Please use the emergency exit in case of fire."},
    {"id": 11, "word": "entry", "pos": "名词", "cn": "进入", "example": "Entry to the museum is free."},
    {"id": 12, "word": "administration", "pos": "名词", "cn": "管理", "example": "The new administration has implemented reforms."},
    {"id": 13, "word": "ministry", "pos": "名词", "cn": "部门", "example": "He works in the Ministry of Education."},
    {"id": 14, "word": "security", "pos": "名词、形容词", "cn": "安全", "example": "Security is very important when traveling."},
    {"id": 15, "word": "visa", "pos": "名词、动词", "cn": "签证", "example": "I need to apply for a visa."},
    {"id": 16, "word": "apply", "pos": "动词", "cn": "申请", "example": "He applied for a job in the company."},
    {"id": 17, "word": "issue", "pos": "名词、动词", "cn": "问题", "example": "The government will issue new policies."},
    {"id": 18, "word": "authority", "pos": "名词", "cn": "权力", "example": "The local authorities are responsible for order."},
    {"id": 19, "word": "luggage", "pos": "名词", "cn": "行李", "example": "He left his luggage at the airport."},
    {"id": 20, "word": "baggage", "pos": "名词", "cn": "行李", "example": "How much baggage can I take on the plane?"},
    {"id": 21, "word": "agency", "pos": "名词", "cn": "代理机构", "example": "I booked the hotel through a travel agency."},
    {"id": 22, "word": "reserve", "pos": "动词、名词", "cn": "预订", "example": "We reserved a table at the restaurant."},
    {"id": 23, "word": "inn", "pos": "名词", "cn": "小旅馆", "example": "We stayed at a cozy inn in the mountains."},
    {"id": 24, "word": "accommodation", "pos": "名词", "cn": "住宿", "example": "The accommodation is very comfortable."},
    {"id": 25, "word": "dormitory", "pos": "名词", "cn": "集体宿舍", "example": "The dormitory is equipped with modern facilities."},
    {"id": 26, "word": "residence", "pos": "名词", "cn": "住宅", "example": "He has a beautiful residence in the countryside."},
    {"id": 27, "word": "escalator", "pos": "名词", "cn": "自动扶梯", "example": "Take the escalator to the second floor."},
    {"id": 28, "word": "elevator", "pos": "名词", "cn": "电梯", "example": "The elevator is out of order."},
    {"id": 29, "word": "lobby", "pos": "名词", "cn": "大厅", "example": "We met in the lobby of the hotel."},
    {"id": 30, "word": "reception", "pos": "名词", "cn": "接待", "example": "The reception at the hotel was very warm."},
    {"id": 31, "word": "laundry", "pos": "名词", "cn": "洗衣房", "example": "I need to take my laundry to the laundry."},
    {"id": 32, "word": "departure", "pos": "名词", "cn": "离开", "example": "The departure time is 9 o'clock."},
    {"id": 33, "word": "check", "pos": "动词、名词", "cn": "检查", "example": "Please check your luggage before you leave."},
    {"id": 34, "word": "destination", "pos": "名词", "cn": "目的地", "example": "Our destination is a small town by the sea."},
    {"id": 35, "word": "attraction", "pos": "名词", "cn": "景点", "example": "The Great Wall is a major tourist attraction."},
    {"id": 36, "word": "heritage", "pos": "名词", "cn": "遗产", "example": "We should protect our cultural heritage."},
    {"id": 37, "word": "museum", "pos": "名词", "cn": "博物馆", "example": "We visited the history museum last weekend."},
    {"id": 38, "word": "gallery", "pos": "名词", "cn": "画廊", "example": "There is an exhibition in the gallery."},
    {"id": 39, "word": "cathedral", "pos": "名词", "cn": "大教堂", "example": "The cathedral is a magnificent building."},
    {"id": 40, "word": "souvenir", "pos": "名词", "cn": "纪念品", "example": "I bought a lot of souvenirs during my trip."},
    {"id": 41, "word": "scenic", "pos": "形容词", "cn": "风景优美的", "example": "We took a drive along the scenic route."},
    {"id": 42, "word": "pleasant", "pos": "形容词", "cn": "令人愉快的", "example": "It was a pleasant trip."},
    {"id": 43, "word": "attractive", "pos": "形容词", "cn": "有吸引力的", "example": "The city has many attractive places."},
    {"id": 44, "word": "fascinating", "pos": "形容词", "cn": "极有吸引力的", "example": "The story is really fascinating."},
    {"id": 45, "word": "marvelous", "pos": "形容词", "cn": "极好的", "example": "The view from the top is marvelous."},
    {"id": 46, "word": "picturesque", "pos": "形容词", "cn": "风景如画的", "example": "The village is really picturesque."},
    {"id": 47, "word": "magnificent", "pos": "形容词", "cn": "壮丽的", "example": "The palace is magnificent."}
]
df = pd.DataFrame(DATA)

# ---------------------------
# 2️⃣ 导航
# ---------------------------
st.sidebar.title("📚 Nova English")
mode = st.sidebar.radio("选择模式", [
    "思维脑图学习",
    "闪卡朗读模式", # 新增
    "单词大闯关",
    "卡片匹配游戏",
    "完整词汇表"
])

# ---------------------------
# 3️⃣ 模式实现
# ---------------------------

# --- 闪卡朗读模式 (新增) ---
if mode == "闪卡朗读模式":
    st.subheader("🗂️ 点击卡片翻面 & 发音")
    
    if "card_idx" not in st.session_state: st.session_state.card_idx = 0
    if "is_flipped" not in st.session_state: st.session_state.is_flipped = False
    
    word_item = DATA[st.session_state.card_idx]
    
    # 显示卡片
    st.markdown(f"""
    <div class="flashcard-container">
        <div class="flashcard">
            <p class="word-text">{word_item['word'] if not st.session_state.is_flipped else word_item['cn']}</p>
            <p style="color:gray;">{'[点击翻面]' if not st.session_state.is_flipped else f'({word_item["pos"]})'}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 交互按钮
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ 上一个"):
            st.session_state.card_idx = (st.session_state.card_idx - 1) % len(DATA)
            st.session_state.is_flipped = False
            st.rerun()
    with col2:
        if st.button("🔄 翻面 / 朗读 🔊"):
            st.session_state.is_flipped = not st.session_state.is_flipped
            speak_word(word_item['word'])
            st.rerun()
    with col3:
        if st.button("下一个 ➡️"):
            st.session_state.card_idx = (st.session_state.card_idx + 1) % len(DATA)
            st.session_state.is_flipped = False
            st.rerun()

# --- 思维脑图学习 ---
elif mode == "思维脑图学习":
    st.subheader("🌟 逻辑联想记忆")
    banner = get_path("banner.jpg")
    if banner: st.image(banner, use_container_width=True)
    
    st.info("💡 记忆口诀：First (准备) -> Next (出发) -> Finally (享受)")
    col1, col2 = st.columns(2)
    with col1:
        st.success("**第一步：准备** (Passport, Visa, Prepare...)")
        st.warning("**第二步：流程** (Check, Departure, Security...)")
    with col2:
        st.error("**第三步：目的地** (Destination, Museum, Scenic...)")

# --- 单词大闯关 ---
elif mode == "单词大闯关":
    st.subheader("🎯 拼写挑战")
    q_idx = st.session_state.get("q_idx", 0)
    row = DATA[q_idx]
    
    st.write(f"第 {q_idx+1} / {len(DATA)} 题")
    st.markdown(f"### 中文：{row['cn']}")
    user_input = st.text_input("拼写英文单词：", key="spell_input")
    
    if st.button("提交答案"):
        if user_input.lower().strip() == row['word'].lower():
            st.balloons()
            st.success("✅ 太棒了！")
            st.session_state.q_idx = (q_idx + 1) % len(DATA)
        else:
            st.error(f"❌ 拼错了，再试一次！正确答案：{row['word']}")

# --- 卡片匹配游戏 ---
elif mode == "卡片匹配游戏":
    st.subheader("🃏 连连看挑战")
    # 增加状态存储避免点击即刷新
    group_idx = st.session_state.get("group_idx", 0)
    current_group = DATA[group_idx*10 : (group_idx+1)*10]
    
    cards = []
    for item in current_group:
        cards.append({"val": item['word'], "id": item['id']})
        cards.append({"val": item['cn'], "id": item['id']})
    
    random.seed(group_idx) # 保证单组内位置固定
    random.shuffle(cards)
    
    cols = st.columns(4)
    for i, card in enumerate(cards):
        with cols[i % 4]:
            st.button(card['val'], key=f"btn_{card['val']}_{i}")

# --- 完整词汇表 ---
elif mode == "完整词汇表":
    st.subheader("📖 全量词汇手册")
    st.dataframe(df[["word","pos","cn","example"]], use_container_width=True)

# ---------------------------
# 4️⃣ 页脚
# ---------------------------
st.divider()
st.caption("“理解是记忆之父，重复是记忆之母。” —— Nova Liu 教学工坊")
