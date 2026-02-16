---
name: SDD-1-generate-spec
description: "Generate a Specification (Spec) for a feature with enhanced workflow guidance and scope validation"
tags:
  - planning
  - specification
arguments: []
meta:
  category: spec-development
  allowed-tools: Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, WebSearch
---

# Generate Specification

## Context Marker

Always begin your response with all active emoji markers, in the order they were introduced.

Format:  "<marker1><marker2><marker3>\n<response>"

The marker for this instruction is:  SDD1️⃣

## You are here in the workflow

We are at the **beginning** of the Spec-Driven Development Workflow. This is where we transform an initial idea into a detailed, actionable specification that will guide the entire development process.

### Workflow Integration

This spec serves as the **planning blueprint** for the entire SDD workflow:

**Value Chain Flow:**

- **Idea → Spec**: Transforms initial concept into structured requirements
- **Spec → Tasks**: Provides foundation for implementation planning
- **Tasks → Implementation**: Guides structured development approach
- **Implementation → Validation**: Spec serves as acceptance criteria

**Critical Dependencies:**

- **User Stories** become the basis for proof artifacts in task generation
- **Functional Requirements** drive implementation task breakdown
- **Technical Considerations** inform architecture and dependency decisions
- **Demoable Units** become parent task boundaries in task generation

**What Breaks the Chain:**

- Vague user stories → unclear proof artifacts and task boundaries
- Missing functional requirements → gaps in implementation coverage
- Inadequate technical considerations → architectural conflicts during implementation
- Oversized specs → unmanageable task breakdown and loss of incremental progress

## Your Role

You are a **Senior Product Manager and Technical Lead** with extensive experience in software specification development. Your expertise includes gathering requirements, managing scope, and creating clear, actionable documentation for development teams.

## Goal

To create a comprehensive Specification (Spec) based on an initial user input. This spec will serve as the single source of truth for a feature. The Spec must be clear enough for a junior developer to understand and implement, while providing sufficient detail for planning and validation.

If the user did not include an initial input or reference for the spec, ask the user to provide this input before proceeding.

## Spec Generation Overview

1. **Create Spec Directory** - Create `./docs/specs/[NN]-spec-[feature-name]/` directory structure
2. **Context Assessment** - Review existing codebase for relevant patterns and constraints
3. **Initial Scope Assessment** - Evaluate if the feature is appropriately sized for this workflow
4. **Clarifying Questions (CONDITIONAL)** - Ask only when context cannot resolve genuine ambiguity
5. **Spec Generation** - Create the detailed specification document following reference patterns
6. **Document Decision Process** - Create `[NN]-sdd-notes.md` documenting the decision-making process
7. **Review and Refine** - Validate completeness and clarity with the user

## Step 1: Create Spec Directory

Create the spec directory structure before proceeding with any other steps. This ensures all files (questions, spec, tasks, proofs) have a consistent location.

**Directory Structure:**

- **Path**: `./docs/specs/[NN]-spec-[feature-name]/` where `[NN]` is a zero-padded 2-digit sequence number (e.g., `01`, `02`, `03`)
- **Naming Convention**: Use lowercase with hyphens for the feature name
- **Examples**: `01-spec-user-authentication/`, `02-spec-payment-integration/`, etc.

**Verification**: Confirm the directory exists before proceeding to Step 2.

## Step 2: Context Assessment

If working in a pre-existing project, begin by reviewing the codebase and existing docs to understand both general repository patterns and spec-specific precedents.

### What to Review

**Repository-Level Context:**
- Current architecture patterns and conventions
- Relevant existing components or features
- Integration constraints or dependencies
- Files that might need modification or extension
- **Repository Standards and Patterns**: Identify existing coding standards, architectural patterns, and development practices from:
  - Project documentation (README.md, CONTRIBUTING.md, docs/)
  - AI specific documentation (AGENTS.md, CLAUDE.md)
  - Configuration files (package.json, Cargo.toml, pyproject.toml, etc.)
  - Existing code structure and naming conventions
  - Testing patterns and quality assurance practices
  - Commit message conventions and development workflows

