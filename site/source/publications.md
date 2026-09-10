---
layout: default
title: Publications
permalink: /publications/
---

## Selected Publications

{% assign selected = site.papers | where: "selected", true | sort: "date" | reverse %}
{% for p in selected %}
  {% include paper_card.html p=p %}
{% endfor %}

## All Publications

{% assign all = site.papers | sort: "date" | reverse %}
{% for p in all %}
  {% include paper_card.html p=p %}
{% endfor %}
