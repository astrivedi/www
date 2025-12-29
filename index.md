---
layout: default
title: Home
---

<div class="heroTop">
  <div>
    <h1>{{ site.title }}</h1>

    <p class="small" style="margin-top:6px;">
      Associate Professor of Computer Science · University of Colorado Boulder
    </p>

    <p class="heroDesc">
      {{ site.description }}
    </p>

    <div class="pills pills-hero">
      <a class="pill" href="{{ site.links.cv }}">CV</a>
      <a class="pill" href="{{ site.links.scholar }}">Google Scholar</a>
      <a class="pill" href="{{ site.links.dblp }}">DBLP</a>
      <a class="pill" href="{{ site.links.email }}">Email</a>
    </div>
  </div>

  <div class="spacer"></div>

  <img
    src="{{ site.baseurl }}/assets/img/portrait.jpg"
    alt="Ashutosh Trivedi"
    class="portrait"
  />
</div>

<div class="blankline"></div>

<div class="cardgrid-2">
  <div class="card">
    <h3>Formal Methods for Reinforcement Learning</h3>
    <div class="meta">
      Foundations and algorithms for verifying, synthesizing, and reasoning about
      reinforcement-learning systems, including temporal objectives, recursion,
      and symbolic representations.
    </div>
  </div>

  <div class="card">
    <h3>Trustworthy Reasoning with Learning and LLMs</h3>
    <div class="meta">
      Combining formal verification, symbolic reasoning, and learning to produce
      explanations and guarantees that are checkable, not just plausible.
    </div>
  </div>

  <div class="card">
    <h3>AI, Software, and Accountability</h3>
    <div class="meta">
      Methods for auditing, testing, and debugging high-stakes software systems,
      with applications to fairness, legal compliance, and socio-technical
      decision-making.
    </div>
  </div>

  <div class="card">
    <h3>Secure & Safe Cyber-Physical Systems</h3>
    <div class="meta">
      Rigorous methods for security, privacy, and safety of cyber-physical and
      learning-enabled systems, with applications to medical devices and
      critical infrastructure.
    </div>
  </div>
</div>

