# Claude Code Marketplace

**Personal marketplace for Claude Code plugins by Tobias Weber**

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> A curated collection of Claude Code plugins for intelligent automation and productivity.

---

## 🚀 Quick Start

### Install the Marketplace

```bash
/plugin marketplace add comzine/claude-code-marketplace
```

### Install Plugins

```bash
/plugin install meta-automation-architect
```

---

## 📦 Available Plugins

### 🤖 Meta-Automation-Architect

**Intelligent project analysis and custom automation generation**

Automatically analyzes your projects using AI agents and generates tailored automation (agents, skills, commands, hooks) based on your specific needs.

**Features:**
- Agent-based project detection with context understanding
- 3 automation modes (Quick/Focused/Comprehensive)
- Smart tool discovery to prevent duplication
- Cost transparency with upfront estimates
- User preference learning and personalized recommendations
- Real metrics tracking (actual time saved vs estimates)
- Rollback capability with automatic backups
- Configuration reuse for similar projects

**Commands:**
- `/meta-analyze` - Quick project analysis
- `/meta-status` - Show automation status
- `/meta-metrics` - Display ROI and metrics
- `/meta-rollback` - Safely undo changes
- `/meta-help` - Get help and documentation

**Documentation:** [meta-automation-architect/README.md](meta-automation-architect/README.md)

**Version:** 2.0.0

---

## 📖 Documentation

### Plugin Documentation
Each plugin has its own detailed documentation:
- **[Meta-Automation-Architect](meta-automation-architect/README.md)** - Complete plugin guide

### Claude Code Reference
Comprehensive reference for Claude Code development:
- **[claude-code-knowledge.md](claude-code-knowledge.md)** - Complete Claude Code documentation (2,382 lines)
  - Skills system
  - Agents & Task tool
  - Custom commands (slash commands)
  - Hooks system
  - MCP integration
  - Best practices and patterns

---

## 🔄 Updating Plugins

To get the latest version of installed plugins:

```bash
/plugin update meta-automation-architect
```

Or update all plugins:

```bash
/plugin update --all
```

---

## 🛠️ Plugin Development

This marketplace follows the Claude Code plugin standard:

### Structure
```
claude-code-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace definition
├── meta-automation-architect/    # Plugin directory
│   ├── .claude-plugin/
│   │   └── plugin.json          # Plugin manifest
│   ├── skills/                   # Skill definitions
│   ├── commands/                 # Slash commands
│   └── README.md                # Plugin docs
├── claude-code-knowledge.md     # Reference documentation
└── README.md                    # This file
```

### Adding More Plugins

To add a new plugin to this marketplace:

1. Create plugin directory: `my-new-plugin/`
2. Add plugin manifest: `my-new-plugin/.claude-plugin/plugin.json`
3. Update `marketplace.json` to list the new plugin
4. Commit and push

---

## 📊 Plugin Statistics

- **Total Plugins:** 1
- **Total Skills:** 1
- **Total Commands:** 5
- **Lines of Code:** ~10,000+
- **Documentation:** 2,000+ lines

---

## 🤝 Contributing

Found a bug or have a suggestion?

1. Open an issue on GitHub
2. Fork and submit a pull request
3. Contact: comzine@gmail.com

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

Individual plugins may have their own licenses.

---

## 🙏 Credits

**Author:** Tobias Weber
**GitHub:** [@comzine](https://github.com/comzine)
**Email:** comzine@gmail.com

Built with [Claude Code](https://claude.ai/code) by Anthropic.

---

## 📧 Support

For questions or issues:
- Open an issue on GitHub
- Email: comzine@gmail.com

---

**Last Updated:** 2025-11-23
