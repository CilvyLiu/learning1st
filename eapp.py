import streamlit as st
import pandas as pd
import random

# 设置页面配置
st.set_page_config(page_title="探险家英语词汇工坊", layout="wide")

# 1. 数据准备
data = [
    [1, "travel", "动词、名词", "旅行，游历；长途行走", "I love to travel around the world and experience different cultures."],
    [2, "trip", "名词、动词", "旅行，旅游；绊倒", "We're planning a trip to the mountains next month."],
    [3, "tour", "名词、动词", "旅行，观光；巡回演出", "The band is on a world tour."],
    [4, "journey", "名词、动词", "（尤指长途）旅行，旅程", "The journey by train is very scenic."],
    [5, "voyage", "名词、动词", "航行，航海；航天", "The Titanic's maiden voyage was tragic."],
    [6, "vacation", "名词、动词", "假期，休假", "We're going on vacation to the beach this summer."],
    [7, "prepare", "动词", "准备，筹备", "She is preparing for the exam."],
    [8, "passport", "名词", "护照；途径", "You need a valid passport to travel abroad."],
    [9, "embassy", "名词", "大使馆", "He works at the embassy."],
    [10, "exit", "名词、动词", "出口；退场", "Please use the emergency exit in case of fire."],
    [11, "entry", "名词", "进入；入口；参赛作品", "Entry to the museum is free."],
    [12, "administration", "名词", "管理；行政；政府", "The new administration has implemented a series of reforms."],
    [13, "ministry", "名词", "（政府的）部；神职", "He works in the Ministry of Education."],
    [14, "security", "名词、形容词", "安全；保安部门", "We need to pay attention to security when traveling."],
    [15, "visa", "名词、动词", "签证", "I need to apply for a visa to go to that country."],
    [16, "apply", "动词", "申请；适用；应用", "He applied for a job in the company."],
    [17, "issue", "名词、动词", "问题；议题；发行", "The government will issue new policies."],
    [18, "authority", "名词", "权力；权威；当局", "The local authorities are responsible for public order."],
    [19, "luggage", "名词", "行李", "He left his luggage at the airport."],
    [20, "baggage", "名词", "行李；负担", "How much baggage can I take on the plane?"],
    [21, "agency", "名词", "代理机构；专门机构", "I booked the hotel through a travel agency."],
    [22, "reserve", "动词、名词", "预订；保留；保护区", "We reserved a table at the restaurant."],
    [23, "inn", "名词", "小旅馆；客栈", "We stayed at a cozy inn in the mountains."],
    [24, "accommodation", "名词", "住处；住宿", "The accommodation in this hotel is very comfortable."],
    [25, "dormitory", "名词", "集体宿舍；学生宿舍", "The dormitory is equipped with modern facilities."],
    [26, "residence", "名词", "住宅；住所", "He has a beautiful residence in the countryside."],
    [27, "escalator", "名词", "自动扶梯", "Take the escalator to the second floor."],
    [28, "elevator", "名词", "电梯；升降机", "The elevator is out of order."],
    [29, "lobby", "名词、动词", "大厅；游说", "We met in the lobby of the hotel."],
    [30, "reception", "名词", "接待；接待处", "The reception at the hotel was very warm."],
    [31, "laundry", "名词", "洗衣房；要洗的衣物", "I need to take my laundry to the laundry."],
    [32, "departure", "名词", "离开；出发", "The departure time of the flight is 9 o'clock."],
    [33, "check", "动词、名词", "检查；核实；支票", "Please check your luggage before you leave."],
    [34, "destination", "名词", "目的地；终点", "Our destination is a small town by the sea."],
    [35, "attraction", "名词", "吸引力；景点", "The Great Wall is a major tourist attraction."],
    [36, "heritage", "名词", "遗产；继承物", "We should protect our cultural heritage."],
    [37, "museum", "名词", "博物馆", "We visited the history museum last weekend."],
    [38, "gallery", "名词", "画廊；美术馆", "There is an art exhibition in the gallery."],
    [39, "cathedral", "名词", "大教堂", "The cathedral is a magnificent building."],
    [40, "souvenir", "名词", "纪念品", "I bought a lot of souvenirs during my trip."],
    [41, "scenic", "形容词", "风景优美的", "We took a drive along the scenic route."],
    [42, "pleasant", "形容词", "令人愉快的；友好的", "It was a pleasant trip."],
    [43, "attractive", "形容词", "有吸引力的；迷人的", "The city has many attractive places."],
    [44, "fascinating", "形容词", "极有吸引力的；迷人的", "The story is really fascinating."],
    [45, "marvelous", "形容词", "极好的；非凡的", "The view from the top is marvelous."],
    [46, "picturesque", "形容词", "风景如画的", "The village is really picturesque."],
    [47, "magnificent", "形容词", "壮丽的；宏伟的", "The palace is magnificent."]
]

