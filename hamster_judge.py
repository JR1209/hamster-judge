import streamlit as st
import random
import time

# 页面配置
st.set_page_config(
    page_title="仓鼠法官裁决系统",
    page_icon="🐹",
    layout="wide"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 18px;
        padding: 15px 30px;
        border-radius: 10px;
        border: none;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown("<h1 style='text-align: center;'>⚖️ 仓鼠法官裁决系统 🐹</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>公正、公平、公开的情侣纠纷智能裁决平台</p>", unsafe_allow_html=True)

# 仓鼠法官形象
st.markdown("<div style='text-align: center; font-size: 100px; margin: 30px 0;'>🐹⚖️</div>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #d35400;'>仓鼠大法官在线待命</h3>", unsafe_allow_html=True)

# API配置（侧边栏）
with st.sidebar:
    st.header("🔧 API 配置")
    api_key = st.text_input("Qwen API Key (可选)", type="password")
    api_url = st.text_input("API 地址", value="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions")
    st.info("💡 暂时使用模拟模式")

# 输入区域
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🙋 甲方陈述")
    party_a = st.text_area(
        "甲方陈述",
        placeholder="请输入甲方的观点和理由...\n\n例如：我觉得他总是不听我说话，每次我想聊天的时候他都在打游戏...",
        height=200,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("### 🙋‍♂️ 乙方陈述")
    party_b = st.text_area(
        "乙方陈述",
        placeholder="请输入乙方的观点和理由...\n\n例如：我每天工作很累，回家想放松一下...",
        height=200,
        label_visibility="collapsed"
    )

# 提交按钮
if st.button("⚖️ 提交裁决", use_container_width=True):
    if not party_a or not party_b:
        st.error("⚠️ 请输入双方的陈述内容！")
    else:
        # 显示加载动画
        with st.spinner("仓鼠法官正在认真审理中..."):
            time.sleep(2)  # 模拟处理时间
            
            # 简单的评分逻辑
            score_a = len(party_a) + random.randint(30, 50)
            score_b = len(party_b) + random.randint(30, 50)
            total = score_a + score_b
            percent_a = round((score_a / total) * 100)
            percent_b = 100 - percent_a
        
        # 显示结果
        st.markdown("---")
        st.markdown("<div style='text-align: center; font-size: 80px;'>⚖️🐹📜</div>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #d35400;'>⚖️ 仓鼠法庭裁决书 ⚖️</h2>", unsafe_allow_html=True)
        
        # 胜负判定
        if percent_a > percent_b:
            winner = f"🎉 甲方占理 {percent_a}% - 胜诉！"
        elif percent_b > percent_a:
            winner = f"🎉 乙方占理 {percent_b}% - 胜诉！"
        else:
            winner = f"🤝 双方各占 {percent_a}% - 平局！"
        
        st.success(winner)
        
        # 百分比展示
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🙋 甲方理据充分度", f"{percent_a}%")
            st.progress(percent_a / 100)
        with col2:
            st.metric("🙋‍♂️ 乙方理据充分度", f"{percent_b}%")
            st.progress(percent_b / 100)
        
        # 裁决书
        st.markdown("### 📜 详细裁决书")
        verdict = f"""
**【案情编号】**：HC-{int(time.time())}  
**【裁决日期】**：{time.strftime('%Y年%m月%d日')}  
**【主审法官】**：仓鼠大法官 🐹

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**一、案情概述**

本案系一起典型的情侣日常纠纷案件。甲乙双方因沟通方式和相处模式产生分歧，特向本庭申请裁决。

**二、双方观点分析**

【甲方观点】  
{party_a[:100]}{'...' if len(party_a) > 100 else ''}

【乙方观点】  
{party_b[:100]}{'...' if len(party_b) > 100 else ''}

**三、法官意见**

经过认真审理，本法官认为双方都有合理诉求。在亲密关系中，情感需求和个人空间同样重要。

**四、最终裁决**

• 甲方理据充分度：{percent_a}%  
• 乙方理据充分度：{percent_b}%

**五、仓鼠法官的建议** 💝

1️⃣ **建立沟通时间表**：固定每天的聊天时间  
2️⃣ **尊重个人空间**：给彼此独处时间  
3️⃣ **表达需求方式**：用"我需要"代替"你总是"  
4️⃣ **增加仪式感**：每周安排固定的约会时间  
5️⃣ **换位思考**：试着站在对方角度理解TA的感受

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

此致  
仓鼠法庭 🐹⚖️  
{time.strftime('%Y-%m-%d %H:%M:%S')}
        """
        st.info(verdict)

# 页脚
st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>Powered by Streamlit | Made with ❤️</p>", unsafe_allow_html=True)