from __future__ import annotations

from hatch.env.collectors.plugin.interface import EnvironmentCollectorInterface
from mkdocs_get_deps import get_deps


class MkDocsEnvironmentCollector(EnvironmentCollectorInterface):
    PLUGIN_NAME = "mkdocs"

    def finalize_config(self, config: dict[str, dict]) -> None:
        for env_name, plugin_env_entry in self.config.items():
            path = plugin_env_entry.get("path", "mkdocs.yml")

            deps = get_deps(config_file=self.root / path)
            env = config.setdefault(env_name, {})

            env["dependencies"] = [*deps, *env.get("dependencies", ())]

            env.setdefault("detached", True)

            scripts_config = env.setdefault("scripts", {})
            scripts_config.setdefault("build", f"mkdocs build -f {path} {{args}}")
            scripts_config.setdefault("serve", f"mkdocs serve -f {path} {{args}}")
            scripts_config.setdefault("gh-deploy", f"mkdocs gh-deploy -f {path} {{args}}")
