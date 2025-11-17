# Feedback Analysis: Prompts vs. Current Site Language

## Executive Summary

The feedback reveals a significant mismatch between how the prompts actually work and how the site presents them. The prompts are **lightweight, transparent, and designed for small work**, but the site language makes them sound like a **heavyweight enterprise process**. This analysis examines the gaps and provides recommendations.

## Key Findings

### 1. The Prompts Are Actually "Prompts," Not "Phases"

**Current Site Language:**

- Uses "Phase 1: Specification", "Phase 2: Task Breakdown", etc.
- Implies a formal, structured process with distinct phases

**Reality from Prompts:**

- These are 4 markdown prompt files that guide an AI assistant
- They're sequential but flexible - more like "steps" than "phases"
- Each prompt is self-contained and can be understood independently

**Recommendation:** Reframe as "4 Prompts" or "4 Steps" rather than "4 Phases"

### 2. Scope Validation Exists But Isn't Highlighted

**What the Prompts Actually Do:**

The `generate-spec.md` prompt has **explicit scope validation** built in:

```markdown
## Step 1: Initial Scope Assessment

Before asking questions, evaluate whether this feature request is
appropriately sized for this spec-driven workflow.

**Too Large (split into multiple specs):**
- Rewriting an entire application architecture
- Migrating a complete database system
- Building a complete microservices architecture

**Too Small (vibe-code directly):**
- Adding a single console.log statement
- Changing the color of a button in CSS
- Fixing a simple off-by-one error

**Just Right (perfect for this workflow):**
- Adding a new CLI flag with validation
- Implementing a single API endpoint
- Creating a single database migration
- Implementing one user story with complete end-to-end flow
```

**Current Site Language:**

- Doesn't mention scope validation at all
- Makes it sound like this workflow is for any size feature

**Recommendation:** Add prominent section highlighting that:

- The prompts automatically validate scope
- This is for Jira stories post-grooming (ready to pick up)
- Too large = prompts suggest splitting
- Too small = prompts suggest direct implementation

### 3. "Roles" Language Is Misleading

**Current Site Language:**

- "Responsible Role: Feature Lead"
- "Responsible Role: Technical Lead or Implementer"
- "Responsible Role: Reviewer or QA Lead"
- Implies multiple people with different roles

**Reality from Prompts:**

- The prompts say "You are a Senior Product Manager..." but this is describing the **AI's role**, not a human role
- The workflow is designed for **one person** to run with an AI assistant
- There are no handoffs between different people
- The "roles" are just different perspectives the AI takes

**Recommendation:** Remove "Responsible Role" language entirely. Replace with:

- "AI Perspective: [description]" or
- "Focus: [description]" or
- Just remove it - it's not necessary

### 4. The "Phases" Language Makes It Sound Too Big

**Current Site Language:**

- "Phase 1: Specification"
- "Phase 2: Task Breakdown"
- "Phase 3: Implementation"
- "Phase 4: Validation"
- Sounds like a multi-day, multi-person process

**Reality:**

- These are 4 markdown prompts
- Example took <15 minutes from start to finish
- One person runs through all 4 prompts sequentially
- It's a lightweight workflow, not a heavyweight process

**Recommendation:**

- Use "Step" or "Prompt" instead of "Phase"
- Emphasize speed: "Complete a feature in minutes, not days"
- Show the actual prompt files are just markdown

### 5. Missing Comparison Against Heavy Tools

**What Should Be Highlighted:**

The prompts are fundamentally different from tools like:

- **Kiro** - Enterprise tool with UI, integrations, workflows
- **SpecKit** - Tooling framework with dependencies
- **Taskmaster** - Project management integration

**Advantages to Highlight:**

- **More accessible**: Just 4 markdown files, no installation
- **Tool agnostic**: Works with any AI assistant, any editor
- **More flexible**: Edit prompts to fit your project/style/company
- **Basic file structure**: Simple `docs/specs/` organization that doesn't pollute repo
- **Transparent**: You can read and modify every prompt

**Recommendation:** Add a comparison section showing how this differs from enterprise tools

