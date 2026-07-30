# AGENTS.md — repository constitution

This file governs every contribution to this repository, human or AI. It is the
canonical source for scope, voice, and style referenced elsewhere in this repository
(`PRD.md`, `RTM.md`, `agents/azure-capacity-manager.agent.md`,
`skills/azure-capacity-management/SKILL.md`, `sre-agent/`). If any other file's
guidance conflicts with this one, this file wins.

## 1. Hard rules

These are gates, not guidelines. A single violation fails the entire contribution —
there is no partial credit and no "fix it next time."

### 1.1 No fabrication — everything links to a canonical source

Every factual claim in this repository must cite its canonical source inline, as a
Markdown link, at the point the claim is made — not just in a "further reading"
list.

- **Default canonical source:** [Microsoft Learn](https://learn.microsoft.com/).
- **FinOps Framework, domain, and capability claims:** [FinOps Foundation](https://www.finops.org/framework/).
- **API/CLI behavior claims:** the official Azure REST API or Azure CLI reference
  page for that operation.
- If a claim has no citable canonical source, it does not go in this repository.
  Rewrite the claim to only state what the source actually says, or remove it.
- Do not cite a blog post, a third-party article, a forum answer, or your own
  inference as if it were the canonical source.
- `scripts/generate_citation_matrix.py` builds a traceability report from citations
  already in the docs. It is a downstream report, not the enforcement mechanism —
  the enforcement mechanism is you, at authoring time.

### 1.2 No operations, no best practices, no opinions

This repository describes Azure and Microsoft controls. It does not tell an ISV how
to run its team, program, or process. It has no opinions.

**Forbidden, always:**
- Recommended org structures, roles, staffing, or team topologies
- Review cadences, meeting rhythms, or approval workflows internal to the ISV
- "You should," "we recommend," "best practice is," "it's a good idea to"
- Decision frameworks, maturity models, or playbooks for how an ISV should operate
- Any prescriptive sequencing of the ISV's *internal* process

**Allowed:** cited, mechanical, step-by-step documentation of Microsoft's own
tools, APIs, and portal surfaces — for example, "run `az capacity reservation
group create` with these parameters, per [Learn](https://learn.microsoft.com/en-us/azure/virtual-machines/capacity-reservation-overview)."
That documents the product surface. It is not an opinion about how the ISV should
run its business.

**The litmus test:** If it reads like a runbook for how an ISV should run its team
or program, it fails. If it reads like a citation-backed description of what an
Azure control does and how to invoke it, it's fine.

### 1.3 Exemption: vendored upstream content

Content under `skills/vendor/**` that is listed in `skills/vendor/MANIFEST.md`'s
source-mapping table is unmodified, upstream Microsoft material from
[`microsoft/azure-skills`](https://github.com/microsoft/azure-skills) — tracked and
attributed via `MANIFEST.md`, not authored by this repository. It is exempt from
§§1.1–1.2's citation-per-claim and no-opinion rules, and from §4's scope boundaries
(for example, vendored `azure-cost` content in scope as vendored material even though
this repository's own authored docs stay narrowly focused on capacity — see §4). Never
edit a vendored file to bring it into compliance with this document; if it needs to
change, re-copy it from its source link in `MANIFEST.md` per the update procedure in
`skills/azure-capacity-management/SKILL.md`. This exemption applies only to files listed
in `MANIFEST.md`'s mapping table — it does not cover `MANIFEST.md` itself or any
repository-authored text (for example, `SKILL.md`'s routing table), which remain fully
governed by this document.

### 1.4 Verified, pinned dependencies

This repository's CI, scripts, and packaging execute third-party code. Every such
dependency is a supply chain entry point into anyone who clones or installs this
repository. GitHub's
[secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
is the canonical source for the mechanics below: "a compromise of a single action
within a workflow can be very significant, as that compromised action would have
access to all secrets configured on your repository, and may be able to use the
`GITHUB_TOKEN` to write to the repository."

- **No ad hoc package runners or piped installers in CI.** A workflow step must
  not fetch code and execute it in the same breath. `npx`, `bunx`, `uvx`,
  `pipx run`, `go run <url>`, `curl … | sh`, and `iwr … | iex` are all banned in
  `.github/**`. Use a checked-in script, a tool preinstalled on the runner, or an
  approved action instead. If a validator is only available through a package
  runner, reproduce the rules it enforces in a checked-in script and cover each
  with a test.
- **A runtime install is allowed only when it's version-pinned**, as
  `dotnet tool install --version` is in `docfx-gh-pages.yml`. Pinning doesn't make
  the fetch disappear; it makes the fetched artifact the same one that was
  reviewed. `@latest` and floating ranges let CI auto-execute releases nobody read.
- **Pin actions to a full-length commit SHA, never a tag, and keep the set small.**
  Per [Learn more](https://docs.github.com/en/actions/reference/security/secure-use#using-third-party-actions),
  pinning to a full-length commit SHA "is currently the only way to use an action as
  an immutable release," while "a tag can be moved or deleted if a bad actor gains
  access to the repository storing the action." The same page requires verifying the
  SHA "is from the action's repository and not a repository fork." Write
  `uses: owner/action@<40-char-sha> # v4`. Actions are allowed by publisher as well as
  by pin — adding one means adding it to the list in
  `.github/scripts/check-supply-chain.py`, which is a review decision. The same risks
  apply to reusable workflows sourced from other repositories.
- **Give every job an explicit `permissions:` block.** GitHub states it's "good
  security practice to set the default permission for the `GITHUB_TOKEN` to read
  access only for repository contents," raised per job only as required.
- **Set `persist-credentials: false` on checkout** unless a later step needs to run
  authenticated git commands. [`actions/checkout`](https://github.com/actions/checkout/tree/11d5960a326750d5838078e36cf38b85af677262#usage)
  persists the auth token in the local git config by default.
- **Don't check out untrusted code in a privileged context.** GitHub identifies
  `pull_request_target` and `workflow_run` combined with an untrusted checkout as
  triggers that "expose the repository to security compromises."
- Verify publisher identity **before** adding any package to CI, a script, or the
  docs — author, source repository, and publish history. A `0.x` release published
  under a personal email address is not first-party, however official its name and
  keywords look.
- Never describe a dependency as "first-party," "official," or "Microsoft" without a
  link that proves it. That's a factual claim, so [1.1](#11-no-fabrication--everything-links-to-a-canonical-source)
  applies to it in full.
- Do not inherit trust from an entry that's already here. A dependency present in the
  repository has not necessarily been vetted.

`.github/scripts/check-supply-chain.py` checks these mechanically, and
`.github/scripts/test-supply-chain.py` covers each rule with a case that must fail.
Both are tripwires that catch mistakes in review, not a root of trust — a pull
request can edit them. The controls that bind sit outside the pull request:
[branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches),
[CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
on `.github/**` — which GitHub recommends specifically so "any proposed changes to
these files will first require approval from a designated reviewer" — and the
repository or organization
[policy that requires actions to be pinned to a full-length commit SHA](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#managing-github-actions-permissions-for-your-repository).

`.github/CODEOWNERS` declares the owners. It requests review on its own, but only
becomes mandatory once a repository admin turns on "Require review from Code Owners"
for the default branch. Writing the rule down here doesn't enforce it; that setting
does.

This rule governs this repository's own automation.
[1.2](#12-no-operations-no-best-practices-no-opinions) constrains the subject-matter
content this repository publishes about Azure; it doesn't stop this document from
setting rules for contributions to this repository. The rule also doesn't reach
documentation that tells a reader how to install Microsoft's own tooling on their own
machine — for example, `Install-Module -Name Az` in a script's prerequisites.

## 2. Mission

This repository documents estate-level Azure quota, capacity, reservation,
monitoring, and billing controls for SaaS ISVs that operate workloads in
ISV-owned subscriptions (Enterprise Agreement or Microsoft Customer Agreement). It
is an addendum to the [ISV landing zone guidance](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/isv-landing-zone),
and it complements the [Azure Cloud Adoption Framework](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/),
[Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/),
and [FinOps Framework](https://www.finops.org/framework/). It does not replace any
of those sources — it maps Azure-specific evidence and mechanics onto their
concepts.

## 3. Audience and voice

The audience is ISV platform teams — engineers and operators who already know how
to run their own product and business. This is peer-to-peer, not vendor-to-customer:

- Write as one practitioner to another. Direct, succinct, neutral.
- Describe knobs, not operating models (see [1.2](#12-no-operations-no-best-practices-no-opinions)).
- Do not reference Microsoft field personas (SE, CSAM, CSA, account team, etc.). Azure
  self-service surfaces (portal, CLI, REST, support tickets) are the interface, not
  people.
- Never write for or about end customers of the ISV. The audience is the ISV itself,
  managing its own Azure estate.

## 4. Scope boundaries

**In scope:**
- Azure subscriptions owned or controlled by the ISV (EA or MCA), used to run the
  ISV's own workloads or multi-tenant SaaS platform
- Quota, region/zonal access, capacity reservations, quota groups, reservations,
  savings plans, monitoring/alerting, and governance as they relate to capacity
- Deployment stamps and scale units as capacity/quota consumers
- EA and MCA billing structures, only as they intersect capacity and quota

**Out of scope:**
- Customer-owned subscriptions (the ISV's customers' Azure tenants)
- Non-Azure clouds
- General cloud cost optimization or FinOps guidance unrelated to capacity or quota
- Security, compliance, or networking guidance not tied to capacity/quota mechanics
- Any ISV-internal process, org design, or best practice (see [1.2](#12-no-operations-no-best-practices-no-opinions))

## 5. Supply and demand framing

Content in this repository is organized around two sides of the same estate, tied
together by governance:

- **Demand side** — the ISV's own forecasting and planning: capacity planning,
  deployment stamps and scale units, forecast-ready usage data. This is the ISV's
  work; this repository only describes the Azure signals that feed it.
- **Supply side** — the Azure-controlled levers that convert a demand forecast into
  deployable, guaranteed capacity: region access, zonal enablement, per-subscription
  and pooled quota (quota groups), and capacity reservations (capacity reservation
  groups).
- **Closing the loop** — monitoring, quota alerts, budget/anomaly alerts, and
  governance gates that feed observed usage back into the next planning cycle.

Use this framing when organizing new content or explaining how a new page relates
to existing ones. Do not invent a different taxonomy — align to this one, or to the
[FinOps Framework](https://www.finops.org/framework/) domains it maps from.

## 6. Writing style

- **Sentence-style capitalization** in headings and titles — capitalize only proper
  nouns and product names. No title case.
- **Contractions are expected** — it's, don't, we're, isn't, can't.
- **Oxford commas** in all lists.
- **Strong, plain verbs** — use, remove, configure, create, delete. Avoid
  "utilize," "leverage," "provision," "spin up" where a plain verb works.
- **Prohibited words** (marketing language, imprecise, or filler): utilize,
  leverage, powerful, seamless, seamlessly, robust, simply, easily, effortlessly,
  cutting-edge, world-class, best-in-class, game-changing, revolutionize,
  unlock, empower, supercharge, delve, in order to, please note.
- **No superlatives or unverifiable claims** — every claim is either cited fact or
  it doesn't belong (see [1.1](#11-no-fabrication--everything-links-to-a-canonical-source)).
- Follow the [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/)
  for anything not covered above.

## 7. Terminology

`docs/operations/glossary.md` is the single source of truth for term definitions.
Do not redefine or restate terms elsewhere — link to the glossary entry instead.
When introducing a new term, add it to the glossary first, with its own citation,
before using it in other content.

## 8. Repository conventions

- `docs/` — Markdown documentation, organized by `docs/toc.yml`. Any new page must
  be added to the relevant `toc.yml` (root or folder-level) or it will not appear in
  the published site.
- `scripts/` — PowerShell and Python tools for quota, capacity, and rate analysis.
  Each script's directory has its own `README.md`.
- `agents/`, `skills/`, `sre-agent/` — packaging of this repository's content as an
  agent, skill, or SRE Agent plugin. These reference `docs/` and `scripts/` via
  symlinks or citations; they do not fork or restate the content.
- `done/` — completed task records for this repository's own build process, not
  end-user documentation.
- Run `python scripts/generate_citation_matrix.py` after adding or changing
  citations to refresh `docs/operations/support-and-reference/citation-matrix.md`.

## 9. Contribution checklist

Before considering any documentation change complete, confirm:

- [ ] Every factual claim has an inline citation to a canonical source
      ([1.1](#11-no-fabrication--everything-links-to-a-canonical-source)) — **except**
      files listed in `skills/vendor/MANIFEST.md`, which are exempt
      ([1.3](#13-exemption-vendored-upstream-content))
- [ ] No operational opinions, best practices, or runbooks
      ([1.2](#12-no-operations-no-best-practices-no-opinions)) — same vendored-content
      exemption applies
- [ ] Sentence-style capitalization used throughout, no title case
- [ ] No prohibited words ([Section 6](#6-writing-style))
- [ ] Terminology matches `docs/operations/glossary.md`; new terms added there first
- [ ] New pages added to the relevant `toc.yml`
- [ ] Citation matrix regenerated if citations changed
- [ ] Any new third-party dependency has a verified publisher and a pinned version,
      no workflow step fetches and executes code, and every action is pinned to a
      commit SHA ([1.4](#14-verified-pinned-dependencies)) — run
      `python3 .github/scripts/check-supply-chain.py`
