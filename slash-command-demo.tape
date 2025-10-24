Output slash-command-demo.mp4

# Set terminal appearance
Set FontSize 14
Set Width 1280
Set Height 720
Set Theme "Dracula"
Set Padding 50
Set TypingSpeed 25ms
Set Margin 60
Set MarginFill "#414558"

# Clear screen and start
Sleep 500ms

# Introduction
Type "# Welcome to the Slash Command Generator Demo"
Sleep 500ms
Enter 2
Sleep 500ms
Type "# This tool generates native slash commands for AI assistants"
Sleep 500ms
Enter 2
Sleep 500ms

# the help
Type "uv run sdd-generate-commands --help"
Enter
Wait
Sleep 500ms

Enter 2

# List all supported agents
Type "# Let's see what agents are supported:"
Sleep 500ms
Enter 2
Type "uv run sdd-generate-commands generate --list-agents"
Enter
Wait
Sleep 500ms

Enter 2

# Dry run demonstration
Type "# Preview what would be generated (dry run):"
Sleep 500ms
Enter 2
Type "uv run sdd-generate-commands generate --dry-run --yes"
Enter
Wait
Sleep 500ms

Enter 2

# Actual generation with detected agents
Type "# Now generating commands for detected agents:"
Sleep 500ms
Enter 2
Type "uv run sdd-generate-commands generate --yes"
Enter
Wait
Sleep 500ms

Enter 2

# generated files
Type "# Generated files:"
Sleep 500ms
Enter 2
Type "ls -la ~/.claude/commands/ | head -5"
Enter
Wait
Sleep 500ms

Enter 2
Type "ls -la ~/.cursor/commands/ | head -5"
Enter
Wait
Sleep 500ms

Enter 2

# contents of a generated file
Type "# Example generated command file:"
Sleep 500ms
Enter 2
Type "head -20 ~/.claude/commands/generate-spec.md"
Enter
Wait
Sleep 500ms

Enter 2

# Demonstrate cleanup functionality
Type "# Cleanup demonstration (dry run):"
Sleep 500ms
Enter 2
Type "uv run sdd-generate-commands cleanup --dry-run --yes"
Enter
Wait
Sleep 500ms

Enter 2

# Final summary
Type "# Summary:"
Sleep 500ms
Enter 2
Type "# ✓ Generate slash commands for multiple AI assistants"
Sleep 500ms
Enter
Sleep 500ms
Type "# ✓ Auto-detect configured agents"
Sleep 500ms
Enter
Sleep 500ms
Type "# ✓ Preview changes with dry-run mode"
Sleep 500ms
Enter
Sleep 500ms
Type "# ✓ Safe cleanup of generated files"
Sleep 500ms
Enter 2
Sleep 500ms
Type "# Learn more: docs/slash-command-generator.md"
Sleep 1s
