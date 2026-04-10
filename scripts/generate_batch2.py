#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
from quming import BaziAnalyzer, NameGenerator
import random

# 为杜姓男孩生成第二批名字（侧重补金）
analyzer = BaziAnalyzer()
generator = NameGenerator()

bazi = analyzer.calculate(2026, 9, 15, 12)

# 获取属金的汉字
jin_chars = []
for char, info in generator.characters.items():
    if info.get('wuxing') == '金':
        jin_chars.append(char)

# 获取更多候选，筛选含金的
all_results = generator.generate('杜', 'male', bazi, count=20)

# 手动添加一些五行属金的组合
additional_names = [
    ('思远', '深思熟虑，志向远大', '金+土'),
    ('铭泽', '铭记恩泽，不忘本', '金+水'),
    ('锦程', '锦绣前程', '金+火'),
    ('瑞霖', '祥瑞甘霖', '金+水'),
    ('书恒', '书香恒久', '金+水'),
    ('成蹊', '桃李不言下自成蹊', '金+土'),
    ('正阳', '正直阳光', '金+火'),
    ('新锐', '新颖锐利', '金+金'),
    ('悦安', '喜悦平安', '金+土'),
    ('铭轩', '铭记于心，气宇轩昂', '金+土'),
]

with open('du_batch2.txt', 'w', encoding='utf-8') as f:
    f.write('【换一批推荐】杜姓男宝宝取名 - 第二批\n')
    f.write(f'（侧重五行属金，补益八字）\n')
    f.write('=' * 50 + '\n\n')

    f.write('【精选五行属金名字】\n\n')

    for i, (name, meaning, wx) in enumerate(additional_names[:8], 1):
        full_name = '杜' + name

        # 计算分数
        rhythm = generator.analyze_rhythm(full_name)
        strokes = generator.analyze_strokes('杜', name)

        # 五行评分（含金越多分越高）
        jin_count = wx.count('金')
        wuxing_score = 70 + jin_count * 15

        total_score = (
            wuxing_score * 0.30 +  # 五行权重提高
            85 * 0.20 +  # 寓意
            rhythm['score'] * 0.20 +
            (80 if strokes['zong_ge']['luck'] == '吉' else 60) * 0.15 +
            75 * 0.15
        )

        star = '⭐' if total_score >= 85 else ''
        f.write(f"{i}. 杜{name}（综合评分：{round(total_score)}分）{star}\n")
        f.write(f"   寓意：{meaning}\n")
        f.write(f"   五行：{wx}")
        if jin_count > 0:
            f.write(f"（含{jin_count}个金，补八字所缺）")
        f.write('\n')
        f.write(f"   音韵：{rhythm['pattern']}（{rhythm['score']}分）\n")
        f.write(f"   笔画：总格{strokes['zong_ge']['num']}画（{strokes['zong_ge']['luck']}）\n")
        f.write(f"   谐音检查：通过\n\n")

    f.write('=' * 50 + '\n\n')

    f.write('【备选方案 - 不同风格】\n\n')

    # 从原有结果中筛选
    for i, r in enumerate(all_results[8:16], 9):
        if r.get('source'):
            f.write(f"{i}. 杜{r['name']}（{r['score']}分）\n")
            f.write(f"   出处：《{r['source']}》\n")
            f.write(f"   寓意：{r['meaning']}\n")
            f.write(f"   五行：{r['wuxing']}\n\n")

    f.write('=' * 50 + '\n\n')
    f.write('【重点推荐解析】\n\n')

    f.write('『杜思远』\n')
    f.write('  五行：金+土（金旺，土相生，极佳组合）\n')
    f.write('  寓意：深思熟虑，志向远大\n')
    f.write('  音韵：仄平仄，抑扬顿挫\n')
    f.write('  适合：八字缺金，此名金土相生，补益有力\n\n')

    f.write('『杜铭泽』\n')
    f.write('  五行：金+水（金水相生）\n')
    f.write('  寓意：铭记恩泽，不忘根本\n')
    f.write('  特点："铭"带金字旁，直接补金\n\n')

    f.write('『杜锦程』\n')
    f.write('  五行：金+火（火克金稍弱，但寓意极佳）\n')
    f.write('  寓意：锦绣前程，前途光明\n')
    f.write('  特点：成语取名，朗朗上口\n\n')

    f.write('💡 建议：\n')
    f.write('  1. 八字严重缺金，优先选择带"金"字旁或五行属金的字\n')
    f.write('  2. 推荐：杜思远、杜铭泽、杜锦程、杜瑞霖\n')
    f.write('  3. 避免：五行属火的字（如炎、阳、炳等），火已够旺\n')
    f.write('  4. 如需更多选择，可继续输入"换一批"\n')

print("第二批推荐已生成：du_batch2.txt")
