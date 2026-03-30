import time
import platform
import subprocess
from horus.parser import parse_log
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

    process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)

    for line in process.stdout:
        data = parse_log(line)

        if data:  # مهم جدًا
            if data["status"] == "failed":
                print(f"\033[1;31m[FAILED ❌]\033[0m User: {data['user']} | IP: {data['ip']}")

            elif data["status"] == "success":
                print(f"\033[1;34m[SUCCESS ✅]\033[0m User: {data['user']} | IP: {data['ip']}")
# 🪟 Windows
def monitor_windows():
    seen = set()

    while True:
        command = [
            "powershell",
            "-Command",
            "Get-WinEvent -LogName Security | Select-Object -First 10 | Format-List"
        ]

        result = subprocess.run(command, capture_output=True, text=True)
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

        time.sleep(5)


def main():
    print("\033[1;31m[ SYSTEM MONITORING ACTIVATED ]\033[0m")
    banner()

    system = platform.system()

    print(f"Running on: {system}")

    if system == "Linux":
        monitor_linux()

    elif system == "Windows":
        monitor_windows()

    else:
        print("Unsupported OS")


if __name__ == "__main__":
    main()