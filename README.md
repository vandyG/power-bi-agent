# power-bi-agent

End-to-end Power BI development assistant for GitHub Copilot. Bundles a chat-mode agent and a set of topic skills (semantic modeling, DAX, performance, visualization, SQL→M) that work together against:

- **[powerbi-modeling-mcp](https://marketplace.visualstudio.com/items?itemName=analysis-services.powerbi-modeling-mcp)** — read/write the live Power BI Desktop / Fabric model.
- **[microsoft-learn MCP](https://learn.microsoft.com/api/mcp)** — ground every recommendation in current Microsoft Learn documentation.

## What's inside

| Path | What it is |
|---|---|
| [`agents/power-bi.agent.md`](agents/power-bi.agent.md) | Consolidated VS Code chat-mode agent that routes to the right skill |
| [`skills/powerbi-modeling/`](skills/powerbi-modeling/) | Star schema, relationships, RLS, calculation groups, naming, documentation |
| [`skills/powerbi-dax/`](skills/powerbi-dax/) | DAX authoring + an "optimize this DAX" mode with diagnosis → rewrite → why → verify |
| [`skills/powerbi-performance/`](skills/powerbi-performance/) | Diagnosis decision tree, model/report/refresh/capacity tuning, KQL monitoring |
| [`skills/powerbi-visualization/`](skills/powerbi-visualization/) | Chart selection, layout patterns, accessibility, mobile design |
| [`skills/powerbi-sql/`](skills/powerbi-sql/) | Wrap a `.sql` file in an M `Sql.Database()` expression |
| [`plugin.json`](plugin.json) | GitHub Copilot CLI plugin manifest (root, per spec) |
| [`.mcp.json`](.mcp.json) | MCP server bundle installed with the plugin |
| [`mcp/mcp.linux.json`](mcp/mcp.linux.json), [`mcp/mcp.wsl.json`](mcp/mcp.wsl.json) | Reference MCP server configs (default and WSL flavor) |

## Install

### As a VS Code chat agent + skills (manual)

VS Code reads chat agents from `~/.copilot/agents/` and skills from `~/.copilot/skills/`. Symlink (or `cp -r`) this repo's contents:

```bash
mkdir -p ~/.copilot/agents ~/.copilot/skills
ln -s "$(pwd)/agents/power-bi.agent.md" ~/.copilot/agents/power-bi.agent.md
for s in skills/*/; do
  ln -s "$(pwd)/$s" "$HOME/.copilot/skills/$(basename "$s")"
done
```

Then in VS Code, configure the MCP servers from `mcp/mcp.linux.json` (or `mcp/mcp.wsl.json`) into your VS Code MCP settings.

### Via Nix (Home Manager)

This repo is consumed as a flake input by [vandyG/nixfiles](https://github.com/vandyG/nixfiles) — see `modules/copilot/copilot.nix` there. The Nix module:
- symlinks `agents/` and `skills/` into `~/.copilot/`
- writes the appropriate `mcp.json` per profile (Linux vs WSL)
- on WSL, downloads the `powerbi-modeling-mcp` VSIX and unpacks it into a Windows-accessible path so Power BI Desktop is discoverable

### As a Copilot CLI plugin

```bash
copilot plugin install vandyG/power-bi-agent
```

## MCP server setup

Add both servers to your VS Code or Copilot CLI MCP settings:

**Linux / macOS (default):**
```json
{
  "servers": {
    "powerbi-modeling-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@microsoft/powerbi-modeling-mcp@latest", "--start"]
    },
    "microsoft-learn": {
      "type": "http",
      "url": "https://learn.microsoft.com/api/mcp"
    }
  }
}
```

**WSL** (so that Power BI Desktop on Windows is discoverable):
```json
{
  "servers": {
    "powerbi-modeling-mcp": {
      "command": "cmd.exe",
      "args": ["/C", "C:\\Users\\<you>\\.vscode\\extensions\\analysis-services.powerbi-modeling-mcp-<ver>-win32-x64\\server\\powerbi-modeling-mcp.exe", "--start"]
    },
    "microsoft-learn": {
      "type": "http",
      "url": "https://learn.microsoft.com/api/mcp"
    }
  }
}
```

The Power BI Modeling MCP must run as a Windows process on WSL hosts; otherwise it cannot enumerate local Power BI Desktop instances.

## Usage

In VS Code, open chat and select **`@power-bi`** (the consolidated agent). Topic skills auto-trigger from the user prompt; you can also invoke them by name:

```
@power-bi optimize this DAX measure for performance
@power-bi review my star schema for star-schema compliance
@power-bi which chart for showing churn cohort over time?
@power-bi convert this .sql to a Power Query expression
```

The agent always:
1. Connects to the live model (when relevant) before advising.
2. Searches Microsoft Learn before recommending non-trivial patterns.
3. Cites the documentation URLs it grounded the answer in.
4. Validates writes (`dax_query_operations(operation: "Validate")`) after creating measures.

## Development

```bash
nix develop  # via the bundled shell.nix (or use direnv)
```

The repo currently has no automated tests; skills are validated by use. Update the `version` in [`plugin.json`](plugin.json) when shipping breaking changes to skill or agent definitions.

## License

MIT — see [LICENSE](LICENSE).

Initial agent/skill structure inspired by the [awesome-copilot](https://github.com/github/awesome-copilot) `power-bi-development` plugin and consolidated into a single chat-mode agent.
