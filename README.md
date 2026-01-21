# Explainable Hybrid Scoring for Resource Allocation and Task Assignment

## Overview

This project presents an explainable artificial intelligence (XAI) framework for resource allocation and task assignment in organizational environments.  
The system is designed as an **intelligent decision support tool**, emphasizing **transparency, interpretability, and practical usability** rather than black-box optimization.

Unlike traditional assignment systems that rely on manual decision-making or opaque models, this project provides **human-interpretable recommendations** supported by explicit reasoning.

This repository contains:
- Interpretable allocation models
- Quantitative evaluation with standard recommendation metrics
- A full academic paper draft
- Reproducible experimental code

---

## Research Motivation

In many real-world organizations, task assignment decisions are still performed manually or guided by simple heuristics. While data-driven optimization methods can improve efficiency, most AI-based systems lack interpretability, which limits trust, accountability, and adoption—especially when decisions affect human resources.

This project addresses that gap by developing an **explainable hybrid scoring framework** that balances:
- Recommendation accuracy
- Workload fairness
- Human trust and oversight

The work aligns with current research directions in:
- Explainable Artificial Intelligence (XAI)
- Intelligent Decision Support Systems
- Resource Allocation and Optimization

---

## Problem Formulation

Given:
- A set of tasks with required skills and priorities
- A set of employees with skills, historical performance, workload, and availability

The objective is to:
- Rank employees for each task
- Maximize the likelihood of successful assignments
- Maintain workload balance
- Provide clear explanations for each recommendation

The problem is formulated as a **ranking-based recommendation task**, where only the top-K candidates are presented to decision-makers.

---

## Models Implemented

### Model A — Skill-Only Baseline
Ranks employees solely by skill overlap with task requirements.

- Fully transparent
- Serves as a reference baseline
- Ignores workload and operational constraints

---

### Model B — Hybrid Explainable Scoring Model (Proposed)

The main contribution of this project.

This model integrates multiple normalized and interpretable factors:
- Skill compatibility
- Historical performance
- Workload balance
- Availability constraints

Each recommendation is accompanied by **human-readable explanations**, such as:
- “Skills matched (3/4)”
- “High historical performance”
- “Low current workload”
- “Employee is available”

Explanations are generated intrinsically, not via post-hoc methods.

---

### Model C — Rule-Based Heuristic
A managerial-style heuristic commonly used in practice:
- Filters by availability and minimum skill overlap
- Applies simple priority rules

Interpretable but inflexible.

---

## Explainability

The system emphasizes **intrinsic explainability**:
- Each score component is normalized and interpretable
- Explanations directly reflect decision logic
- No black-box or post-hoc approximation methods

This design supports:
- Trust in AI-assisted decisions
- Human oversight
- Justifiable and accountable recommendations

---

## Evaluation

A synthetic yet realistic dataset is constructed, including:
- Tasks
- Employees
- Historical task–employee assignments with success labels

### Metrics
- Precision@3
- Recall@3

### Results (Average)

| Model | Precision@3 | Recall@3 |
|------|-------------|----------|
| Skill-only | 0.458 | 0.594 |
| Hybrid Explainable | **0.583** | **0.708** |
| Rule-based | 0.292 | 0.406 |

The hybrid explainable model consistently outperforms baseline approaches while maintaining full transparency.

---

## Academic Paper

A full academic paper draft is included in this repository:

The paper covers:
- Problem formulation
- Methodology
- Experimental setup
- Results and discussion
- Future research directions

This draft is intended as a **research portfolio artifact** and has not yet been submitted.

---

## Project Structure

xai-resource-allocation-study/
├── data/ # Synthetic datasets
├── src/ # Models and evaluation code
├── paper/ # Academic paper draft
│ └── paper.md
├── figures/ # Evaluation plots
├── README.md

---

## How to Run

```bash
git clone https://github.com/BEZZARRANYA/xai-resource-allocation-study.git
cd xai-resource-allocation-study
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/evaluate_models.py
