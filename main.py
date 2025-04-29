import json
import random

# 載入易經資料
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

hexagrams = {h['binary']: h for h in data['hexagrams']}
trigrams = {t['binary']: t for t in data['trigrams']}


def generate_lines():
    # 模擬六個爻，每個爻為 0 陰爻、1 陽爻；加上動爻機制（50% 機率動爻）
    lines = []
    changing = []
    for _ in range(6):
        base = random.choice([0, 1])
        is_changing = random.choice([True, False])
        lines.append(base)
        changing.append(is_changing)
    return lines, changing


def to_binary(lines):
    return ''.join(str(i) for i in reversed(lines))  # 由下往上


def change_hexagram(lines, changing):
    return [(1 - bit if changing[i] else bit) for i, bit in enumerate(lines)]


def get_trigram_key(lines):
    return ''.join(str(i) for i in lines)


def get_hexagram_info(binary):
    return hexagrams.get(binary)


def display_hexagram(title, hexagram, lines, changing=None):
    print(f"\n==== {title} ====")
    print(f"卦象：{hexagram['name']} {hexagram['character']} ({''.join(str(i) for i in reversed(lines))})")
    print(f"卦辭：{hexagram['text']}")
    print(f"解釋：{''.join(hexagram['description']['text'])}")

    if changing:
        print("\n● 動爻解釋：")
        for i, is_changing in enumerate(changing):
            if is_changing and i < len(hexagram['yao']):
                line = hexagram['yao'][i]
                print(f"{line['name']}：{line['text']}")
                print(f"解釋：{''.join(line['description']['text'])}")


def get_intermediate_hexagram(lines):
    # 互卦：第2~4爻為下卦，第3~5爻為上卦
    lower = lines[1:4]
    upper = lines[2:5]
    binary = ''.join(str(i) for i in reversed(upper + lower))
    return hexagrams.get(binary)


def main():
    print("請選擇占卜類別：")
    questions = ["事業", "感情", "健康", "財運", "家庭"]
    for idx, q in enumerate(questions, 1):
        print(f"{idx}. {q}")
    choice = int(input("輸入編號："))
    print(f"你選擇的是：「{questions[choice - 1]}」\n")

    lines, changing = generate_lines()
    main_binary = to_binary(lines)
    main_hex = get_hexagram_info(main_binary)

    # 變卦
    if any(changing):
        changed_lines = change_hexagram(lines, changing)
        changed_binary = to_binary(changed_lines)
        changed_hex = get_hexagram_info(changed_binary)
    else:
        changed_lines = None
        changed_hex = None

    # 互卦
    inter_hex = get_intermediate_hexagram(lines)

    # 顯示主卦
    display_hexagram("主卦", main_hex, lines, changing)

    # 顯示互卦
    if inter_hex:
        display_hexagram("互卦", inter_hex, lines[2:5] + lines[1:4])

    # 顯示變卦
    if changed_lines:
        display_hexagram("變卦", changed_hex, changed_lines)

if __name__ == "__main__":
    main()
