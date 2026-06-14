import os
import sys
import json
import subprocess
import tempfile
import logging
from typing import Dict, Any, Tuple

# Dynamic path resolution to find project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

logger = logging.getLogger("BlenderExecutor")

class BlenderExecutor:
    def __init__(self, blender_path: str = None):
        """Initializes the Blender Executor with the path to the Blender executable.
        If not provided, attempts to find the portable Blender runtime in `blender/bin/blender.exe`.
        If that fails, falls back to the system path executable `blender`.
        """
        configured_blender_path = blender_path or os.getenv("BLENDER_EXECUTABLE")
        if configured_blender_path:
            self.blender_path = configured_blender_path
        else:
            # Check for portable blender executable in the project
            portable_path = os.path.join(project_root, "blender", "bin", "blender.exe")
            if os.path.exists(portable_path):
                self.blender_path = os.path.abspath(portable_path)
            else:
                logger.warning(f"Portable Blender not found at {portable_path}. Falling back to system 'blender'.")
                self.blender_path = "blender"

    def execute_generator(
        self,
        generator_script: str,
        params: Dict[str, Any],
        export_path: str,
        render_path: str = None,
        timeout_seconds: int = 60
    ) -> Tuple[bool, str]:
        """Executes a procedural Blender generator script headlessly.
        
        Args:
            generator_script: Absolute path to the blender generator python script.
            params: Parameters dictionary to feed into the generator.
            export_path: Destination path for the exported GLB model.
            render_path: Optional destination path for the preview PNG render.
            timeout_seconds: Subprocess timeout in seconds.
            
        Returns:
            Tuple[bool, str]: (Success status, stdout/stderr log output)
        """
        # Ensure directories exist
        os.makedirs(os.path.dirname(os.path.abspath(export_path)), exist_ok=True)
        if render_path:
            os.makedirs(os.path.dirname(os.path.abspath(render_path)), exist_ok=True)

        # Create a temporary JSON file for parameter passing
        temp_json_fd, temp_json_path = tempfile.mkstemp(suffix=".json")
        try:
            with os.fdopen(temp_json_fd, 'w') as temp_file:
                json.dump(params, temp_file, indent=2)
            
            # Build the command line argument list
            # Format: blender.exe --background --python <generator_script> -- --params <temp_json> --export <glb_output> --render <png_output>
            cmd = [
                self.blender_path,
                "--background",
                "--python", os.path.abspath(generator_script),
                "--",
                "--params", os.path.abspath(temp_json_path),
                "--export", os.path.abspath(export_path)
            ]
            
            if render_path:
                cmd.extend(["--render", os.path.abspath(render_path)])
                
            logger.info(f"Running Blender command: {' '.join(cmd)}")
            
            # Execute command
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=timeout_seconds,
                check=False
            )
            
            success = result.returncode == 0
            return success, result.stdout
            
        except subprocess.TimeoutExpired as e:
            logger.error(f"Blender process timed out after {timeout_seconds} seconds.")
            return False, f"Blender execution timed out: {e.stdout or ''}"
        except Exception as e:
            logger.error(f"Error during Blender execution: {e}")
            return False, f"Executor error: {str(e)}"
        finally:
            # Clean up the temporary JSON file
            try:
                if os.path.exists(temp_json_path):
                    os.remove(temp_json_path)
            except Exception as e:
                logger.warning(f"Failed to remove temp JSON file {temp_json_path}: {e}")

    def execute_script(
        self,
        script_path: str,
        script_args=None,
        timeout_seconds: int = 120
    ) -> Tuple[bool, str]:
        """Executes an arbitrary Blender Python script headlessly."""
        cmd = [
            self.blender_path,
            "--background",
            "--python", os.path.abspath(script_path),
            "--"
        ]

        if script_args:
            cmd.extend([str(arg) for arg in script_args])

        logger.info(f"Running Blender script command: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=timeout_seconds,
                check=False
            )
            return result.returncode == 0, result.stdout
        except subprocess.TimeoutExpired as e:
            logger.error(f"Blender script timed out after {timeout_seconds} seconds.")
            return False, f"Blender script timed out: {e.stdout or ''}"
        except Exception as e:
            logger.error(f"Error during Blender script execution: {e}")
            return False, f"Executor error: {str(e)}"

if __name__ == "__main__":
    # Self-test when run directly
    logging.basicConfig(level=logging.INFO)
    executor = BlenderExecutor()
    print(f"Using blender executable: {executor.blender_path}")
