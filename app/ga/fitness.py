from collections import defaultdict


def calculate_fitness(timetable):

    fitness = 100

    lecturer_schedule = defaultdict(list)

    hall_schedule = defaultdict(list)

    student_schedule = defaultdict(list)

    lecturer_daily_hours = defaultdict(int)

    for entry in timetable:

        day = entry["day"]

        start = entry["start_slot"]

        end = (

            start +

            entry["duration"] - 1
        )

        lecturer = entry["lecturer_id"]

        hall = entry["hall_id"]

        student_group = entry["student_group"]

        # -------------------------
        # LECTURER CONFLICTS
        # -------------------------

        for existing in lecturer_schedule[lecturer]:

            if existing["day"] == day:

                overlap = not (

                    end < existing["start"]

                    or

                    start > existing["end"]
                )

                if overlap:

                    fitness -= 50

        lecturer_schedule[lecturer].append({

            "day": day,

            "start": start,

            "end": end
        })

        # -------------------------
        # HALL CONFLICTS
        # -------------------------

        for existing in hall_schedule[hall]:

            if existing["day"] == day:

                overlap = not (

                    end < existing["start"]

                    or

                    start > existing["end"]
                )

                if overlap:

                    fitness -= 50

        hall_schedule[hall].append({

            "day": day,

            "start": start,

            "end": end
        })

        # -------------------------
        # STUDENT GROUP CONFLICTS
        # -------------------------

        for existing in student_schedule[student_group]:

            if existing["day"] == day:

                overlap = not (

                    end < existing["start"]

                    or

                    start > existing["end"]
                )

                if overlap:

                    fitness -= 50

        student_schedule[student_group].append({

            "day": day,

            "start": start,

            "end": end
        })

        # -------------------------
        # LUNCH BREAK PENALTY
        # -------------------------

        for slot in range(start, end + 1):

            if slot == 5:

                fitness -= 20

        # -------------------------
        # LATE EVENING PENALTY
        # -------------------------

        if end >= 8:

            fitness -= 10

        # -------------------------
        # DAILY HOURS TRACK
        # -------------------------

        lecturer_key = f"{lecturer}_{day}"

        lecturer_daily_hours[lecturer_key] += (

            entry["duration"]
        )

    # -------------------------
    # OVERWORKED LECTURERS
    # -------------------------

    for key in lecturer_daily_hours:

        if lecturer_daily_hours[key] > 6:

            fitness -= 15

    # -------------------------
    # MINIMUM FITNESS
    # -------------------------

    if fitness < 0:

        fitness = 0

    return fitness