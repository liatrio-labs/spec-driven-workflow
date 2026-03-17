## Relevant Files

- `docs/ai-native-development-primitives.html` - New deep-dive page for the long-form teaching content and workflow examples.
- `docs/ai-techniques.html` - Existing overview page that should link readers into the deeper companion resource.
- `docs/reference-materials.html` - Reference-oriented page that should frame the new page as a companion for studying real SDD artifacts.
- `docs/assets/js/navigation.js` - Shared site navigation; add the new page as a top-level destination.
- `docs/assets/css/styles.css` - Shared styling for new page sections, layouts, and page-specific visual treatments.

### Notes

- This repository uses standalone HTML pages in `docs/` with shared CSS and JavaScript rather than a framework router.
- Run `pre-commit run --all-files` to satisfy markdown, YAML, and secret-scanning quality gates before handoff.
- Follow the site's existing visual language and content patterns instead of introducing a new design system.

## Tasks

### [x] 1.0 Create the deep-dive page scaffold and primitives framing

#### 1.0 Proof Artifact(s)

- URL: `/ai-native-development-primitives.html` loads in the docs site and demonstrates the new page exists as a standalone destination
- Screenshot: hero and opening section of `/ai-native-development-primitives.html` demonstrates the "AI-native development primitives" framing and the analogy to software-development primitives
- HTML: `docs/ai-native-development-primitives.html` contains the page title, companion framing to `ai-techniques.html`, and the introductory sections that establish purpose and audience

#### 1.0 Tasks

- [x] 1.1 Finalize the public-facing page name, file path, and navigation label using the spec answers (`AI-Native Development Primitives`) so implementation uses one consistent label everywhere.
- [x] 1.2 Create `docs/ai-native-development-primitives.html` with the shared site shell (`head`, injected navigation/footer, shared assets, and page title metadata) to match the docs-site architecture.
- [x] 1.3 Build the opening sections that explain the "AI-native development primitives" framing, relate it to software-development primitives, and position the page as the deeper companion to `docs/ai-techniques.html`.
- [x] 1.4 Add an orientation section that explains how readers should use the page: learn the concepts, study SDD-specific examples, and reuse the patterns outside full SDD adoption.

### [x] 2.0 Add deep-dive teaching sections for all eight techniques

#### 2.0 Proof Artifact(s)

- Screenshot: representative technique sections on `/ai-native-development-primitives.html` demonstrate the repeated teaching structure is present and readable
- HTML: `docs/ai-native-development-primitives.html` contains all eight technique headings with content for what the technique is, why it matters, how SDD uses it, one SDD-specific example, and one broader software-development or AI-assisted engineering example per technique
- Diff: page content changes in `docs/ai-native-development-primitives.html` demonstrate that the deep-dive material substantially expands beyond the overview page blurbs

#### 2.0 Tasks

- [x] 2.1 Define a reusable section pattern for each technique that covers what it is, why it matters, how SDD uses it, one SDD-specific example, and one broader software-development or AI-assisted engineering example.
- [x] 2.2 Write deep-dive sections for Task Decomposition, Progressive Disclosure, Structured Outputs, and Serialized External State using the agreed teaching pattern and concrete examples.
- [x] 2.3 Write deep-dive sections for Dynamic Context Injection, Human / Resumable Checkpoints, Evidence-Based Validation, and Reasoning Protocols using the same teaching pattern and concrete examples.
- [x] 2.4 Review all eight sections for consistency, beginner-friendly wording, and balanced use of SDD-specific versus broader engineering examples.

### [ ] 3.0 Connect the techniques to workflow behavior and reusable practice

#### 3.0 Proof Artifact(s)

- Screenshot: workflow-mapping section on `/ai-native-development-primitives.html` demonstrates how the primitives connect to `SDD-1` through `SDD-4`
- Screenshot: "borrow these patterns" or equivalent section demonstrates the page explains how readers can apply the primitives outside the full SDD workflow
- HTML: `docs/ai-native-development-primitives.html` includes links or references to `ai-techniques.html`, `reference-materials.html`, prompts, or other related docs resources that ground the page in real SDD artifacts

#### 3.0 Tasks

- [ ] 3.1 Add a section that maps the eight primitives to `SDD-1` through `SDD-4`, making it clear that these are broader AI-native development patterns that power SDD and other workflows.
- [ ] 3.2 Add sections that connect the page back to real SDD artifacts and prompt behavior, including concise references to the existing overview page, reference materials, and relevant prompt resources.
- [ ] 3.3 Add a practical reuse section that explains which primitives teams can borrow independently, with examples outside the exact SDD workflow.
- [ ] 3.4 Verify that the page avoids hidden chain-of-thought framing and instead describes observable workflow behaviors, checkpoints, and evidence patterns.

### [ ] 4.0 Integrate the page into the docs experience and visual system

#### 4.0 Proof Artifact(s)

- Screenshot: site navigation with the new page linked and active demonstrates the page is discoverable from the broader docs experience
- Screenshot: existing overview or reference pages showing CTA links to `/ai-native-development-primitives.html` demonstrates cross-page integration
- Diff: `docs/assets/js/navigation.js`, `docs/assets/css/styles.css`, and linked docs pages demonstrate the new page is wired into navigation, shared styling, and reference flow
- Screenshot: narrow-width rendering of `/ai-native-development-primitives.html` demonstrates the page follows existing responsive patterns without expanding scope into a general mobile-site fix

#### 4.0 Tasks

- [ ] 4.1 Add the new page to `docs/assets/js/navigation.js` and update `docs/ai-techniques.html` so readers can move from the overview page into the deep-dive companion.
- [ ] 4.2 Update `docs/reference-materials.html` to frame the new page as a reference companion for studying how the primitives appear in a real SDD run.
- [ ] 4.3 Add or extend shared styles in `docs/assets/css/styles.css` for the deep-dive page sections, ensuring the new page feels distinct from the overview page while staying within the site's visual system.
- [ ] 4.4 Verify the new page and its entry points on desktop and narrow-width layouts, focusing on the new page's readability and navigation flow without expanding scope into a broader mobile-site remediation effort.
