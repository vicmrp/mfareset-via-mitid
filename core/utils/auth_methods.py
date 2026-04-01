def get_auth_method_label(odata_type: str) -> str:
    if odata_type.endswith("passwordAuthenticationMethod"):
        return "Password"
    if odata_type.endswith("phoneAuthenticationMethod"):
        return "Phone"
    if odata_type.endswith("microsoftAuthenticatorAuthenticationMethod"):
        return "Microsoft Authenticator"
    if odata_type.endswith("softwareOathAuthenticationMethod"):
        return "Software OATH token"
    if odata_type.endswith("windowsHelloForBusinessAuthenticationMethod"):
        return "Windows Hello for Business"
    return "Unknown method"


def is_deletable_auth_method(odata_type: str) -> bool:
    return (
        odata_type.endswith("phoneAuthenticationMethod")
        or odata_type.endswith("softwareOathAuthenticationMethod")
        or odata_type.endswith("microsoftAuthenticatorAuthenticationMethod")
    )


def sanitize_raw_auth_method(method):
    odata_type = method.get("@odata.type", "")
    return {
        "type": odata_type,
        "label": get_auth_method_label(odata_type),
        "can_delete": is_deletable_auth_method(odata_type),
    }


def sanitize_prepared_auth_method(method):
    return {
        "type": method.get("type", ""),
        "label": method.get("label", "Unknown method"),
        "can_delete": bool(method.get("can_delete", False)),
    }


def prepare_auth_methods(methods):
    pretty = []

    for method in methods:
        odata_type = method.get("@odata.type", "")
        label = get_auth_method_label(odata_type)
        details = ""
        can_delete = is_deletable_auth_method(odata_type)

        if odata_type.endswith("passwordAuthenticationMethod"):
            created = method.get("createdDateTime")
            if created:
                details = f"Created: {created}"

        elif odata_type.endswith("phoneAuthenticationMethod"):
            phone_type = method.get("phoneType", "")
            phone_number = method.get("phoneNumber", "")
            details = f"{phone_type}: {phone_number}"

        elif odata_type.endswith("microsoftAuthenticatorAuthenticationMethod"):
            display_name = method.get("displayName", "")
            device_tag = method.get("deviceTag", "")
            details = f"{display_name} ({device_tag})"

        elif odata_type.endswith("windowsHelloForBusinessAuthenticationMethod"):
            display_name = method.get("displayName") or "Unnamed device"
            created = method.get("createdDateTime", "")
            details = f"{display_name} (created {created})"

        else:
            details = str(method)

        if can_delete:
            pretty.append(
                {
                    "label": label,
                    "details": details,
                    "id": method.get("id", ""),
                    "type": odata_type,
                    "can_delete": can_delete,
                }
            )

    return pretty
