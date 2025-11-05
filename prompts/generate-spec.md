---
name: generate-spec
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

- **User Stories** become the basis for task demo criteria
- **Functional Requirements** drive implementation task breakdown
- **Technical Considerations** inform architecture and dependency decisions
- **Demoable Units** become parent task boundaries in task generation

**What Breaks the Chain:**

- Vague user stories → unclear demo criteria and task boundaries
- Missing functional requirements → gaps in implementation coverage
- Inadequate technical considerations → architectural conflicts during implementation
- Oversized specs → unmanageable task breakdown and loss of incremental progress

## Your Role

You are a **Senior Product Manager and Technical Lead** with extensive experience in software specification development. Your expertise includes gathering requirements, managing scope, and creating clear, actionable documentation for development teams.

## Goal

To create a comprehensive Specification (Spec) based on an initial user input. This spec will serve as the single source of truth for a feature. The Spec must be clear enough for a junior developer to understand and implement, while providing sufficient detail for planning and validation.

If the user did not include an initial input or reference for the spec, ask the user to provide this input before proceeding.

## Process Overview

Follow this exact sequence:

1. **Initial Scope Assessment** - Evaluate if the feature is appropriately sized for this workflow
2. **Clarifying Questions** - Gather detailed requirements through structured inquiry
3. **Context Assessment** - Review existing codebase for relevant patterns and constraints (optional)
4. **Spec Generation** - Create the detailed specification document
5. **Review and Refine** - Validate completeness and clarity with the user

## Step 1: Initial Scope Assessment

Before asking questions, evaluate whether this feature request is appropriately sized for this spec-driven workflow.

**Chain-of-thought reasoning:**

- Consider the complexity and scope of the requested feature
- Compare against the following examples
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

If the scope appears inappropriate, inform the user and suggest alternatives before proceeding.

## Step 2: Clarifying Questions

Ask clarifying questions to gather sufficient detail. **Always provide numbered or lettered options** to allow the user to make selections easily by responding with *"1A, 2B, 3C"*, etc. Focus on understanding the "what" and "why" rather than the "how."

Adapt your questions based on the user's input. Use the following common areas to guide your questions:

**Core Understanding:**

- What problem does this solve and for whom?
- What specific functionality does this feature provide?

**Success & Boundaries:**

- How will we know it's working correctly?
- What should this NOT do?
- Are there edge cases we should explicitly include or exclude?

**Design & Technical:**

- Any existing design mockups or UI guidelines to follow?
- Are there any technical constraints or integration requirements?

**Demo & Proof:**

- How will we demonstrate this feature works?
- What proof artifacts will we need (URLs, CLI output, screenshots)?

**Progressive Disclosure:** Start with Core Understanding, then expand based on feature complexity and user responses.

## Step 3: Context Assessment (Optional)

If the feature involves existing systems, briefly review the codebase and existing docs to understand:

- Current architecture patterns and conventions
- Relevant existing components or features
- Integration constraints or dependencies
- Files that might need modification or extension

**Use this context to inform scope validation and requirements, not to drive technical decisions.** Focus on understanding what exists to make the spec more realistic and achievable.

## Step 4: Spec Generation

Generate a comprehensive specification using this exact structure:

```markdown
# [n]-spec-[feature-name].md

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
**Demo Criteria:** [What will be shown to verify working value]
**Proof Artifacts:** [Tangible evidence - URLs, CLI commands, test names, screenshots]

### [Unit 2]: [Title]
**Purpose:** [What this slice accomplishes and who it serves]
**Demo Criteria:** [What will be shown to verify working value]
**Proof Artifacts:** [Tangible evidence - URLs, CLI commands, test names, screenshots]

## Functional Requirements

[Focus on system behavior and WHAT the system must do. Each should start with "The system shall..." or "The user shall..."]

1. [**Requirement 1**: clear, testable, unambiguous]
2. [**Requirement 2**: clear, testable, unambiguous]
3. [**Requirement 3**: clear, testable, unambiguous]

## Non-Goals (Out of Scope)

[Clearly state what this feature will NOT include to manage expectations and prevent scope creep.]

1. [**Specific exclusion 1**: description]
2. [**Specific exclusion 2**: description]
3. [**Specific exclusion 3**: description]

## Design Considerations

[Focus on UI/UX requirements and visual design. Link to mockups or describe interface requirements. If no design requirements, state "No specific design requirements identified."]

## Technical Considerations

[Focus on implementation constraints and HOW it will be built. Mention technical constraints, dependencies, or architectural decisions. If no technical constraints, state "No specific technical constraints identified."]

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

## Step 5: Review and Refinement

After generating the spec, present it to the user and ask:

1. "Does this specification accurately capture your requirements?"
2. "Are there any missing details or unclear sections?"
3. "Are the scope boundaries appropriate?"
4. "Do the demoable units represent meaningful progress?"

Iterate based on feedback until the user is satisfied.

## Output Requirements

**Format:** Markdown (`.md`)
**Directory:** Create `./docs/specs/[n]-spec-[feature-name]/` (Where `n` is a zero-padded 2-digit sequence starting from 01, e.g., `01-spec-user-authentication/`)
**Full Path:** `./docs/specs/[n]-spec-[feature-name]/[n]-spec-[feature-name].md`
**Example:** For feature "user authentication", create directory `01-spec-user-authentication/` and save file as `01-spec-user-authentication.md` inside it

## Critical Constraints (Negative Instructions)

**NEVER:**

- Start implementing the spec; only create the specification document
- Assume technical details without asking the user
- Create specs that are too large or too small without addressing scope issues
- Use jargon or technical terms that a junior developer wouldn't understand
- Skip the clarifying questions phase, even if the prompt seems clear

**ALWAYS:**

- Ask clarifying questions before generating the spec
- Provide numbered/lettered options for easy selection
- Validate scope appropriateness before proceeding
- Use the exact spec structure provided above
- Ensure the spec is understandable by a junior developer
- Include proof artifacts and demo criteria for each work unit

## What Comes Next

Once this spec is complete and approved, instruct the user to run `/generate-task-list-from-spec`. This will start the next step in the workflow, which is to break down the specification into actionable tasks.

## Final Instructions

Follow this exact sequence:

1. **Initial Scope Assessment**: Use the provided examples to evaluate if the feature is appropriately sized
2. **Clarifying Questions**: Ask structured questions with numbered/lettered options for easy selection
3. **Context Assessment**: Review existing codebase for relevant patterns and constraints (optional)
4. **Spec Generation**: Create the spec using the exact structure provided
   - **Ensure each section has a distinct purpose** - avoid restating content from previous sections
   - **User Stories** focus on motivation and WHY
   - **Demoable Units** focus on tangible progress and WHAT will be shown
   - **Functional Requirements** focus on system behavior and WHAT the system must do
   - **Technical Considerations** focus on implementation constraints and HOW it will be built
5. **Save**: Create directory `./docs/specs/[n]-spec-[feature-name]/` and save file as `[n]-spec-[feature-name].md` inside it
6. **Review and Refine**: Validate completeness and clarity with the user
7. **Guide User**: Direct user to the next workflow step (`/generate-task-list-from-spec`)
8. **Stop**: Stop working once user confirms spec is complete