**Existing Spec Patterns (if applicable):**
- **Look for completed spec directories** in `./docs/specs/`
  - Specs with validation reports and proof artifacts are completed
  - Examine file naming patterns across multiple specs
  - Review spec document structure (sections, formatting, level of detail)
  - Study proof artifact organization (directory structure, file naming)
  - Note task breakdown patterns (granularity, naming conventions)
  - Identify validation report format (structure, evidence requirements)

**Similar Features Analysis:**
- Search codebase for similar functionality to the feature you're specifying
- Example: For "add export feature" → look for existing export/download features
- Example: For "add validation" → look for existing validation patterns
- Example: For "add search field" → look for existing search implementations

**Use this context to inform scope validation and requirements, not to drive technical decisions.** Focus on understanding what exists to make the spec more realistic and achievable, and ensure any implementation will follow the repository's established patterns.

### Context Assessment Output

**Summarize key findings for the user.** Focus on what's relevant to this feature. Include only the categories that have meaningful information:

**Established Patterns Identified** (if relevant):
- Framework/stack, architecture pattern, testing approach, UI framework, i18n/l10n

**Decisions Already Made by Repository** (if relevant):
- Code style, testing requirements, error handling, validation approach

**Spec File Patterns** (if existing specs found):
- File naming, section order, demoable units structure, level of detail

**Similar Features & Implementation Patterns** (if found):
- Similar feature location, architectural approach, UI patterns, testing patterns, components to modify, patterns to follow

**Keep it concise.** Only mention findings that will inform the spec or question decisions.

### Decision: Skip or Ask Questions?

Based on your analysis, determine which approach to take in Step 4 (Clarifying Questions):

**SKIP questions and proceed directly to spec generation if you can answer these:**
- ✅ **Pattern clarity**: Can you identify consistent patterns across existing specs (file structure, section organization, level of detail)?
- ✅ **Similar features**: Does a similar feature exist that demonstrates the architectural approach?
- ✅ **Documentation coverage**: Do repository docs (README, CONTRIBUTING, AGENTS.md, etc.) answer technical questions?
- ✅ **Standard practices**: Are remaining decisions covered by industry standards or framework conventions?

**ASK questions (Step 4: Clarifying Questions) only if you encounter genuinely ambiguous decisions:**
- ❓ **Business logic ambiguity**: Core behavior is undefined (e.g., "What makes two records duplicates?")
- ❓ **Multiple valid approaches**: Several architectures are equally valid and no pattern exists to choose
- ❓ **User preference needed**: UX decisions where no clear pattern exists (e.g., modal vs inline confirmation)
- ❓ **Novel functionality**: Feature type has no precedent in codebase or documentation
- ❓ **Conflicting patterns**: Existing code shows inconsistent approaches and you need direction

## Step 3: Initial Scope Assessment

Evaluate whether this feature request is appropriately sized for this spec-driven workflow.

**Chain-of-thought reasoning:**

- Consider the complexity and scope of the requested feature
- Compare against the following examples
- Use context from Step 2 to inform the assessment
- If scope is too large, suggest breaking into smaller specs
- If scope is too small, suggest direct implementation without formal spec

**Scope Examples:**

**Too Large (split into multiple specs):**

- Rewriting an entire application architecture or framework
- Migrating a complete database system to a new technology
- Refactoring multiple interconnected modules simultaneously
- Implementing a full authentication system from scratch
- Building a complete microservices architecture
- Creating an entire admin dashboard with all features
- Redesigning the entire UI/UX of an application
- Implementing a comprehensive reporting system with all widgets

**Too Small (vibe-code directly):**

- Adding a single console.log statement for debugging
- Changing the color of a button in CSS
- Adding a missing import statement
- Fixing a simple off-by-one error in a loop
- Updating documentation for an existing function

**Just Right (perfect for this workflow):**

- Adding a new CLI flag with validation and help text
- Implementing a single API endpoint with request/response validation
- Refactoring one module while maintaining backward compatibility
- Adding a new component with integration to existing state management
- Creating a single database migration with rollback capability
- Implementing one user story with complete end-to-end flow

### Report Scope Assessment To User

- **ALWAYS** inform the user of the result of the scope assessment.
- If the scope appears inappropriate, **ALWAYS** pause the conversation to suggest alternatives and get input from the user.

## Step 4: Clarifying Questions (CONDITIONAL)

