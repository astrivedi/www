---
layout: paper
title: "Omega-Regular Objectives in Model-Free Reinforcement Learning"
authors:
  - "Ernst Moritz Hahn"
  - "Mateo Perez"
  - "Sven Schewe"
  - "Fabio Somenzi"
  - "Ashutosh Trivedi"
  - "Dominik Wojtczak"
venue: "TACAS 2019"
year: 2019
date: 2019-04-04
tags: [formalrl, theory, top, trustuworthyAI]
selected: true

pdf: /assets/papers/2019-tacas-omega-rl.pdf
bibtex: /assets/papers/2019-tacas-omega-rl.bib
slides:
video:
arxiv: https://arxiv.org/abs/1810.00950
doi: 10.1007/978-3-030-17462-0_27
code:

abstract: |
  We provide the first solution for model-free reinforcement learning of ω-regular objectives for Markov decision processes (MDPs). We present a constructive reduction from the almost-sure satisfaction of ω-regular objectives to an almost-sure reachability problem, and extend this technique to learning how to control an unknown model so that the chance of satisfying the objective is maximized.

  We compile ω-regular properties into limit-deterministic Büchi automata instead of the traditional Rabin automata; this choice sidesteps difficulties that have marred previous proposals. Our approach allows us to apply model-free, off-the-shelf reinforcement learning algorithms to compute optimal strategies from the observations of the MDP. We present an experimental evaluation of our technique on benchmark learning problems.
---
