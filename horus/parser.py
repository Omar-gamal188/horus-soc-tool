import re

# compile regex مرة واحدة (أسرع)
FAILED_REGEX = re.compile(
    r"Failed password for (?:invalid user )?([a-zA-Z0-9._-]+) from ([0-9a-fA-F:.]+)"
)

SUCCESS_REGEX = re.compile(
    r"Accepted password for ([a-zA-Z0-9._-]+) from ([0-9a-fA-F:.]+)"
)


def parse_log(line):
    try:
        # ❌ Failed login
        failed = FAILED_REGEX.search(line)
        if failed:
            return {
                "user": failed.group(1),
                "ip": failed.group(2),
                "status": "failed"
            }

        # ✅ Success login
        success = SUCCESS_REGEX.search(line)
        if success:
            return {
                "user": success.group(1),
                "ip": success.group(2),
                "status": "success"
            }

    except Exception:
        pass

    return None