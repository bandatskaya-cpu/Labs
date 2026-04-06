# Вариант 3. Подсчёт точечных мутаций
# задайте две строки ДНК s и t равной длины
# не превышающей одной килобазы
# запишем их в отдельный файл и позаботимся о нём

import random
import os
import hashlib
import logging
import datetime

file = 'лабапервая.fasta'
file_path = 'd:/PPPPython/pythonn/лабапервая.fasta'
temp_file = file_path + ".tmp"
logging.basicConfig(filename='file_audit.log', level=logging.INFO)
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
directory = os.path.dirname(file_path)
last_known_hash = None

with open(file_path, 'rb') as f:
    current_hash = hashlib.sha256(f.read()).hexdigest()

if os.path.exists('file_audit.log'):
    with open('file_audit.log', 'r') as f:
        for line in f:
            if "Hash:" in line:
                last_known_hash = line.split("Hash: ")[1].strip()


if current_hash != last_known_hash:
    print("О УЖАС!!: Обнаружено ручное изменение файла!")
    logging.warning(f"[{datetime.datetime.now()}] ТРЕВОГА: Хеш не совпадает \
                    с логом!")
else:
    print("Файлу норм, вмешательств не обнаружено.")
    logging.info(f"[{datetime.datetime.now()}] Проверка пройдена: файл цел.")


population = ["A", "C", "T", "G"]
d = random.randint(1, 999)
s = ''.join(random.choices(k=d, population=population))
t = ''.join(random.choices(k=d, population=population))
# пример
# s = "GAGCCTACTAACGGGAT"
# t = "CATCGTAATGACGGCCT"
dn = 0
if len(s) != len(t) and len(s) < 1000:
    print("s и t должны быть равной длины")

for i in range(len(s)):
    if s[i] != t[i]:
        dn += 1

os.chmod(file_path, 0o600)
logging.info(f"[{current_time}] Снята защита с файла для дозаписи")

with open(file, 'w') as f:
    f.write(s + "\n")
    f.write(t + "\n")
    f.write(str(dn))

if os.path.exists(file):
    print(f"Файл {file} существует")
else:
    print(f"Файл {file} не найден")


with open(temp_file, 'w', encoding='utf-8') as f:
    f.write(f"S: {s}\nT: {t}\nMutations: {dn}\n")
    f.flush()
    os.fsync(f.fileno())

# f.fileno числовой идентификатор файла в системе .
# os.fsync команда оперативке забудь про все свои кеши и оптимизации,
# немедленно запиши эти байты на диск

with open(temp_file, 'rb') as f:
    file_hash = hashlib.sha256(f.read()).hexdigest()

if os.path.exists(file_path):
    os.remove(file_path)

os.rename(temp_file, file_path)

os.chmod(file_path, 0o400)
print(os.access(file_path, os.W_OK))
logging.info(f"[{current_time}] Файл {file_path} записан. Hash: {file_hash}")
