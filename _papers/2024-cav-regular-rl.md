---
layout: paper
title: "Regular Reinforcement Learning"
authors:
  - "Taylor Dohmen"
  - "Mateo Perez"
  - "Fabio Somenzi"
  - "Ashutosh Trivedi"
venue: "CAV"
year: 2024
date: 2024-07-26
tags: [top, award, formalrl, trustworthyAI]
selected: true

pdf: /assets/papers/2024-cav-regular-rl.pdf
bibtex: /assets/papers/2024-cav-regular-rl.bib
slides:
video:
arxiv:
doi: https://doi.org/10.1007/978-3-031-65633-0_9
code:
award: "CAV Distinguished Paper Award"

abstract: |
  In reinforcement learning, an agent incrementally refines a behavioral policy through a series of episodic interactions with its environment. This process can be characterized as explicit reinforcement learning, as it deals with explicit states and concrete transitions. Building upon the concept of symbolic model checking, we propose a symbolic variant of reinforcement learning, in which sets of states are represented through predicates and transitions are represented by predicate transformers. Drawing inspiration from regular model checking, we choose regular languages over the states as our predicates, and rational transductions as predicate transformations. We refer to this framework as regular reinforcement learning, and study its utility as a symbolic approach to reinforcement learning. Theoretically, we establish results around decidability, approximability, and efficient learnability in the context of regular reinforcement learning. Towards practical applications, we develop a deep regular reinforcement learning algorithm, enabled by the use of graph neural networks, and showcase the applicability and effectiveness of (deep) regular reinforcement learning through empirical evaluation on a diverse set of case studies. :contentReference[oaicite:1]{index=1}
---
