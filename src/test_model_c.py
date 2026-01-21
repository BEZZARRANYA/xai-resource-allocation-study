from models import load_data, model_c_rule_based

tasks, employees = load_data()

task = tasks.iloc[0]
results = model_c_rule_based(task, employees)

print("Task:", task["task_id"], task["required_skills"])
print("Top 5 employees (Model C):")
for r in results[:5]:
    print(r["employee_id"], r["score"])
    print("  reasons:", r["reasons"])

