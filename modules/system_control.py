"""
ZARA - Advanced Real-time Intelligent Assistant
System Control Module - Power management and system status
"""

import subprocess
import psutil
import socket
import time
from datetime import timedelta
from typing import Dict, Any, Optional


class SystemControl:
    """
    System power control and status monitoring.
    Handles shutdown, restart, sleep, lock, and system information.
    """

    def __init__(self):
        """Initialize system control."""
        pass

    def shutdown(self, delay: int = 0) -> Dict[str, Any]:
        """
        Shutdown the system.
        
        Args:
            delay: Delay in seconds before shutdown (default: 0)
            
        Returns:
            Status dictionary
        """
        try:
            cmd = f"shutdown /s /t {delay}"
            subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if delay > 0:
                return {
                    "success": True,
                    "message": f"System will shutdown in {delay} seconds",
                    "delay": delay,
                    "action": "shutdown_scheduled"
                }
            else:
                return {
                    "success": True,
                    "message": "System shutting down",
                    "action": "shutdown_immediate"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def restart(self, delay: int = 0) -> Dict[str, Any]:
        """
        Restart the system.
        
        Args:
            delay: Delay in seconds before restart (default: 0)
            
        Returns:
            Status dictionary
        """
        try:
            cmd = f"shutdown /r /t {delay}"
            subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if delay > 0:
                return {
                    "success": True,
                    "message": f"System will restart in {delay} seconds",
                    "delay": delay,
                    "action": "restart_scheduled"
                }
            else:
                return {
                    "success": True,
                    "message": "System restarting",
                    "action": "restart_immediate"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def sleep(self) -> Dict[str, Any]:
        """
        Put system to sleep mode.
        
        Returns:
            Status dictionary
        """
        try:
            # Use rundll32 to enter sleep mode
            cmd = "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            return {
                "success": True,
                "message": "System entering sleep mode",
                "action": "sleep"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def hibernate(self) -> Dict[str, Any]:
        """
        Put system to hibernate mode.
        
        Returns:
            Status dictionary
        """
        try:
            cmd = "shutdown /h"
            subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            return {
                "success": True,
                "message": "System hibernating",
                "action": "hibernate"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def lock(self) -> Dict[str, Any]:
        """
        Lock the workstation.
        
        Returns:
            Status dictionary
        """
        try:
            cmd = "rundll32.exe user32.dll,LockWorkStation"
            subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            return {
                "success": True,
                "message": "Workstation locked",
                "action": "lock"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def cancel_shutdown(self) -> Dict[str, Any]:
        """
        Cancel a pending shutdown/restart.
        
        Returns:
            Status dictionary
        """
        try:
            cmd = "shutdown /a"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": "Shutdown cancelled successfully",
                    "action": "cancel_shutdown"
                }
            else:
                return {
                    "success": False,
                    "message": "No shutdown to cancel",
                    "action": "cancel_shutdown"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_uptime(self) -> str:
        """
        Get system uptime as readable string.
        
        Returns:
            Formatted uptime string (e.g., "2d 5h 30m 15s")
        """
        try:
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            uptime = timedelta(seconds=int(uptime_seconds))
            
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            if days > 0:
                return f"{days}d {hours}h {minutes}m {seconds}s"
            elif hours > 0:
                return f"{hours}h {minutes}m {seconds}s"
            elif minutes > 0:
                return f"{minutes}m {seconds}s"
            else:
                return f"{seconds}s"
                
        except Exception as e:
            return f"Error: {e}"

    def get_battery(self) -> Dict[str, Any]:
        """
        Get battery status.
        
        Returns:
            Battery percentage and charging status
        """
        try:
            battery = psutil.sensors_battery()
            
            if battery is None:
                return {
                    "available": False,
                    "message": "No battery detected (Desktop PC)",
                    "plugged_in": True
                }
            
            return {
                "available": True,
                "percent": battery.percent,
                "plugged_in": battery.power_plugged,
                "charging": battery.power_plugged,
                "time_left": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None,
                "time_left_str": self._format_time_left(battery.secsleft) if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited"
            }
            
        except Exception as e:
            return {"available": False, "error": str(e)}

    def _format_time_left(self, secs: int) -> str:
        """Format seconds to readable time string."""
        if secs is None or secs < 0:
            return "Unknown"
        
        hours = secs // 3600
        minutes = (secs % 3600) // 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"

    def get_cpu_usage(self) -> Dict[str, Any]:
        """
        Get CPU usage percentage.
        
        Returns:
            CPU usage info including percentage, frequency, cores
        """
        try:
            # Get CPU usage with interval for accurate reading
            usage = psutil.cpu_percent(interval=0.5)
            
            # Get CPU frequency
            freq = psutil.cpu_freq()
            
            # Get core counts
            cores_physical = psutil.cpu_count(logical=False)
            cores_logical = psutil.cpu_count(logical=True)
            
            # Get per-core usage
            per_cpu = psutil.cpu_percent(interval=0.5, percpu=True)
            
            return {
                "usage_percent": usage,
                "frequency_mhz": round(freq.current, 2) if freq else None,
                "max_frequency_mhz": round(freq.max, 2) if freq else None,
                "cores_physical": cores_physical,
                "cores_logical": cores_logical,
                "per_core_usage": per_cpu,
                "avg_core_usage": round(sum(per_cpu) / len(per_cpu), 2) if per_cpu else 0
            }
            
        except Exception as e:
            return {"error": str(e)}

    def get_ram_usage(self) -> Dict[str, Any]:
        """
        Get RAM usage info.
        
        Returns:
            RAM used/total in GB with percentage
        """
        try:
            mem = psutil.virtual_memory()
            
            used_gb = mem.used / (1024 ** 3)
            total_gb = mem.total / (1024 ** 3)
            available_gb = mem.available / (1024 ** 3)
            free_gb = mem.free / (1024 ** 3)
            
            return {
                "used_gb": round(used_gb, 2),
                "total_gb": round(total_gb, 2),
                "available_gb": round(available_gb, 2),
                "free_gb": round(free_gb, 2),
                "percent": mem.percent,
                "usage_status": self._get_ram_status(mem.percent)
            }
            
        except Exception as e:
            return {"error": str(e)}

    def _get_ram_status(self, percent: float) -> str:
        """Get RAM usage status string."""
        if percent < 50:
            return "Good"
        elif percent < 75:
            return "Moderate"
        elif percent < 90:
            return "High"
        else:
            return "Critical"

    def get_disk_usage(self, drive: str = "C:") -> Dict[str, Any]:
        """
        Get disk usage info for specified drive.
        
        Args:
            drive: Drive letter (default: C:)
            
        Returns:
            Disk usage info
        """
        try:
            disk = psutil.disk_usage(drive)
            
            used_gb = disk.used / (1024 ** 3)
            total_gb = disk.total / (1024 ** 3)
            free_gb = disk.free / (1024 ** 3)
            
            return {
                "drive": drive,
                "used_gb": round(used_gb, 2),
                "total_gb": round(total_gb, 2),
                "free_gb": round(free_gb, 2),
                "percent": disk.percent,
                "usage_status": self._get_disk_status(disk.percent)
            }
            
        except Exception as e:
            return {"error": str(e)}

    def _get_disk_status(self, percent: float) -> str:
        """Get disk usage status string."""
        if percent < 70:
            return "Good"
        elif percent < 85:
            return "Warning"
        else:
            return "Critical"

    def get_network_info(self) -> Dict[str, Any]:
        """
        Get network information.
        
        Returns:
            IP address, connection status, network speed
        """
        try:
            # Get hostname and IP
            hostname = socket.gethostname()
            
            try:
                ip_address = socket.gethostbyname(hostname)
            except:
                ip_address = "127.0.0.1"
            
            # Get network interfaces
            interfaces = psutil.net_if_stats()
            connected = False
            interface_name = None
            interface_speed = None
            
            for name, stats in interfaces.items():
                if stats.isup and stats.link_duplex == psutil.NIC_DUPLEX_FULL:
                    connected = True
                    interface_name = name
                    interface_speed = stats.speed
                    break
            
            # Get network I/O statistics
            net_io = psutil.net_io_counters()
            
            # Get bytes sent/received in MB
            bytes_sent_mb = round(net_io.bytes_sent / (1024 ** 2), 2)
            bytes_recv_mb = round(net_io.bytes_recv / (1024 ** 2), 2)
            
            return {
                "hostname": hostname,
                "ip_address": ip_address,
                "connected": connected,
                "interface": interface_name,
                "interface_speed_mbps": interface_speed,
                "bytes_sent_mb": bytes_sent_mb,
                "bytes_recv_mb": bytes_recv_mb,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
                "errors_in": net_io.errin,
                "errors_out": net_io.errout
            }
            
        except Exception as e:
            return {"error": str(e)}

    def get_process_count(self) -> int:
        """
        Get number of running processes.
        
        Returns:
            Process count
        """
        return len(psutil.pids())

    def get_top_processes(self, limit: int = 10) -> list:
        """
        Get top processes by memory usage.
        
        Args:
            limit: Number of processes to return
            
        Returns:
            List of process info dictionaries
        """
        try:
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'memory_info']):
                try:
                    mem_info = proc.info['memory_info']
                    processes.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "cpu_percent": proc.info['cpu_percent'],
                        "memory_percent": proc.info['memory_percent'],
                        "memory_mb": round(mem_info.rss / (1024 * 1024), 2) if mem_info else 0
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by memory usage and limit
            processes.sort(key=lambda x: x['memory_percent'], reverse=True)
            return processes[:limit]
            
        except Exception as e:
            return []

    def kill_process(self, pid: int) -> Dict[str, Any]:
        """
        Kill a process by PID.
        
        Args:
            pid: Process ID
            
        Returns:
            Status dictionary
        """
        try:
            process = psutil.Process(pid)
            process.terminate()
            
            return {
                "success": True,
                "message": f"Process {pid} ({process.name()}) terminated"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def full_system_status(self) -> Dict[str, Any]:
        """
        Get complete system status.
        
        Returns:
            Formatted dictionary with all system info
        """
        return {
            "uptime": self.get_uptime(),
            "battery": self.get_battery(),
            "cpu": self.get_cpu_usage(),
            "ram": self.get_ram_usage(),
            "disk": self.get_disk_usage(),
            "network": self.get_network_info(),
            "process_count": self.get_process_count(),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def get_temperature(self) -> Dict[str, Any]:
        """
        Get system temperature (if available).
        
        Returns:
            Temperature info from sensors
        """
        try:
            temps = psutil.sensors_temperatures()
            
            if not temps:
                return {
                    "available": False,
                    "message": "Temperature sensors not available"
                }
            
            result = {}
            for name, entries in temps.items():
                for entry in entries:
                    result[entry.label or name] = {
                        "current_c": entry.current,
                        "high_c": entry.high,
                        "critical_c": entry.critical
                    }
            
            return {
                "available": True,
                "sensors": result
            }
            
        except Exception as e:
            return {"available": False, "error": str(e)}

    def get_system_info(self) -> Dict[str, Any]:
        """
        Get basic system information.
        
        Returns:
            System info dictionary
        """
        try:
            import platform
            
            return {
                "system": platform.system(),
                "version": platform.version(),
                "platform": platform.platform(),
                "processor": platform.processor(),
                "architecture": platform.architecture()[0],
                "python_version": platform.python_version()
            }
            
        except Exception as e:
            return {"error": str(e)}