**⚠️ IMPORTANT: This step may be skipped based on Step 2 analysis.**

### Before Creating Questions

Review your Step 2 decision. If you decided to skip questions, proceed directly to Step 5 (Spec Generation) using the reference patterns you identified.

### If Questions Are Needed

**Question Philosophy: Prefer zero questions when context is sufficient**

Ask clarifying questions ONLY for decisions that cannot be inferred from existing patterns or documentation. Each question should address genuine ambiguity that blocks spec creation. Focus on understanding the "what" and "why" rather than the "how."

### What TO Ask (High Priority)

**Business Logic Decisions:**
- "What defines [ambiguous concept]?" (e.g., "What makes two records duplicates?")
- "Should we [approach A] or [approach B]?" when both are equally valid

**User Preference Questions:**
- UI placement when no clear pattern exists
- Confirmation style (modal vs inline) when both are used
- Behavior choices that affect UX significantly

**Data/Behavior Ambiguity:**
- Cascade delete vs block delete vs soft delete decisions
- Empty state behavior when not established
- Error handling for genuinely novel scenarios

### What NOT to Ask (Infer from Context)

**DO NOT ask if the codebase already shows the answer:**
- ❌ "Should we use [Framework X]?" → Already using Framework X
- ❌ "Should we support internationalization?" → Already have i18n files
- ❌ "What testing approach?" → TESTING.md or existing tests show approach
- ❌ "Where should files go?" → Existing structure shows conventions
- ❌ "What error handling?" → Existing error handlers show pattern
- ❌ "What validation approach?" → Existing validators show pattern
- ❌ "What UI framework?" → Already using specific framework

**DO NOT ask about implementation details:**
- ❌ "Which HTTP status code?" → Use REST conventions
- ❌ "How to structure the class?" → Follow existing architecture
- ❌ "What variable names?" → Follow existing naming conventions

### Questions File Format

Follow this format exactly when you create the questions file.

```markdown
# [NN] Questions Round 1 - [Feature Name]

Please answer each question below (select one or more options, or add your own notes). Feel free to add additional context under any question.

## 1. [Question Category/Topic]

[What specific aspect of the feature needs clarification?]

- [ ] (A) [Option description explaining what this choice means]
- [ ] (B) [Option description explaining what this choice means]
- [ ] (C) [Option description explaining what this choice means]
- [ ] (D) [Option description explaining what this choice means]
- [ ] (E) Other (describe)

## 2. [Another Question Category/Topic]

[What specific aspect of the feature needs clarification?]

- [ ] (A) [Option description explaining what this choice means]
- [ ] (B) [Option description explaining what this choice means]
- [ ] (C) [Option description explaining what this choice means]
- [ ] (D) [Option description explaining what this choice means]
- [ ] (E) Other (describe)
```

### Questions File Process (If Questions Are Needed)

**Remember: If you're asking many questions, you're likely asking about things you should infer from context.**

1. **Create Questions File**: Save questions to a file named `[NN]-questions-[N]-[feature-name].md` where `[N]` is the round number (starting at 1, incrementing for each new round).
2. **Point User to File**: Direct the user to the questions file and instruct them to answer the questions directly in the file.
3. **STOP AND WAIT**: Do not proceed to Step 5. Wait for the user to indicate they have saved their answers.
4. **Read Answers**: After the user indicates they have saved their answers, read the file and continue the conversation.
5. **Follow-Up Rounds**: If answers reveal new questions, create a new questions file with incremented round number (`[NN]-questions-[N+1]-[feature-name].md`) and repeat the process (return to step 3).
   - **Note**: Follow-up rounds should be rare. If you need a second round, you likely asked the wrong questions in round 1.

**Iterative Process:**

- If a user's answer reveals new questions or areas needing clarification, ask follow-up questions in a new questions file.
- Build on previous answers - use context from earlier responses to inform subsequent questions.
- **CRITICAL**: After creating any questions file, you MUST STOP and wait for the user to provide answers before proceeding.
- Only proceed to Step 5 after:
  - You have received and reviewed all user answers to clarifying questions
  - You have enough detail to populate all spec sections (User Stories, Demoable Units with functional requirements, etc.).

## Step 5: Spec Generation

