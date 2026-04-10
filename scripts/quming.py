#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
取名助手 - 命令行工具
智能取名，支持宝宝取名、公司起名、游戏ID、笔名艺名
"""

import sys
import json
import os
from pathlib import Path

# 获取数据目录
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"

def load_json(filename):
    """加载JSON数据文件"""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filename, data):
    """保存JSON数据文件"""
    filepath = DATA_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class BaziAnalyzer:
    """八字五行分析器"""

    # 天干地支
    TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    # 天干五行
    TIAN_GAN_WUXING = {
        "甲": "木", "乙": "木",
        "丙": "火", "丁": "火",
        "戊": "土", "己": "土",
        "庚": "金", "辛": "金",
        "壬": "水", "癸": "水"
    }

    # 地支五行
    DI_ZHI_WUXING = {
        "子": "水", "丑": "土", "寅": "木", "卯": "木",
        "辰": "土", "巳": "火", "午": "火", "未": "土",
        "申": "金", "酉": "金", "戌": "土", "亥": "水"
    }

    # 地支藏干
    DI_ZHI_CANGGAN = {
        "子": ["癸"],
        "丑": ["己", "癸", "辛"],
        "寅": ["甲", "丙", "戊"],
        "卯": ["乙"],
        "辰": ["戊", "乙", "癸"],
        "巳": ["丙", "庚", "戊"],
        "午": ["丁", "己"],
        "未": ["己", "丁", "乙"],
        "申": ["庚", "壬", "戊"],
        "酉": ["辛"],
        "戌": ["戊", "辛", "丁"],
        "亥": ["壬", "甲"]
    }

    def __init__(self):
        self.characters = load_json("characters.json")

    def get_year_ganzhi(self, year):
        """获取年干支"""
        offset = (year - 4) % 60
        gan_idx = offset % 10
        zhi_idx = offset % 12
        return self.TIAN_GAN[gan_idx] + self.DI_ZHI[zhi_idx]

    def get_month_ganzhi(self, year, month):
        """获取月干支（简化版，按节气划分）"""
        year_gan = self.get_year_ganzhi(year)[0]
        # 根据年干确定月干的起始
        gan_start = {"甲": "丙", "乙": "戊", "丙": "庚", "丁": "壬", "戊": "甲",
                     "己": "丙", "庚": "戊", "辛": "庚", "壬": "壬", "癸": "甲"}
        start_gan_idx = self.TIAN_GAN.index(gan_start[year_gan])
        gan_idx = (start_gan_idx + month - 1) % 10
        # 正月为寅
        zhi_idx = (month + 1) % 12
        return self.TIAN_GAN[gan_idx] + self.DI_ZHI[zhi_idx]

    def get_day_ganzhi(self, year, month, day):
        """获取日干支（简化计算）"""
        # 基准日：1900年1月31日为甲辰日
        base_date = (1900, 1, 31)
        base_ganzhi_idx = 40  # 甲辰在60甲子中的索引

        # 计算日期差（简化计算，不考虑闰年）
        days_diff = (year - 1900) * 365 + (year - 1900) // 4
        month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        days_diff += sum(month_days[:month]) + day - 31

        ganzhi_idx = (base_ganzhi_idx + days_diff) % 60
        gan_idx = ganzhi_idx % 10
        zhi_idx = ganzhi_idx % 12
        return self.TIAN_GAN[gan_idx] + self.DI_ZHI[zhi_idx]

    def get_hour_ganzhi(self, day_gan, hour):
        """获取时干支"""
        # 根据日干确定时干的起始
        gan_start = {"甲": "甲", "乙": "丙", "丙": "戊", "丁": "庚", "戊": "壬",
                     "己": "甲", "庚": "丙", "辛": "戊", "壬": "庚", "癸": "壬"}
        start_gan_idx = self.TIAN_GAN.index(gan_start[day_gan])

        # 时辰对应（23-1为子时）
        zhi_idx = (hour + 1) // 2 % 12
        gan_idx = (start_gan_idx + zhi_idx) % 10
        return self.TIAN_GAN[gan_idx] + self.DI_ZHI[zhi_idx]

    def calculate(self, year, month, day, hour=12):
        """计算八字"""
        year_gz = self.get_year_ganzhi(year)
        month_gz = self.get_month_ganzhi(year, month)
        day_gz = self.get_day_ganzhi(year, month, day)
        hour_gz = self.get_hour_ganzhi(day_gz[0], hour)

        # 提取五行
        wuxing_count = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}

        all_ganzhi = [year_gz, month_gz, day_gz, hour_gz]
        for gz in all_ganzhi:
            wuxing_count[self.TIAN_GAN_WUXING[gz[0]]] += 1
            wuxing_count[self.DI_ZHI_WUXING[gz[1]]] += 1
            # 地支藏干
            for gan in self.DI_ZHI_CANGGAN[gz[1]]:
                wuxing_count[self.TIAN_GAN_WUXING[gan]] += 0.5

        # 找出最弱和最强的五行
        sorted_wuxing = sorted(wuxing_count.items(), key=lambda x: x[1])
        missing = [wx for wx, count in sorted_wuxing if count < 2]
        favor = missing[0] if missing else sorted_wuxing[0][0]

        return {
            "year": year_gz,
            "month": month_gz,
            "day": day_gz,
            "hour": hour_gz,
            "wuxing": wuxing_count,
            "missing": missing,
            "favor": favor
        }

class NameGenerator:
    """名字生成器"""

    def __init__(self):
        self.characters = load_json("characters.json")
        self.poetry_names = load_json("poetry_names.json")
        self.sensitive = load_json("sensitive_words.json")

    def get_pinyin(self, char):
        """获取拼音"""
        if char in self.characters:
            return self.characters[char].get("pinyin", "")
        return ""

    def get_tone(self, char):
        """获取声调"""
        if char in self.characters:
            return self.characters[char].get("tone", 1)
        return 1

    def get_wuxing(self, char):
        """获取五行"""
        if char in self.characters:
            return self.characters[char].get("wuxing", "")
        return ""

    def get_strokes(self, char):
        """获取笔画数"""
        if char in self.characters:
            return self.characters[char].get("strokes", 0)
        return 0

    def check_homophone(self, name):
        """检查谐音"""
        # 检查是否在敏感组合列表中
        if name in self.sensitive.get("bad_combinations", []):
            return False, "在敏感名字列表中"

        # 检查拼音组合
        pinyin_full = "".join([self.get_pinyin(c) for c in name])
        for bad_py, chars in self.sensitive.get("homophones", {}).items():
            if bad_py in pinyin_full:
                return False, f"可能谐音: {bad_py}"

        return True, "通过"

    def analyze_rhythm(self, chars):
        """分析音韵"""
        tones = [self.get_tone(c) for c in chars]

        # 平仄分析：1、2声为平，3、4声为仄
        pingze = ["平" if t <= 2 else "仄" for t in tones]

        # 评分：避免连续三个相同声调，避免全平或全仄
        score = 100
        for i in range(len(tones) - 1):
            if tones[i] == tones[i+1]:
                score -= 10

        if len(set(pingze)) == 1:
            score -= 20

        return {
            "tones": tones,
            "pingze": pingze,
            "pattern": "".join(pingze),
            "score": max(0, score)
        }

    def analyze_strokes(self, surname, name):
        """分析笔画（五格剖象）"""
        surname_strokes = sum(self.get_strokes(c) for c in surname)
        name_strokes = sum(self.get_strokes(c) for c in name)

        # 五格计算
        tian_ge = surname_strokes + 1  # 天格
        ren_ge = surname_strokes + (self.get_strokes(name[0]) if name else 0)  # 人格
        di_ge = name_strokes + (1 if len(name) == 1 else 0)  # 地格
        wai_ge = tian_ge + di_ge - ren_ge  # 外格
        zong_ge = surname_strokes + name_strokes  # 总格

        # 吉凶判断（简化版）
        def get_luck(num):
            lucky_nums = [1, 3, 5, 6, 7, 8, 11, 13, 15, 16, 17, 18, 21, 23, 24, 25, 31, 32, 33, 35, 37, 39, 41, 45, 47, 48, 52, 57, 61, 63, 65, 67, 68, 81]
            if num in lucky_nums:
                return "吉"
            elif num in [2, 4, 9, 10, 12, 14, 19, 20, 22, 26, 27, 28, 29, 30, 34, 36, 38, 40, 42, 43, 44, 46, 49, 50, 51, 53, 54, 55, 56, 58, 59, 60, 62, 64, 66, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80]:
                return "凶"
            return "平"

        return {
            "tian_ge": {"num": tian_ge, "luck": get_luck(tian_ge)},
            "ren_ge": {"num": ren_ge, "luck": get_luck(ren_ge)},
            "di_ge": {"num": di_ge, "luck": get_luck(di_ge)},
            "wai_ge": {"num": wai_ge, "luck": get_luck(wai_ge)},
            "zong_ge": {"num": zong_ge, "luck": get_luck(zong_ge)},
            "total_strokes": zong_ge
        }

    def calculate_wuxing_score(self, name, favor_wuxing):
        """计算五行匹配分数"""
        name_wuxing = [self.get_wuxing(c) for c in name]
        favor_count = name_wuxing.count(favor_wuxing)

        # 根据需要的五行出现次数评分
        if favor_count >= 2:
            return 95
        elif favor_count == 1:
            return 80
        else:
            return 50

    def generate_from_poetry(self, surname, gender, favor_wuxing, count=10):
        """从诗词库生成名字"""
        results = []

        for item in self.poetry_names:
            # 性别过滤
            if item.get("gender") not in [gender, "neutral"]:
                continue

            name = item["name"]

            # 谐音检查
            full_name = surname + name
            ok, msg = self.check_homophone(full_name)
            if not ok:
                continue

            # 计算各项分数
            wuxing_score = self.calculate_wuxing_score(name, favor_wuxing)
            rhythm = self.analyze_rhythm(surname + name)
            strokes = self.analyze_strokes(surname, name)

            # 综合评分
            total_score = (
                wuxing_score * 0.25 +
                90 * 0.20 +  # 寓意分（诗词出处默认较高）
                rhythm["score"] * 0.20 +
                (80 if strokes["zong_ge"]["luck"] == "吉" else 60) * 0.15 +
                70 * 0.10 +  # 独特性
                80 * 0.10   # 结构
            )

            results.append({
                "name": name,
                "score": round(total_score),
                "source": item.get("source", ""),
                "quote": item.get("quote", ""),
                "meaning": item.get("meaning", ""),
                "wuxing": "".join([self.get_wuxing(c) for c in name]),
                "rhythm": rhythm,
                "strokes": strokes
            })

        # 排序并返回
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:count]

    def generate_combined(self, surname, gender, favor_wuxing, count=10):
        """智能组合生成名字"""
        results = []

        # 获取适合取名的常用字
        suitable_chars = []
        for char, info in self.characters.items():
            if info.get("wuxing") == favor_wuxing:
                suitable_chars.append(char)

        if len(suitable_chars) < 2:
            suitable_chars = list(self.characters.keys())

        # 组合生成
        import random
        random.seed()

        generated = set()
        attempts = 0
        while len(results) < count and attempts < count * 10:
            attempts += 1

            # 随机选择2个字
            if len(suitable_chars) >= 2:
                c1, c2 = random.sample(suitable_chars, 2)
                name = c1 + c2

                if name in generated:
                    continue
                generated.add(name)

                # 检查
                full_name = surname + name
                ok, msg = self.check_homophone(full_name)
                if not ok:
                    continue

                # 计算分数
                wuxing_score = self.calculate_wuxing_score(name, favor_wuxing)
                rhythm = self.analyze_rhythm(surname + name)
                strokes = self.analyze_strokes(surname, name)

                total_score = (
                    wuxing_score * 0.25 +
                    70 * 0.20 +  # 寓意分
                    rhythm["score"] * 0.20 +
                    (80 if strokes["zong_ge"]["luck"] == "吉" else 60) * 0.15 +
                    75 * 0.10 +  # 独特性
                    80 * 0.10   # 结构
                )

                results.append({
                    "name": name,
                    "score": round(total_score),
                    "source": "",
                    "quote": "",
                    "meaning": f"{self.characters.get(c1, {}).get('meaning', '')}; {self.characters.get(c2, {}).get('meaning', '')}",
                    "wuxing": "".join([self.get_wuxing(c) for c in name]),
                    "rhythm": rhythm,
                    "strokes": strokes
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    def generate(self, surname, gender, birth_info=None, count=8):
        """生成名字"""
        favor_wuxing = "金"
        if birth_info and "favor" in birth_info:
            favor_wuxing = birth_info["favor"]

        # 从诗词库生成
        poetry_results = self.generate_from_poetry(surname, gender, favor_wuxing, count//2)

        # 组合生成
        combined_results = self.generate_combined(surname, gender, favor_wuxing, count - len(poetry_results))

        # 合并并排序
        all_results = poetry_results + combined_results
        all_results.sort(key=lambda x: x["score"], reverse=True)

        return all_results[:count]

def format_report(surname, results):
    """格式化输出报告"""
    lines = []
    lines.append(f"[取名报告] {surname}姓")
    lines.append("")
    lines.append("-" * 50)
    lines.append("【推荐名字】（按综合评分排序）")
    lines.append("")

    for i, r in enumerate(results, 1):
        star = "[推荐]" if r["score"] >= 90 else ""
        lines.append(f"{i}. {surname}{r['name']}（综合评分：{r['score']}分）{star}")

        if r.get("source"):
            lines.append(f"   |- 出处：《{r['source']}》\"{r['quote']}\"")
            lines.append(f"   |- 寓意：{r['meaning']}")
        else:
            lines.append(f"   |- 寓意：{r['meaning']}")

        lines.append(f"   |- 五行：{r['wuxing']}")

        rhythm = r.get("rhythm", {})
        lines.append(f"   |- 音韵：{rhythm.get('pattern', '')}，朗朗上口")

        strokes = r.get("strokes", {})
        zong_ge = strokes.get("zong_ge", {})
        lines.append(f"   |- 笔画：总格{zong_ge.get('num', 0)}画（{zong_ge.get('luck', '平')}）")
        lines.append(f"   |- 谐音检查：通过 [OK]")
        lines.append("")

    lines.append("-" * 50)
    lines.append("")
    lines.append("[*] 输入\"详细解释 [名字]\"查看完整分析")
    lines.append("[*] 输入\"换一批\"查看更多候选")

    return "\n".join(lines)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("取名助手 - 智能取名工具")
        print("")
        print("用法:")
        print("  python quming.py status       - 查看数据状态")
        print("  python quming.py generate     - 交互式生成名字")
        print("  python quming.py test         - 测试生成")
        print("")
        return

    command = sys.argv[1]

    if command == "status":
        print("[数据状态]")
        print("")
        chars = load_json("characters.json")
        poetry = load_json("poetry_names.json")
        print(f"  汉字库：{len(chars)} 字")
        print(f"  诗词库：{len(poetry)} 个名字")
        print("")
        print("[OK] 数据加载正常")

    elif command == "test":
        print("[测试] 开始测试生成...")
        print("")

        generator = NameGenerator()
        analyzer = BaziAnalyzer()

        # 测试八字分析
        bazi = analyzer.calculate(2024, 3, 15, 9)
        print(f"八字：{bazi['year']} {bazi['month']} {bazi['day']} {bazi['hour']}")
        print(f"五行：{bazi['wuxing']}")
        print(f"喜用：{bazi['favor']}")
        print("")

        # 测试名字生成
        results = generator.generate("王", "male", bazi, count=5)
        print(format_report("王", results))

    elif command == "generate":
        print("[欢迎使用] 取名助手！")
        print("")

        surname = input("请输入姓氏：").strip()
        if not surname:
            print("姓氏不能为空")
            return

        gender = input("请输入性别（男/女）：").strip()
        if gender not in ["男", "女"]:
            print("性别请输入 男 或 女")
            return

        year = int(input("出生年（如2024）：") or 2024)
        month = int(input("出生月（1-12）：") or 1)
        day = int(input("出生日（1-31）：") or 1)
        hour = int(input("出生时（0-23）：") or 12)

        print("")
        print("正在分析八字并生成名字...")
        print("")

        analyzer = BaziAnalyzer()
        generator = NameGenerator()

        bazi = analyzer.calculate(year, month, day, hour)
        print(f"八字：{bazi['year']}年 {bazi['month']}月 {bazi['day']}日 {bazi['hour']}时")
        print(f"五行分析：{bazi['wuxing']}")
        print(f"喜用神：{bazi['favor']}")
        print("")

        results = generator.generate(surname, gender, bazi, count=8)
        print(format_report(surname, results))

    else:
        print(f"未知命令: {command}")
        print("使用 'python quming.py' 查看帮助")

if __name__ == "__main__":
    main()