df = pd.DataFrame(data, columns=["序号", "英文", "词性", "中文", "例句"])

# 2. 界面设计
st.title("🎒 少年探险家：50年名师带你征服单词")
st.markdown("### 💡 思维方式：First (准备), Next (通关), Finally (享受)")

# 侧边栏
st.sidebar.header("学习导航")
mode = st.sidebar.radio("选择学习模式", ["思维脑图学习", "单词大闯关", "完整词汇表"])

if mode == "思维脑图学习":
    st.subheader("🌟 建立记忆链接")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Step 1: Prepare (准备阶段)**\n\n想象你要出国。首先你得 `prepare`，去 `agency` 咨询，准备 `passport`，去 `embassy` 申请 `visa`。")
        st.success("**Step 2: Next (通关与住宿)**\n\n到达 `destination`。经过 `security` 检查，通过 `entry/exit`。最后入住 `accommodation`，在 `lobby` 的 `reception` 办手续。")
    
    with col2:
        st.warning("**Step 3: Finally (游历美景)**\n\n你会看到 `scenic` 的风景，去 `museum` 看 `heritage`。这些 `magnificent` 的景色会让你觉得旅行非常 `fascinating`。")

    selected_word = st.selectbox("搜索单词深度学习：", df["英文"].tolist())
    word_info = df[df["英文"] == selected_word].iloc[0]
    st.write(f"### {word_info['英文']} ({word_info['词性']})")
    st.write(f"**中文解释：** {word_info['中文']}")
    st.write(f"**地道例句：** {word_info['例句']}")

elif mode == "单词大闯关":
    st.subheader("🎯 挑战你的记忆力")
    if 'quiz_idx' not in st.session_state:
        st.session_state.quiz_idx = random.randint(0, len(data)-1)
    
    q_word = data[st.session_state.quiz_idx]
    st.write(f"#### 这个单词的中文是：**“{q_word[3]}”**，它是哪个词？")
    
    user_ans = st.text_input("输入英文单词：").strip().lower()
    if st.button("检查答案"):
        if user_ans == q_word[1].lower():
            st.balloons()
            st.success("太棒了！你已经掌握了这个探险词汇！")
            if st.button("下一个"):
                st.session_state.quiz_idx = random.randint(0, len(data)-1)
                st.rerun()
        else:
            st.error(f"差一点点！正确答案是：{q_word[1]}。再试一次？")

elif mode == "完整词汇表":
    st.subheader("📖 词汇字典")
    st.dataframe(df, use_container_width=True)
    
    # 下载功能
    csv = df.to_csv(index=False).encode('utf_8_sig')
    st.download_button("下载词汇表 (CSV)", csv, "vocabulary_list.csv", "text/csv")

# 页脚名师寄语
st.divider()
st.caption("“理解是记忆之父，重复是记忆之母。” —— Nova Liu & Gemini 联合呈现")
