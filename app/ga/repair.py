import random


DAYS = [

    "Monday",

    "Tuesday",

    "Wednesday",

    "Thursday",

    "Friday"
]


def overlaps(a, b):

    if a["day"] != b["day"]:

        return False

    a_start = a["start_slot"]

    a_end = (

        a_start +

        a["duration"] - 1
    )

    b_start = b["start_slot"]

    b_end = (

        b_start +

        b["duration"] - 1
    )

    return not (

        a_end < b_start

        or

        a_start > b_end
    )


def repair_timetable(timetable):

    repaired = []

    for entry in timetable:

        fixed = False

        attempts = 0

        while not fixed and attempts < 100:

            attempts += 1

            start = entry["start_slot"]

            duration = entry["duration"]

            end = start + duration - 1

            # -------------------------
            # LUNCH CHECK
            # -------------------------

            lunch_conflict = False

            for slot in range(start, end + 1):

                if slot == 5:

                    lunch_conflict = True

            # -------------------------
            # LATE CLASS CHECK
            # -------------------------

            late_conflict = False

            if end >= 8:

                late_conflict = True

            lecturer_conflict = False

            hall_conflict = False

            student_conflict = False

            # -------------------------
            # CHECK EXISTING
            # -------------------------

            for existing in repaired:

                if overlaps(existing, entry):

                    # Lecturer clash
                    if (

                        existing["lecturer_id"]

                        ==

                        entry["lecturer_id"]
                    ):

                        lecturer_conflict = True

                    # Hall clash
                    if (

                        existing["hall_id"]

                        ==

                        entry["hall_id"]
                    ):

                        hall_conflict = True

                    # Student clash
                    if (

                        existing["student_group"]

                        ==

                        entry["student_group"]
                    ):

                        student_conflict = True

            # -------------------------
            # VALID ENTRY
            # -------------------------

            if (

                not lecturer_conflict

                and

                not hall_conflict

                and

                not student_conflict

                and

                not lunch_conflict

                and

                not late_conflict
            ):

                repaired.append(entry)

                fixed = True

            else:

                # -------------------------
                # REPAIR
                # -------------------------

                entry["day"] = random.choice(DAYS)

                entry["start_slot"] = random.randint(1, 6)

        # FAILSAFE
        if not fixed:

            repaired.append(entry)

    return repaired