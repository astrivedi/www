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


