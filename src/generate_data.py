import random
import pandas as pd

random.seed(42)

def generate_data(n_tasks=8, n_employees=12):
    tasks = []
    employees = []

    for i in range(n_tasks):
        tasks.append({
            "task_id": f"T{i+1}",
            "required_skills": random.sample(
                ["python", "ml", "data", "backend", "sql", "frontend"], k=2
            ),
            "priority": random.randint(1, 5)
        })

    for i in range(n_employees):
        employees.append({
            "employee_id": f"E{i+1}",
            "skills": random.sample(
                ["python", "ml", "data", "backend", "sql", "frontend"], k=3
            ),
            "rating": round(random.uniform(3.0, 5.0), 1),
            "workload": random.randint(5, 40),
            "available": random.choice([0, 1])
        })

    return tasks, employees

if __name__ == "__main__":
    tasks, employees = generate_data()

    df_tasks = pd.DataFrame(tasks)
    df_employees = pd.DataFrame(employees)

    df_tasks.to_csv("data/tasks.csv", index=False)
    df_employees.to_csv("data/employees.csv", index=False)

    print("Synthetic data generated.")
    print(df_tasks.head())
    print(df_employees.head())

