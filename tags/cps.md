---
layout: default
title: "Tag: cps"
permalink: /tags/cps/
tag: cps
---
<h2>Accountable Cyber-Physical Systems</h2>

{% assign papers = site.papers | default: nil %}

{% if papers == nil %}
  {% assign papers = site.collections.papers.docs | default: "" | split: "" %}
{% endif %}

{% assign papers = papers | sort: "date" | reverse %}
{% assign found = 0 %}

{% for p in papers %}
{% if p.tags and p.tags contains page.tag %}
{% assign found = found | plus: 1 %}
{% include paper_card.html p=p %}
{% endif %}
{% endfor %}

{% if found == 0 %}
<p>No papers tagged <code>{{ page.tag }}</code> yet.</p>
{% endif %}

