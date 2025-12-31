---
layout: paper
title: "Fairness-aware Configuration of Machine Learning Libraries"
authors:
  - "Saeid Tizpaz-Niari"
  - "Ashish Kumar"
  - "Gang (Gary) Tan"
  - "Ashutosh Trivedi"
venue: "ICSE 2022"
year: 2022
date: 2022-05-25
tags: [accountableSE, trustworthyAI]
selected: true

pdf: assets/papers/2022-icse-fairaware.pdf 
bibtex: /assets/papers/2022-icse-fairaware.bib
slides:
video:
arxiv: https://arxiv.org/abs/2202.06196
doi: 10.1145/3510003.3510202
code:

abstract: |
  Machine-learning (ML) software is increasingly deployed in socially critical applications where ensuring fairness is essential. While existing approaches to fairness typically modify the training dataset or the learning algorithm, the configuration of ML hyperparameters also significantly influences fairness outcomes. This paper investigates how hyperparameters can either amplify or mitigate discrimination present in datasets. We design three search-based software testing algorithms to uncover the **precision-fairness frontier** across the hyperparameter space and augment this with statistical debugging to explain how parameters affect fairness. We implement our techniques in **Parfait-ML** (PARameter FAIrness Testing for ML Libraries) and demonstrate effectiveness across five mature ML algorithms and six social-critical applications, identifying configurations that **improve fairness without sacrificing precision**. Surprisingly, some hyperparameter settings (e.g., restricted attribute search space for random forests) can **amplify bias**, and our findings corroborate similar observations in the literature. :contentReference[oaicite:1]{index=1}
---
