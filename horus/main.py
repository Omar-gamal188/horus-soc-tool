import time
import platform
import subprocess
from horus.parser import parse_log
from horus.geoip import get_ip_info


def banner():
    print("\033[1;32m")
    print(r"""
██╗  ██╗ ██████╗ ██████╗ ██╗   ██╗███████╗
██║  ██║██╔═══██╗██╔══██╗██║   ██║██╔════╝
███████║██║   ██║██████╔╝██║   ██║███████╗
██╔══██║██║   ██║██╔══██╗██║   ██║╚════██║
██║  ██║╚██████╔╝██║  ██║╚██████╔╝███████║
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝

            [ HORUS 👁️ ]

==============================================
   >> Cross-Platform SOC Monitoring Tool <<
==============================================
        >> Powered by Sa5met <<
==============================================
""")
    print("\033[0m")


# 🐧 Linux / Kali
def monitor_linux():
    print("[+] Monitoring Linux logs (journalctl)...\n")

    command = ["journalctl", "-f", "-n", "5"]
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    failed_attempts = {}

    for line in process.stdout:
        try:
            data = parse_log(line)
        except Exception:
            continue

        # skip لو مفيش data
        if not data or "ip" not in data or "status" not in data:
            continue

        ip = data.get("ip", "Unknown")
        user = data.get("user", "Unknown")

        # تجاهل localhost
        if ip == "::1" or ip.startswith("127."):
            continue

        # 🌍 GeoIP
        geo = get_ip_info(ip)
        country = geo.get("country", "Unknown")
        city = geo.get("city", "Unknown")

        # ❌ Failed
        if data["status"] == "failed":
            failed_attempts[ip] = failed_attempts.get(ip, 0) + 1

            print(f"\033[1;31m[FAILED ❌]\033[0m User: {user} | IP: {ip} | {country}, {city}")

            # 🚨 Alert
            if failed_attempts[ip] >= 5:
                print(f"\033[1;33m🚨 BRUTE FORCE DETECTED from {ip} ({country})\033[0m")

        # ✅ Success
        elif data["status"] == "success":
            print(f"\033[1;34m[SUCCESS ✅]\033[0m User: {user} | IP: {ip} | {country}, {city}")

            # reset counter
            failed_attempts[ip] = 0


# 🪟 Windows
def monitor_windows():
    seen = set()

    while True:
        try:
            command = [
                "powershell",
                "-Command",
                "Get-WinEvent -LogName Security | Select-Object -First 10 | Format-List"
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore"
            )

            logs = result.stdout
            events = logs.split("TimeCreated")

            for event in events:
                if event not in seen:
                    seen.add(event)

                    if "Id           : 4625" in event:
                        print("\033[1;31m[FAILED LOGIN ❌]\033[0m")
                        print(event)

                    elif "Id           : 4624" in event:
                        print("\033[1;34m[SUCCESS LOGIN ✅]\033[0m")
                        print(event)

        except Exception:
            pass

        time.sleep(5)


def main():
    print("\033[1;31m[ SYSTEM MONITORING ACTIVATED ]\033[0m")
    banner()

    system = platform.system()
    print(f"Running on: {system}")

    try:
        if system == "Linux":
            monitor_linux()
        elif system == "Windows":
            monitor_windows()
        else:
            print("Unsupported OS")
    except KeyboardInterrupt:
        print("\n[!] Stopped by user")


if __name__ == "__main__":
    main()