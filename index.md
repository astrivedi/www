---
layout: default
title: Home
---

<div class="heroTop">
  <img
    src="{{ site.baseurl }}/ast-bw.jpeg"
    alt="Ashutosh Trivedi"
    class="portrait"
  />
    <div class="spacer"></div>
  <div>
    <h1>{{ site.title }}</h1>

    <p class="small" style="margin-top:6px;">
      Associate Professor of Computer Science · University of Colorado Boulder
    </p>

    <p class="heroDesc">
      I work on formal methods for reinforcement learning, trustworthy AI, and safety-critical software and cyber-physical systems.
    </p>

    <div class="pills pills-hero">
      <a class="pill" href="{{ site.links.cv }}">CV</a>
      <a class="pill" href="{{ site.links.scholar }}">Google Scholar</a>
      <a class="pill" href="{{ site.links.dblp }}">DBLP</a>
      <a class="pill" href="{{ site.links.email }}">Email</a>
    </div>
  </div>

</div>

<div class="blankline"></div>
<h2>Research</h2>
<div class="cardgrid-2">
  <div class="card">
    <h3>Formal Methods for Reinforcement Learning</h3>
    <div class="meta">
      Verification, synthesis, and symbolic reasoning for reinforcement-learning systems,
      including temporal objectives, recursion, and structured representations.
    </div>
  </div>

  <div class="card">
    <h3>Trustworthy Reasoning with LLMs</h3>
    <div class="meta">
      Formal and symbolic methods for producing explanations and guarantees with rigorous foundations.
    </div>
  </div>

  <div class="card">
    <h3>AI, Software, and Accountability</h3>
    <div class="meta">
      Auditing, testing, and debugging methods for high-stakes software, with applications
      to fairness, legal compliance, and socio-technical decision-making.
    </div>
  </div>

  <div class="card">
    <h3>Secure & Safe Cyber-Physical Systems</h3>
    <div class="meta">
      Security, privacy, and safety methods for cyber-physical and learning-enabled
      systems, with applications to medical devices and critical infrastructure.
    </div>
  </div>
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

{% include selected_pubs_grid.html limit=9 %}