### 6. Missing "Flow Input" Concept

**Current Site:**

- Doesn't explain what users bring to the workflow
- Jumps straight into "Specification" without context

**Reality:**

- Users bring different inputs: an idea, a Jira story, a GitHub issue, etc.
- The prompts adapt to whatever input is provided
- This should be explained upfront

**Recommendation:** Add a section explaining "Flow Input" - what you bring to start the workflow

## Detailed Prompt Analysis

### Prompt 1: `generate-spec.md`

- **Purpose**: Transform initial idea into structured spec
- **Key Features**: Scope validation, clarifying questions, context assessment
- **Output**: Single markdown spec file in `docs/specs/[NN]-spec-[name]/`
- **Time**: ~5-10 minutes typically

### Prompt 2: `generate-task-list-from-spec.md`

- **Purpose**: Break spec into actionable tasks
- **Key Features**: Two-phase (parent tasks first, then sub-tasks), demo criteria, proof artifacts
- **Output**: Task list markdown file
- **Time**: ~2-3 minutes typically

### Prompt 3: `manage-tasks.md`

- **Purpose**: Execute tasks with verification
- **Key Features**: Checkpoint modes, proof artifacts, git workflow
- **Output**: Code changes + proof files
- **Time**: Variable (depends on feature size)

### Prompt 4: `validate-spec-implementation.md`

- **Purpose**: Verify implementation matches spec
- **Key Features**: Coverage matrix, evidence verification, validation gates
- **Output**: Validation report markdown
- **Time**: ~2-3 minutes typically

## Recommendations Summary

### High Priority Changes

1. **Reframe "Phases" → "Prompts" or "Steps"**
   - Change all "Phase X" language to "Prompt X" or "Step X"
   - Emphasize these are markdown files, not formal process phases

2. **Add Scope Validation Section**
   - Prominently feature that prompts validate scope automatically
   - Explain "too large" vs "too small" vs "just right"
   - Emphasize this is for Jira stories post-grooming

3. **Remove "Roles" Language**
   - Delete "Responsible Role" from all cards
   - Replace with "Focus" or remove entirely
   - Emphasize one-person workflow

4. **Add Speed Emphasis**
   - Highlight example: "<15 minutes from start to finish"
   - Show this is lightweight, not heavyweight
   - Contrast with multi-day enterprise processes

5. **Add Comparison Section**
   - Compare against Kiro, SpecKit, Taskmaster
   - Highlight: accessible, tool-agnostic, flexible, transparent

6. **Add "Flow Input" Concept**
   - Explain what users bring (idea, Jira story, GitHub issue)
   - Show prompts adapt to any input type

### Medium Priority Changes

1. **Show Actual Prompt Files**
   - Link to or show snippets of actual prompt files
   - Demonstrate transparency and simplicity

2. **Emphasize File Structure**
   - Show simple `docs/specs/` organization
   - Explain it doesn't pollute the repo

3. **Add GitHub Pages Migration**
   - Technical task but important for accessibility

## Content Structure Recommendations

### New Hero Section Should Say

- "4 Transparent Prompts for Small Features"
- "Complete a feature in minutes, not days"
- "Just markdown files - no tools, no dependencies"

### New Flow Input Section

- "What You Bring: An idea, a Jira story, a GitHub issue - anything"
- "The prompts adapt to your input and guide you through"

### New Scope Section

- "Built-in Scope Validation"
- "Prompts automatically check if work is too large or too small"
- "Perfect for Jira stories post-grooming"

### New Comparison Section

- "Why Not [Heavy Tool]?"
- Side-by-side comparison table
- Highlight transparency, flexibility, accessibility

## Conclusion

The feedback is spot-on. The current site language makes this sound like an enterprise process when it's actually a lightweight, transparent workflow. The prompts themselves are well-designed for small work with built-in scope validation, but the site doesn't communicate this effectively.

The key insight: **This is 4 markdown prompts, not a formal process**. The language should reflect simplicity, speed, and transparency rather than formality, roles, and phases.
