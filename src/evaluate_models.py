import pandas as pd
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

        relevant = assignments[
            (assignments["task_id"] == task_id) &
            (assignments["success"] == 1)
        ]["employee_id"].tolist()

        if not relevant:
            continue

        recs = model_func(task, employees, top_k=K)
        recommended_ids = [r["employee"]["employee_id"] for r in recs]

        p, r = precision_recall_at_k(recommended_ids, relevant, K)
        precisions.append(p)
        recalls.append(r)

    if not precisions:
        return 0.0, 0.0

    return sum(precisions) / len(precisions), sum(recalls) / len(recalls)


def main():
    tasks, employees = load_data()
    assignments = pd.read_csv("data/assignments.csv")

    results = []
    for name, model in [
        ("Model A (Skill-only)", model_a_skill_only),
        ("Model B (Hybrid XAI)", model_b_hybrid_explainable),
        ("Model C (Rule-based)", model_c_rule_based),
    ]:
        p, r = evaluate_model(model, tasks, employees, assignments)
        results.append((name, p, r))

    print(f"\nEvaluation Results (Precision@{K}, Recall@{K})")
    print("-" * 60)
    for name, p, r in results:
        print(f"{name:<24} | Precision={p:.3f} | Recall={r:.3f}")


if __name__ == "__main__":
    main()

