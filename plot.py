import csv
import matplotlib.pyplot as plt

FILES = [
    "benchmarks/benchmark_static_1.csv",
    "benchmarks/benchmark_static_2.csv",
    "benchmarks/benchmark_static_3.csv",
    "benchmarks/benchmark_static_4.csv"
]

FILE_RESULT = 'graphs/graph1.png'


def read_csv(path):
    data = {}
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            n = int(row["N1"])
            t = float(row["time"])
            data.setdefault(n, []).append(t)
    return data


plt.figure()

markers = ['v', '^', 'd', 'o']
for path, marker in zip(FILES, markers):
    data = read_csv(path)
    Ns = sorted(data.keys())
    times = [min(data[n]) for n in Ns]
    label = path.replace("benchmark_", "").replace(".csv", "")
    plt.plot(Ns, times, marker=marker, linestyle='-', markersize=7, label=label)

plt.xlabel("Длина ключа N")
plt.ylabel("Время взлома, с")
plt.title("Зависимость времени взлома от длины ключа")
plt.grid(True)
# plt.legend()
plt.tight_layout()
plt.savefig(FILE_RESULT, dpi=150)
print("Сохранено:", FILE_RESULT)
