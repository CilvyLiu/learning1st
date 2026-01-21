import streamlit as st
import pandas as pd
import random
import os
import time
import re
import base64

# ---------------------------
# 0️⃣ 路径与初始化
# ---------------------------
base_path = os.path.dirname(__file__)

def get_path(file_name):
    p = os.path.join(base_path, file_name)
    return p if os.path.exists(p) else None

# 页面配置
st.set_page_config(page_title="探险家英语词汇工坊", page_icon="🎒", layout="wide")

# 初始化所有核心状态，确保刷新时不丢失
if "score" not in st.session_state: st.session_state.score = 0
if "q_idx" not in st.session_state: st.session_state.q_idx = 0
if "ex_idx" not in st.session_state: st.session_state.ex_idx = 0
if "card_idx" not in st.session_state: st.session_state.card_idx = 0
if "is_flipped" not in st.session_state: st.session_state.is_flipped = False
if "matched_ids" not in st.session_state: st.session_state.matched_ids = set()
if "selection" not in st.session_state: st.session_state.selection = []

# ---------------------------
# 1️⃣ 强化版 CSS (动画、阴影、卡片样式)
# ---------------------------
st.markdown("""
<style>
    .main { background-color: #f5f7f9; }
    .score-box { background: #2e7d32; color: white; padding: 12px; border-radius: 12px; text-align: center; font-size: 22px; margin-bottom: 20px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    
    /* 匹配游戏 3D 核心动画 */
    .game-container { width: 100%; height: 160px; perspective: 1000px; margin-bottom: 15px; }
    .game-inner { 
        position: relative; width: 100%; height: 100%; text-align: center; 
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); 
        transform-style: preserve-3d; 
        box-shadow: 0 8px 20px rgba(0,0,0,0.25); /* 边缘阴影 */
        border-radius: 12px;
    }
    .is-flipped { transform: rotateY(180deg); }
    
    .game-front, .game-back { 
        position: absolute; width: 100%; height: 100%; backface-visibility: hidden; 
        display: flex; align-items: center; justify-content: center; border-radius: 12px; padding: 15px;
    }
    
    /* 卡背：如果有图片则显示图片，否则显示默认绿色 */
    .game-back { background-color: #2e7d32; color: white; font-size: 40px; font-weight: bold; }
    .card-img { width: 100%; height: 100%; object-fit: cover; border-radius: 12px; }
    
    /* 卡面：翻转后显示文字 */
    .game-front { 
        background-color: white; color: #2e7d32; transform: rotateY(180deg); 
        border: 3px solid #2e7d32; font-size: 18px; font-weight: bold; overflow-wrap: break-word;
    }
    
    /* 匹配成功消除样式 */
    .is-matched { visibility: hidden; opacity: 0; transition: opacity 0.5s ease-out; }

    /* 拼写打乱显示框 */
    .scramble-box { 
        background: #e8f5e9; border: 2px dashed #2e7d32; padding: 15px; 
        border-radius: 10px; font-size: 28px; letter-spacing: 8px; 
        color: #1b5e20; font-weight: bold; text-align: center; margin: 20px 0;
    }

    .word-text { font-size: 32px; font-weight: bold; color: #2e7d32; }
    .stButton>button { width: 100%; border-radius: 20px; font-weight: bold; height: 3.5em; }
</style>
""", unsafe_allow_html=True)

# TTS 朗读函数
# 重新定义的朗读函数：使用更稳健的注入方式
def speak_word(word):
    if word:
        # 生成一个带随机数的 key 避免缓存
        rid = random.randint(0, 99999)
        js_code = f"""
        <div style="display:none;" id="tts_{rid}">
            <script>
                (function() {{
                    window.speechSynthesis.cancel();
                    var msg = new SpeechSynthesisUtterance('{word}');
                    msg.lang = 'en-US';
                    msg.rate = 0.9;
                    window.speechSynthesis.speak(msg);
                    document.getElementById('tts_{rid}').remove();
                }})();
            </script>
        </div>
        """
        # 使用 st.markdown 配合 unsafe_allow_html 避开组件错误
        st.markdown(js_code, unsafe_allow_html=True)

# ---------------------------
# 2️⃣ 完整词库 (47个单词)
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
    {"id": 17, "word": "issue", "pos": "名词、动词", "cn": "问题/发行", "example": "The government will issue new policies."},
    {"id": 18, "word": "authority", "pos": "名词", "cn": "权力/当局", "example": "The local authorities are responsible for order."},
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
# 3️⃣ 侧边栏与导航
# ---------------------------
logo_path = get_path("logo.png")
if logo_path:
    st.sidebar.image(logo_path, width=200)

