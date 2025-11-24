#!/usr/bin/env python3
"""
Simple Template Renderer
Renders templates with variable substitution
"""

import re
from pathlib import Path
from typing import Dict, Any

class TemplateRenderer:
    """Simple template renderer using {{variable}} syntax"""

    def __init__(self, template_dir: str = "templates"):
        self.template_dir = Path(__file__).parent.parent / template_dir

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Render a template with the given context

        Args:
            template_name: Name of template file (e.g., 'agent-base.md.template')
            context: Dictionary of variables to substitute

        Returns:
            Rendered template string
        """
        template_path = self.template_dir / template_name

        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        template_content = template_path.read_text(encoding='utf-8')

        # Simple variable substitution using {{variable}} syntax
        def replace_var(match):
            var_name = match.group(1)
            value = context.get(var_name, f"{{{{MISSING: {var_name}}}}}")
            return str(value)

        rendered = re.sub(r'\{\{(\w+)\}\}', replace_var, template_content)

        return rendered

    def render_to_file(self, template_name: str, context: Dict[str, Any], output_path: str) -> None:
        """
        Render template and write to file

        Args:
            template_name: Name of template file
            context: Dictionary of variables
            output_path: Where to write rendered output
        """
        rendered = self.render(template_name, context)

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding='utf-8')

    def list_templates(self) -> list:
        """List available templates"""
        if not self.template_dir.exists():
            return []

        return [
            f.name for f in self.template_dir.iterdir()
            if f.is_file() and f.suffix == '.template'
        ]

# Example usage
if __name__ == '__main__':
    renderer = TemplateRenderer()

    # Example: Render an agent
    context = {
        'agent_name': 'security-analyzer',
        'agent_title': 'Security Analyzer',
        'description': 'Analyzes code for security vulnerabilities',
        'tools': 'Read, Grep, Glob, Bash',
        'color': 'Red',
        'model': 'sonnet',
        'session_id': 'test-123',
        'mission': 'Find security vulnerabilities in the codebase',
        'process': '1. Scan for common patterns\n2. Check dependencies\n3. Review auth code'
    }

    print("Available templates:")
    for template in renderer.list_templates():
        print(f"  - {template}")

    print("\nRendering example agent...")
    rendered = renderer.render('agent-base.md.template', context)
    print("\n" + "="*60)
    print(rendered[:500] + "...")
