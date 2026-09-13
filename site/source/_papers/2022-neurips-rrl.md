---
{
  "layout": "paper",
  "title": "Recursive Reinforcement Learning",
  "authors": [
    "Ernst Moritz Hahn",
    "Mateo Perez",
    "Sven Schewe",
    "Fabio Somenzi",
    "Ashutosh Trivedi",
    "Dominik Wojtczak"
  ],
  "venue": "NeurIPS",
  "year": 2022,
  "date": "2022-12-01",
  "tags": [
    "top",
    "formalrl",
    "theory",
    "trustworthyAI"
  ],
  "selected": true,
  "pdf": "/assets/papers/2022-neurips-rrl.pdf",
  "bibtex": "/assets/papers/2022-neurips-rrl.bib",
  "slides": null,
  "video": null,
  "arxiv": "https://arxiv.org/abs/2206.11430",
  "doi": null,
  "abstract": "Recursion is the fundamental paradigm to finitely describe potentially infinite objects. As state-of-the-art reinforcement learning (RL) algorithms cannot directly reason about recursion, they must rely on the practitioner's ingenuity in designing a suitable \"flat\" representation of the environment. The resulting manual feature constructions and approximations are cumbersome and error-prone; their lack of transparency hampers scalability. To overcome these challenges, we develop RL algorithms capable of computing optimal policies in environments described as a collection of Markov decision processes (MDPs) that can recursively invoke one another. Each constituent MDP is characterized by several entry and exit points that correspond to input and output values of these invocations. These recursive MDPs (or RMDPs) are expressively equivalent to probabilistic pushdown systems (with call-stack playing the role of the pushdown stack), and can model probabilistic programs with recursive procedural calls. We introduce Recursive Q-learning -- a model-free RL algorithm for RMDPs -- and prove that it converges for finite, single-exit and deterministic multi-exit RMDPs under mild assumptions.",
  "abstract_source": "https://arxiv.org/abs/2206.11430"
}
---
