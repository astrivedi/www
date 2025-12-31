---
layout: paper
title: "Uncovering Discrimination Clusters: Quantifying and Explaining Systematic Fairness Violations"
authors:
  - "Ranit Akash"
  - "Ashish Kumar" 
  - "Verya Monjezi"
  - "Ashutosh Trivedi"
  - "Gang Tan"
  - "Saeid Tizpaz-Niari"
venue: "ASE 2025"
year: 2025
date: 2025-08-01
tags: [accountableSE, trustworthyAI, ai]
selected: true

pdf: /assets/papers/2025-ase-discrimination-clusters.pdf
bibtex: /assets/papers/2025-ase-discrimination-clusters.bib
slides: /assets/papers/2025-ase-discrimination-clusters.pptx
video:
arxiv:
doi:
code:

abstract: |
  Fairness in algorithmic decision-making is often framed in terms of individual fairness, which requires that similar individuals receive similar outcomes. A system violates individual fairness if there exists a pair of inputs differing only in protected attributes (such as race or gender) that lead to significantly different outcomes, one favorable and the other unfavorable. While this notion highlights isolated instances of unfairness, it fails to capture broader patterns of clustered discrimination that may affect entire subgroups.

  We introduce and motivate the concept of discrimination clustering, a generalization of individual fairness violations. Rather than detecting single counterfactual disparities, we seek to uncover regions of the input space where small perturbations in protected features lead to k-significantly distinct clusters of outcomes. That is, for a given input, we identify a local neighborhood, differing only in protected attributes, whose members’ outputs separate into many distinct clusters. These clusters reveal arbitrariness in treatment based solely on protected attributes, exposing patterns of algorithmic bias that elude pairwise fairness checks.

  We present HYFAIR, a hybrid technique that combines formal symbolic analysis (via SMT and MILP solvers) to certify individual fairness with randomized search to discover discriminatory clusters. This combination enables both formal guarantees when no counterexamples exist and the detection of severe violations that are computationally challenging for symbolic methods alone. Given a set of inputs exhibiting high k-discrimination, we further introduce a novel explanation method that generates interpretable, decision-tree-style artifacts.

  Our experiments show that HYFAIR outperforms state-of-the-art fairness verification and local explanation methods. It reveals that some benchmarks exhibit substantial discrimination clustering, while others show limited or no disparities with respect to protected attributes. It also provides intuitive explanations that support understanding and mitigation of unfairness.
---
