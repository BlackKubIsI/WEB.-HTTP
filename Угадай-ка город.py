import os
CITIES = ["Ломе", "Манго", "Благовещенск", "Бобров", "Новый Оскол",
 "Томск", "Фатеж", "Шахты", "Юрьев-Польский"]

for i in CITIES:
    os.system(f"python3 g.py {i}")
    otw = input()
    if otw == i:
        print(True)
    else:
        print(False)