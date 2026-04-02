"""
ZARA - Advanced Real-time Intelligent Assistant
PDF Tools Module - PDF manipulation and processing
"""

import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path


class PDFTools:
    """
    PDF manipulation tools - merge, split, read, create PDFs.
    Handles PDF operations using PyPDF2 and fpdf2.
    """

    def __init__(self):
        """Initialize PDF tools."""
        # Output directory for processed PDFs
        self.output_dir = os.path.join(
            os.path.expanduser("~"),
            "Documents",
            "ARIA PDFs"
        )
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Supported PDF extensions
        self.pdf_extensions = ['.pdf']

    def _get_output_path(self, filename: str) -> str:
        """Get full output path for processed PDF."""
        return os.path.join(self.output_dir, filename)

    def _generate_filename(self, prefix: str = "pdf") -> str:
        """Generate timestamped filename."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.pdf"

    # ============== Merge PDFs ==============

    def merge_pdfs(self, pdf_list: List[str], output_path: str = None) -> Dict[str, Any]:
        """
        Merge multiple PDFs into one.
        
        Args:
            pdf_list: List of PDF file paths to merge
            output_path: Output PDF path (default: auto-generated)
            
        Returns:
            Status dictionary
        """
        try:
            # Import PyPDF2
            try:
                from PyPDF2 import PdfMerger
            except ImportError:
                return {
                    "success": False,
                    "message": "PyPDF2 not installed. Run: pip install PyPDF2",
                    "action": "merge_pdfs"
                }
            
            # Validate input files
            valid_pdfs = []
            for pdf_path in pdf_list:
                if os.path.exists(pdf_path) and pdf_path.lower().endswith('.pdf'):
                    valid_pdfs.append(pdf_path)
                else:
                    print(f"Skipping invalid PDF: {pdf_path}")
            
            if not valid_pdfs:
                return {
                    "success": False,
                    "message": "No valid PDF files provided",
                    "action": "merge_pdfs"
                }
            
            # Generate output path if not provided
            if output_path is None:
                output_path = self._get_output_path(self._generate_filename("merged"))
            elif not output_path.endswith('.pdf'):
                output_path += '.pdf'
            
            # Create merger
            merger = PdfMerger()
            
            # Add PDFs
            for pdf in valid_pdfs:
                merger.append(pdf)
            
            # Write output
            merger.write(output_path)
            merger.close()
            
            return {
                "success": True,
                "message": f"Merged {len(valid_pdfs)} PDFs",
                "input_files": valid_pdfs,
                "output": output_path,
                "merged_count": len(valid_pdfs),
                "action": "merge_pdfs"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def merge_folder_pdfs(self, folder_path: str, output_path: str = None) -> Dict[str, Any]:
        """
        Merge all PDFs in a folder.
        
        Args:
            folder_path: Path to folder containing PDFs
            output_path: Output PDF path
            
        Returns:
            Status dictionary
        """
        try:
            from PyPDF2 import PdfMerger
            
            if not os.path.exists(folder_path):
                return {
                    "success": False,
                    "message": f"Folder not found: {folder_path}",
                    "action": "merge_folder_pdfs"
                }
            
            # Get all PDFs in folder
            pdf_files = []
            for filename in os.listdir(folder_path):
                if filename.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(folder_path, filename))
            
            if not pdf_files:
                return {
                    "success": False,
                    "message": "No PDF files found in folder",
                    "action": "merge_folder_pdfs"
                }
            
            # Sort by filename
            pdf_files.sort()
            
            # Generate output path
            if output_path is None:
                folder_name = os.path.basename(folder_path)
                output_path = self._get_output_path(
                    f"{folder_name}_merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                )
            
            # Merge
            merger = PdfMerger()
            for pdf in pdf_files:
                merger.append(pdf)
            
            merger.write(output_path)
            merger.close()
            
            return {
                "success": True,
                "message": f"Merged {len(pdf_files)} PDFs from folder",
                "input_folder": folder_path,
                "output": output_path,
                "merged_count": len(pdf_files),
                "action": "merge_folder_pdfs"
            }
            
        except ImportError:
            return {
                "success": False,
                "message": "PyPDF2 not installed",
                "action": "merge_folder_pdfs"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Split PDF ==============

    def split_pdf(self, pdf_path: str, output_folder: str = None) -> Dict[str, Any]:
        """
        Split PDF into individual pages.
        
        Args:
            pdf_path: Path to input PDF
            output_folder: Output folder (default: auto-created)
            
        Returns:
            Status dictionary
        """
        try:
            from PyPDF2 import PdfReader, PdfWriter
            
            if not os.path.exists(pdf_path):
                return {
                    "success": False,
                    "message": f"PDF not found: {pdf_path}",
                    "action": "split_pdf"
                }
            
            # Create output folder
            if output_folder is None:
                pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
                output_folder = self._get_output_path(f"{pdf_name}_split")
            
            os.makedirs(output_folder, exist_ok=True)
            
            # Read PDF
            reader = PdfReader(pdf_path)
            total_pages = len(reader.pages)
            
            if total_pages == 0:
                return {
                    "success": False,
                    "message": "PDF has no pages",
                    "action": "split_pdf"
                }
            
            # Split into individual pages
            output_files = []
            
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                
                output_filename = f"page_{i+1:03d}.pdf"
                output_path = os.path.join(output_folder, output_filename)
                
                with open(output_path, 'wb') as f:
                    writer.write(f)
                
                output_files.append(output_path)
            
            return {
                "success": True,
                "message": f"Split PDF into {total_pages} pages",
                "input": pdf_path,
                "output_folder": output_folder,
                "pages": total_pages,
                "output_files": output_files,
                "action": "split_pdf"
            }
            
        except ImportError:
            return {
                "success": False,
                "message": "PyPDF2 not installed",
                "action": "split_pdf"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def extract_pages(self, pdf_path: str, pages: List[int], output_path: str = None) -> Dict[str, Any]:
        """
        Extract specific pages from PDF.
        
        Args:
            pdf_path: Path to input PDF
            pages: List of page numbers (1-indexed)
            output_path: Output PDF path
            
        Returns:
            Status dictionary
        """
        try:
            from PyPDF2 import PdfReader, PdfWriter
            
            if not os.path.exists(pdf_path):
                return {
                    "success": False,
                    "message": f"PDF not found: {pdf_path}",
                    "action": "extract_pages"
                }
            
            reader = PdfReader(pdf_path)
            total_pages = len(reader.pages)
            
            # Generate output path
            if output_path is None:
                output_path = self._get_output_path(self._generate_filename("extracted"))
            
            # Create writer
            writer = PdfWriter()
            
            # Add selected pages (convert to 0-indexed)
            for page_num in pages:
                if 1 <= page_num <= total_pages:
                    writer.add_page(reader.pages[page_num - 1])
            
            # Write output
            with open(output_path, 'wb') as f:
                writer.write(f)
            
            return {
                "success": True,
                "message": f"Extracted {len(pages)} pages",
                "input": pdf_path,
                "output": output_path,
                "pages_extracted": len(pages),
                "action": "extract_pages"
            }
            
        except ImportError:
            return {
                "success": False,
                "message": "PyPDF2 not installed",
                "action": "extract_pages"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Read PDF ==============

    def read_pdf(self, pdf_path: str, pages: List[int] = None) -> Dict[str, Any]:
        """
        Extract text from PDF.
        
        Args:
            pdf_path: Path to PDF file
            pages: List of page numbers to read (None for all)
            
        Returns:
            Dictionary with extracted text
        """
        try:
            from PyPDF2 import PdfReader
            
            if not os.path.exists(pdf_path):
                return {
                    "success": False,
                    "message": f"PDF not found: {pdf_path}",
                    "action": "read_pdf"
                }
            
            reader = PdfReader(pdf_path)
            total_pages = len(reader.pages)
            
            # Determine which pages to read
            if pages is None:
                pages_to_read = list(range(total_pages))
            else:
                pages_to_read = [p - 1 for p in pages if 1 <= p <= total_pages]  # Convert to 0-indexed
            
            # Extract text
            text_parts = []
            
            for i in pages_to_read:
                page = reader.pages[i]
                text = page.extract_text()
                if text:
                    text_parts.append(f"--- Page {i + 1} ---\n{text}")
            
            full_text = "\n\n".join(text_parts)
            
            return {
                "success": True,
                "message": f"Extracted text from {len(pages_to_read)} page(s)",
                "path": pdf_path,
                "total_pages": total_pages,
                "pages_read": len(pages_to_read),
                "text": full_text.strip() if full_text.strip() else "No text found in PDF",
                "text_length": len(full_text.strip()) if full_text.strip() else 0,
                "action": "read_pdf"
            }
            
        except ImportError:
            return {
                "success": False,
                "message": "PyPDF2 not installed",
                "action": "read_pdf"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def read_pdf_summary(self, pdf_path: str) -> Dict[str, Any]:
        """
        Get PDF summary (first page text).
        
        Args:
            pdf_path: Path to PDF
            
        Returns:
            Dictionary with summary
        """
        try:
            from PyPDF2 import PdfReader
            
            if not os.path.exists(pdf_path):
                return {
                    "success": False,
                    "message": f"PDF not found: {pdf_path}",
                    "action": "read_pdf_summary"
                }
            
            reader = PdfReader(pdf_path)
            
            if len(reader.pages) == 0:
                return {
                    "success": False,
                    "message": "PDF has no pages",
                    "action": "read_pdf_summary"
                }
            
            # Get first page text
            first_page = reader.pages[0]
            text = first_page.extract_text()
            
            return {
                "success": True,
                "message": "PDF summary extracted",
                "path": pdf_path,
                "total_pages": len(reader.pages),
                "summary": text.strip()[:500] if text.strip() else "No text found",
                "action": "read_pdf_summary"
            }
            
        except ImportError:
            return {
                "success": False,
                "message": "PyPDF2 not installed",
                "action": "read_pdf_summary"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Folder Operations ==============

    def folder_to_pdf(self, folder_path: str, output_path: str = None) -> Dict[str, Any]:
        """
        Create a PDF summary of all files in a folder.
        
        Args:
            folder_path: Path to folder
            output_path: Output PDF path
            
        Returns:
            Status dictionary
        """
        try:
            from fpdf import FPDF
            
            if not os.path.exists(folder_path):
                return {
                    "success": False,
                    "message": f"Folder not found: {folder_path}",
                    "action": "folder_to_pdf"
                }
            
            # Get all files
            files = []
            for filename in os.listdir(folder_path):
                filepath = os.path.join(folder_path, filename)
                if os.path.isfile(filepath):
                    files.append({
                        "name": filename,
                        "size": os.path.getsize(filepath),
                        "modified": datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
                    })
            
            if not files:
                return {
                    "success": False,
                    "message": "Folder is empty",
                    "action": "folder_to_pdf"
                }
            
            # Generate output path
            if output_path is None:
                folder_name = os.path.basename(folder_path)
                output_path = self._get_output_path(
                    f"{folder_name}_contents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                )
            
            # Create PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            
            # Title
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, f"Folder Contents: {os.path.basename(folder_path)}", ln=True)
            pdf.ln(5)
            
            # File list
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 10, f"Total Files: {len(files)}", ln=True)
            pdf.ln(5)
            
            # Table header
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(80, 8, 'Filename', 1)
            pdf.cell(40, 8, 'Size', 1)
            pdf.cell(70, 8, 'Modified', 1)
            pdf.ln()
            
            # File rows
            pdf.set_font('Arial', '', 10)
            for file in sorted(files, key=lambda x: x['name']):
                size_kb = file['size'] / 1024
                size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb/1024:.2f} MB"
                
                # Handle long filenames
                name = file['name'][:35] + '...' if len(file['name']) > 38 else file['name']
                
                pdf.cell(80, 8, name, 1)
                pdf.cell(40, 8, size_str, 1)
                pdf.cell(70, 8, file['modified'][:10], 1)
                pdf.ln()
            
            # Save PDF
            pdf.output(output_path)
            
            return {
                "success": True,
                "message": f"Created PDF with {len(files)} files",
                "input_folder": folder_path,
                "output": output_path,
                "file_count": len(files),
                "action": "folder_to_pdf"
            }
            
        except ImportError:
            return {
                "success": False,
                "message": "fpdf2 not installed. Run: pip install fpdf2",
                "action": "folder_to_pdf"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def scan_folder_pdfs(self, folder_path: str) -> Dict[str, Any]:
        """
        List all PDF files in a folder.
        
        Args:
            folder_path: Path to folder
            
        Returns:
            Dictionary with PDF list
        """
        try:
            if not os.path.exists(folder_path):
                return {
                    "success": False,
                    "message": f"Folder not found: {folder_path}",
                    "action": "scan_folder_pdfs"
                }
            
            pdfs = []
            
            for filename in os.listdir(folder_path):
                if filename.lower().endswith('.pdf'):
                    filepath = os.path.join(folder_path, filename)
                    pdfs.append({
                        "name": filename,
                        "path": filepath,
                        "size": os.path.getsize(filepath),
                        "size_formatted": self._format_size(os.path.getsize(filepath))
                    })
            
            return {
                "success": True,
                "message": f"Found {len(pdfs)} PDF(s)",
                "folder": folder_path,
                "pdfs": pdfs,
                "count": len(pdfs),
                "action": "scan_folder_pdfs"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== PDF Info ==============

    def get_pdf_info(self, pdf_path: str) -> Dict[str, Any]:
        """
        Get detailed PDF information.
        
        Args:
            pdf_path: Path to PDF
            
        Returns:
            Dictionary with PDF info
        """
        try:
            from PyPDF2 import PdfReader
            
            if not os.path.exists(pdf_path):
                return {
                    "success": False,
                    "message": f"PDF not found: {pdf_path}",
                    "action": "get_pdf_info"
                }
            
            reader = PdfReader(pdf_path)
            
            # Get metadata
            metadata = {}
            if reader.metadata:
                metadata = {
                    "title": reader.metadata.get('/Title', 'N/A'),
                    "author": reader.metadata.get('/Author', 'N/A'),
                    "subject": reader.metadata.get('/Subject', 'N/A'),
                    "creator": reader.metadata.get('/Creator', 'N/A'),
                    "producer": reader.metadata.get('/Producer', 'N/A'),
                    "creation_date": reader.metadata.get('/CreationDate', 'N/A')
                }
            
            return {
                "success": True,
                "path": pdf_path,
                "filename": os.path.basename(pdf_path),
                "pages": len(reader.pages),
                "file_size": os.path.getsize(pdf_path),
                "file_size_formatted": self._format_size(os.path.getsize(pdf_path)),
                "metadata": metadata,
                "is_encrypted": reader.is_encrypted,
                "action": "get_pdf_info"
            }
            
        except ImportError:
            return {
                "success": False,
                "message": "PyPDF2 not installed",
                "action": "get_pdf_info"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Utilities ==============

    def _format_size(self, size: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"

    def create_text_pdf(self, text: str, output_path: str = None) -> Dict[str, Any]:
        """
        Create PDF from text content.
        
        Args:
            text: Text content
            output_path: Output PDF path
            
        Returns:
            Status dictionary
        """
        try:
            from fpdf import FPDF
            
            if output_path is None:
                output_path = self._get_output_path(self._generate_filename("document"))
            
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font('Arial', '', 12)
            
            # Handle text encoding
            text = text.encode('latin-1', 'replace').decode('latin-1')
            
            # Add text line by line
            for line in text.split('\n'):
                # Handle long lines
                while len(line) > 180:
                    pdf.cell(0, 10, line[:180], ln=True)
                    line = line[180:]
                pdf.cell(0, 10, line, ln=True)
            
            pdf.output(output_path)
            
            return {
                "success": True,
                "message": "PDF created from text",
                "output": output_path,
                "text_length": len(text),
                "action": "create_text_pdf"
            }
            
        except ImportError:
            return {
                "success": False,
                "message": "fpdf2 not installed",
                "action": "create_text_pdf"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_status(self) -> Dict[str, Any]:
        """Get PDF tools status."""
        return {
            "available": True,
            "output_dir": self.output_dir,
            "capabilities": [
                "merge_pdfs", "split_pdf", "read_pdf",
                "extract_pages", "folder_to_pdf", "get_pdf_info"
            ]
        }
