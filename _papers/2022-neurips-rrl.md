---
layout: paper
title: "Recursive Reinforcement Learning"
authors:
  - "Ernst Moritz Hahn"
  - "Mateo Perez"
  - "Sven Schewe"
  - "Fabio Somenzi"
  - "Ashutosh Trivedi"
  - "Dominik Wojtczak"
venue: "NeurIPS"
year: 2022
date: 2022-12-01
tags: [top, formalrl, theory, trustworthyAI]
selected: true

pdf: /assets/papers/2022-neurips-rrl.pdf
bibtex: /assets/papers/2022-neurips-rrl.bib
slides:
video:
arxiv:
doi:

abstract: |
  Recursion is the fundamental paradigm to finitely describe potentially infinite objects. As state-of-the-art reinforcement learning (RL) algorithms cannot directly reason about recursion, they must rely on manually crafted “flat” environment representations, which hamper scalability and generalization. To overcome this limitation, we study environments modeled as a collection of Markov decision processes (MDPs) that can recursively invoke one another — recursive MDPs (RMDPs) — which are expressively equivalent to probabilistic pushdown systems.

  We introduce **Recursive Q-learning**, a model-free RL algorithm for RMDPs, and prove convergence guarantees for finite, single-exit and deterministic multi-exit settings under mild assumptions. Our approach enables computing optimal policies in recursive environments without flattening, broadening the applicability of RL to structured decision processes. Empirical examples demonstrate the potential of the framework on recursive problems that challenge traditional RL methods. :contentReference[oaicite:1]{index=1}
---
