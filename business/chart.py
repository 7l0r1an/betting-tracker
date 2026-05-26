import matplotlib.pyplot as plt
from repository import file_repo
from repository import accumulator_repo

def show_profit_chart():
    bets = file_repo.load_bets()
    accumulators = accumulator_repo.load_accumulators()

    # combinam toate pariurile finalizate sortate
    finished_bets = [b for b in bets if b.result is not None]
    finished_acc = [a for a in accumulators if a.result is not None]

    if not finished_bets and not finished_acc:
        print("Nu ai pariuri finalizate pentru grafic.")
        return

    # calculam profitul cumulativ
    profits = []
    labels = []
    cumulative = 0

    for b in finished_bets:
        cumulative += b.profit
        profits.append(cumulative)
        labels.append(b.match[:15])  # primele 15 caractere

    for a in finished_acc:
        cumulative += a.profit
        profits.append(cumulative)
        labels.append("Acumulator")

    # desenam graficul
    plt.figure(figsize=(12, 6))
    plt.plot(profits, marker="o", linewidth=2, color="green" if profits[-1] >= 0 else "red")
    plt.axhline(y=0, color="gray", linestyle="--", linewidth=1)  # linie la 0

    # coloram zonele pozitive/negative
    plt.fill_between(range(len(profits)), profits, 0,
                     where=[p >= 0 for p in profits],
                     alpha=0.3, color="green", label="Profit")
    plt.fill_between(range(len(profits)), profits, 0,
                     where=[p < 0 for p in profits],
                     alpha=0.3, color="red", label="Pierdere")

    plt.xticks(range(len(labels)), labels, rotation=45, ha="right", fontsize=8)
    plt.title("Evolutie Profit", fontsize=14)
    plt.ylabel("Profit (RON)")
    plt.xlabel("Pariuri")
    plt.legend()
    plt.tight_layout()
    plt.show()