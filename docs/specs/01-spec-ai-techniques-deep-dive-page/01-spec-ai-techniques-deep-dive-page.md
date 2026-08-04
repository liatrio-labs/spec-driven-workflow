# 01-spec-ai-techniques-deep-dive-page.md

## Introduction/Overview

Create a new deep-dive documentation page for the docs site that teaches the eight AI techniques already introduced on `docs/ai-techniques.html` in a much more substantial, beginner-friendly way. The page should position these techniques as core primitives of AI-native development, similar to how control flow, data structures, and functions act as primitives in software development, while grounding the explanation in concrete SDD examples rather than abstract theory.

## Goals

- Publish a dedicated deep-dive page that gives readers enough context to understand, compare, and internalize each AI technique beyond a one-sentence summary.
- Introduce the "AI-native primitives" framing in a way that feels current, credible, and aligned with modern agent, context engineering, and eval-driven development guidance.
- Connect each technique to specific SDD workflow behavior across `SDD-1` through `SDD-4` using concrete examples from the prompts and existing docs artifacts.
- Preserve the docs site's current visual language and educational tone while clearly differentiating the deep-dive page from the existing overview page.
- Keep the content reusable for readers who want to borrow these patterns outside of full SDD adoption.

## User Stories

- **As a software engineer who is new to AI-native development**, I want a deeper explanation of each technique so that I can understand what the technique is, why it matters, and how to recognize it in practice.
- **As an engineering lead evaluating SDD**, I want the site to explain the underlying primitives behind the workflow so that I can see the method as a teachable operating model rather than a collection of prompts.
- **As a practitioner already using SDD**, I want concrete prompt-level and artifact-level examples so that I can reuse these patterns in adjacent AI workflows.
- **As a reader coming from the existing AI Techniques page**, I want a clear path into a more detailed reference so that I can continue learning without losing the high-level overview.

## Demoable Units of Work

### Unit 1: Establish the deep-dive page and primitives framing

**Purpose:** Create the new page shell, introduce the "AI-native primitives" concept, and explain why these techniques matter in modern AI-native development.

**Functional Requirements:**

- The system shall create a new standalone docs page for the AI techniques deep dive under the existing docs site structure.
- The system shall introduce the idea that these techniques are foundational primitives of AI-native development without claiming they are the only valid primitives in the field.
- The system shall explain the analogy between software-development primitives and AI-native-development primitives in plain language that a junior developer can understand.
- The system shall frame the page as an educational companion to the existing `docs/ai-techniques.html` overview page.

**Proof Artifacts:**

- Screenshot: Deep-dive page hero and opening section demonstrates the new page exists and introduces the primitives framing.
- HTML source: New page file demonstrates the page was added to the docs site with the required introductory structure.

### Unit 2: Add substantial deep-dive sections for each technique

**Purpose:** Give each AI technique enough content to help readers understand and digest the concept through definitions, significance, SDD usage, and examples.

**Functional Requirements:**

- The system shall include a dedicated subsection for each of the eight techniques already presented on the overview page.
- The system shall explain each technique using a consistent structure that includes what it is, why it matters, how SDD uses it, at least one concrete SDD-related example, and one or more examples drawn from software development or AI-assisted engineering more broadly.
- The system shall include enough explanatory content for readers who are unfamiliar with agent or context engineering concepts, rather than relying on short blurbs alone.
- The system shall use multiple examples per technique so the concept feels approachable in both the specific SDD workflow and general software-development practice.
- The system shall avoid hidden chain-of-thought framing and instead describe observable workflow patterns, reasoning protocols, or validation practices.

**Proof Artifacts:**

- Screenshot: One or more technique sections demonstrates the repeated deep-dive teaching structure is present and readable.
- HTML source: Technique section markup demonstrates all eight techniques are represented with substantial content.

### Unit 3: Connect the techniques to SDD workflow behavior and real artifacts

**Purpose:** Make the page practical by showing where each primitive appears in `SDD-1` through `SDD-4` and by pointing readers to real SDD examples.

**Functional Requirements:**

- The system shall map each technique to the relevant SDD prompts or workflow stages.
- The system shall include SDD-specific examples drawn from the workflow, prompt behavior, or existing reference materials so the page stays grounded in real usage.
- The system shall include at least one section that explains what readers can borrow from these primitives even if they do not adopt the full SDD workflow.
- The system shall connect readers to existing docs resources such as `docs/ai-techniques.html`, `docs/reference-materials.html`, prompt links, or related docs pages.

**Proof Artifacts:**

- Screenshot: Workflow mapping or cross-link section demonstrates the page connects the techniques to SDD prompts and reference materials.
- URL/HTML: Navigation or CTA links demonstrate the deep-dive page is integrated into the broader docs experience.

### Unit 4: Integrate the page into the docs site experience

**Purpose:** Make the new page discoverable and visually coherent with the rest of the docs site.

**Functional Requirements:**

- The system shall add a discoverable path from the existing AI Techniques overview page to the new deep-dive page.
- The system shall integrate the new page into the site navigation, reference flow, or both, using existing site conventions.
- The system shall provide section layouts, spacing, and background treatments that stay consistent with the current site visual language while distinguishing the deep-dive page from overview content.
- The system shall work on both desktop and mobile layouts using the site's existing responsive patterns.