<h2>Selected publications</h2>
<div class="cardgrid-3">

  <div class="card">
    <h3 class="pubTitle">
      <a href="https://link.springer.com/chapter/10.1007/978-3-030-17462-0_27">
        ω-regular Objectives in Model-Free Reinforcement Learning
      </a>
    </h3>
    <div class="badges">
      <span class="badge">Formal RL</span>
    </div>
    <div class="pubBlurb">
      A reduction that enables model-free RL for ω-regular objectives via limit-deterministic Büchi automata.
    </div>
    <div class="meta">TACAS · 2019</div>
    <div class="actions">
      <a class="link" href="https://arxiv.org/pdf/1810.00950.pdf">PDF</a>
      <a class="link" href="https://link.springer.com/chapter/10.1007/978-3-030-17462-0_27">Details</a>
    </div>
  </div>

  <div class="card">
    <h3 class="pubTitle">
      <a href="https://arxiv.org/abs/2206.11430">
        Recursive Reinforcement Learning
      </a>
    </h3>
    <div class="badges">
      <span class="badge">Formal RL</span>
    </div>
    <div class="pubBlurb">
      Model-free learning for recursive MDPs (probabilistic pushdown systems) with convergence guarantees.
    </div>
    <div class="meta">NeurIPS · 2022</div>
    <div class="actions">
      <a class="link" href="https://proceedings.neurips.cc/paper_files/paper/2022/file/e6f8759254d86ea9c197d30b92b313ca-Paper-Conference.pdf">PDF</a>
      <a class="link" href="https://arxiv.org/abs/2206.11430">Details</a>
    </div>
  </div>

  <div class="card">
    <h3 class="pubTitle">
      <a href="https://link.springer.com/chapter/10.1007/978-3-031-65633-0_9">
        Regular Reinforcement Learning
      </a>
    </h3>
    <div class="badges">
      <span class="badge">Trustworthy Reasoning</span>
    </div>
    <div class="pubBlurb">
      Symbolic RL using regular languages and rational transductions, with a deep variant enabled by GNNs.
    </div>
    <div class="meta">CAV · 2024</div>
    <div class="actions">
      <a class="link" href="https://link.springer.com/chapter/10.1007/978-3-031-65633-0_9">PDF</a>
      <a class="link" href="https://link.springer.com/chapter/10.1007/978-3-031-65633-0_9">Details</a>
    </div>
  </div>

  <div class="card">
    <h3 class="pubTitle">
      <a href="https://conf.researchr.org/details/icse-2022/icse-2022-papers/175/Fairness-aware-Configuration-of-Machine-Learning-Libraries">
        Fairness-aware Configuration of Machine Learning Libraries
      </a>
    </h3>
    <div class="badges">
      <span class="badge">Accountability</span>
    </div>
    <div class="pubBlurb">
      Search-based testing of hyperparameter space to expose the precision–fairness frontier and debug fairness bugs.
    </div>
    <div class="meta">ICSE · 2022</div>
    <div class="actions">
      <a class="link" href="https://arxiv.org/pdf/2202.06196.pdf">PDF</a>
      <a class="link" href="https://conf.researchr.org/details/icse-2022/icse-2022-papers/175/Fairness-aware-Configuration-of-Machine-Learning-Libraries">Details</a>
    </div>
  </div>

  <div class="card">
    <h3 class="pubTitle">
      <a href="https://arxiv.org/abs/2305.17519">
        Closure Certificates
      </a>
    </h3>
    <div class="badges">
      <span class="badge">CPS  & Security</span>
    </div>
    <div class="pubBlurb">
      Extends barrier certificates to transition invariants, enabling automated refutation for temporal specifications.
    </div>
    <div class="meta">HSCC · 2024</div>
    <div class="actions">
      <a class="link" href="https://arxiv.org/pdf/2305.17519.pdf">PDF</a>
      <a class="link" href="https://arxiv.org/abs/2305.17519">Details</a>
    </div>
  </div>

  <div class="card">
    <h3 class="pubTitle">
      <a href="https://dblp.org/rec/conf/icse/TizpazNiariMWDRT23">
        Metamorphic Testing and Debugging of Tax Preparation Software
      </a>
    </h3>
    <div class="badges">
      <span class="badge">Accountability</span>
    </div>
    <div class="pubBlurb">
      Metamorphic relations from IRS rules + randomized test generation to uncover compliance and accountability bugs.
    </div>
    <div class="meta">ICSE-SEIS · 2023</div>
    <div class="actions">
      <a class="link" href="https://arxiv.org/pdf/2205.04998.pdf">PDF</a>
      <a class="link" href="https://dblp.org/rec/conf/icse/TizpazNiariMWDRT23">Details</a>
    </div>
  </div>

</div>

<h2>Join the group</h2>
<div class="card ctaRow">
  <div>
    <h3>PhD students & postdocs</h3>
    <div class="meta">
      I’m recruiting PhD students and occasional postdocs interested in formal methods,
      reinforcement learning, cyber-physical systems, and AI accountability. Strong
      theoretical foundations and curiosity about real-world impact are especially welcome.
    </div>
  </div>
  <a class="pill" href="/group/">Current openings →</a>
</div>

<h2>Recent news</h2>
<div class="card">
  {% assign items = site.data.news | slice: 0, 5 %}
  {% if items.size == 0 %}
    <div class="meta">News updates coming soon.</div>
  {% else %}
    {% for item in items %}
      <div class="newsRow">
        <div class="newsDate">{{ item.date }}</div>
        <div class="newsText">{{ item.text }}</div>
      </div>
    {% endfor %}
  {% endif %}
</div>
<p class="small" style="margin-top:10px;">
  <a class="link" href="/news/">All news →</a>
</p>
