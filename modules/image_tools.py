"""
ARIA - Advanced Real-time Intelligent Assistant
Image Tools Module - Image processing, OCR, and PDF conversion
"""

import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from PIL import Image


class ImageTools:
    """
    Image processing tools - conversion, OCR, resize, format change, compression.
    Handles image to PDF, batch processing, and image manipulation.
    """

    def __init__(self):
        """Initialize image tools."""
        # Output directory for processed images
        self.output_dir = os.path.join(
            os.path.expanduser("~"),
            "Pictures",
            "ARIA Edited"
        )
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Supported formats
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']

    def _get_output_path(self, filename: str) -> str:
        """Get full output path for processed image."""
        return os.path.join(self.output_dir, filename)

    def _generate_filename(self, prefix: str = "image", extension: str = ".png") -> str:
        """Generate timestamped filename."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}{extension}"

    # ============== Image to PDF ==============

    def image_to_pdf(self, image_path: str, output_path: str = None) -> Dict[str, Any]:
        """
        Convert a single image to PDF.
        
        Args:
            image_path: Path to input image
            output_path: Output PDF path (default: auto-generated)
            
        Returns:
            Status dictionary
        """
        try:
            # Check if image exists
            if not os.path.exists(image_path):
                return {
                    "success": False,
                    "message": f"Image not found: {image_path}",
                    "action": "image_to_pdf"
                }
            
            # Generate output path if not provided
            if output_path is None:
                output_path = self._get_output_path(
                    self._generate_filename("image", ".pdf")
                )
            elif not output_path.endswith('.pdf'):
                output_path += '.pdf'
            
            # Open and convert image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary (for JPEG)
            if image.mode in ('RGBA', 'P'):
                image = image.convert('RGB')
            
            # Save as PDF
            image.save(output_path, 'PDF', resolution=100.0)
            
            return {
                "success": True,
                "message": "Image converted to PDF",
                "input": image_path,
                "output": output_path,
                "action": "image_to_pdf"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def batch_images_to_pdf(self, folder_path: str, output_path: str = None) -> Dict[str, Any]:
        """
        Convert all images in a folder to a single PDF.
        
        Args:
            folder_path: Path to folder containing images
            output_path: Output PDF path (default: auto-generated)
            
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(folder_path):
                return {
                    "success": False,
                    "message": f"Folder not found: {folder_path}",
                    "action": "batch_images_to_pdf"
                }
            
            # Get all images in folder
            image_files = []
            for filename in os.listdir(folder_path):
                if any(filename.lower().endswith(ext) for ext in self.supported_formats):
                    image_files.append(os.path.join(folder_path, filename))
            
            if not image_files:
                return {
                    "success": False,
                    "message": "No images found in folder",
                    "action": "batch_images_to_pdf"
                }
            
            # Generate output path if not provided
            if output_path is None:
                folder_name = os.path.basename(folder_path)
                output_path = self._get_output_path(
                    f"{folder_name}_combined_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                )
            elif not output_path.endswith('.pdf'):
                output_path += '.pdf'
            
            # Convert images to PDF
            pdf_images = []
            for img_path in sorted(image_files):
                try:
                    image = Image.open(img_path)
                    if image.mode in ('RGBA', 'P'):
                        image = image.convert('RGB')
                    pdf_images.append(image)
                except Exception as e:
                    print(f"Skipping {img_path}: {e}")
            
            if not pdf_images:
                return {
                    "success": False,
                    "message": "No valid images could be processed",
                    "action": "batch_images_to_pdf"
                }
            
            # Save first image with others appended
            pdf_images[0].save(
                output_path,
                'PDF',
                resolution=100.0,
                save_all=True,
                append_images=pdf_images[1:]
            )
            
            return {
                "success": True,
                "message": f"Created PDF with {len(pdf_images)} images",
                "input_folder": folder_path,
                "output": output_path,
                "image_count": len(pdf_images),
                "action": "batch_images_to_pdf"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== OCR - Text Extraction ==============

    def extract_text_ocr(self, image_path: str) -> Dict[str, Any]:
        """
        Extract text from image using OCR (pytesseract).
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with extracted text
        """
        try:
            # Import pytesseract
            try:
                import pytesseract
            except ImportError:
                return {
                    "success": False,
                    "message": "pytesseract not installed. Run: pip install pytesseract",
                    "action": "extract_text_ocr"
                }
            
            if not os.path.exists(image_path):
                return {
                    "success": False,
                    "message": f"Image not found: {image_path}",
                    "action": "extract_text_ocr"
                }
            
            # Open image
            image = Image.open(image_path)
            
            # Perform OCR
            text = pytesseract.image_to_string(image)
            
            return {
                "success": True,
                "message": "Text extracted from image",
                "text": text.strip() if text.strip() else "No text found in image",
                "text_length": len(text.strip()) if text.strip() else 0,
                "image_path": image_path,
                "action": "extract_text_ocr"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def extract_text_from_images_batch(self, folder_path: str) -> Dict[str, Any]:
        """
        Extract text from all images in a folder.
        
        Args:
            folder_path: Path to folder containing images
            
        Returns:
            Dictionary with extracted text from all images
        """
        try:
            import pytesseract
            
            if not os.path.exists(folder_path):
                return {
                    "success": False,
                    "message": f"Folder not found: {folder_path}",
                    "action": "extract_text_from_images_batch"
                }
            
            results = []
            total_text = []
            
            for filename in os.listdir(folder_path):
                if any(filename.lower().endswith(ext) for ext in self.supported_formats):
                    img_path = os.path.join(folder_path, filename)
                    
                    try:
                        image = Image.open(img_path)
                        text = pytesseract.image_to_string(image)
                        
                        results.append({
                            "filename": filename,
                            "text": text.strip() if text.strip() else "No text found",
                            "text_length": len(text.strip()) if text.strip() else 0
                        })
                        
                        total_text.append(f"=== {filename} ===\n{text}")
                        
                    except Exception as e:
                        results.append({
                            "filename": filename,
                            "error": str(e)
                        })
            
            return {
                "success": True,
                "message": f"Processed {len(results)} images",
                "results": results,
                "combined_text": "\n\n".join(total_text),
                "action": "extract_text_from_images_batch"
            }
            
        except ImportError:
            return {
                "success": False,
                "message": "pytesseract not installed",
                "action": "extract_text_from_images_batch"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Image Manipulation ==============

    def resize_image(self, path: str, width: int, height: int = None, maintain_aspect: bool = True) -> Dict[str, Any]:
        """
        Resize an image.
        
        Args:
            path: Path to input image
            width: New width
            height: New height (None to calculate from aspect ratio)
            maintain_aspect: Maintain aspect ratio
            
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(path):
                return {
                    "success": False,
                    "message": f"Image not found: {path}",
                    "action": "resize_image"
                }
            
            # Open image
            image = Image.open(path)
            original_size = image.size
            
            # Calculate height if not provided
            if height is None and maintain_aspect:
                aspect_ratio = image.height / image.width
                height = int(width * aspect_ratio)
            
            # Resize
            if maintain_aspect:
                image = image.resize((width, height), Image.Resampling.LANCZOS)
            else:
                image = image.resize((width, height), Image.Resampling.LANCZOS)
            
            # Generate output path
            filename = self._generate_filename("resized", self._get_extension(path))
            output_path = self._get_output_path(filename)
            
            # Save
            image.save(output_path, quality=95)
            
            return {
                "success": True,
                "message": f"Image resized to {width}x{height}",
                "input": path,
                "output": output_path,
                "original_size": list(original_size),
                "new_size": [width, height],
                "action": "resize_image"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def convert_format(self, path: str, target_format: str) -> Dict[str, Any]:
        """
        Convert image to different format.
        
        Args:
            path: Path to input image
            target_format: Target format (jpg, png, bmp, gif, webp, tiff)
            
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(path):
                return {
                    "success": False,
                    "message": f"Image not found: {path}",
                    "action": "convert_format"
                }
            
            target_format = target_format.lower().lstrip('.')
            
            # Map format to extension
            format_map = {
                'jpg': ('JPEG', '.jpg'),
                'jpeg': ('JPEG', '.jpeg'),
                'png': ('PNG', '.png'),
                'bmp': ('BMP', '.bmp'),
                'gif': ('GIF', '.gif'),
                'webp': ('WEBP', '.webp'),
                'tiff': ('TIFF', '.tiff')
            }
            
            if target_format not in format_map:
                return {
                    "success": False,
                    "message": f"Unsupported format: {target_format}",
                    "supported": list(format_map.keys()),
                    "action": "convert_format"
                }
            
            pil_format, extension = format_map[target_format]
            
            # Open image
            image = Image.open(path)
            
            # Convert mode if necessary
            if target_format in ['jpg', 'jpeg'] and image.mode in ('RGBA', 'P'):
                image = image.convert('RGB')
            
            # Generate output path
            filename = self._generate_filename("converted", extension)
            output_path = self._get_output_path(filename)
            
            # Save
            image.save(output_path, pil_format)
            
            return {
                "success": True,
                "message": f"Image converted to {target_format.upper()}",
                "input": path,
                "output": output_path,
                "format": target_format.upper(),
                "action": "convert_format"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def compress_image(self, path: str, quality: int = 85, max_size: int = None) -> Dict[str, Any]:
        """
        Compress an image by reducing quality and/or size.
        
        Args:
            path: Path to input image
            quality: JPEG quality (1-100, default: 85)
            max_size: Maximum dimension (width or height), None to keep original
            
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(path):
                return {
                    "success": False,
                    "message": f"Image not found: {path}",
                    "action": "compress_image"
                }
            
            quality = max(1, min(100, quality))
            
            # Open image
            image = Image.open(path)
            original_size = image.size
            original_format = image.format
            
            # Resize if max_size specified
            if max_size:
                ratio = min(max_size / image.width, max_size / image.height)
                if ratio < 1:
                    new_size = (int(image.width * ratio), int(image.height * ratio))
                    image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Determine output format
            if original_format in ['JPEG', 'JPG']:
                output_format = 'JPEG'
                extension = '.jpg'
                # Convert to RGB if necessary
                if image.mode in ('RGBA', 'P'):
                    image = image.convert('RGB')
            elif original_format == 'PNG':
                output_format = 'PNG'
                extension = '.png'
            else:
                output_format = 'JPEG'
                extension = '.jpg'
                if image.mode in ('RGBA', 'P'):
                    image = image.convert('RGB')
            
            # Generate output path
            filename = self._generate_filename("compressed", extension)
            output_path = self._get_output_path(filename)
            
            # Save with compression
            if output_format == 'JPEG':
                image.save(output_path, output_format, quality=quality, optimize=True)
            elif output_format == 'PNG':
                image.save(output_path, output_format, optimize=True)
            else:
                image.save(output_path, output_format, quality=quality)
            
            # Get compressed size
            compressed_size = os.path.getsize(output_path)
            original_size_bytes = os.path.getsize(path)
            compression_ratio = (1 - compressed_size / original_size_bytes) * 100
            
            return {
                "success": True,
                "message": f"Image compressed ({compression_ratio:.1f}% reduction)",
                "input": path,
                "output": output_path,
                "original_size_bytes": original_size_bytes,
                "compressed_size_bytes": compressed_size,
                "compression_ratio": round(compression_ratio, 2),
                "quality": quality,
                "action": "compress_image"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Utilities ==============

    def _get_extension(self, path: str) -> str:
        """Get file extension."""
        _, ext = os.path.splitext(path)
        return ext.lower()

    def get_image_info(self, path: str) -> Dict[str, Any]:
        """
        Get detailed image information.
        
        Args:
            path: Path to image
            
        Returns:
            Dictionary with image info
        """
        try:
            if not os.path.exists(path):
                return {
                    "success": False,
                    "message": f"Image not found: {path}",
                    "action": "get_image_info"
                }
            
            image = Image.open(path)
            
            return {
                "success": True,
                "path": path,
                "filename": os.path.basename(path),
                "format": image.format,
                "mode": image.mode,
                "size": image.size,
                "width": image.width,
                "height": image.height,
                "file_size": os.path.getsize(path),
                "file_size_formatted": self._format_size(os.path.getsize(path)),
                "action": "get_image_info"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _format_size(self, size: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"

    def get_supported_formats(self) -> List[str]:
        """Get list of supported image formats."""
        return self.supported_formats.copy()

    def get_status(self) -> Dict[str, Any]:
        """Get image tools status."""
        return {
            "available": True,
            "output_dir": self.output_dir,
            "supported_formats": self.supported_formats,
            "capabilities": [
                "image_to_pdf", "batch_to_pdf", "ocr",
                "resize", "convert_format", "compress"
            ]
        }
