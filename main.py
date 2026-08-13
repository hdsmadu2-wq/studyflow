import json, random, time
from pathlib import Path

BASE = Path(__file__).parent
QUESTIONS_FILE = BASE / "questions.json"
SCORES_FILE = BASE / "scores.json"

def load_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default
    except (OSError, json.JSONDecodeError):
        return default

def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

DEFAULT_QUESTIONS = [
    {"question":"Berapakah hasil dari 12 × 8?","options":["86","96","108","112"],"answer":1},
    {"question":"Jika 3x + 5 = 20, maka x = ...","options":["3","5","7","8"],"answer":1},
    {"question":"Luas persegi dengan sisi 9 cm adalah ...","options":["18 cm²","36 cm²","72 cm²","81 cm²"],"answer":3},
    {"question":"Nilai dari 2⁵ adalah ...","options":["10","16","25","32"],"answer":3},
    {"question":"Rata-rata 6, 8, 10, dan 12 adalah ...","options":["8","9","10","11"],"answer":1},
    {"question":"Hasil dari 144 ÷ 12 adalah ...","options":["10","11","12","14"],"answer":2},
    {"question":"Luas segitiga alas 10 cm dan tinggi 6 cm adalah ...","options":["20 cm²","30 cm²","40 cm²","60 cm²"],"answer":1},
    {"question":"Hasil dari 15 + 7 × 2 adalah ...","options":["44","29","30","34"],"answer":1},
    {"question":"FPB dari 24 dan 36 adalah ...","options":["6","8","12","18"],"answer":2},
    {"question":"25% dari 200 adalah ...","options":["25","40","50","75"],"answer":2}
]

if not QUESTIONS_FILE.exists():
    save_json(QUESTIONS_FILE, DEFAULT_QUESTIONS)
if not SCORES_FILE.exists():
    save_json(SCORES_FILE, [])

def clear():
    print("\033[2J\033[H", end="")

def pause():
    input("\nTekan ENTER untuk melanjutkan...")

def quiz():
    questions = load_json(QUESTIONS_FILE, DEFAULT_QUESTIONS)
    name = input("Nama pemain: ").strip() or "Pemain"

    try:
        jumlah = int(input(f"Jumlah soal (1-{len(questions)}): "))
        jumlah = max(1, min(jumlah, len(questions)))
    except ValueError:
        jumlah = min(5, len(questions))

    selected = random.sample(questions, jumlah)
    score = 0
    start = time.perf_counter()

    for nomor, q in enumerate(selected, 1):
        clear()
        print("=" * 60)
        print(f" APLIKASI KUIS | {name} | Soal {nomor}/{jumlah}")
        print("=" * 60)
        print("\n" + q["question"] + "\n")

        for i, option in enumerate(q["options"]):
            print(f"  {chr(65+i)}. {option}")

        while True:
            jawaban = input("\nJawaban [A-D]: ").strip().upper()
            if jawaban in "ABCD":
                break
            print("Input tidak valid.")

        index = ord(jawaban) - 65
        if index == q["answer"]:
            print("✓ Benar!")
            score += 1
        else:
            benar = chr(65 + q["answer"])
            print(f"✗ Salah. Jawaban benar: {benar}. {q['options'][q['answer']]}")
        time.sleep(0.7)

    elapsed = time.perf_counter() - start
    nilai = round(score / jumlah * 100, 1)

    scores = load_json(SCORES_FILE, [])
    scores.append({
        "nama": name, "skor": score, "total": jumlah,
        "nilai": nilai, "waktu_detik": round(elapsed, 1)
    })
    scores.sort(key=lambda x: (-x["skor"], x["waktu_detik"]))
    save_json(SCORES_FILE, scores[:20])

    clear()
    print("=" * 60)
    print(" HASIL KUIS")
    print("=" * 60)
    print(f"Nama  : {name}")
    print(f"Skor  : {score}/{jumlah}")
    print(f"Nilai : {nilai}")
    print(f"Waktu : {elapsed:.1f} detik")
    print("Feedback:", "Sangat baik!" if nilai >= 80 else
          "Cukup baik, terus berlatih!" if nilai >= 60 else
          "Tetap semangat, coba lagi!")
    pause()

def leaderboard():
    clear()
    scores = load_json(SCORES_FILE, [])
    print("=" * 65)
    print(" LEADERBOARD")
    print("=" * 65)

    if not scores:
        print("Belum ada data skor.")
    else:
        print(f"{'No':<4}{'Nama':<20}{'Skor':<10}{'Nilai':<10}Waktu")
        print("-" * 55)
        for no, s in enumerate(scores[:10], 1):
            print(f"{no:<4}{s['nama'][:18]:<20}"
                  f"{s['skor']}/{s['total']:<7}"
                  f"{s['nilai']:<10}{s['waktu_detik']}s")
    pause()

def about():
    clear()
    print("=" * 60)
    print(" TENTANG PROYEK")
    print("=" * 60)
    print("Aplikasi Kuis Interaktif - Proyek Kolaborasi Kelas XII")
    print("\nMateri pemrograman:")
    print("- Variabel dan tipe data")
    print("- Percabangan")
    print("- Perulangan")
    print("- Fungsi")
    print("- List/struktur data")
    print("- Randomisasi")
    print("- Validasi input")
    print("- File I/O JSON")
    print("- Sorting leaderboard")
    pause()

def main():
    while True:
        clear()
        print("=" * 60)
        print("       APLIKASI KUIS INTERAKTIF")
        print("=" * 60)
        print("1. Mulai Kuis")
        print("2. Leaderboard")
        print("3. Tentang Proyek")
        print("4. Keluar")

        pilihan = input("\nPilih menu [1-4]: ").strip()

        if pilihan == "1":
            quiz()
        elif pilihan == "2":
            leaderboard()
        elif pilihan == "3":
            about()
        elif pilihan == "4":
            print("Terima kasih. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid.")
            time.sleep(0.8)

if __name__ == "__main__":
    main()
