import json


def parse_plan(plan_data):
    """
    Parse Terraform plan JSON.

    Accepts:
    - Uploaded Streamlit file
    - JSON bytes
    - JSON string
    - File path
    """

    # Streamlit UploadedFile
    if hasattr(plan_data, "read"):
        content = plan_data.read()

        if isinstance(content, bytes):
            content = content.decode("utf-8")

        plan = json.loads(content)

    # Bytes
    elif isinstance(plan_data, bytes):
        plan = json.loads(plan_data.decode("utf-8"))

    # JSON string
    elif isinstance(plan_data, str):

        # If it looks like JSON, parse it directly
        if plan_data.strip().startswith("{"):
            plan = json.loads(plan_data)

        # Otherwise treat it as a file path
        else:
            with open(plan_data, "r", encoding="utf-8") as file:
                plan = json.load(file)

    # Already parsed dictionary
    elif isinstance(plan_data, dict):
        plan = plan_data

    else:
        raise ValueError("Unsupported Terraform plan input.")

    resources = []

    for resource in plan.get("resource_changes", []):

        address = resource.get("address", "Unknown")

        change = resource.get("change", {})

        actions = change.get("actions", [])

        before = change.get("before")
        after = change.get("after")

        # Terraform actions can be:
        # ["create"]
        # ["update"]
        # ["delete"]
        # ["delete", "create"] -> replace

        if actions == ["create"]:
            action = "create"

        elif actions == ["update"]:
            action = "update"

        elif actions == ["delete"]:
            action = "delete"

        elif actions == ["delete", "create"]:
            action = "replace"

        elif actions == ["create", "delete"]:
            action = "replace"

        else:
            action = ", ".join(actions)

        resources.append({
            "address": address,
            "action": action,
            "before": before,
            "after": after
        })

    return resources