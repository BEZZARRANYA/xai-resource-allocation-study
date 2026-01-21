import pandas as pd

def load_data():
    tasks = pd.read_csv("data/tasks.csv")
    employees = pd.read_csv("data/employees.csv")

    # Convert skill strings to sets
    tasks["required_skills"] = tasks["required_skills"].apply(
        lambda x: set(x.replace("[", "").replace("]", "").replace("'", "").split(", "))
    )
    employees["skills"] = employees["skills"].apply(
        lambda x: set(x.replace("[", "").replace("]", "").replace("'", "").split(", "))
    )

    return tasks, employees


def skill_only_score(task_skills, employee_skills):
    if len(task_skills) == 0:
        return 0.0
    return len(task_skills & employee_skills) / len(task_skills)


# -----------------------------
# Model A: Skill-only baseline
# -----------------------------
def model_a_skill_only(task, employees, top_k=3):
    results = []
    req = task["required_skills"]

    for _, emp in employees.iterrows():
        score = skill_only_score(req, emp["skills"])
        matched = len(req & emp["skills"])
        total = len(req)

        results.append({
            "employee": {"employee_id": emp["employee_id"]},
            "score": round(score, 3),
            "reasons": [f"Matched {matched}/{total} skills (skill-only baseline)"]
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


# -----------------------------------------
# Model B: Hybrid explainable weighted score
# -----------------------------------------
def model_b_hybrid_explainable(task, employees, top_k=3,
                              w_skill=0.45, w_rating=0.25, w_workload=0.20, w_avail=0.10):
    results = []
    req = task["required_skills"]

    for _, emp in employees.iterrows():
        # normalized components 0..1
        skill = skill_only_score(req, emp["skills"])
        rating = emp["rating"] / 5.0
        workload = max(0.0, 1.0 - (emp["workload"] / 40.0))
        avail = 1.0 if emp["available"] == 1 else 0.0

        score = (w_skill * skill) + (w_rating * rating) + (w_workload * workload) + (w_avail * avail)

        matched = len(req & emp["skills"])
        total = len(req)

        reasons = []
        reasons.append(f"Skill match {matched}/{total} (ratio={skill:.2f})")
        reasons.append(f"Rating {emp['rating']:.1f}/5")
        reasons.append(f"Workload {emp['workload']}")
        reasons.append("Available" if emp["available"] == 1 else "Not available")

        breakdown = {
            "skill": round(w_skill * skill, 3),
            "rating": round(w_rating * rating, 3),
            "workload": round(w_workload * workload, 3),
            "availability": round(w_avail * avail, 3),
        }

        results.append({
            "employee": {"employee_id": emp["employee_id"]},
            "score": round(score, 3),
            "breakdown": breakdown,
            "reasons": reasons
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


# -------------------------------
# Model C: Rule-based heuristic
# -------------------------------
def model_c_rule_based(task, employees, top_k=3):
    results = []
    req = task["required_skills"]

    for _, emp in employees.iterrows():
        matched = len(req & emp["skills"])

        # Rule filters
        if emp["available"] != 1:
            continue
        if matched == 0:
            continue

        # Rule-based scoring (interpretable)
        score = (matched * 1.0) + (emp["rating"] * 0.5) + (max(0, 40 - emp["workload"]) * 0.05)

        reasons = [
            "Rule: Available",
            f"Rule: Matched {matched}/{len(req)} required skills",
            f"Rule: Workload={emp['workload']}",
            f"Rule: Rating={emp['rating']:.1f}/5"
        ]

        results.append({
            "employee": {"employee_id": emp["employee_id"]},
            "score": round(score, 3),
            "reasons": reasons
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

