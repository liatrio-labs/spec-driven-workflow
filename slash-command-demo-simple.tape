# Output slash-command-demo-simple.gif
Output slash-command-demo-simple.mp4
# Output frames/

# Simple demo for quick preview
Set FontSize 14
Set Width 1280
Set Height 720
Set Theme "Dracula"
Set Padding 50
Set TypingSpeed 10ms
Set Margin 60
Set MarginFill "#414558"

# Clear screen
Sleep 300ms

# Introduction
Type "# Welcome to the Slash Command Generator Demo"
Sleep 500ms
Enter 2
Sleep 500ms
Show
Type "# This tool generates native slash commands for AI assistants"
Sleep 500ms
Enter 2
Sleep 500ms
Show

# Show the command
Type "uv run sdd-generate-commands generate --list-agents"
Enter 2
Wait
Sleep 500ms


Type "uv run sdd-generate-commands generate --dry-run --yes"
Enter 2
Wait
Sleep 500ms

Type "# 🎉 Commands generated successfully!"
Enter
Sleep 500ms