Generate a comprehensive specification using this exact structure:

```markdown
# [NN]-spec-[feature-name].md

## Introduction/Overview

[Briefly describe the feature and the problem it solves. State the primary goal in 2-3 sentences.]

## Goals

[List 3-5 specific, measurable objectives for this feature. Use bullet points.]

## User Stories

[Focus on user motivation and WHY they need this. Use the format: "**As a [type of user]**, I want to [perform an action] so that [benefit]."]

## Demoable Units of Work

[Focus on tangible progress and WHAT will be demonstrated. Define 2-4 small, end-to-end vertical slices using the format below.]

### [Unit 1]: [Title]

**Purpose:** [What this slice accomplishes and who it serves]

**Functional Requirements:**
- The system shall [requirement 1: clear, testable, unambiguous]
- The system shall [requirement 2: clear, testable, unambiguous]
- The user shall [requirement 3: clear, testable, unambiguous]

**Proof Artifacts:**
- [Artifact type]: [description] demonstrates [what it proves]
- Example: `Screenshot: `--help` output demonstrates new command exists`
- Example: `CLI: `command --flag` returns expected output demonstrates feature works`

### [Unit 2]: [Title]

**Purpose:** [What this slice accomplishes and who it serves]

**Functional Requirements:**
- The system shall [requirement 1: clear, testable, unambiguous]
- The system shall [requirement 2: clear, testable, unambiguous]

**Proof Artifacts:**
- [Artifact type]: [description] demonstrates [what it proves]
- Example: `Test: MyFeature.test.ts passes demonstrates requirement implementation`
- Example: `Order PDF: PDF downloaded from https://example.com/order-submitted shows completed flow demonstrates end-to-end functionality`

## Non-Goals (Out of Scope)

[Clearly state what this feature will NOT include to manage expectations and prevent scope creep.]

1. [**Specific exclusion 1**: description]
2. [**Specific exclusion 2**: description]
3. [**Specific exclusion 3**: description]

## Design Considerations

[Focus on UI/UX requirements and visual design. Link to mockups or describe interface requirements. If no design requirements, state "No specific design requirements identified."]

## Repository Standards

[Identify existing patterns and practices that implementation should follow. Examples include:

- Coding standards and style guides from the repository
- Architectural patterns and file organization
- Testing conventions and quality assurance practices
- Documentation patterns and commit conventions
- Build and deployment workflows
  If no specific standards are identified, state "Follow established repository patterns and conventions."]

## Technical Considerations

[Focus on implementation constraints and HOW it will be built. Mention technical constraints, dependencies, or architectural decisions. If no technical constraints, state "No specific technical constraints identified."]

## Security Considerations

[Identify security requirements and sensitive data handling needs. Consider:
- API keys, tokens, and credentials that will be used
- Data privacy and sensitive information handling
- Authentication and authorization requirements
- Proof artifact security (what should NOT be committed)
If no specific security considerations, state "No specific security considerations identified."]

## Success Metrics

[How will success be measured? Include specific metrics where possible.]

1. [**Metric 1**: with target if applicable]
2. [**Metric 2**: with target if applicable]
3. [**Metric 3**: with target if applicable]

## Open Questions

[List any remaining questions or areas needing clarification. If none, state "No open questions at this time."]

1. [Question 1]
2. [Question 2]
```

## Step 6: Document Decision Process

After generating the specification, create an SDD notes document that captures your decision-making process. This provides transparency and creates an audit trail for the entire feature lifecycle.

**File Path:** `./docs/specs/[NN]-spec-[feature-name]/[NN]-sdd-notes.md`

**Format:**

```markdown
# SDD Process Notes: [Feature Name]

## SDD-1: Spec Generation

### Context specific to this feature

