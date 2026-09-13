---
{
  "layout": "paper",
  "title": "Metamorphic Testing and Debugging of Tax Preparation Software",
  "authors": [
    "Saeid Tizpaz-Niari",
    "Verya Monjezi",
    "Morgan Wagner",
    "Shiva Darian",
    "Krystia Reed",
    "Ashutosh Trivedi"
  ],
  "venue": "ICSE-SEIS 2023",
  "year": 2023,
  "date": "2023-05-01",
  "tags": [
    "accountableSE",
    "top",
    "trustworthyAI"
  ],
  "selected": true,
  "pdf": "/assets/papers/2023-icse-seis-tax-prep.pdf",
  "bibtex": "/assets/papers/2023-icse-seis-tax-prep.bib",
  "slides": null,
  "video": null,
  "arxiv": "https://arxiv.org/abs/2205.04998",
  "doi": "https://doi.org/10.1109/ICSE-SEIS58686.2023.00019",
  "code": null,
  "abstract": "This paper presents a data-driven framework to improve the trustworthiness of US tax preparation software systems. Given the legal implications of bugs in such software on its users, ensuring compliance and trustworthiness of tax preparation software is of paramount importance. The key barriers in developing debugging aids for tax preparation systems are the unavailability of explicit specifications and the difficulty of obtaining oracles. We posit that, since the US tax law adheres to the legal doctrine of precedent, the specifications about the outcome of tax preparation software for an individual taxpayer must be viewed in comparison with individuals that are deemed similar. Consequently, these specifications are naturally available as properties on the software requiring similar inputs provide similar outputs. Inspired by the metamorphic testing paradigm, we dub these relations metamorphic relations. In collaboration with legal and tax experts, we explicated metamorphic relations for a set of challenging properties from various US Internal Revenue Services (IRS) publications including Publication 596 (Earned Income Tax Credit), Schedule 8812 (Qualifying Children/Other Dependents), and Form 8863 (Education Credits). We focus on an open-source tax preparation software for our case study and develop a randomized test-case generation strategy to systematically validate the correctness of tax preparation software guided by metamorphic relations. We further aid this test-case generation by visually explaining the behavior of software on suspicious instances using easy to-interpret decision-tree models. Our tool uncovered several accountability bugs with varying severity ranging from non-robust behavior in corner-cases (unreliable behavior when tax returns are close to zero) to missing eligibility conditions in the updated versions of software.",
  "abstract_source": "https://arxiv.org/abs/2205.04998"
}
---
