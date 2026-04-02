"""
ZARA - Advanced Real-time Intelligent Assistant
File Manager Module - File and folder operations
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional


class FileManager:
    """
    File and folder management.
    Handles file operations like create, delete, move, copy, rename, search, zip, unzip.
    """

    def __init__(self):
        """Initialize file manager."""
        self.home = Path.home()
        self.documents = self.home / "Documents"
        self.downloads = self.home / "Downloads"
        self.pictures = self.home / "Pictures"

    # ============== Folder Operations ==============

    def create_folder(self, path: str, exist_ok: bool = True) -> Dict[str, Any]:
        """
        Create a new folder.
        
        Args:
            path: Folder path to create
            exist_ok: If True, don't error if folder exists
            
        Returns:
            Status dictionary
        """
        try:
            # Expand user home if path starts with ~
            if path.startswith('~'):
                path = os.path.expanduser(path)
            
            os.makedirs(path, exist_ok=exist_ok)
            
            return {
                "success": True,
                "message": f"Folder created: {path}",
                "path": path,
                "action": "create_folder"
            }
            
        except FileExistsError:
            return {
                "success": False,
                "message": f"Folder already exists: {path}",
                "path": path,
                "action": "create_folder"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete_folder(self, path: str, confirm: bool = True) -> Dict[str, Any]:
        """
        Delete a folder and all its contents.
        
        Args:
            path: Folder path to delete
            confirm: Require confirmation flag
            
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(path):
                return {
                    "success": False,
                    "message": f"Folder not found: {path}",
                    "action": "delete_folder"
                }
            
            if not os.path.isdir(path):
                return {
                    "success": False,
                    "message": f"Not a folder: {path}",
                    "action": "delete_folder"
                }
            
            shutil.rmtree(path)
            
            return {
                "success": True,
                "message": f"Folder deleted: {path}",
                "path": path,
                "action": "delete_folder"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== File Operations ==============

    def delete_file(self, path: str, confirm: bool = True) -> Dict[str, Any]:
        """
        Delete a file.
        
        Args:
            path: File path to delete
            confirm: Require confirmation flag
            
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(path):
                return {
                    "success": False,
                    "message": f"File not found: {path}",
                    "action": "delete_file"
                }
            
            if not os.path.isfile(path):
                return {
                    "success": False,
                    "message": f"Not a file: {path}",
                    "action": "delete_file"
                }
            
            os.remove(path)
            
            return {
                "success": True,
                "message": f"File deleted: {path}",
                "path": path,
                "action": "delete_file"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def move_file(self, src: str, dst: str) -> Dict[str, Any]:
        """
        Move a file from source to destination.
        
        Args:
            src: Source file path
            dst: Destination path
            
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(src):
                return {
                    "success": False,
                    "message": f"Source file not found: {src}",
                    "action": "move_file"
                }
            
            # Create destination directory if it doesn't exist
            dst_dir = os.path.dirname(dst)
            if dst_dir and not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            
            shutil.move(src, dst)
            
            return {
                "success": True,
                "message": f"File moved from {src} to {dst}",
                "source": src,
                "destination": dst,
                "action": "move_file"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def copy_file(self, src: str, dst: str) -> Dict[str, Any]:
        """
        Copy a file from source to destination.
        
        Args:
            src: Source file path
            dst: Destination path
            
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(src):
                return {
                    "success": False,
                    "message": f"Source file not found: {src}",
                    "action": "copy_file"
                }
            
            # Create destination directory if it doesn't exist
            dst_dir = os.path.dirname(dst)
            if dst_dir and not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            
            shutil.copy2(src, dst)  # copy2 preserves metadata
            
            return {
                "success": True,
                "message": f"File copied from {src} to {dst}",
                "source": src,
                "destination": dst,
                "action": "copy_file"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def rename_file(self, old: str, new: str) -> Dict[str, Any]:
        """
        Rename a file.
        
        Args:
            old: Current file path
            new: New file path
            
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(old):
                return {
                    "success": False,
                    "message": f"File not found: {old}",
                    "action": "rename_file"
                }
            
            os.rename(old, new)
            
            return {
                "success": True,
                "message": f"File renamed from {old} to {new}",
                "old_path": old,
                "new_path": new,
                "action": "rename_file"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== List & Search ==============

    def list_files(self, directory: str = None, extension: str = None) -> Dict[str, Any]:
        """
        List files in directory with optional extension filter.
        
        Args:
            directory: Directory path (default: current directory)
            extension: File extension to filter (e.g., '.txt', '.pdf')
            
        Returns:
            Dictionary with file list
        """
        try:
            if directory is None:
                directory = os.getcwd()
            
            if not os.path.exists(directory):
                return {
                    "success": False,
                    "message": f"Directory not found: {directory}",
                    "action": "list_files"
                }
            
            items = os.listdir(directory)
            files = []
            folders = []
            
            for item in items:
                item_path = os.path.join(directory, item)
                
                if os.path.isfile(item_path):
                    # Filter by extension if specified
                    if extension:
                        if item.lower().endswith(extension.lower()):
                            files.append({
                                "name": item,
                                "path": item_path,
                                "size": os.path.getsize(item_path)
                            })
                    else:
                        files.append({
                            "name": item,
                            "path": item_path,
                            "size": os.path.getsize(item_path)
                        })
                else:
                    folders.append({
                        "name": item,
                        "path": item_path
                    })
            
            return {
                "success": True,
                "directory": directory,
                "files": files,
                "folders": folders,
                "file_count": len(files),
                "folder_count": len(folders),
                "total_count": len(items),
                "action": "list_files"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def search_file(self, name: str, search_path: str = 'C:/') -> Dict[str, Any]:
        """
        Search for files by name using os.walk.
        
        Args:
            name: Filename or partial name to search
            search_path: Root directory to start search
            
        Returns:
            Dictionary with search results
        """
        try:
            if not os.path.exists(search_path):
                return {
                    "success": False,
                    "message": f"Search path not found: {search_path}",
                    "action": "search_file"
                }
            
            results = []
            name_lower = name.lower()
            
            for root, dirs, files in os.walk(search_path):
                # Skip hidden and system directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['Windows', 'Program Files', 'Program Files (x86)']]
                
                for file in files:
                    if name_lower in file.lower():
                        file_path = os.path.join(root, file)
                        results.append({
                            "name": file,
                            "path": file_path,
                            "directory": root,
                            "size": os.path.getsize(file_path)
                        })
                        
                        # Limit results
                        if len(results) >= 50:
                            return {
                                "success": True,
                                "query": name,
                                "search_path": search_path,
                                "results": results,
                                "count": len(results),
                                "truncated": True,
                                "message": f"Found {len(results)}+ files (results truncated)",
                                "action": "search_file"
                            }
            
            return {
                "success": True,
                "query": name,
                "search_path": search_path,
                "results": results,
                "count": len(results),
                "message": f"Found {len(results)} file(s)",
                "action": "search_file"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Open File ==============

    def open_file(self, filepath: str) -> Dict[str, Any]:
        """
        Open a file with its default application.
        
        Args:
            filepath: Path to file
            
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(filepath):
                return {
                    "success": False,
                    "message": f"File not found: {filepath}",
                    "action": "open_file"
                }
            
            os.startfile(filepath)
            
            return {
                "success": True,
                "message": f"Opening: {os.path.basename(filepath)}",
                "path": filepath,
                "action": "open_file"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def open_folder(self, folder_path: str) -> Dict[str, Any]:
        """
        Open a folder in file explorer.
        
        Args:
            folder_path: Path to folder
            
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(folder_path):
                return {
                    "success": False,
                    "message": f"Folder not found: {folder_path}",
                    "action": "open_folder"
                }
            
            os.startfile(folder_path)
            
            return {
                "success": True,
                "message": f"Opening: {folder_path}",
                "path": folder_path,
                "action": "open_folder"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== File Info ==============

    def get_file_info(self, filepath: str) -> Dict[str, Any]:
        """
        Get detailed file information.
        
        Args:
            filepath: Path to file
            
        Returns:
            Dictionary with file info
        """
        try:
            if not os.path.exists(filepath):
                return {
                    "success": False,
                    "message": f"File not found: {filepath}",
                    "action": "get_file_info"
                }
            
            stat = os.stat(filepath)
            
            return {
                "success": True,
                "path": filepath,
                "name": os.path.basename(filepath),
                "size": stat.st_size,
                "size_formatted": self._format_size(stat.st_size),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
                "is_file": os.path.isfile(filepath),
                "is_directory": os.path.isdir(filepath),
                "action": "get_file_info"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _format_size(self, size: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"

    # ============== Zip/Unzip ==============

    def zip_folder(self, folder_path: str, output_path: str = None) -> Dict[str, Any]:
        """
        Create a zip archive of a folder.
        
        Args:
            folder_path: Path to folder to zip
            output_path: Output zip file path (default: folder_name.zip)
            
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(folder_path):
                return {
                    "success": False,
                    "message": f"Folder not found: {folder_path}",
                    "action": "zip_folder"
                }
            
            if not os.path.isdir(folder_path):
                return {
                    "success": False,
                    "message": f"Not a folder: {folder_path}",
                    "action": "zip_folder"
                }
            
            # Generate output path if not provided
            if output_path is None:
                folder_name = os.path.basename(folder_path)
                output_path = f"{folder_name}.zip"
            
            # Create zip archive
            shutil.make_archive(output_path.replace('.zip', ''), 'zip', folder_path)
            
            # Ensure .zip extension
            if not output_path.endswith('.zip'):
                output_path += '.zip'
            
            return {
                "success": True,
                "message": f"Folder zipped: {output_path}",
                "source": folder_path,
                "output": output_path,
                "action": "zip_folder"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def unzip_file(self, zip_path: str, extract_to: str = None) -> Dict[str, Any]:
        """
        Extract a zip file.
        
        Args:
            zip_path: Path to zip file
            extract_to: Extraction directory (default: current directory)
            
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(zip_path):
                return {
                    "success": False,
                    "message": f"Zip file not found: {zip_path}",
                    "action": "unzip_file"
                }
            
            if not zipfile.is_zipfile(zip_path):
                return {
                    "success": False,
                    "message": f"Not a valid zip file: {zip_path}",
                    "action": "unzip_file"
                }
            
            # Create extraction directory if not provided
            if extract_to is None:
                extract_to = os.path.dirname(zip_path) or '.'
            
            os.makedirs(extract_to, exist_ok=True)
            
            # Extract zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            
            return {
                "success": True,
                "message": f"Extracted to: {extract_to}",
                "source": zip_path,
                "destination": extract_to,
                "action": "unzip_file"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== System Folders ==============

    def open_documents(self) -> Dict[str, Any]:
        """Open Documents folder."""
        return self.open_folder(str(self.documents))

    def open_downloads(self) -> Dict[str, Any]:
        """Open Downloads folder."""
        return self.open_folder(str(self.downloads))

    def open_pictures(self) -> Dict[str, Any]:
        """Open Pictures folder."""
        return self.open_folder(str(self.pictures))

    def open_desktop(self) -> Dict[str, Any]:
        """Open Desktop folder."""
        return self.open_folder(str(self.home / "Desktop"))

    def open_home(self) -> Dict[str, Any]:
        """Open user home folder."""
        return self.open_folder(str(self.home))

    # ============== Utilities ==============

    def get_directory_size(self, path: str) -> Dict[str, Any]:
        """
        Get total size of a directory.
        
        Args:
            path: Directory path
            
        Returns:
            Size dictionary
        """
        try:
            total_size = 0
            file_count = 0
            
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        total_size += os.path.getsize(filepath)
                        file_count += 1
            
            return {
                "success": True,
                "path": path,
                "total_size": total_size,
                "total_size_formatted": self._format_size(total_size),
                "file_count": file_count,
                "action": "get_directory_size"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_status(self) -> Dict[str, Any]:
        """Get file manager status."""
        return {
            "available": True,
            "home": str(self.home),
            "documents": str(self.documents),
            "downloads": str(self.downloads),
            "pictures": str(self.pictures),
            "current_directory": os.getcwd()
        }