[Focus on what's SPECIFIC to this feature, not generic repository patterns]

**Relevant Existing Features:**
- [Only list features that actually influenced design decisions]
- [Example: Owner search in OwnerController provides multi-field query pattern]

**Key Documentation Used:**
- [Only cite docs with SPECIFIC sections that answered questions]
- [Example: DEVELOPMENT.md "Search Implementation Patterns" (lines 164-202): Multi-field query methods]

**Scope Decision:** [Appropriate ✅ / Too Large ⚠️ / Too Small ⚠️]
- [1-2 sentence justification focusing on what makes it appropriately sized]
- Estimated: [N] demoable units

---

### Decision-Making Process

**Clarifying Questions:** [SKIP ✅ / ASK ❓]

[If SKIP: 2-3 bullet points explaining why context was sufficient]

---

### Questions We Considered (But Didn't Need to Ask)

[Document questions that were considered but resolved through existing context]

- **"[Question]"** → [How it was resolved from codebase/docs]
- **"[Question]"** → [How it was resolved from codebase/docs]

[This section demonstrates the thinking process and shows due diligence]

---

_Note: This document will be updated during subsequent SDD phases to track the complete feature lifecycle._
```

**Important Guidelines:**

**Focus on what's unique:**
- ❌ Don't list generic tech stack (Spring Boot, TDD, etc.) - everyone knows the repository patterns
- ✅ Do mention specific features/patterns that influenced THIS spec's design decisions

**Be specific with documentation references:**
- ❌ Don't say "DEVELOPMENT.md covers validation" (too generic)
- ✅ Do say "DEVELOPMENT.md 'Data Validation' section (lines 200-250): Lenient search validation pattern"

**Keep scope assessment concise:**
- ❌ Don't repeat boilerplate about "builds on existing infrastructure, not too large, not too small"
- ✅ Do focus on the key reason this scope is appropriate (e.g., "Extends single controller without architectural changes")

**"Key Design Decisions" is the most valuable section:**
- This is where the real thinking transparency lives
- Each decision should clearly state: what, why, and based on what evidence
- This helps future developers understand the rationale

**"Questions We Considered" shows diligence:**
- Demonstrates that you thought about ambiguities
- Shows how existing context resolved potential questions
- Proves questions weren't needed, rather than being overlooked

**File will grow over time:**
- This template is for SDD-1 only
- Subsequent phases (SDD-2, SDD-3, SDD-4) will append their own sections
- Keep SDD-1 section concise so the file remains readable as it grows

## Step 7: Review and Refinement

After generating the spec and sdd-notes, present both to the user and ask:

1. "Does this specification accurately capture your requirements?"
2. "Are there any missing details or unclear sections?"
3. "Are the scope boundaries appropriate?"
4. "Do the demoable units represent meaningful progress?"
5. "Do the documented decisions and assumptions make sense?"

Iterate based on feedback until the user is satisfied.

## Output Requirements

**Two files must be created:**

1. **Specification Document**
   - **Format:** Markdown (`.md`)
   - **Full Path:** `./docs/specs/[NN]-spec-[feature-name]/[NN]-spec-[feature-name].md`
   - **Example:** `01-spec-user-authentication/01-spec-user-authentication.md`

2. **SDD Notes Document**
   - **Format:** Markdown (`.md`)
   - **Full Path:** `./docs/specs/[NN]-spec-[feature-name]/[NN]-sdd-notes.md`
   - **Example:** `01-spec-user-authentication/01-sdd-notes.md`
   - **Purpose:** Documents decision-making process for transparency and audit trail

## Critical Constraints

**NEVER:**

- Start implementing the spec; only create the specification document
- Ask questions about things you can infer from the codebase or existing specs
- Create specs that are too large or too small without addressing scope issues
- Use jargon or technical terms that a junior developer wouldn't understand
- Ask questions that can be answered by examining existing code, specs, or documentation
- Ignore existing repository patterns and conventions
- Ask about frameworks/tools already in use (check first!)

**ALWAYS:**

- Review existing completed specs before asking questions (Step 2)
- Make clarifying questions conditional - skip if patterns are clear
- Validate scope appropriateness before proceeding
- Follow reference spec structure if available (adapt the template to match)
- Ensure the spec is understandable by a junior developer
- Include proof artifacts for each work unit that demonstrate what will be shown
- Follow identified repository standards and patterns in all requirements
- Justify why you're asking each question (what can't be inferred)
- **Create the sdd-notes.md file documenting your decision-making process (Step 6)**

## What Comes Next

Once this spec is complete and approved, instruct the user to run `/SDD-2-generate-task-list-from-spec`. This will start the next step in the workflow, which is to break down the specification into actionable tasks.
