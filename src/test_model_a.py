from models import load_data, model_a_skill_only

tasks, employees = load_data()

task = tasks.iloc[0]
results = model_a_skill_only(task, employees)

print("Task:", task["task_id"], task["required_skills"])
print("Top 5 employees:")
for r in results[:5]:
    print(r)

