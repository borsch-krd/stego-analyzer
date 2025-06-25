#!/usr/bin/env python3
"""
Steganography Analyzer
A comprehensive tool for steganography analysis and extraction using multiple tools.
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json
import argparse
from colorama import init, Fore, Style
import logging

# Initialize colorama for Windows
init()

class StegoAnalyzer:
    """Main steganography analyzer class"""
    
    def __init__(self):
        self.results = {}
        self.temp_dir = tempfile.mkdtemp(prefix="stego_")
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('stego_analyzer.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def check_tool_availability(self) -> Dict[str, bool]:
        """Check which tools are available on the system"""
        tools = {
            'zsteg': self._check_command('zsteg'),
            'steghide': self._check_command('steghide'),
            'outguess': self._check_command('outguess'),
            'exiftool': self._check_command('exiftool'),
            'binwalk': self._check_command('binwalk'),
            'foremost': self._check_command('foremost'),
            'strings': self._check_command('strings')
        }
        return tools
    
    def _check_command(self, command: str) -> bool:
        """Check if a command is available in PATH"""
        try:
            result = subprocess.run([command, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            try:
                result = subprocess.run([command, '-h'], 
                                      capture_output=True, text=True, timeout=5)
                return result.returncode == 0
            except:
                return False
    
    def run_zsteg(self, file_path: str) -> Dict:
        """Run zsteg analysis on image files"""
        if not self._check_command('zsteg'):
            return {"error": "zsteg not available"}
        
        try:
            result = subprocess.run(['zsteg', '-a', file_path], 
                                  capture_output=True, text=True, timeout=60)
            return {
                "tool": "zsteg",
                "output": result.stdout,
                "errors": result.stderr,
                "success": result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {"error": "zsteg analysis timed out"}
        except Exception as e:
            return {"error": f"zsteg error: {str(e)}"}
    
    def run_steghide(self, file_path: str, password: str = "") -> Dict:
        """Run steghide analysis"""
        if not self._check_command('steghide'):
            return {"error": "steghide not available"}
        
        try:
            # Try to extract with steghide
            output_file = os.path.join(self.temp_dir, "steghide_output.txt")
            cmd = ['steghide', 'extract', '-sf', file_path, '-xf', output_file]
            if password:
                cmd.extend(['-p', password])
            else:
                cmd.extend(['-p', ''])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            extracted_content = ""
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8', errors='ignore') as f:
                    extracted_content = f.read()
            
            return {
                "tool": "steghide",
                "output": result.stdout,
                "errors": result.stderr,
                "extracted_content": extracted_content,
                "success": result.returncode == 0
            }
        except Exception as e:
            return {"error": f"steghide error: {str(e)}"}
    
    def run_outguess(self, file_path: str) -> Dict:
        """Run outguess analysis"""
        if not self._check_command('outguess'):
            return {"error": "outguess not available"}
        
        try:
            output_file = os.path.join(self.temp_dir, "outguess_output.txt")
            result = subprocess.run(['outguess', '-r', file_path, output_file], 
                                  capture_output=True, text=True, timeout=30)
            
            extracted_content = ""
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8', errors='ignore') as f:
                    extracted_content = f.read()
            
            return {
                "tool": "outguess",
                "output": result.stdout,
                "errors": result.stderr,
                "extracted_content": extracted_content,
                "success": result.returncode == 0
            }
        except Exception as e:
            return {"error": f"outguess error: {str(e)}"}
    
    def run_exiftool(self, file_path: str) -> Dict:
        """Run exiftool to extract metadata"""
        if not self._check_command('exiftool'):
            return {"error": "exiftool not available"}
        
        try:
            result = subprocess.run(['exiftool', '-j', file_path], 
                                  capture_output=True, text=True, timeout=30)
            metadata = {}
            if result.stdout:
                try:
                    metadata = json.loads(result.stdout)[0] if result.stdout.strip().startswith('[') else {}
                except json.JSONDecodeError:
                    pass
            
            return {
                "tool": "exiftool",
                "metadata": metadata,
                "raw_output": result.stdout,
                "errors": result.stderr,
                "success": result.returncode == 0
            }
        except Exception as e:
            return {"error": f"exiftool error: {str(e)}"}
    
    def run_binwalk(self, file_path: str) -> Dict:
        """Run binwalk analysis"""
        if not self._check_command('binwalk'):
            return {"error": "binwalk not available"}
        
        try:
            # Run binwalk with extraction
            extract_dir = os.path.join(self.temp_dir, "binwalk_extract")
            os.makedirs(extract_dir, exist_ok=True)
            
            result = subprocess.run(['binwalk', '-e', '-C', extract_dir, file_path], 
                                  capture_output=True, text=True, timeout=60)
            
            # Also run signature analysis
            sig_result = subprocess.run(['binwalk', file_path], 
                                      capture_output=True, text=True, timeout=30)
            
            return {
                "tool": "binwalk",
                "signatures": sig_result.stdout,
                "extraction_output": result.stdout,
                "errors": result.stderr,
                "extract_dir": extract_dir,
                "success": result.returncode == 0
            }
        except Exception as e:
            return {"error": f"binwalk error: {str(e)}"}
    
    def run_foremost(self, file_path: str) -> Dict:
        """Run foremost file carving"""
        if not self._check_command('foremost'):
            return {"error": "foremost not available"}
        
        try:
            output_dir = os.path.join(self.temp_dir, "foremost_output")
            os.makedirs(output_dir, exist_ok=True)
            
            result = subprocess.run(['foremost', '-i', file_path, '-o', output_dir], 
                                  capture_output=True, text=True, timeout=60)
            
            # Read audit file
            audit_file = os.path.join(output_dir, "audit.txt")
            audit_content = ""
            if os.path.exists(audit_file):
                with open(audit_file, 'r', encoding='utf-8', errors='ignore') as f:
                    audit_content = f.read()
            
            return {
                "tool": "foremost",
                "output": result.stdout,
                "errors": result.stderr,
                "audit": audit_content,
                "output_dir": output_dir,
                "success": result.returncode == 0
            }
        except Exception as e:
            return {"error": f"foremost error: {str(e)}"}
    
    def run_strings(self, file_path: str) -> Dict:
        """Run strings analysis"""
        if not self._check_command('strings'):
            return {"error": "strings not available"}
        
        try:
            result = subprocess.run(['strings', file_path], 
                                  capture_output=True, text=True, timeout=30)
            
            # Filter interesting strings
            lines = result.stdout.split('\n')
            interesting_strings = []
            for line in lines:
                line = line.strip()
                if len(line) > 5:  # Only keep strings longer than 5 chars
                    interesting_strings.append(line)
            
            return {
                "tool": "strings",
                "all_strings": result.stdout,
                "interesting_strings": interesting_strings[:100],  # Limit output
                "total_strings": len(lines),
                "errors": result.stderr,
                "success": result.returncode == 0
            }
        except Exception as e:
            return {"error": f"strings error: {str(e)}"}
    
    def analyze_file(self, file_path: str, password: str = "") -> Dict:
        """Perform comprehensive analysis on a file"""
        if not os.path.exists(file_path):
            return {"error": "File not found"}
        
        self.logger.info(f"Starting analysis of: {file_path}")
        
        results = {
            "file_path": file_path,
            "file_size": os.path.getsize(file_path),
            "analysis_results": {}
        }
        
        # Check available tools
        available_tools = self.check_tool_availability()
        self.logger.info(f"Available tools: {available_tools}")
        
        # Run each available tool
        if available_tools.get('zsteg'):
            self.logger.info("Running zsteg analysis...")
            results["analysis_results"]["zsteg"] = self.run_zsteg(file_path)
        
        if available_tools.get('steghide'):
            self.logger.info("Running steghide analysis...")
            results["analysis_results"]["steghide"] = self.run_steghide(file_path, password)
        
        if available_tools.get('outguess'):
            self.logger.info("Running outguess analysis...")
            results["analysis_results"]["outguess"] = self.run_outguess(file_path)
        
        if available_tools.get('exiftool'):
            self.logger.info("Running exiftool analysis...")
            results["analysis_results"]["exiftool"] = self.run_exiftool(file_path)
        
        if available_tools.get('binwalk'):
            self.logger.info("Running binwalk analysis...")
            results["analysis_results"]["binwalk"] = self.run_binwalk(file_path)
        
        if available_tools.get('foremost'):
            self.logger.info("Running foremost analysis...")
            results["analysis_results"]["foremost"] = self.run_foremost(file_path)
        
        if available_tools.get('strings'):
            self.logger.info("Running strings analysis...")
            results["analysis_results"]["strings"] = self.run_strings(file_path)
        
        self.results[file_path] = results
        return results
    
    def print_results(self, results: Dict):
        """Print analysis results in a formatted way"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"STEGANOGRAPHY ANALYSIS RESULTS")
        print(f"{'='*60}{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}File:{Style.RESET_ALL} {results['file_path']}")
        print(f"{Fore.YELLOW}Size:{Style.RESET_ALL} {results['file_size']} bytes")
        
        for tool_name, tool_results in results["analysis_results"].items():
            print(f"\n{Fore.GREEN}[{tool_name.upper()}]{Style.RESET_ALL}")
            print("-" * 40)
            
            if "error" in tool_results:
                print(f"{Fore.RED}Error: {tool_results['error']}{Style.RESET_ALL}")
                continue
            
            if not tool_results.get("success", False):
                print(f"{Fore.YELLOW}No results found{Style.RESET_ALL}")
            
            # Print tool-specific results
            if tool_name == "zsteg" and tool_results.get("output"):
                print(tool_results["output"])
            
            elif tool_name == "steghide":
                if tool_results.get("extracted_content"):
                    print(f"{Fore.CYAN}Extracted content:{Style.RESET_ALL}")
                    print(tool_results["extracted_content"][:500] + "..." if len(tool_results["extracted_content"]) > 500 else tool_results["extracted_content"])
                else:
                    print("No hidden content extracted")
            
            elif tool_name == "outguess":
                if tool_results.get("extracted_content"):
                    print(f"{Fore.CYAN}Extracted content:{Style.RESET_ALL}")
                    print(tool_results["extracted_content"][:500] + "..." if len(tool_results["extracted_content"]) > 500 else tool_results["extracted_content"])
                else:
                    print("No hidden content extracted")
            
            elif tool_name == "exiftool":
                metadata = tool_results.get("metadata", {})
                for key, value in metadata.items():
                    print(f"{key}: {value}")
            
            elif tool_name == "binwalk":
                if tool_results.get("signatures"):
                    print(tool_results["signatures"])
            
            elif tool_name == "foremost":
                if tool_results.get("audit"):
                    print(tool_results["audit"])
            
            elif tool_name == "strings":
                interesting = tool_results.get("interesting_strings", [])
                if interesting:
                    print(f"Found {tool_results.get('total_strings', 0)} strings, showing first 10 interesting ones:")
                    for i, string in enumerate(interesting[:10]):
                        print(f"  {i+1}: {string}")
    
    def save_results(self, output_file: str):
        """Save results to JSON file"""
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n{Fore.GREEN}Results saved to: {output_file}{Style.RESET_ALL}")
    
    def cleanup(self):
        """Clean up temporary files"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Steganography Analyzer - Multi-tool analysis")
    parser.add_argument("file", help="File to analyze")
    parser.add_argument("-p", "--password", default="", help="Password for steghide")
    parser.add_argument("-o", "--output", help="Output JSON file for results")
    parser.add_argument("--gui", action="store_true", help="Launch GUI interface")
    
    args = parser.parse_args()
    
    if args.gui:
        # Import and launch GUI
        try:
            import sys
            import os
            # Add current directory to path for executable
            if hasattr(sys, '_MEIPASS'):
                sys.path.insert(0, sys._MEIPASS)
            else:
                sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            
            from stego_gui import StegoGUI
            app = StegoGUI()
            app.run()
        except ImportError as e:
            print(f"{Fore.RED}GUI not available: {str(e)}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Make sure tkinter is installed or use the GUI executable directly.{Style.RESET_ALL}")
        return
    
    analyzer = StegoAnalyzer()
    
    try:
        # Analyze the file
        results = analyzer.analyze_file(args.file, args.password)
        
        # Print results
        analyzer.print_results(results)
        
        # Save results if requested
        if args.output:
            analyzer.save_results(args.output)
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Analysis interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
    finally:
        analyzer.cleanup()

if __name__ == "__main__":
    main()
