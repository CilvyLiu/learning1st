import streamlit as st
import pandas as pd
import random
import os
import time
import re

# ---------------------------
# 0️⃣ 路径与初始化
# ---------------------------
base_path = os.path.dirname(__file__)

def get_path(file_name):
    p = os.path.join(base_path, file_name)
    return p if os.path.exists(p) else None

# 页面配置
st.set_page_config(page_title="探险家英语词汇工坊", page_icon="🎒", layout="wide")

# 初始化积分和状态
if "score" not in st.session_state: st.session_state.score = 0
if "q_idx" not in st.session_state: st.session_state.q_idx = 0
if "ex_idx" not in st.session_state: st.session_state.ex_idx = 0
if "card_idx" not in st.session_state: st.session_state.card_idx = 0
if "is_flipped" not in st.session_state: st.session_state.is_flipped = False

# 全局 CSS
st.markdown("""
<style>
    .main { background-color: #f5f7f9; }
    .score-box { background: #2e7d32; color: white; padding: 12px; border-radius: 12px; text-align: center; font-size: 22px; margin-bottom: 20px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .flashcard-container { perspective: 1000px; margin: 20px auto; max-width: 350px; height: 220px; cursor: pointer; }
    .flashcard { background-color: white; border: 2px solid #2e7d32; border-radius: 15px; height: 100%; display: flex; 
                 flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 20px; 
                 box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    .word-text { font-size: 32px; font-weight: bold; color: #2e7d32; }
    .stButton>button { width: 100%; border-radius: 20px; font-weight: bold; height: 3em; }
</style>
""", unsafe_allow_html=True)

# TTS 朗读函数
def speak_word(word):
    js_code = f"""<script>var msg = new SpeechSynthesisUtterance('{word}'); msg.lang = 'en-US'; window.speechSynthesis.speak(msg);</script>"""
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

# ---------------------------
# 2️⃣ 导航与分组
# ---------------------------
logo_path = get_path("logo.png")
if logo_path: st.sidebar.image(logo_path)

st.sidebar.title("📚 Nova English")
mode = st.sidebar.radio("选择模式", [
    "思维脑图学习", "闪卡朗读模式", "单词大闯关", "卡片匹配游戏", "例句挖空练习", "完整词汇表"
])

group_options = {
    "1-10": (0, 10), "11-20": (10, 20), "21-30": (20, 30), "31-40": (30, 40), "41-47": (40, 47)
}
group_key = st.sidebar.selectbox("选择词汇组", list(group_options.keys()))
start, end = group_options[group_key]
CURRENT_DATA = DATA[start:end]

# 顶部积分
st.markdown(f'<div class="score-box">⭐ 探险积分：{st.session_state.score}</div>', unsafe_allow_html=True)

# ---------------------------
# 3️⃣ 模式实现
# ---------------------------

# --- A. 思维脑图 (包含 banner.jpg 和 mindmap.png) ---
if mode == "思维脑图学习":
    st.subheader("🌟 逻辑联想记忆")
    
    # 加载 Banner
    banner_img = get_path("banner.jpg")
    if banner_img:
        st.image(banner_img, use_container_width=True)
    
    st.info("💡 记忆口诀：First (准备) -> Next (出发) -> Finally (享受)")
    
    # 加载思维脑图
    mindmap_img = get_path("mindmap.png")
    if mindmap_img:
        st.image(mindmap_img, caption="核心词汇思维导图", use_container_width=True)
    else:
        # 如果没有图，显示文字版简易导图
        col1, col2 = st.columns(2)
        with col1:
            st.success("**第一步：准备** (Passport, Visa, Prepare...)")
        with col2:
            st.error("**第二步：目的地** (Destination, Museum, Scenic...)")

