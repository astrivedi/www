---
layout: default
title: Tags
permalink: /tags/
---

## Tags

{% assign alltags = "" | split: "" %}
{% for p in site.papers %}
  {% for t in p.tags %}
    {% assign alltags = alltags | push: t %}
  {% endfor %}
{% endfor %}
{% assign alltags = alltags | uniq | sort %}

{% for t in alltags %}
- [{{ t }}](/tags/{{ t | downcase | uri_escape }}/)
{% endfor %}
