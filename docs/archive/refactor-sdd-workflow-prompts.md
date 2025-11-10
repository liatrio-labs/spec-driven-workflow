# Spec-Driven Development Workflow Refactoring

The main goal here is to improve the workflow while maintaining its simplicity. One of the main points of the workflow is to keep it simple and easy to use - that is what differentiates it from other workflows like Taskmaster, GitHub SpecKit, Kiro, etc.

Additional goals:

- The workflow should be accessible to newcomers
- Configuration should be barebones since different tools support different customizations. Any customization of the workflow should be handled within the prompts.

## Best Practices to document

1. Start each workflow command in a fresh conversation to avoid context confusion and overloading
2. Provide clear instructions on what to expect from the AI and what to expect from the user

## Improvements

### Improve prompt clarity and structure based on research findings

Based on prompt engineering best practices for spec-driven development, the workflow should provide more guidance to newcomers without requiring constant reference to the README. Each prompt should guide users through the flow with clear context and next steps.

**Prompt Structure Improvements:**

- Use explicit role-based prompting ("You are a senior developer implementing...")
- Add chain-of-thought reasoning steps to prevent premature task generation
- Include negative constraints to prevent common failure modes
- Add output format templates with concrete examples
- Implement progressive disclosure - reveal complexity gradually

**General pattern for all prompts:**

- Each prompt should start with "You are here in the workflow" context
- End with "What comes next" guidance
- Include progress indicators where applicable

#### Specific Prompt Enhancements

**generate-spec.md:**

- Add scope size validation prompts with the Bad/Good examples
- Add clear guidance on "What happens next" section after spec creation, including when to move to task generation and how to do it

**generate-task-list-from-spec.md:**

- Add explanation of why parent tasks are generated first
- Add guidance on how to evaluate top-level tasks against the spec
- Enhance the "Generate sub tasks" interaction with clearer context
- Add "DO NOT generate sub-tasks until explicitly requested" constraint
- Add clear guidance on "What happens next" section after task generation, including when to move to task implementation and how to do it

**manage-tasks.md:**

- Instruct the AI to present checkpoint options prominently at the start of this prompt
- Add a brief overview of what this prompt does and how it progresses through tasks
- Add clear guidance on "What happens next" section after task implementation, including when to move to validation and how to do it
- Add explicit commit enforcement protocol after each parent task completion to ensure consistent git history. Commits should be created, at minimum, for each parent task completion.
- Add proof artifact generation and validation steps to ensure they are created during task implementation and invocation of the `/manage-tasks` command

**validate-spec-implementation.md:**

- Add brief "When to use this prompt" context (after completing all tasks in a spec)
- Update Auto-Discovery Protocol to look in `./docs/specs/` instead of `/tasks/`

### Scope size recommendation as part of initial spec creation

The intent here is to detect when a spec is too large and should be split into multiple specs. The workflow is currently focused with the expected output of the workflow to be code changes of a relatively small scope.

Similarly, the workflow should attempt to evaluate when a spec is too small and could probably be "vibe-coded" instead of going through the entire workflow.

#### Bad Examples (scope too large)

- Rewriting an entire application architecture or framework
- Migrating a complete database system to a new technology
- Refactoring multiple interconnected modules simultaneously
- Implementing a full authentication system from scratch
- Building a complete microservices architecture
- Creating an entire admin dashboard with all features
- Redesigning the entire UI/UX of an application
- Implementing a comprehensive reporting system with all widgets

#### Bad Examples (scope too small)

- Adding a single console.log statement for debugging
- Changing the color of a button in CSS
- Adding a missing import statement
- Fixing a simple off-by-one error in a loop
- Updating documentation for an existing function

#### Good Examples (scope just right)

- Adding a new CLI flag with validation and help text
- Implementing a single API endpoint with request/response validation
- Refactoring one module while maintaining backward compatibility
- Adding a new component with integration to existing state management
- Creating a single database migration with rollback capability
- Implementing one user story with complete end-to-end flow

> Note: these examples should be incorporated into the documentation for this workflow.

### Optional input for defining when the AI should ask the user for input/continue

This would allow the user to specify how the AI should manage the implementation in `/manage-tasks`. Basically there are three options:

- Ask for input/continue after each sub task (1.1, 1.2, 1.3)
- Ask for input/continue after each task (1.0, 2.0, 3.0)
- Ask for input/continue after each spec

If the user does not specify one of these options up invocation of the `/manage-tasks` command, then the AI should ask the user which option they would like to use for this invocation. The prompt should instruct the AI to use any option that was previously specified by the user in the current conversation.

### Centralize spec/tasks/proofs location

All specs, tasks, and proofs should be stored in `./docs/specs`. Simple directory structure:

```text
./docs/specs/
├── 01-spec-feature-name
    ├── 01-spec-feature-name.md
    ├── 01-tasks-feature-name.md
    └── 01-proofs/
        ├── 01-01-proofs.md
        ├── 01-02-proofs.md
        ├── 01-03-proofs.md
├── 02-spec-another-feature
    ├── 02-spec-another-feature.md
    ├── 02-tasks-another-feature.md
    └── 02-proofs/
        ├── 02-01-proofs.md
        ├── 02-02-proofs.md
        ├── 02-03-proofs.md
```

**Key Principles:**

- **Spec-based organization**: Each spec gets its own directory with related files
- **Co-located artifacts**: Proofs are organized by task number within each spec
- **Team-managed lifecycle**: Teams determine when to archive specs, tasks, and proofs as they see fit
- **Clear traceability**: Easy to see which proofs belong to which tasks and specs
- **Consistent naming**: Proof artifacts follow single Markdown file pattern `[spec]-[task]-proofs.md` containing all evidence as Markdown code blocks

### Simplify numbering system

The numbering system should have a single leading zero based on 01, 02, 03, etc. Having 3 leading zeros is not necessary and makes it more difficult to navigate the files.