st.sidebar.title("📚 Nova English")
mode = st.sidebar.radio("切换学习模式", [
    "思维脑图学习", "闪卡朗读模式", "单词大闯关", "卡片匹配游戏", "例句挖空练习", "完整词汇表"
])

group_options = {
    "1-10": (0, 10), "11-20": (10, 20), "21-30": (20, 30), "31-40": (30, 40), "41-47": (40, 47)
}
group_key = st.sidebar.selectbox("选择词汇组", list(group_options.keys()))
start, end = group_options[group_key]
CURRENT_DATA = DATA[start:end]

with st.sidebar.expander("💡 词根词缀记忆贴士"):
    st.markdown("""
    - **-port-**: 携带/港口 -> `passport` (护照)
    - **-it-**: 走 -> `exit` (出口), `entry` (入口)
    - **-scen-**: 看 -> `scenic` (风景的)
    - **-pre-**: 提前 -> `prepare` (预备)
    - **-esque**: 像...一样的 -> `picturesque` (如画的)
    """)

st.markdown(f'<div class="score-box">⭐ 探险积分：{st.session_state.score}</div>', unsafe_allow_html=True)

# ---------------------------
# 4️⃣ 模式实现
# ---------------------------

# --- A. 思维脑图 ---
if mode == "思维脑图学习":
    st.subheader("🌟 逻辑联想记忆")
    banner = get_path("banner.jpg")
    if banner: st.image(banner, use_container_width=True)
    st.info("💡 记忆口诀：First (准备) -> Next (出发) -> Finally (享受)")
    mindmap = get_path("mindmap.png")
    if mindmap:
        st.image(mindmap, caption="核心词汇思维脑图", use_container_width=True)
    else:
        st.warning("请确保 mindmap.png 在脚本同级目录。")

