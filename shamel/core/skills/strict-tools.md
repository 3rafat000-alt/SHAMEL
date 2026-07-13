## | أدوات | Tool Usage

Purpose: Correct, efficient use of SHAMEL tooling for every task.
Activated when: agent needs to read, write, search, execute, or fetch.

### Available Tools & Purpose

| Tool | When to use | When NOT to use |
|------|-------------|-----------------|
| **Read** | Read file or directory listing | Reading binary, very large files (>5MB) |
| **Write** | Create new file, overwrite existing | Small edits (use Edit) |
| **Edit** | Modify specific lines in existing file | New file creation (use Write) |
| **Glob** | Find files by name/pattern | Content search (use Grep) |
| **Grep** | Search file contents by regex | File name search (use Glob) |
| **Bash** | Run commands, git, npm, docker | Reading files (use Read), searching (use Grep) |
| **WebFetch** | Get rendered content from URL | Deep research (use WebSearch + WebFetch combo) |
| **WebSearch** | Search internet for information | Known facts you can verify locally |

### Tool Decision Tree

```
Task: What do I need?
├── Read a file → Read
├── Search codebase
│   ├── By filename → Glob
│   └── By content → Grep
├── Modify code
│   ├── New file → Write
│   └── Edit existing → Read → Edit → Verify (Read)
├── Run command → Bash
├── Need external info
│   ├── Specific URL → WebFetch
│   └── Unknown source → WebSearch → WebFetch best results
└── Debug / investigate
    └── Read logs (Bash) → Search patterns (Grep) → Understand (Read)
```

### Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| Tool timeout | Operation too slow | Retry with narrower scope or higher timeout |
| File not found | Wrong path | Glob to find correct path, then retry |
| Permission denied | Missing access | Check file ownership, suggest fix to user |
| API rate limited | Too many requests | Backoff 30s, batch requests |
| Network failure | No connectivity | Retry once after 5s, then report if persistent |

### Tool Chaining — Common Patterns

- **Find + Read + Understand:** Glob → Read → Read (multiple files)
- **Investigate bug:** Bash (logs) → Grep (pattern) → Read (source) → Edit (fix) → Bash (verify)
- **Research + Apply:** WebSearch → WebFetch → Read (current code) → Edit → Bash (test)
- **Code review:** Read (diff) → Grep (related patterns) → Write (review output)

### Prohibited Uses

- **Never** use Bash to read/search files (use Read/Grep/Glob)
- **Never** use Bash for text processing of file content (use Edit/Grep)
- **Never** pipe large binaries through Bash tools
- **Never** run interactive commands (use explicit arguments only)
