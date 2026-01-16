## Technical Exercise — Data Extraction & JSONL Pipeline

**Duration:** ~45 minutes (live, working session)
**Format:** You can code in any language you’re comfortable with.
You may use official documentation, man pages, and CLI tools.
Please **talk through your thinking as you work**.

This exercise simulates a simplified version of real migration work: extracting data from an external system, transforming it into a stable format, and making it robust as requirements evolve.

---

### Context

We need to migrate issue data from GitHub into another system.
Your task is to build a small exporter that fetches issues from the GitHub REST API, normalizes them, and writes them as **JSON Lines (JSONL)**.

---

## Part 1 — Fetch and inspect (warm-up)

Using the GitHub REST API:

* Fetch issues from the repository:
  **`octocat/Hello-World`**
* Use the endpoint:
  `GET /repos/{owner}/{repo}/issues`
* Fetch a small page (for example, `per_page=10`).

**Task**

* Inspect the response.
* Identify which fields you’ll need.
* Normalize **3 issues** into the schema below and print them to stdout.

You do **not** need to write to a file yet.

---

## Part 2 — Normalize & write JSONL

Extend your solution to write output to a file called:

```
out.jsonl
```

### Output schema (one JSON object per line)

```json
{
  "external_id": 123456789,
  "number": 42,
  "title": "Issue title",
  "state": "open",
  "created_at": "2025-12-20T10:11:12Z",
  "author": "octocat",
  "labels": ["bug", "priority:high"],
  "url": "https://github.com/OWNER/REPO/issues/42"
}
```

### Rules

* Each line must be valid JSON (no surrounding array).
* Exclude pull requests (the issues endpoint includes PRs).
* `author` should be `null` if missing.
* `labels` should always be an array of strings.

---

## Part 3 — Scale it (pagination)

Now assume the repository has **many issues**.

**Task**

* Fetch **all issues**, not just the first page.
* Handle pagination using GitHub’s response headers.
* Write results incrementally to `out.jsonl`.

### Constraints

* Do **not** load all issues into memory.
* Your script should keep running even if there are many pages.
* Basic progress logging (counts) is encouraged.

---

## Part 4 — Small change in requirements (TODO)

Filtering:

* Exclude issues with the label `wontfix` (case-insensitive), or
* Only include issues created on or after a given date (`YYYY-MM-DD`).

Explain briefly how you chose to implement it.

---

??? Maybe show some logs, make him identify an issue?

---

## Communication

Throughout the exercise:

* Explain what you’re doing and why.
* If something is unclear, ask clarifying questions.
* If you make an assumption, call it out.

At the end, be ready to briefly explain:

* What your script does
* How it would behave with very large datasets
* What you would improve if this were production code

---

### Notes

* A `GITHUB_TOKEN` environment variable may be used if you want to avoid rate limits, but it is optional.
* This is **not** about finishing everything perfectly. We care more about your approach, tradeoffs, and communication than about polish.

---

**Let me know when you’re ready to start.**