# --- B. 闪卡朗读 ---
elif mode == "闪卡朗读模式":
    st.subheader("🗂️ 点击卡片翻面 & 发音")
    word_item = CURRENT_DATA[st.session_state.card_idx % len(CURRENT_DATA)]
    
    st.markdown(f"""
    <div class="flashcard-container">
        <div class="flashcard">
            <p class="word-text">{word_item['word'] if not st.session_state.is_flipped else word_item['cn']}</p>
            <p style="color:gray;">{'[点击翻面]' if not st.session_state.is_flipped else f'({word_item["pos"]})'}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ 上一个"):
            st.session_state.card_idx = (st.session_state.card_idx - 1) % len(CURRENT_DATA)
            st.session_state.is_flipped = False
            st.rerun()
    with col2:
        if st.button("🔄 翻面 / 朗读 🔊"):
            st.session_state.is_flipped = not st.session_state.is_flipped
            speak_word(word_item['word'])
            st.rerun()
    with col3:
        if st.button("下一个 ➡️"):
            st.session_state.card_idx = (st.session_state.card_idx + 1) % len(CURRENT_DATA)
            st.session_state.is_flipped = False
            st.rerun()

# --- C. 单词大闯关 ---
elif mode == "单词大闯关":
    st.subheader("🎯 拼写挑战")
    row = CURRENT_DATA[st.session_state.q_idx % len(CURRENT_DATA)]
    st.markdown(f"### 中文：{row['cn']}")
    user_input = st.text_input("拼写英文单词：", key="spell_input").strip().lower()
    
    if st.button("确定提交"):
        if user_input == row['word'].lower():
            st.balloons()
            st.success("✅ 正确！+10 分")
            st.session_state.score += 10
            st.session_state.q_idx += 1
            time.sleep(1)
            st.rerun()
        else:
            st.error(f"❌ 拼错了。正确答案：{row['word']}")

# --- D. 卡片匹配游戏 ---
elif mode == "卡片匹配游戏":
    st.subheader("🃏 连连看挑战")
    if "game_cards" not in st.session_state or st.session_state.get("last_group_match") != group_key:
        pool = []
        for d in CURRENT_DATA:
            pool.append({"id": d['id'], "val": d['word']})
            pool.append({"id": d['id'], "val": d['cn']})
        random.shuffle(pool)
        st.session_state.game_cards = pool
        st.session_state.matched_ids = set()
        st.session_state.selection = []
        st.session_state.last_group_match = group_key

    if len(st.session_state.selection) == 2:
        i1, i2 = st.session_state.selection
        if st.session_state.game_cards[i1]['id'] == st.session_state.game_cards[i2]['id']:
            st.session_state.matched_ids.add(st.session_state.game_cards[i1]['id'])
            st.session_state.score += 20
            st.toast("✅ 匹配成功！+20分")
        else:
            time.sleep(0.8)
        st.session_state.selection = []
        st.rerun()

    back_img = get_path("card.png")
    cols = st.columns(4)
    for i, card in enumerate(st.session_state.game_cards):
        with cols[i % 4]:
            if card['id'] in st.session_state.matched_ids:
                st.write("") # 消除
            else:
                is_sel = i in st.session_state.selection
                if not is_sel:
                    if back_img: 
                        st.image(back_img, use_container_width=True)
                    if st.button("翻开", key=f"match_{i}"):
                        st.session_state.selection.append(i)
                        st.rerun()
                else:
                    st.button(card['val'], key=f"open_{i}", disabled=True)

# --- E. 例句挖空练习 ---
elif mode == "例句挖空练习":
    st.subheader("📝 语境大考验")
    row = CURRENT_DATA[st.session_state.ex_idx % len(CURRENT_DATA)]
    display_sent = re.sub(row['word'], "________", row['example'], flags=re.IGNORECASE)
    
    st.markdown(f"#### 根据语境填空：\n`{display_sent}`")
    st.caption(f"提示：{row['cn']}")
    ans = st.text_input("填入单词：", key="ex_input").strip().lower()
    
    if st.button("确定答案"):
        if ans == row['word'].lower():
            st.success("✅ 语境理解正确！+15 分")
            st.session_state.score += 15
            st.session_state.ex_idx += 1
            time.sleep(1)
            st.rerun()
        else:
            st.error(f"❌ 再试一次？正确单词首字母：{row['word'][0]}")

# --- F. 完整词汇表 ---
elif mode == "完整词汇表":
    st.subheader("📖 全量词汇手册")
    st.dataframe(pd.DataFrame(DATA)[["word","pos","cn","example"]], use_container_width=True)

# ---------------------------
# 4️⃣ 页脚
# ---------------------------
st.divider()
st.caption("“理解是记忆之父，重复是记忆之母。” —— Nova Liu 教学工坊")
