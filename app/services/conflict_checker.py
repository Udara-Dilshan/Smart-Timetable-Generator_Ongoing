def has_conflict(existing_entries, new_entry):

    new_start = new_entry["start_slot"]

    new_end = (

        new_start +

        new_entry["duration"] - 1
    )

    for entry in existing_entries:

        # SAME DAY ONLY
        if entry["day"] != new_entry["day"]:

            continue

        existing_start = entry["start_slot"]

        existing_end = (

            existing_start +

            entry["duration"] - 1
        )

        overlap = not (

            new_end < existing_start

            or

            new_start > existing_end
        )

        if overlap:

            return True

    return False