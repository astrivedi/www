---
layout: default
title: Publications
permalink: /publications/
---

<h1>Publications</h1>

<p>
This page lists selected and recent publications. For a complete and always up-to-date
list, see my <a class="link" href="{{ site.links.scholar }}">Google Scholar profile</a>.
</p>

<div class="sectionline"></div>

{% for block in site.data.publications %}
  <h2>{{ block.year }}</h2>

  <ul>
    {% for pub in block.entries %}
      <li style="margin-bottom:12px;">
        <strong>{{ pub.title }}</strong><br/>
        {{ pub.authors }}<br/>
        <em>{{ pub.venue }}</em>
        {% if pub.awards %} — {{ pub.awards }}{% endif %}

        {% if pub.links %}
          <span class="small">
            {% if pub.links.pdf %} · <a class="link" href="{{ pub.links.pdf }}">PDF</a>{% endif %}
            {% if pub.links.arxiv %} · <a class="link" href="{{ pub.links.arxiv }}">arXiv</a>{% endif %}
            {% if pub.links.doi %} · <a class="link" href="{{ pub.links.doi }}">DOI</a>{% endif %}
          </span>
        {% endif %}
      </li>
    {% endfor %}
  </ul>

  <div class="sectionline"></div>
{% endfor %}
