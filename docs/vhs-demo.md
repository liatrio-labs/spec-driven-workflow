# VHS Terminal Demo

This project includes VHS tape files that demonstrate the slash command generation functionality.

## Prerequisites

Install VHS (Video Home System) for creating terminal demos:

```bash
# macOS
brew install vhs

# Linux
# Download from https://github.com/charmbracelet/vhs/releases
# Or install via your package manager

# Using Go
go install github.com/charmbracelet/vhs@latest
```

## Running the Demo

Generate the demo GIF:

```bash
# From the project root
vhs slash-command-demo.tape
```

This will create `slash-command-demo.gif` (~950KB) demonstrating:
- Listing supported agents
- Dry-run mode for previewing changes
- Generating commands for detected agents
- Viewing generated files
- Cleanup functionality

### Simple Demo

For a quicker preview, run the simplified version:

```bash
vhs slash-command-demo-simple.tape
```

## Demo Script

The demo tape (`slash-command-demo.tape`) demonstrates the following features:

1. **Help Documentation**: Shows available CLI options
2. **List Agents**: Displays all supported AI assistants
3. **Dry Run**: Previews what would be generated without writing files
4. **Generation**: Creates command files for detected agents
5. **File Inspection**: Shows generated command files
6. **Cleanup**: Demonstrates removing generated files

## Customizing the Demo

Edit `slash-command-demo.tape` to customize:

- **Output**: Change the GIF filename
- **Theme**: Modify terminal colors (`Set Theme`)
- **Size**: Adjust width/height (`Set Width`, `Set Height`)
- **Font**: Change font size (`Set FontSize`)
- **Commands**: Add or modify command demonstrations

## Publishing the Demo

To publish the generated GIF online:

```bash
vhs publish slash-command-demo.gif
```

This uploads the GIF and provides a shareable URL.

## Troubleshooting

### Common Errors

**Error: Invalid command: Control**

VHS uses `Ctrl+L` (not `Control L`) for key combinations. Always use the shortened form.

**Error: invalid Set Theme**

Use the correct theme name. Common themes include:
- `Molokai` (not "Monokai")
- `Monokai`
- `Dracula`
- `Nord`

## Reference

- [VHS GitHub Repository](https://github.com/charmbracelet/vhs)
- [VHS Documentation](https://github.com/charmbracelet/vhs#readme)
- [VHS Publishing](https://charm.sh/blog/vhs-publish/)
