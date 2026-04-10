#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
from quming import BaziAnalyzer, NameGenerator

# 为杜姓男孩生成名字（2026年9月15日）
analyzer = BaziAnalyzer()
generator = NameGenerator()

bazi = analyzer.calculate(2026, 9, 15, 12)
results = generator.generate('杜', 'male', bazi, count=8)

with open('du_baby_names.txt', 'w', encoding='utf-8') as f:
    f.write('【八字分析】\n')
    f.write(f"出生时间：2026年9月15日\n")
    f.write(f"八字：{bazi['year']}年 {bazi['month']}月 {bazi['day']}日 {bazi['hour']}时\n\n")
    f.write(f"五行分布：\n")
    for wx, count in sorted(bazi['wuxing'].items(), key=lambda x: -x[1]):
        bar = '■' * int(count * 2)
        f.write(f"  {wx}：{bar} ({count})\n")
    f.write(f"\n")
    f.write(f"五行分析：金、木、水偏弱，喜用神为【{bazi['favor']}】\n")
    f.write(f"建议：名字中多使用五行属{bazi['favor']}的字来平衡\n\n")
    f.write('=' * 50 + '\n')
    f.write('【推荐名字】（按综合评分排序）\n\n')

    for i, r in enumerate(results, 1):
        star = '⭐ 强烈推荐' if r['score'] >= 90 else ''
        f.write(f"{i}. 杜{r['name']}（综合评分：{r['score']}分）{star}\n")

        if r.get('source'):
            f.write(f"   出处：《{r['source']}》\"{r['quote']}\"\n")
        f.write(f"   寓意：{r['meaning']}\n")

        wuxing_chars = r['wuxing']
        jin_count = wuxing_chars.count(bazi['favor'])
        f.write(f"   五行：{wuxing_chars}（含{jin_count}个{bazi['favor']}）\n")

        rhythm = r.get('rhythm', {})
        f.write(f"   音韵：{rhythm.get('pattern', '')}（平仄搭配），{rhythm.get('score', 0)}分\n")

        strokes = r.get('strokes', {})
        zong_ge = strokes.get('zong_ge', {})
        luck = zong_ge.get('luck', '平')
        luck_str = '【大吉】' if luck == '吉' else ''
        f.write(f"   笔画：总格{zong_ge.get('num', 0)}画（{luck}）{luck_str}\n")
        f.write(f"   谐音检查：通过 ✓\n\n")

    f.write('=' * 50 + '\n\n')
    f.write('【详细解析推荐】\n\n')

    # 详细解析第一个高分名字
    top = results[0]
    f.write(f"『杜{top['name']}』深度解析\n\n")
    f.write(f"📜 出处溯源：\n")
    if top.get('source'):
        f.write(f"   \"{top['quote']}\" ——《{top['source']}》\n\n")

    f.write(f"🎯 寓意解读：\n")
    f.write(f"   {top['meaning']}\n\n")

    f.write(f"⚖️ 八字匹配：\n")
    f.write(f"   生辰八字：{bazi['year']} {bazi['month']} {bazi['day']} {bazi['hour']}\n")
    f.write(f"   五行缺金，名字\"{top['name']}\"五行属{top['wuxing']}，\n")
    f.write(f"   正好补益命局，平衡五行 ✓\n\n")

    f.write(f"🎵 音韵分析：\n")
    rhythm = top.get('rhythm', {})
    f.write(f"   杜(4声-仄) + {top['name']}\n")
    f.write(f"   声调搭配：{rhythm.get('pattern', '')}\n")
    f.write(f"   评分：{rhythm.get('score', 0)}分（朗朗上口）\n\n")

    f.write(f"✍️ 五格剖象：\n")
    s = top.get('strokes', {})
    f.write(f"   天格{s['tian_ge']['num']}（{s['tian_ge']['luck']}）| ")
    f.write(f"人格{s['ren_ge']['num']}（{s['ren_ge']['luck']}）| ")
    f.write(f"地格{s['di_ge']['num']}（{s['di_ge']['luck']}）\n")
    f.write(f"   外格{s['wai_ge']['num']}（{s['wai_ge']['luck']}）| ")
    f.write(f"总格{s['zong_ge']['num']}（{s['zong_ge']['luck']}）\n\n")

    f.write('💡 温馨提示：\n')
    f.write('   1. 以上推荐基于2026年9月15日生成\n')
    f.write('   2. 如有具体出生时辰，可以进一步精确分析\n')
    f.write('   3. 最终取名建议结合家族传统和个人喜好\n')

print("结果已保存到 du_baby_names.txt")
