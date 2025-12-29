---
layout: paper
title: "Stochastic Neural Simulation Relations for Control Transfer"
authors:
  - "Alireza Nadali"
  - "Ashutosh Trivedi"
  - "Majid Zamani"
venue: "International Conference on Neuro-symbolic Systems, 28-30 May 2025,
                  University of Pennsylvania, Philadelphia, Pennsylvania, {USA}"
year: 2025
date: "12 Sep 2025"
tags: [cps,top,award]
selected: true

pdf: /assets/papers/2025-neus-stochastic-neural-simulation.pdf
bibtex: /assets/papers/22025-neus-stochastic-neural-simulation.bib
slides: 
video:
arxiv:
doi:
code:
award: "DARPA Disruptive Idea Award"

abstract: |
    This paper explores a neurosymbolic approach to probabilistic transfer of control logic from a source stochastic control system to a target system while ensuring approximately equivalent behavioral guarantees in both domains. Traditional methods struggle with this problem due to the absence of a complete characterization of behavioral specifications, which prevents a direct formulation in terms of loss functions. To address this challenge, we leverage the concept of stochastic simulation relations to establish probabilistic observational equivalence between the behaviors of two (black-box) stochastic systems. These functions ensure that the outputs of both systems, equipped with their respective controllers, remain probabilistically close over time. By parameterizing stochastic simulation functions with neural networks, we introduce the notion of stochastic neural simulation functions, enabling a data-driven mechanism to transfer any synthesized controller—along with its proof of correctness—without requiring explicit specification of behavioral constraints. This neurosymbolic integration combines the scalability of neural methods with the formal guarantees of symbolic approaches, bridging the gap between learning-based control synthesis and formal verification. Compared to prior methods, our approach eliminates the need for a closed-loop mathematical model and explicit requirement specifications for both the source and target systems, while providing probabilistic guarantees over an infinite horizon. We also introduce validity conditions that, when satisfied, ensure the closeness of the outputs of two systems equipped with their corresponding controllers, removing the need for post-facto verification. We demonstrate the effectiveness of our approach through four case studies, highlighting its potential to advance scalable, formally grounded, and transferable control synthesis.
---
