import os
import sys
import urllib.request
import zipfile
import shutil

def setup():
    url = "https://mirrors.ocf.berkeley.edu/blender/release/Blender4.1/blender-4.1.1-windows-x64.zip"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(script_dir, "blender.zip")
    bin_dir = os.path.join(script_dir, "bin")
    
    # 1. Download Blender Zip if not already downloaded
    if not os.path.exists(zip_path) and not os.path.exists(os.path.join(bin_dir, "blender.exe")):
        print(f"Starting download from: {url}")
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            )
            with urllib.request.urlopen(req) as response, open(zip_path, 'wb') as out_file:
                total_size = int(response.info().get('Content-Length', 0))
                block_size = 1024 * 1024 # 1MB chunks
                downloaded = 0
                while True:
                    chunk = response.read(block_size)
                    if not chunk:
                        break
                    out_file.write(chunk)
                    downloaded += len(chunk)
                    percent = min(100, (downloaded / total_size) * 100) if total_size else 0
                    sys.stdout.write(f"\rDownloading Blender: {percent:.1f}% ({downloaded / (1024*1024):.1f}MB / {total_size / (1024*1024):.1f}MB)")
                    sys.stdout.flush()
            print("\nDownload complete.")
        except Exception as e:
            print(f"\nError downloading Blender: {e}")
            sys.exit(1)
    
    # 2. Extract Blender Zip
    if os.path.exists(zip_path):
        print(f"Extracting Blender to: {bin_dir}...")
        try:
            if not os.path.exists(bin_dir):
                os.makedirs(bin_dir)
            
            # Extract to a temp directory
            temp_extract_dir = os.path.join(script_dir, "temp_extract")
            if os.path.exists(temp_extract_dir):
                shutil.rmtree(temp_extract_dir)
            os.makedirs(temp_extract_dir)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                infos = zip_ref.infolist()
                total_files = len(infos)
                for idx, info in enumerate(infos):
                    zip_ref.extract(info, temp_extract_dir)
                    if idx % 100 == 0 or idx == total_files - 1:
                        sys.stdout.write(f"\rExtracting: {((idx + 1) / total_files) * 100:.1f}% ({idx + 1}/{total_files} files)")
                        sys.stdout.flush()
            print("\nExtraction complete.")
            
            # Inside temp_extract, there will be blender-4.1.1-windows-x64
            inner_dir = os.path.join(temp_extract_dir, "blender-4.1.1-windows-x64")
            if os.path.exists(inner_dir):
                print("Moving Blender files to bin folder...")
                # Clear bin folder if it already has files
                for item in os.listdir(bin_dir):
                    item_path = os.path.join(bin_dir, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
                
                # Move files from inner_dir to bin_dir
                for item in os.listdir(inner_dir):
                    shutil.move(os.path.join(inner_dir, item), bin_dir)
                
                print("Clean up temp files...")
                shutil.rmtree(temp_extract_dir)
                os.remove(zip_path)
                print("Setup finished successfully! blender.exe is ready in blender/bin/.")
            else:
                print(f"Error: Could not find extracted folder: {inner_dir}")
                sys.exit(1)
        except Exception as e:
            print(f"\nError during extraction/movement: {e}")
            sys.exit(1)
    else:
        if os.path.exists(os.path.join(bin_dir, "blender.exe")):
            print("Blender is already installed and ready.")
        else:
            print("Error: Blender ZIP not found and blender.exe not present in bin.")

if __name__ == "__main__":
    setup()
