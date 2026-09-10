---
layout: paper
title: "Continuous-Time Reward Machines"
authors:
  - "Amin Falah"
  - "Shibashis Guha"
  - "Ashutosh Trivedi"
venue: "Proceedings of the Thirty-Fourth International Joint Conference on
                  Artificial Intelligence, {IJCAI} 2025, Montreal, Canada, August 16-22,
                  2025"
year: 2025
date: "24 Sep 2025"
tags: [formalRL]
selected: true

pdf: /assets/papers/2025-ijcai-continuous-time-rewards.pdf 
bibtex: /assets/papers/2025-ijcai-continuous-time-rewards.bib
arxiv: https://www.ijcai.org/proceedings/2025/563

abstract: >
  Reinforcement Learning (RL) is a sampling-based method for sequential decision-making, in which a learning agent iteratively converges toward an optimal policy by leveraging feedback from the environment in the form of scalar reward signals. While timing information is often abstracted in discrete-time domains, time-critical learning applications—such as queuing systems, population processes, and manufacturing systems—are naturally modeled as Continuous-Time Markov Decision Processes (CTMDPs). Since the seminal work of Bradtke and Duff, model-free RL for CTMDPs has become well-understood. However, in many practical applications, practitioners possess high-quality information about system rates derived from traditional queuing theory, which learning agents could potentially exploit to accelerate convergence. Despite this, classical RL algorithms for CTMDPs typically re-learn these parameters through sampling. In this work, we propose continuous-time reward machines (CTRMs), a novel framework that embeds reward functions and real-time state-action dynamics into a unified structure. CTRMs enable RL agents to effectively navigate dense-time environments while leveraging reward shaping and counterfactual experiences for accelerated learning. Our empirical results demonstrate CTRMs' ability to improve learning efficiency in time-critical environments.
---
