import logging
import os
from datetime import datetime
from typing import Dict

from backend.blender_executor import BlenderExecutor


logger = logging.getLogger("PrintExporter")

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)


class PrintExporter:
    def __init__(self, executor: BlenderExecutor = None, exports_dir: str = None):
        self.executor = executor or BlenderExecutor()
        self.exports_dir = exports_dir or os.path.join(project_root, "exports")
        self.asset_script_path = os.path.join(project_root, "blender", "export_asset_to_stl.py")

    def export_asset_to_stl(self, asset_id: int, glb_path: str) -> Dict[str, str]:
        os.makedirs(self.exports_dir, exist_ok=True)

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"kchiro_asset_{asset_id}_{stamp}.stl"
        output_path = os.path.join(self.exports_dir, filename)

        success, logs = self.executor.execute_script(
            script_path=self.asset_script_path,
            script_args=[
                "--input", os.path.abspath(glb_path),
                "--output", output_path,
            ],
            timeout_seconds=180,
        )

        if not success or not os.path.exists(output_path):
            logger.error("Asset STL export failed. Blender logs:\n%s", logs)
            raise RuntimeError("Failed to build the printable STL asset file.")

        return {
            "filename": filename,
            "download_url": f"/exports/{filename}",
        }
