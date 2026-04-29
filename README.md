# power-bi-agent

End-to-end Power BI development assistant for GitHub Copilot. Bundles a chat-mode agent and a set of topic skills (semantic modeling, DAX, performance, visualization, SQL→M) that work together against live models and Power BI Project files:

- **[powerbi-modeling-mcp](https://marketplace.visualstudio.com/items?itemName=analysis-services.powerbi-modeling-mcp)** — read/write the live Power BI Desktop / Fabric model.
- **[microsoft-learn MCP](https://learn.microsoft.com/api/mcp)** — ground every recommendation in current Microsoft Learn documentation.
- **Power BI Project files (PBIP/PBIR/TMDL)** — edit supported report and semantic model metadata directly when project files are present in the workspace.

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
2. Checks for PBIP/PBIR/TMDL files when report or visual work can be done through source-controlled project files.
3. Searches Microsoft Learn before recommending non-trivial patterns.
4. Cites the documentation URLs it grounded the answer in.
5. Uses `vscode_askQuestions` if a Power BI Modeling MCP call returns a file/artifact URI, because the agent can only inspect it after the user saves it into the workspace.
6. Validates writes (`dax_query_operations(operation: "Validate")`) after creating measures.

## PBIP workflow

When a workspace contains Power BI Project files, the agent can work directly against supported text metadata instead of treating report development as Desktop-only.

- Report-side editable surfaces: `definition.pbir`, PBIR `definition/` folders, and already-registered files under `StaticResources/RegisteredResources/`.
- Report-side non-editable preview surfaces: `report.json`, `mobileState.json`, `semanticModelDiagramLayout.json`.
- Semantic model file workflow: prefer the Modeling MCP for live changes, but use `*.SemanticModel/definition/` when the project is using TMDL and the task is explicitly file-based or source-control oriented.
- After external file edits, Power BI Desktop must be reopened or restarted before the changes appear.
- If a Modeling MCP result produces a file URI or `vscode-chat-response-resource://` artifact, the user must save it to a workspace path before the agent can read it. If no file was generated because there was no data, the agent should continue without blocking.

## Development

```bash
nix develop  # via the bundled shell.nix (or use direnv)
```

The repo currently has no automated tests; skills are validated by use. Update the `version` in [`plugin.json`](plugin.json) when shipping breaking changes to skill or agent definitions.

## License

MIT — see [LICENSE](LICENSE).

Initial agent/skill structure inspired by the [awesome-copilot](https://github.com/github/awesome-copilot) `power-bi-development` plugin and consolidated into a single chat-mode agent.
