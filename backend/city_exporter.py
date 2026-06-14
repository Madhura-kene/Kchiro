import json
import logging
import os
from datetime import datetime
from typing import Any, Dict

from backend.blender_executor import BlenderExecutor

logger = logging.getLogger("CityExporter")

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)


class CityExporter:
    def __init__(self, executor: BlenderExecutor = None, exports_dir: str = None):
        self.executor = executor or BlenderExecutor()
        self.exports_dir = exports_dir or os.path.join(project_root, "exports")
        self.script_path = os.path.join(project_root, "blender", "export_city_to_blend.py")

    def export_city_to_blend(self, manifest: Dict[str, Any]) -> Dict[str, str]:
        os.makedirs(self.exports_dir, exist_ok=True)

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"kchiro_city_{stamp}"
        manifest_filename = f"{base_name}.json"
        output_filename = f"{base_name}.blend"
        manifest_path = os.path.join(self.exports_dir, manifest_filename)
        output_path = os.path.join(self.exports_dir, output_filename)

        with open(manifest_path, "w", encoding="utf-8") as manifest_file:
            json.dump(manifest, manifest_file, indent=2)

        success, logs = self.executor.execute_script(
            script_path=self.script_path,
            script_args=[
                "--manifest", manifest_path,
                "--output", output_path,
            ],
            timeout_seconds=180,
        )

        if not success or not os.path.exists(output_path):
            logger.error("City export failed. Blender logs:\n%s", logs)
            raise RuntimeError("Failed to build the Blender city file.")

        return {
            "filename": output_filename,
            "download_url": f"/exports/{output_filename}",
            "manifest_url": f"/exports/{manifest_filename}",
        }
