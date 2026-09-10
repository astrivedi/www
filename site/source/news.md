---
layout: default
title: News
permalink: /news/
---

<h1>News</h1>
<p class="small">Updates on papers, talks, awards, and group milestones.</p>

<div class="sectionline"></div>

<div class="card">
  {% if site.data.news == nil or site.data.news.size == 0 %}
    <div class="meta">News updates coming soon.</div>
  {% else %}
    {% for item in site.data.news %}
      <div class="newsRow">
        <div class="newsDate">{{ item.date }}</div>
        <div class="newsText">{{ item.text }}</div>
      </div>
    {% endfor %}
  {% endif %}
</div>
