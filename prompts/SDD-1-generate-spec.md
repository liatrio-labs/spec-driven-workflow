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
4. **Clarifying Questions** - Gather detailed requirements through structured inquiry
5. **Spec Generation** - Create the detailed specification document
6. **Review and Refine** - Validate completeness and clarity with the user

## Step 1: Create Spec Directory

Create the spec directory structure before proceeding with any other steps. This ensures all files (questions, spec, tasks, proofs) have a consistent location.

**Directory Structure:**

- **Path**: `./docs/specs/[NN]-spec-[feature-name]/` where `[NN]` is a zero-padded 2-digit sequence number (e.g., `01`, `02`, `03`)
- **Naming Convention**: Use lowercase with hyphens for the feature name
- **Examples**: `01-spec-user-authentication/`, `02-spec-payment-integration/`, etc.

**Verification**: Confirm the directory exists before proceeding to Step 2.

## Step 2: Context Assessment

If working in a pre-existing project, conduct research to understand the codebase. This is the PRIMARY research phase - gather the context needed to generate a comprehensive, accurate spec that follows repository patterns.

**What to Understand:**

- **Project Spec Standards**: Understand the structure, detail level, and conventions used in specs for this project from:
  - Completed specs in `docs/specs/`
- **Architecture Patterns and Conventions**: Understand the system structure and design patterns from:
  - Project documentation (README.md, CONTRIBUTING.md, ARCHITECTURE.md, docs/)
  - AI-specific documentation (AGENTS.md, CLAUDE.md)
  - Existing code structure and module organization
- **Testing Standards and Practices**: Understand testing requirements and patterns from:
  - TESTING.md or testing documentation
  - Existing test files and test structure
  - Quality assurance practices
- **Repository Standards**: Understand coding standards and development practices from:
  - Configuration files (package.json, Cargo.toml, pyproject.toml, pom.xml, etc.)
  - Code naming conventions and file organization
  - Commit message conventions and development workflows
- **Related Implementations**: Search for existing code that implements similar operations, data models, or workflows

**Use this context to inform all aspects of the spec - scope, requirements, and technical approach. Follow the repository's established patterns and technical decisions rather than asking questions about them.**

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

## Step 4: Identify Information Gaps

Determine what additional information is needed to generate the spec beyond what was learned in Step 2. Use a two-phase approach: first identify what information is needed and check if Step 2 research already provided it, then ask the user only about genuine gaps.

### Phase A: Identify Information Gaps (REQUIRED)

Using ONLY the context gathered in Step 2 (do not do new research), determine what additional information is needed to generate the spec.

1. **Identify what information is needed** to write this spec:
   - How should this be tested?
   - What UI/UX patterns should be followed?
   - What technical approach should be used?
   - How should data be validated?
   - What error handling is needed?
   - What edge cases need to be handled?
   - What proof artifacts will demonstrate it works?

2. **Check if Step 2 research already answered these**:
   - If Step 2 provided ANY relevant information → consider it answered
   - Only mark as "needs user input" if Step 2 context provides ZERO guidance

3. **Identify genuine gaps**:
   - Business logic that cannot be inferred from existing patterns
   - Product decisions that require user choice
   - Novel functionality without precedent in the codebase

### Phase B: Create Questions File (If Needed)

After completing Phase A, create a questions file only if there is information that cannot be determined from Step 2 context.

**Only create questions for information that cannot be determined from context:**
- Business logic ambiguity (e.g., "What defines a duplicate?")
- Choices between valid technical approaches (e.g., "Cascade delete or block delete?")
- Novel functionality without precedent in the codebase
- Edge cases without established patterns

**Do NOT ask questions about:**
- Technical decisions already made by the repository (frameworks, tools, patterns)
- Testing approaches documented in TESTING.md or visible in existing tests
- UI/UX patterns that match existing implementations
- File structure and naming conventions that follow established patterns
- i18n support that already exists in the codebase

**Progressive Disclosure:** Focus on essential questions only. The number of questions will vary based on available context:
- **Mature codebases** (3+ completed specs, clear patterns): Aim for 0-5 questions, or skip questions entirely if all requirements are clear
- **New codebases** (limited context): May require 8-12 questions to establish requirements
- **Always prioritize**: Questions about business logic, product decisions, and novel functionality over technical implementation details

**If no questions are needed:** Skip directly to Step 5 (Spec Generation). Use the context gathered in Step 2 and Phase A to inform the spec.

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

### Questions File Process

1. **Create Questions File**: Save questions to a file named `[NN]-questions-[N]-[feature-name].md` where `[N]` is the round number (starting at 1, incrementing for each new round).
2. **Point User to File**: Direct the user to the questions file and instruct them to answer the questions directly in the file.
3. **STOP AND WAIT**: Do not proceed to Step 5. Wait for the user to indicate they have saved their answers.
4. **Read Answers**: After the user indicates they have saved their answers, read the file and continue the conversation.

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

## Step 6: Review and Refinement

After generating the spec, present it to the user and ask:

1. "Does this specification accurately capture your requirements?"
2. "Are there any missing details or unclear sections?"
3. "Are the scope boundaries appropriate?"
4. "Do the demoable units represent meaningful progress?"

Iterate based on feedback until the user is satisfied.

## Output Requirements

**Format:** Markdown (`.md`)
**Full Path:** `./docs/specs/[NN]-spec-[feature-name]/[NN]-spec-[feature-name].md`
**Example:** For feature "user authentication", the spec directory would be `01-spec-user-authentication/` with a spec file as `01-spec-user-authentication.md` inside it

## Critical Constraints

**NEVER:**

- Start implementing the spec; only create the specification document
- Ask questions about technical decisions already made by the repository (frameworks, tools, patterns)
- Create specs that are too large or too small without addressing scope issues
- Use jargon or technical terms that a junior developer wouldn't understand
- Skip context-based question resolution (Phase A) before asking questions
- Ask questions about things clearly answered by existing codebase patterns
- Ignore existing repository patterns and conventions

**ALWAYS:**

- Conduct thorough research in Step 2 to gather context before Step 4
- Use Step 2 context to determine requirements in Phase A (do not do new research in Step 4)
- Only create questions file if genuine user input is needed; skip to spec generation if all requirements are clear
- Validate scope appropriateness before proceeding
- Use the exact spec structure provided above
- Ensure the spec is understandable by a junior developer
- Include proof artifacts for each work unit that demonstrate what will be shown
- Follow identified repository standards and patterns in all requirements

## What Comes Next

Once this spec is complete and approved, instruct the user to run `/SDD-2-generate-task-list-from-spec`. This will start the next step in the workflow, which is to break down the specification into actionable tasks.
