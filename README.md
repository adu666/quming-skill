# 取名 - 智能取名助手

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://claude.ai/code)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)](https://python.org)

> 基于八字五行、诗词典故、音韵笔画等传统智慧的智能取名助手

## ✨ 功能特点

### 🍼 宝宝取名
- **生辰八字分析**：根据出生年月日时辰计算八字、五行
- **五行补缺**：智能推荐五行平衡的名字
- **诗词典故**：从《诗经》《楚辞》等经典中提取名字
- **五格剖象**：天格、人格、地格、外格、总格分析

### 🏢 公司/品牌起名
- 行业属性匹配
- 易记易传播
- 寓意吉祥
- 中英文适配建议

### 🎮 游戏ID/网名
- 酷炫、古风、二次元风格
- 英文适配
- 独特性评分

### ✍️ 笔名/艺名
- 文艺气质
- 独特记忆点
- 创作领域匹配

## 📦 安装方法

### 方式一：命令行安装

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/quming-skill.git

# 2. 复制到Claude Code skills目录
cp -r quming-skill ~/.claude/skills/取名

# 3. 完成！直接在Claude Code中使用
```

### 方式二：手动安装

1. 下载 [最新Release](https://github.com/yourusername/quming-skill/releases)
2. 解压到 `~/.claude/skills/取名/`
3. 在Claude Code中开始使用

## 🚀 使用方法

在Claude Code中直接输入：

```
帮我给宝宝取个名字
```

Claude会自动：
1. 询问姓氏、性别、出生时间
2. 分析八字五行
3. 智能推荐适合的名字
4. 提供详细解析（出处、寓意、五行、音韵、笔画）

### 示例对话

```
用户：帮我给宝宝取个名字
Claude：好的！请提供以下信息：
      1. 姓氏：杜
      2. 性别：男
      3. 出生时间：2026年9月15日 12时

Claude：[分析八字] 丙午年 戊戌月 壬辰日 丙午时
      [五行分析] 火土旺，缺金

      ━━━━━━━━━━━━━━━━━━━
      【推荐名字】
      
      1. 杜正阳（综合评分：86分）⭐
         五行：金+火（补金）
         寓意：正直阳光
         音韵：平仄平，朗朗上口
         笔画：总格11画（大吉）
         
      2. 杜瑞霖（综合评分：83分）
         五行：金+水（金水相生）
         寓意：祥瑞甘霖
         出处：祥瑞之意
         
      💡 输入"详细解释 杜正阳"查看完整分析
      💡 输入"换一批"查看更多候选
```

## 📊 评分维度

```
综合评分 = 
  五行匹配 × 30% +  （根据八字喜用神）
  寓意深度 × 20% +  （诗词出处、文化内涵）
  音韵和谐 × 20% +  （平仄搭配、朗朗上口）
  笔画吉凶 × 15% +  （五格剖象）
  独特性   × 10% +  （常见度评估）
  结构平衡 × 5%     （字形搭配）
```

## 📁 项目结构

```
取名/
├── SKILL.md                    # Skill主文档
├── README.md                   # 项目说明
├── LICENSE                     # MIT许可证
├── .gitignore                  # Git忽略文件
├── scripts/
│   ├── quming.py              # 主程序（八字分析、名字生成）
│   └── generate_for_du.py     # 示例脚本
└── data/
    ├── characters.json        # 汉字库（300+常用字）
    ├── poetry_names.json      # 诗词名字库（200+诗经名字）
    └── sensitive_words.json   # 敏感词/谐音检查
```

## 🛠️ 技术实现

- **八字计算**：天干地支、五行分析
- **名字生成**：诗词提取 + 智能组合
- **音韵分析**：平仄搭配、声调评分
- **笔画分析**：五格剖象（天/人/地/外/总格）
- **谐音检查**：敏感词库过滤

## 🔧 命令行工具

```bash
cd ~/.claude/skills/取名/scripts

# 查看数据状态
python quming.py status

# 交互式生成
python quming.py generate

# 测试生成
python quming.py test
```

## 📝 数据来源

- **汉字五行**：康熙字典 + 传统姓名学
- **诗词出处**：《诗经》《楚辞》《唐诗》《宋词》
- **五格算法**：日本熊崎健翁《姓名的神秘》

## ⚠️ 免责声明

1. 取名结果仅供参考，传统文化内容存在多种解读
2. 八字五行、五格剖象等属传统文化范畴，请理性看待
3. 最终取名决定权在用户，建议结合家族传统、个人喜好综合考虑

## 🤝 贡献指南

欢迎提交Issue和PR！

### 添加新的诗词名字

编辑 `data/poetry_names.json`，按以下格式添加：

```json
{
  "name": "子衿",
  "gender": "neutral",
  "source": "诗经·郑风",
  "quote": "青青子衿，悠悠我心",
  "meaning": "文雅有才情之人"
}
```

### 添加汉字

编辑 `data/characters.json`，补充汉字信息：

```json
{
  "新": {
    "pinyin": "xin",
    "tone": 1,
    "wuxing": "金",
    "meaning": "新颖、更新",
    "strokes": 13,
    "structure": "左右",
    "category": ["通用", "新颖"]
  }
}
```

## 🙏 致谢

- [Claude Code](https://claude.ai/code) 提供Skill框架
- 《康熙字典》提供汉字五行参考
- 《诗经》《楚辞》等古典文献

## 📄 许可证

[MIT](LICENSE) © 2026 取名项目组

---

**祝您的宝宝拥有一个美好而有意义的名字！** 🎉
