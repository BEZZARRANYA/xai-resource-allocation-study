from models import load_data, model_b_hybrid_explainable

tasks, employees = load_data()

task = tasks.iloc[0]
results = model_b_hybrid_explainable(task, employees)

print("Task:", task["task_id"], task["required_skills"])
print("Top 3 employees (Model B):")
for r in results[:3]:
    print(r["employee_id"], r["score"])
    print("  breakdown:", r["breakdown"])
    print("  reasons:", r["reasons"])

