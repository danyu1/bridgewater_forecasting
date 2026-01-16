import math

events = [
    {"name":"GPT-4","ym":(2023,3),"input":30.0,"output":60.0},
    {"name":"GPT-4-Turbo","ym":(2023,11),"input":10.0,"output":30.0},
    {"name":"GPT-4o","ym":(2024,5),"input":2.5,"output":10.0},
    {"name":"GPT-5","ym":(2025,8),"input":1.25,"output":10.0},
    {"name":"GPT-5.1","ym":(2025,11),"input":1.25,"output":10.0},
    {"name":"GPT-5.2","ym":(2025,12),"input":1.75,"output":14.0},
]

def ym_to_int(ym):
    return ym[0]*12 + ym[1]

first = ym_to_int(events[0]["ym"])
last_cut = ym_to_int(events[3]["ym"])
months_cut_window = last_cut - first
cut_count = 3
cut_hazard = cut_count / months_cut_window
class1_rate = 1 - math.exp(-cut_hazard * 2)

class2_rate = 0.05

all_changes = len(events) - 1
all_window = ym_to_int(events[-1]["ym"]) - ym_to_int(events[0]["ym"])
change_hazard = all_changes / all_window
change_2m = 1 - math.exp(-change_hazard * 2)
cut_fraction = 3 / all_changes
class3_rate = change_2m * cut_fraction

weights = [0.4, 0.3, 0.3]
base_rate = weights[0]*class1_rate + weights[1]*class2_rate + weights[2]*class3_rate

print("class1_rate", class1_rate)
print("class2_rate", class2_rate)
print("class3_rate", class3_rate)
print("weighted_base_rate", base_rate)
