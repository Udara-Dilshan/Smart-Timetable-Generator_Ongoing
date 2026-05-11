import random

from app.models.subject import Subject
from app.models.lecturer import Lecturer
from app.models.hall import Hall
from app.models.timetable import Timetable

from app.services.conflict_checker import has_conflict


DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday"
]


def generate_random_timetable(db):

    db.query(Timetable).delete()

    db.commit()

    timetable = []

    subjects = db.query(Subject).all()

    lecturers = db.query(Lecturer).all()

    halls = db.query(Hall).all()

    lecturer_daily_hours = {}

    for subject in subjects:

        valid = False

        while not valid:

            lecturer = random.choice(lecturers)

            duration = subject.credits

            start_slot = random.randint(1, 7)

            end_slot = start_slot + duration - 1

            day = random.choice(DAYS)

            # AFTER 5PM
            if end_slot > 9:

                continue

            # LUNCH BREAK
            lunch_conflict = False

            for slot in range(start_slot, end_slot + 1):

                if slot == 5:

                    lunch_conflict = True

            if lunch_conflict:

                continue

            # UNAVAILABLE SLOTS
            if (

                lecturer.unavailable_day == day

                and

                lecturer.unavailable_slot >= start_slot

                and

                lecturer.unavailable_slot <= end_slot
            ):

                continue

            # MAX HOURS
            key = f"{lecturer.id}_{day}"

            current_hours = lecturer_daily_hours.get(

                key,

                0
            )

            if (

                current_hours + duration >

                lecturer.max_hours_per_day
            ):

                continue

            # VALID HALLS
            valid_halls = []

            for hall in halls:

                if (

                    hall.hall_type ==

                    subject.preferred_hall_type
                ):

                    valid_halls.append(hall)

            if len(valid_halls) == 0:

                continue

            hall = random.choice(valid_halls)

            entry = {

                "subject_id": subject.id,

                "subject_name": subject.subject_name,

                "student_group": subject.student_group,

                "lecturer_id": lecturer.id,

                "lecturer_name": lecturer.lecturer_name,

                "hall_id": hall.id,

                "hall_name": hall.hall_name,

                "day": day,

                "start_slot": start_slot,

                "duration": duration
            }

            lecturer_conflict = False

            hall_conflict = False

            student_conflict = False

            time_conflict = has_conflict(

                timetable,

                entry
            )

            if time_conflict:

                continue

            for existing in timetable:

                overlap = has_conflict(

                    [existing],

                    entry
                )

                if (

                    overlap

                    and

                    existing["lecturer_id"] ==

                    entry["lecturer_id"]
                ):

                    lecturer_conflict = True

                if (

                    overlap

                    and

                    existing["hall_id"] ==

                    entry["hall_id"]
                ):

                    hall_conflict = True

                if (

                    overlap

                    and

                    existing["student_group"] ==

                    entry["student_group"]
                ):

                    student_conflict = True

            if (

                not lecturer_conflict

                and

                not hall_conflict

                and

                not student_conflict
            ):

                timetable.append(entry)

                lecturer_daily_hours[key] = (

                    current_hours + duration
                )

                db_entry = Timetable(

                    subject_id=subject.id,

                    lecturer_id=lecturer.id,

                    hall_id=hall.id,

                    day=day,

                    start_slot=start_slot,

                    duration=duration
                )

                db.add(db_entry)

                db.commit()

                valid = True

    return timetable