# --- B. 闪卡朗读 ---
# --- B. 闪卡朗读 ---
elif mode == "闪卡朗读模式":
    st.subheader("🗂️ 点击翻面 & 朗读")
    
    # 获取当前单词
    word_item = CURRENT_DATA[st.session_state.card_idx % len(CURRENT_DATA)]
    
    # 样式容器
    st.markdown("""
    <style>
        .flashcard-box {
            background-color: white;
            border: 4px solid #2e7d32;
            border-radius: 20px;
            padding: 50px 20px;
            text-align: center;
            margin: 20px 0;
            box-shadow: 0 12px 30px rgba(0,0,0,0.15);
            min-height: 250px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 显示内容
    if not st.session_state.is_flipped:
        # 正面
        content_html = f"""
        <div class="flashcard-box">
            <div style="font-size: 48px; font-weight: bold; color: #2e7d32;">{word_item['word']}</div>
            <div style="color: #666; margin-top: 15px;">[ 点击中间按钮翻看中文 ]</div>
        </div>
        """
    else:
        # 反面
        content_html = f"""
        <div class="flashcard-box">
            <div style="font-size: 36px; font-weight: bold; color: #1b5e20;">{word_item['cn']}</div>
            <div style="font-size: 20px; color: #4caf50; margin-top: 10px;">{word_item['pos']}</div>
        </div>
        """
    st.markdown(content_html, unsafe_allow_html=True)
    
    # 控制按钮
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⬅️ 上一个"):
            st.session_state.card_idx = (st.session_state.card_idx - 1) % len(CURRENT_DATA)
            st.session_state.is_flipped = False
            st.rerun()
    with c2:
        if st.button("🔄 翻面并朗读 🔊"):
            # 先切换状态
            st.session_state.is_flipped = not st.session_state.is_flipped
            # 触发朗读
            speak_word(word_item['word'])
            # 强制刷新页面以应用状态
            st.rerun()
    with c3:
        if st.button("下一个 ➡️"):
            st.session_state.card_idx = (st.session_state.card_idx + 1) % len(CURRENT_DATA)
            st.session_state.is_flipped = False
            st.rerun()

# --- C. 单词大闯关 ---
elif mode == "单词大闯关":
    st.subheader("🎯 字母还原挑战")
    row = CURRENT_DATA[st.session_state.q_idx % len(CURRENT_DATA)]
    
    if "scrambled_word" not in st.session_state or st.session_state.get("current_q") != st.session_state.q_idx:
        w_list = list(row['word'])
        random.shuffle(w_list)
        st.session_state.scrambled_word = "".join(w_list)
        st.session_state.current_q = st.session_state.q_idx

    st.markdown(f"### 中文提示：{row['cn']}")
    st.markdown(f'<div class="scramble-box">{st.session_state.scrambled_word}</div>', unsafe_allow_html=True)
    
    user_input = st.text_input("拼写正确的英文单词：", key=f"q_{st.session_state.q_idx}").strip().lower()
    if st.button("确定提交"):
        if user_input == row['word'].lower():
            st.balloons()
            st.success("✅ 完美还原！+10 分")
            st.session_state.score += 10
            st.session_state.q_idx += 1
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ 顺序不对哦，再试一次！")

# --- D. 卡片匹配游戏 ---
elif mode == "卡片匹配游戏":
    st.subheader("🃏 3D 翻转连连看")

    def get_base64_img(path):
        if path and os.path.exists(path):
            with open(path, "rb") as f:
                data = f.read()
            return base64.b64encode(data).decode()
        return None

    card_bg_base64 = get_base64_img(get_path("card.png"))
    bg_style = f"background-image: url('data:image/png;base64,{card_bg_base64}'); background-size: cover;" if card_bg_base64 else "background-color: #2e7d32;"

    if "game_cards" not in st.session_state or st.session_state.get("current_g_key") != group_key:
        pool = []
        for d in CURRENT_DATA:
            pool.append({"id": d['id'], "val": d['word']})
            pool.append({"id": d['id'], "val": d['cn']})
        st.session_state.game_cards = random.sample(pool, len(pool))
        st.session_state.matched_ids = set()
        st.session_state.selection = []
        st.session_state.current_g_key = group_key

    cols = st.columns(4)
    for i, card in enumerate(st.session_state.game_cards):
        with cols[i % 4]:
            is_matched = card['id'] in st.session_state.matched_ids
            is_flipped = i in st.session_state.selection 
            
            flip_class = "is-flipped" if is_flipped else ""
            match_class = "is-matched" if is_matched else ""
            
            st.markdown(f"""
            <div class="game-container {match_class}">
                <div class="game-inner {flip_class}">
                    <div class="game-back" style="{bg_style}"></div>
                    <div class="game-front">{card['val']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if not is_matched and not is_flipped and len(st.session_state.selection) < 2:
                if st.button("翻转", key=f"match_btn_{i}"):
                    st.session_state.selection.append(i)
                    st.rerun()

    if len(st.session_state.selection) == 2:
        idx1, idx2 = st.session_state.selection
        if st.session_state.game_cards[idx1]['id'] == st.session_state.game_cards[idx2]['id']:
            st.session_state.matched_ids.add(st.session_state.game_cards[idx1]['id'])
            st.session_state.score += 20
            st.toast("🔥 Bingo! 匹配成功！")
            time.sleep(0.5)
            st.session_state.selection = []
            if len(st.session_state.matched_ids) == len(CURRENT_DATA):
                st.balloons()
            st.rerun()
        else:
            time.sleep(1.2)
            st.session_state.selection = []
            st.rerun()

# --- E. 例句练习 ---
elif mode == "例句挖空练习":
    st.subheader("📝 语境大考验")
    row = CURRENT_DATA[st.session_state.ex_idx % len(CURRENT_DATA)]
    display_sent = re.sub(row['word'], "________", row['example'], flags=re.IGNORECASE)
    st.markdown(f"#### 根据语境填空：\n`{display_sent}`")
    st.caption(f"提示：{row['cn']}")
    ans = st.text_input("填入单词：", key=f"ex_{st.session_state.ex_idx}").strip().lower()
    if st.button("验证"):
        if ans == row['word'].lower():
            st.success("✅ 语境理解正确！+15 分")
            st.session_state.score += 15
            st.session_state.ex_idx += 1
            time.sleep(1); st.rerun()
        else:
            st.error(f"提示：首字母是 {row['word'][0]}")

# --- F. 完整词汇表 ---
elif mode == "完整词汇表":
    st.subheader("📖 词汇全手册")
    st.dataframe(pd.DataFrame(DATA)[["word","pos","cn","example"]], use_container_width=True)

# ---------------------------
# 5️⃣ 页脚
# ---------------------------
st.divider()
st.caption("First 理解, Next 练习, Finally 掌握。 —— Nova Liu 教学工坊")
