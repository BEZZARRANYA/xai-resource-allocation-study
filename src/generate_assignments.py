import random
import pandas as pd
from models import load_data, skill_only_score

random.seed(42)

def generate_assignments(n_per_task=6):
    tasks, employees = load_data()
    rows = []

    for _, task in tasks.iterrows():
        # Score all employees by skill match (used only to create realistic ground truth)
        scored = []
        for _, emp in employees.iterrows():
            s = skill_only_score(task["required_skills"], emp["skills"])
            scored.append((emp["employee_id"], s, emp["rating"], emp["workload"], emp["available"]))

        # Sort by "true success tendency" (skills + rating, prefer availability, lower workload)
        scored.sort(key=lambda x: (x[1], x[2], -x[3], x[4]), reverse=True)

        # Pick top candidates as more likely successful
        top_candidates = scored[:n_per_task]

        for emp_id, s, rating, workload, avail in top_candidates:
            # success probability: higher with skills+rating, lower with workload, zero-ish if unavailable
            prob = 0.20 + 0.50*s + 0.15*(rating/5.0) + 0.10*(1 - workload/40.0)
            if avail == 0:
                prob *= 0.4  # less likely if unavailable

            prob = max(0.0, min(0.95, prob))
            success = 1 if random.random() < prob else 0

            rows.append({
                "task_id": task["task_id"],
                "employee_id": emp_id,
                "success": success
            })

    df = pd.DataFrame(rows)
    df.to_csv("data/assignments.csv", index=False)
    print("Generated data/assignments.csv")
    print(df.head())

if __name__ == "__main__":
    generate_assignments()

