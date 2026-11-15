def parse_application(text):
    if text is None or not isinstance(text, str):
        raise ValueError("invalid application text")
    parts = text.split(":")
    if len(parts) != 2:
        raise ValueError("expected format visa:entries")
    visa, entries = parts
    visa = visa.strip().title()
    entries = entries.strip()
    if entries == "":
        raise ValueError("entries must be an integer")
    return visa, int(entries)


def processing_average(days_csv):
    if days_csv is None or not isinstance(days_csv, str):
        raise ValueError("invalid processing days CSV")
    parts = days_csv.split(",")
    if len(parts) == 0 or any(part.strip() == "" for part in parts):
        raise ValueError("processing days must be comma-separated integers")
    values = [int(part.strip()) for part in parts]
    if len(values) == 0:
        raise ValueError("no processing days provided")
    return sum(values) // len(values)


def payable_fee(text):
    if text is None or not isinstance(text, str):
        raise ValueError("invalid fee text")
    parts = text.split("|")
    if len(parts) != 2:
        raise ValueError("expected format fee|discount")
    fee, discount = parts
    try:
        total = float(fee.strip()) * 1.18 - float(discount.strip())
    except ValueError:
        raise ValueError("fee and discount must be numeric")
    return max(total, 0)


def main():
    print("==== Running parse_application ====")
    user_input = input("Enter visa type:entries (e.g. tourist:2): ")
    result = parse_application(user_input)
    print("Visa Type and Entries:", result)

    print("\n==== Running processing_average ====")
    user_input = input("Enter processing days as CSV (e.g. 5,10,21): ")
    result = processing_average(user_input)
    print("Average Processing Days:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 6000|500): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result)


if __name__ == "__main__":
    main()
