---
layout: paper
title: "Closure Certificates"
authors:
  - "Vishnu Murali"
  - "Ashutosh Trivedi"
  - "Majid Zamani"
venue: "HSCC 2024"
year: 2024
date: 2024-05-14
tags: [top, cps, theory]
selected: true

pdf: /assets/papers/2024-hscc-closure-certificates.pdf
bibtex: /assets/papers/2024-hscc-closure-certificates.bib
slides:
video:
arxiv: https://arxiv.org/pdf/2305.17519.pdf
doi: 10.1145/3641513.3650120
code:

abstract: |
  We introduce *closure certificates* as a generalization of barrier certificates that reason about the **transitive closure of transition relations** to enable automated verification of dynamical systems against a broad class of specifications including *ω-regular properties*. Traditional barrier certificates reason only over single transitions, which makes refuting recurrence properties conservative or ineffective. Closure certificates instead operate over pairs of states to capture transition invariants and use sum-of-squares (SOS) and SMT-based characterizations to search for suitable certificates. We show that closure certificates can prove safety even when barrier certificates of the same template do not exist, and subsume existing barrier-certificate-based verification approaches. Case studies illustrate the utility of closure certificates for verifying safety, persistence (finite visits), and LTL properties for continuous and hybrid dynamical systems. :contentReference[oaicite:1]{index=1}
---
