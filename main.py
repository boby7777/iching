import json
import random

# 載入易經資料
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

hexagrams = {h['binary']: h for h in data['hexagrams']}
trigrams = {t['binary']: t for t in data['trigrams']}

# 建立 binary 對應正式卦名對照表
hexagram_name_map = {h['binary']: h['name'] for h in data['hexagrams']}

def toss_coins():
    coins = [random.choice([0, 1]) for _ in range(3)]
    print(coins)
    total = sum(coins)
    if total == 3:
        return 1, True   # 老陽：陽動
    elif total == 2:
        return 0, False  # 少陰：陰靜
    elif total == 1:
        return 1, False  # 少陽：陽靜
    else:
        return 0, True   # 老陰：陰動

def manual_divination():
    lines = []
    changing = []
    print("開始擲筊，每一爻從下到上擲三枚硬幣...")
    for i in range(6):
        input(f"\n請按 Enter 擲第 {i+1} 爻...")
        line, is_changing = toss_coins()
        lines.append(line)
        changing.append(is_changing)
        print(f"結果：{'陽' if line else '陰'} {'（動爻）' if is_changing else ''}")
    return lines, changing

def to_binary(lines):
    return ''.join(str(i) for i in reversed(lines))

def change_hexagram(lines, changing):
    return [(1 - bit if changing[i] else bit) for i, bit in enumerate(lines)]

def get_hexagram_info(binary):
    return hexagrams.get(binary)

def display_hexagram(title, hexagram, lines, changing=None):
    print(f"\n==== {title} ====")
    print(f"卦象：{hexagram['name']} {hexagram['character']} ({''.join(str(i) for i in reversed(lines))})")
    print(f"卦辭：{hexagram['text']}")
    if hexagram.get('description') and hexagram['description'].get('text'):
        print(f"解釋：{''.join(hexagram['description']['text'])}")

    if changing:
        reversed_changing = list(reversed(changing))
        reversed_lines = list(reversed(lines))
        print("\n● 動爻解釋：")
        for i, is_changing in enumerate(reversed_changing):
            if is_changing and i < len(hexagram['yao']):
                line = hexagram['yao'][i]
                yao_type = "陽" if reversed_lines[i] == 1 else "陰"
                motion = "動" if is_changing else "靜"
                print(f"{line['name']}（{yao_type}{motion}）：{line['text']}")
                if 'description' in line:
                    print(f"解釋：{''.join(line['description']['text'])}")

def get_intermediate_hexagram(lines):
    lower = lines[1:4]
    upper = lines[2:5]
    binary = ''.join(str(i) for i in reversed(upper + lower))
    return hexagrams.get(binary), upper + lower

def print_trigram_info(title, lines):
    bottom = lines[:3]
    top = lines[3:]
    bottom_key = ''.join(str(i) for i in bottom)
    top_key = ''.join(str(i) for i in top)

    bottom_trigram = next((t for t in trigrams.values() if t['binary'] == bottom_key), None)
    top_trigram = next((t for t in trigrams.values() if t['binary'] == top_key), None)

    def trigram_desc(tri):
        if tri:
            return f"{tri['name']} ({tri['character']})｜五行：{tri['element']}｜方位：{tri['position']}｜性質：{tri['nature']}"
        return "未知"

    print(f"\n=== {title} 卦的上下卦資訊 ===")
    print(f"上卦：{trigram_desc(top_trigram)}")
    print(f"下卦：{trigram_desc(bottom_trigram)}")

def print_full_hexagram_name(title, lines):
    binary = to_binary(lines)
    full_name = hexagram_name_map.get(binary, "未知卦")
    print(f"{title}卦：{full_name}")

def main():
    print("請選擇占卜方式：")
    options = ["1. 隨機起卦", "2. 擲筊起卦（自己手動）"]
    for option in options:
        print(option)
    method = int(input("輸入選項號碼："))

    print("\n請選擇占卜類別：")
    questions = ["事業", "感情", "健康", "財運", "家庭"]
    for idx, q in enumerate(questions, 1):
        print(f"{idx}. {q}")
    choice = int(input("輸入編號："))
    print(f"你選擇的是：「{questions[choice - 1]}」\n")

    if method == 1:
        lines = [random.choice([0, 1]) for _ in range(6)]
        changing = [random.choice([True, False]) for _ in range(6)]
    else:
        lines, changing = manual_divination()

    main_binary = to_binary(lines)
    main_hex = get_hexagram_info(main_binary)

    if any(changing):
        changed_lines = change_hexagram(lines, changing)
        changed_hex = get_hexagram_info(to_binary(changed_lines))
    else:
        changed_lines = None
        changed_hex = None

    inter_hex, inter_lines = get_intermediate_hexagram(lines)

    # 顯示主卦
    display_hexagram("主卦", main_hex, lines, changing)
    print_trigram_info("主卦", lines)
    print_full_hexagram_name("主", lines)

    # 顯示互卦
    if inter_hex:
        display_hexagram("互卦", inter_hex, inter_lines)
        print_trigram_info("互卦", inter_lines)
        print_full_hexagram_name("互", inter_lines)

    # 顯示變卦
    if changed_lines:
        display_hexagram("變卦", changed_hex, changed_lines)
        print_trigram_info("變卦", changed_lines)
        print_full_hexagram_name("變", changed_lines)

if __name__ == "__main__":
    main()
