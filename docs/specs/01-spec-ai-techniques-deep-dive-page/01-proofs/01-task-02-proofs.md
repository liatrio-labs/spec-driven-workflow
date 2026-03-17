# Task 02 Proofs - Deep-dive sections for all eight primitives

## Task Summary

This task adds the core teaching content to the new page. Each of the eight AI-native development primitives now has a
dedicated deep-dive section covering what the primitive is, why it matters, how SDD uses it, one SDD-specific example,
and broader software-development examples.

## What This Task Proves

- The page now includes a substantial section for all eight primitives introduced by the overview page.
- The repeated teaching structure is consistent across the page.
- Each primitive includes both SDD-specific and broader engineering examples so the concepts are easier to generalize.

## Evidence Summary

- The page source contains exactly eight `primitive-detail-card` sections.
- All eight primitive headings are present in the HTML file.
- The full-page screenshot shows the new deep-dive section rendered as part of the docs page.

## Artifact: Primitive section coverage check

**What it proves:** The page contains all eight expected primitive sections.

**Why it matters:** The task is incomplete if even one primitive is missing or if the page only partially expands the
overview content.

**Command:**

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('docs/ai-native-development-primitives.html').read_text()
print('primitive_detail_cards=', text.count('<article class="primitive-detail-card">'))
for heading in [
    'Task Decomposition',
    'Progressive Disclosure',
    'Structured Outputs',
    'Serialized External State',
    'Dynamic Context Injection',
    'Human / Resumable Checkpoints',
    'Evidence-Based Validation',
    'Reasoning Protocols',
]:
    print(f'{heading}:', heading in text)
PY
```

**Result summary:** The coverage check found eight primitive cards, and every expected heading returned `True`.

```text
primitive_detail_cards= 8
Task Decomposition: True
Progressive Disclosure: True
Structured Outputs: True
Serialized External State: True
Dynamic Context Injection: True
Human / Resumable Checkpoints: True
Evidence-Based Validation: True
Reasoning Protocols: True
```

## Artifact: Repeated deep-dive structure in page source

**What it proves:** The HTML file includes the expected section heading and repeated cards with broader-example blocks.

**Why it matters:** This verifies the task added a consistent teaching pattern rather than a collection of unrelated
paragraphs.

**Command:**

```bash
grep -n "The Eight Primitives in Depth\|primitive-detail-card\|Broader examples" "docs/ai-native-development-primitives.html"
```

**Result summary:** The output shows the section heading plus repeated `primitive-detail-card` and `Broader examples`
markers throughout the file, confirming the shared structure is present.

```text
93:                <h2 class="section-title">The Eight Primitives in Depth</h2>
98:                    <article class="primitive-detail-card">
117:                        <h4>Broader examples</h4>
126:                    <article class="primitive-detail-card">
141:                        <h4>Broader examples</h4>
150:                    <article class="primitive-detail-card">
165:                        <h4>Broader examples</h4>
174:                    <article class="primitive-detail-card">
191:                        <h4>Broader examples</h4>
200:                    <article class="primitive-detail-card">
216:                        <h4>Broader examples</h4>
225:                    <article class="primitive-detail-card">
241:                        <h4>Broader examples</h4>
250:                    <article class="primitive-detail-card">
265:                        <h4>Broader examples</h4>
274:                    <article class="primitive-detail-card">
292:                        <h4>Broader examples</h4>
```

## Artifact: Rendered deep-dive page with technique sections

**What it proves:** The new deep-dive sections render in the page and are available for human review.

**Why it matters:** The feature is meant to teach readers, so the rendered page matters as much as the raw source.

**Artifact path:** `docs/specs/01-spec-ai-techniques-deep-dive-page/01-proofs/01-task-02-techniques.png`

**Result summary:** The full-page screenshot shows the new deep-dive section extending the initial scaffold with all
eight primitive cards and their explanatory content.

![Full-page screenshot showing the rendered primitive deep-dive sections](01-task-02-techniques.png)

## Reviewer Conclusion

These artifacts show that the page has moved beyond a scaffold: it now contains complete deep-dive content for all
eight primitives, with a consistent educational pattern and examples that connect SDD to broader engineering practice.