**Proof Artifacts:**

- Screenshot: Navigation and CTA states demonstrate the deep-dive page is discoverable from the existing docs flow.
- Screenshot: Mobile or narrow-layout rendering demonstrates the new page remains readable and visually coherent on smaller screens.

## Non-Goals (Out of Scope)

1. **Rewriting the existing AI Techniques overview page from scratch**: The current overview page should remain the concise entry point; this work adds a deeper companion resource.
2. **Turning the page into a vendor-agnostic academic survey of all agent design patterns**: The page should stay centered on the eight techniques already introduced through SDD and their role in Liatrio's workflow.
3. **Changing the core SDD workflow or prompt behavior**: This work explains and teaches the existing workflow; it does not modify the prompts or redefine the operational steps.
4. **Focusing too much on responsive fidelity:** There are known issues with the mobile version of the site; do not attempt to remedy issues with the mobile view as part of this spec.

## Design Considerations

The page should feel like a teaching-oriented companion to `docs/ai-techniques.html`, not a copy of that page with more words. It should preserve the existing site style: dark surfaces, accent green, layered section backgrounds, strong section headers, and responsive card or content-block layouts. The visual hierarchy should help readers digest long-form content through scannable subsections, repeated patterns, and clear transitions between overview, explanation, examples, and cross-links.

## Repository Standards

- Follow the existing static-site structure in `docs/` with standalone HTML pages, shared site styling in `docs/assets/css/styles.css`, and shared navigation behavior in `docs/assets/js/navigation.js`.
- Preserve the site's current voice: transparent, learnable, tool-agnostic, repo-native, and evidence-oriented.
- Reuse established docs patterns already visible in `docs/ai-techniques.html`, `docs/index.html`, and `docs/reference-materials.html`, including section headers, CTA blocks, card grids, and themed background treatments.
- Keep content and labels junior-friendly, avoiding unnecessary jargon or unexplained specialist terminology.
- Maintain the repository's responsive layout conventions and existing visual language instead of introducing a separate design system.

## Technical Considerations

- Create the page as a docs-site HTML page rather than an external asset or embedded document so it stays consistent with the current site architecture.
- Consider naming and placement that supports the educational flow. A likely pattern is a new page linked from `docs/ai-techniques.html` and referenced from `docs/reference-materials.html`, but the exact page name may remain an editorial decision.
- Current external guidance supports the page's framing around simple, composable patterns:
  - Anthropic's "Building effective agents" (published Dec 19, 2024) emphasizes simple, composable patterns, transparency, tool clarity, and explicit planning steps over heavy abstraction.
  - Anthropic's "Effective context engineering for AI agents" (published Sep 29, 2025) frames modern AI engineering as context engineering rather than prompt wording alone, and highlights progressive disclosure, just-in-time context retrieval, externalized notes/state, and long-horizon context management.
  - OpenAI's structured outputs guidance recommends explicit schemas and predictable output structures instead of brittle formatting prompts.
  - OpenAI's reasoning and evaluation guidance recommends simple direct prompts, clear success criteria, and eval-driven development rather than vibe-based validation.
- The page should align with that modern thinking by emphasizing practical primitives such as structured outputs, context curation, explicit checkpoints, and evidence-based validation rather than treating prompt phrasing as the main skill.
- The page should avoid overstating the claim. Current public framing should treat these techniques as **core** or **foundational** primitives used by SDD, not as an exhaustive or universally agreed-on taxonomy for all AI-native development.
- If the implementation uses examples from prompt files or reference artifacts, prefer concise excerpts or summarized examples over dumping long prompt quotations into the page.

## Security Considerations

- No new credentials, tokens, or secret-handling flows are expected for this feature.
- Any examples drawn from reference materials or prompt content shall avoid exposing sensitive data or implying that proof artifacts should contain real secrets.
- Outbound links to external sources or prompt files shall use the same safe linking patterns already established in the docs site.

## Success Metrics

1. **Coverage**: All eight techniques receive their own substantial deep-dive treatment on the new page.
2. **Discoverability**: Readers can navigate from the existing overview page or related docs pages to the new deep-dive page in one click.
3. **Educational clarity**: The page explains the primitives framing, the role of each technique, and multiple concrete examples per technique, including at least one SDD-specific example and one broader software-development example, without requiring prior familiarity with agent-engineering jargon.

## Open Questions

1. What final public-facing page name should be used: a direct deep-dive label (for example, `AI Techniques Deep Dive`) or a stronger framing around `AI-Native Development Primitives`?
   1. AI-Native Development Primitives
2. Should the new page live as a top-level docs page in navigation, be presented as part of `Reference Materials`, or be both navigable directly and framed as a reference companion?
   1. be both navigable directly and framed as a reference companion - we'll try this first
3. How strongly should the page distinguish between "core primitives used in SDD" and "broader AI-native development patterns" in its headline and section copy?
   1. I'd like it to be framed as "broader AI-native development patterns" that power SDD and other AI-native development
