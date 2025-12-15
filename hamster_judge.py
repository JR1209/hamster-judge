import streamlit as st
import random
import time
import requests
import json

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
    
    # API模式选择
    api_mode = st.radio(
        "选择运行模式",
        ["模拟模式", "AI模式"],
        help="模拟模式使用随机算法，AI模式使用大语言模型进行智能判断"
    )
    
    if api_mode == "AI模式":
        st.markdown("### API设置")
        api_provider = st.selectbox(
            "API提供商",
            ["通义千问 (Qwen)", "OpenAI", "自定义"],
            help="选择你使用的AI服务提供商"
        )
        
        if api_provider == "通义千问 (Qwen)":
            api_key = st.text_input(
                "API Key", 
                type="password",
                help="在阿里云控制台获取: https://dashscope.console.aliyun.com/apiKey"
            )
            api_url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
            model_name = st.text_input("模型名称", value="qwen-plus", help="可选: qwen-plus, qwen-turbo, qwen-max")
        elif api_provider == "OpenAI":
            api_key = st.text_input("API Key", type="password")
            api_url = "https://api.openai.com/v1/chat/completions"
            model_name = st.text_input("模型名称", value="gpt-3.5-turbo")
        else:  # 自定义
            api_key = st.text_input("API Key", type="password")
            api_url = st.text_input("API 地址", value="https://api.example.com/v1/chat/completions")
            model_name = st.text_input("模型名称", value="gpt-3.5-turbo")
        
        # 判断依据配置
        st.markdown("---")
        st.markdown("### ⚖️ 判断依据配置")
        
        use_custom_criteria = st.checkbox("使用自定义判断标准", value=False)
        
        if use_custom_criteria:
            custom_criteria = st.text_area(
                "自定义判断标准",
                value="""请根据以下标准进行评判：
1. 沟通有效性（30%）：表达是否清晰、理性
2. 情感合理性（25%）：诉求是否合情合理
3. 责任意识（25%）：是否愿意承担责任和改进
4. 尊重程度（20%）：对对方的尊重和理解程度

请给出：
- 甲方得分（0-100）
- 乙方得分（0-100）
- 详细分析
- 建议""",
                height=200,
                help="这将作为AI判断的依据"
            )
        else:
            custom_criteria = None
    else:
        st.info("💡 当前使用模拟模式")
        api_key = None
        api_url = None
        model_name = None
        custom_criteria = None

# AI调用函数
def call_ai_api(party_a_text, party_b_text, api_key, api_url, model_name, criteria=None):
    """调用AI API进行裁决"""
    try:
        # 构建提示词
        if criteria:
            system_prompt = f"""你是一位公正、专业的情侣关系调解专家——仓鼠大法官。
            
{criteria}

请严格按照以上标准进行评判，给出客观、公正的分析。"""
        else:
            system_prompt = """你是一位公正、专业的情侣关系调解专家——仓鼠大法官。

请根据以下标准评判双方的理据充分度：
1. 沟通有效性（30%）：表达是否清晰、理性
2. 情感合理性（25%）：诉求是否合情合理  
3. 责任意识（25%）：是否愿意承担责任和改进
4. 尊重程度（20%）：对对方的尊重和理解程度

请按以下格式输出：
【甲方得分】：X分（0-100）
【乙方得分】：Y分（0-100）
【详细分析】：
（分析内容）
【调解建议】：
（建议内容）"""

        user_prompt = f"""【甲方陈述】
{party_a_text}

【乙方陈述】
{party_b_text}

请对此纠纷进行公正裁决。"""

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        data = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7
        }
        
        response = requests.post(api_url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        ai_response = result['choices'][0]['message']['content']
        
        # 解析AI响应
        return parse_ai_response(ai_response)
        
    except Exception as e:
        st.error(f"❌ AI调用失败: {str(e)}")
        return None

def parse_ai_response(response_text):
    """解析AI返回的结果"""
    try:
        # 简单的解析逻辑
        lines = response_text.split('\n')
        score_a = 50
        score_b = 50
        analysis = response_text
        
        # 尝试提取分数
        for line in lines:
            if '甲方得分' in line or '甲方：' in line:
                import re
                match = re.search(r'(\d+)', line)
                if match:
                    score_a = int(match.group(1))
            elif '乙方得分' in line or '乙方：' in line:
                import re
                match = re.search(r'(\d+)', line)
                if match:
                    score_b = int(match.group(1))
        
        return {
            'score_a': score_a,
            'score_b': score_b,
            'analysis': analysis
        }
    except:
        return {
            'score_a': 50,
            'score_b': 50,
            'analysis': response_text
        }

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
            if api_mode == "AI模式" and api_key:
                # 使用AI进行裁决
                ai_result = call_ai_api(party_a, party_b, api_key, api_url, model_name, custom_criteria)
                
                if ai_result:
                    score_a = ai_result['score_a']
                    score_b = ai_result['score_b']
                    ai_analysis = ai_result['analysis']
                else:
                    # API失败时降级到模拟模式
                    st.warning("⚠️ AI调用失败，使用模拟模式")
                    score_a = len(party_a) + random.randint(30, 50)
                    score_b = len(party_b) + random.randint(30, 50)
                    ai_analysis = None
            else:
                # 模拟模式
                time.sleep(2)  # 模拟处理时间
                score_a = len(party_a) + random.randint(30, 50)
                score_b = len(party_b) + random.randint(30, 50)
                ai_analysis = None
            
            # 计算百分比
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
        
        if ai_analysis:
            # 使用AI分析结果
            verdict = f"""
**【案情编号】**：HC-{int(time.time())}  
**【裁决日期】**：{time.strftime('%Y年%m月%d日')}  
**【主审法官】**：仓鼠大法官 🐹  
**【裁决模式】**：AI智能裁决

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**一、案情概述**

本案系一起情侣纠纷案件。甲乙双方存在分歧，特向本庭申请裁决。

**二、双方陈述**

【甲方陈述】  
{party_a}

【乙方陈述】  
{party_b}

**三、AI法官分析与裁决**

{ai_analysis}

**四、最终评分**

• 甲方得分：{score_a}分（占比{percent_a}%）  
• 乙方得分：{score_b}分（占比{percent_b}%）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

此致  
仓鼠法庭 🐹⚖️  
{time.strftime('%Y-%m-%d %H:%M:%S')}
            """
        else:
            # 使用模拟模式结果
            verdict = f"""
**【案情编号】**：HC-{int(time.time())}  
**【裁决日期】**：{time.strftime('%Y年%m月%d日')}  
**【主审法官】**：仓鼠大法官 🐹  
**【裁决模式】**：模拟裁决

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