#!/bin/bash

# 仓鼠法官快速部署脚本

echo "🐹⚖️ 仓鼠法官部署助手"
echo "================================"
echo ""

# 检查是否安装了git
if ! command -v git &> /dev/null; then
    echo "❌ 错误：未安装 Git"
    echo "请先安装 Git: https://git-scm.com/downloads"
    exit 1
fi

echo "📝 请输入你的GitHub用户名："
read github_username

echo "📝 请输入仓库名称（默认: hamster-judge）："
read repo_name
repo_name=${repo_name:-hamster-judge}

echo ""
echo "⏳ 正在初始化 Git 仓库..."
git init

echo "⏳ 添加文件..."
git add .

echo "⏳ 创建提交..."
git commit -m "Initial commit: 仓鼠法官裁决系统"

echo ""
echo "📌 接下来请完成以下步骤："
echo ""
echo "1️⃣ 在浏览器中打开: https://github.com/new"
echo "2️⃣ 仓库名称输入: $repo_name"
echo "3️⃣ 设置为 Public（公开）"
echo "4️⃣ 不要勾选任何初始化选项"
echo "5️⃣ 点击 'Create repository'"
echo ""
echo "完成后按回车继续..."
read -r

echo ""
echo "⏳ 关联远程仓库..."
git remote add origin "https://github.com/$github_username/$repo_name.git"

echo "⏳ 推送代码到 GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 代码已成功推送到 GitHub!"
    echo ""
    echo "🚀 下一步：部署到 Streamlit Cloud"
    echo "================================"
    echo "1️⃣ 访问: https://share.streamlit.io/"
    echo "2️⃣ 点击 'New app'"
    echo "3️⃣ 选择仓库: $github_username/$repo_name"
    echo "4️⃣ Branch: main"
    echo "5️⃣ Main file: hamster_judge.py"
    echo "6️⃣ 点击 'Deploy!'"
    echo ""
    echo "⏱️  等待几分钟，你的应用就会上线！"
    echo ""
    echo "📱 部署完成后，你会得到一个网址，可以分享给任何人访问！"
else
    echo ""
    echo "❌ 推送失败，请检查："
    echo "1. GitHub用户名是否正确"
    echo "2. 是否已在GitHub创建仓库"
    echo "3. 是否有推送权限"
    echo ""
    echo "如需帮助，请查看 '部署指南.md'"
fi

echo ""
echo "💡 提示: 详细说明请查看 '部署指南.md' 文件"

