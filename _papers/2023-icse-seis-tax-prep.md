---
layout: paper
title: "Metamorphic Testing and Debugging of Tax Preparation Software"
authors:
  - "Saeid Tizpaz-Niari"
  - "Verya Monjezi"
  - "Morgan Wagner"
  - "Shiva Darian"
  - "Krystia Reed"
  - "Ashutosh Trivedi"
venue: "ICSE-SEIS 2023"
year: 2023
date: 2023-05-01
tags: [accountableSE, top, trustworthyAI]
selected: true

pdf: /assets/papers/2023-icse-seis-tax-prep.pdf
bibtex: /assets/papers/2023-icse-seis-tax-prep.bib
slides:
video:
arxiv: https://arxiv.org/abs/2205.04998
doi: 10.1109/ICSE-SEIS58686.2023.00019
code:

abstract: |
  We present a **data-driven debugging framework** to improve the trustworthiness of U.S. tax preparation software, a class of socio-legal critical systems with pervasive societal impact. Correctness specifications for such software are often unavailable and oracles are difficult to obtain, because determining the correct tax outcome requires expert interpretation of complex tax law. Drawing on the legal doctrine of *precedent*, we formulate correctness in terms of **metamorphic relations** between similar inputs — relations that must hold for software to behave consistently on related taxpayer scenarios.

  The framework uses these relations to guide **randomized test-case generation**, systematically exploring input space and revealing instances of incorrect or surprising behavior. To support comprehension of failures, we integrate **interpretable decision tree models** that explain suspicious outputs. Applied to open-source tax preparation software, the approach uncovers several accountability bugs ranging from non-robust behavior near corner cases to missing eligibility logic, demonstrating the effectiveness of metamorphic testing for auditing and debugging legal-critical software systems. :contentReference[oaicite:1]{index=1}
---
