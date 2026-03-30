import re

def parse_log(line):
    # Failed login
    failed = re.search(r"Failed password for (?:invalid user )?(\w+) from ([\d.:]+)", line)
    if failed:
        return {
            "user": failed.group(1),
            "ip": failed.group(2),
            "status": "failed"
        }

    # Success login
    success = re.search(r"Accepted password for (\w+) from ([\d.:]+)", line)
    if success:
        return {
            "user": success.group(1),
            "ip": success.group(2),
            "status": "success"
        }

    return None