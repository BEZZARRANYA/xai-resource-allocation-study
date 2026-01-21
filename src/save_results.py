import os
import pandas as pd
import matplotlib.pyplot as plt

from models import (
    load_data,
    model_a_skill_only,
    model_b_hybrid_explainable,
    model_c_rule_based
)

K = 3

def precision_recall_at_k(recommended_ids, relevant_ids, k):
    recommended_k = recommended_ids[:k]
    relevant_set = set(relevant_ids)
    tp = len([e for e in recommended_k if e in relevant_set])
    precision = tp / k if k else 0.0
    recall = tp / len(relevant_set) if relevant_set else 0.0
    return precision, recall

def evaluate_model(model_func, tasks, employees, assignments):
    precisions = []
    recalls = []
    for _, task in tasks.iterrows():
        task_id = task["task_id"]
        relevant = assignments[(assignments["task_id"] == task_id) & (assignments["success"] == 1)]["employee_id"].tolist()
        if not relevant:
            continue
        recs = model_func(task, employees, top_k=K)
        recommended_ids = [r["employee"]["employee_id"] for r in recs]
        p, r = precision_recall_at_k(recommended_ids, relevant, K)
        precisions.append(p)
        recalls.append(r)
    return sum(precisions)/len(precisions), sum(recalls)/len(recalls)

def main():
    os.makedirs("results/tables", exist_ok=True)
    os.makedirs("results/figures", exist_ok=True)

    tasks, employees = load_data()
    assignments = pd.read_csv("data/assignments.csv")

    rows = []
    models = [
        ("Model A (Skill-only)", model_a_skill_only),
        ("Model B (Hybrid XAI)", model_b_hybrid_explainable),
        ("Model C (Rule-based)", model_c_rule_based),
    ]

    for name, fn in models:
        p, r = evaluate_model(fn, tasks, employees, assignments)
        rows.append({"model": name, "precision_at_3": round(p, 3), "recall_at_3": round(r, 3)})

    df = pd.DataFrame(rows)
    out_csv = "results/tables/eval_results.csv"
    df.to_csv(out_csv, index=False)
    print(f"Saved table: {out_csv}")
    print(df)

    # Plot: Precision@3 and Recall@3 bars
    x = range(len(df))
    plt.figure()
    plt.bar([i - 0.2 for i in x], df["precision_at_3"], width=0.4, label="Precision@3")
    plt.bar([i + 0.2 for i in x], df["recall_at_3"], width=0.4, label="Recall@3")
    plt.xticks(list(x), df["model"], rotation=15, ha="right")
    plt.ylim(0, 1.0)
    plt.title("Model Comparison on Synthetic Assignments")
    plt.legend()

    out_png = "results/figures/model_comparison.png"
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    print(f"Saved figure: {out_png}")

if __name__ == "__main__":
    main()

