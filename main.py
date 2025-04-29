import json
import random

# 載入易經資料
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

hexagrams = {h['binary']: h for h in data['hexagrams']}


def toss_coins():
    # 擲三枚銅錢，0為反面（陰），1為正面（陽）
    coins = [random.choice([0, 1]) for _ in range(3)]
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
        print("\n● 動爻解釋：")
        for i, is_changing in enumerate(changing):
            if is_changing and i < len(hexagram['yao']):
                line = hexagram['yao'][i]
                print(f"{line['name']}：{line['text']}")
                print(f"解釋：{''.join(line['description']['text'])}")


def get_intermediate_hexagram(lines):
    lower = lines[1:4]
    upper = lines[2:5]
    binary = ''.join(str(i) for i in reversed(upper + lower))
    return hexagrams.get(binary)


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
        changed_binary = to_binary(changed_lines)
        changed_hex = get_hexagram_info(changed_binary)
    else:
        changed_lines = None
        changed_hex = None

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
