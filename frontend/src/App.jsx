import { useEffect, useState } from "react";

import axios from "axios";

import "./App.css";

const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];

const SLOTS = [
  { slot: 1, label: "8AM - 9AM" },

  { slot: 2, label: "9AM - 10AM" },

  { slot: 3, label: "10AM - 11AM" },

  { slot: 4, label: "11AM - 12PM" },

  { slot: 5, label: "12PM - 1PM" },

  { slot: 6, label: "1PM - 2PM" },

  { slot: 7, label: "2PM - 3PM" },

  { slot: 8, label: "3PM - 4PM" },

  { slot: 9, label: "4PM - 5PM" },
];

function App() {
  const [timetable, setTimetable] = useState([]);

  const [fitness, setFitness] = useState(0);

  const [subjects, setSubjects] = useState([]);

  const [lecturers, setLecturers] = useState([]);

  // SUBJECT FORM
  const [formData, setFormData] = useState({
    subject_code: "",

    subject_name: "",

    credits: 1,

    session_type: "Lecture",

    preferred_hall_type: "Lecture Hall",

    student_group: "",
  });

  // LECTURER FORM
  const [lecturerForm, setLecturerForm] = useState({
    lecturer_name: "",

    max_hours_per_day: 4,

    preferred_days: "",

    unavailable_day: "",

    unavailable_slot: 1,
  });

  // LOAD SUBJECTS
  const loadSubjects = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/subjects");

      setSubjects(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  // LOAD LECTURERS
  const loadLecturers = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/lecturers");

      setLecturers(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    loadSubjects();

    loadLecturers();
  }, []);

  // SUBJECT INPUT CHANGE
  const handleChange = (e) => {
    setFormData({
      ...formData,

      [e.target.name]: e.target.value,
    });
  };

  // LECTURER INPUT CHANGE
  const handleLecturerChange = (e) => {
    setLecturerForm({
      ...lecturerForm,

      [e.target.name]: e.target.value,
    });
  };

  // ADD SUBJECT
  const addSubject = async () => {
    try {
      await axios.post(
        "http://127.0.0.1:8000/subjects",

        formData,
      );

      loadSubjects();

      setFormData({
        subject_code: "",

        subject_name: "",

        credits: 1,

        session_type: "Lecture",

        preferred_hall_type: "Lecture Hall",

        student_group: "",
      });
    } catch (error) {
      console.log(error);
    }
  };

  // DELETE SUBJECT
  const deleteSubject = async (id) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/subjects/${id}`);

      loadSubjects();
    } catch (error) {
      console.log(error);
    }
  };

  // ADD LECTURER
  const addLecturer = async () => {
    try {
      await axios.post(
        "http://127.0.0.1:8000/lecturers",

        lecturerForm,
      );

      loadLecturers();

      setLecturerForm({
        lecturer_name: "",

        max_hours_per_day: 4,

        preferred_days: "",

        unavailable_day: "",

        unavailable_slot: 1,
      });
    } catch (error) {
      console.log(error);
    }
  };

  // DELETE LECTURER
  const deleteLecturer = async (id) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/lecturers/${id}`);

      loadLecturers();
    } catch (error) {
      console.log(error);
    }
  };

  // GENERATE TIMETABLE
  const generateTimetable = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/ga-optimize");

      setTimetable(response.data.best_timetable);

      setFitness(response.data.best_fitness);
    } catch (error) {
      console.log(error);
    }
  };

  // GET SLOT DATA
  const getSlotData = (day, slot) => {
    return timetable.find((entry) => {
      const start = entry.start_slot;

      const end = start + entry.duration - 1;

      return entry.day === day && slot >= start && slot <= end;
    });
  };

  return (
    <div className="app-layout">
      {/* SIDEBAR */}

      <div className="sidebar">
        <h2>UniSchedule</h2>

        <ul>
          <li>Dashboard</li>

          <li>Subjects</li>

          <li>Lecturers</li>

          <li>Timetable</li>

          <li>Analytics</li>
        </ul>
      </div>

      {/* MAIN */}

      <div className="main-content">
        {/* NAVBAR */}

        <div className="navbar">
          <h1>Smart Timetable Dashboard</h1>

          <button onClick={generateTimetable}>Generate Timetable</button>
        </div>

        {/* CARDS */}

        <div className="cards">
          <div className="card">
            <h3>Fitness Score</h3>

            <p>{fitness}</p>
          </div>

          <div className="card">
            <h3>Subjects</h3>

            <p>{subjects.length}</p>
          </div>

          <div className="card">
            <h3>Lecturers</h3>

            <p>{lecturers.length}</p>
          </div>

          <div className="card">
            <h3>Working Days</h3>

            <p>5 Days</p>
          </div>
        </div>

        {/* SUBJECT FORM */}

        <div className="subject-form">
          <h2>Add Subject</h2>

          <div className="form-grid">
            <input
              name="subject_code"
              placeholder="Subject Code"
              value={formData.subject_code}
              onChange={handleChange}
            />

            <input
              name="subject_name"
              placeholder="Subject Name"
              value={formData.subject_name}
              onChange={handleChange}
            />

            <input
              name="credits"
              type="number"
              placeholder="Credits"
              value={formData.credits}
              onChange={handleChange}
            />

            <input
              name="student_group"
              placeholder="Student Group"
              value={formData.student_group}
              onChange={handleChange}
            />

            <select
              name="session_type"
              value={formData.session_type}
              onChange={handleChange}
            >
              <option>Lecture</option>

              <option>Practical</option>
            </select>

            <select
              name="preferred_hall_type"
              value={formData.preferred_hall_type}
              onChange={handleChange}
            >
              <option>Lecture Hall</option>

              <option>ICT Lab</option>

              <option>Smart Room</option>
            </select>
          </div>

          <button className="add-btn" onClick={addSubject}>
            Add Subject
          </button>
        </div>

        {/* SUBJECT TABLE */}

        <div className="subject-table-container">
          <h2>Subject List</h2>

          <table className="subject-table">
            <thead>
              <tr>
                <th>Code</th>

                <th>Name</th>

                <th>Credits</th>

                <th>Group</th>

                <th>Type</th>

                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              {subjects.map((subject) => (
                <tr key={subject.id}>
                  <td>{subject.subject_code}</td>

                  <td>{subject.subject_name}</td>

                  <td>{subject.credits}</td>

                  <td>{subject.student_group}</td>

                  <td>{subject.session_type}</td>

                  <td>
                    <button
                      className="delete-btn"
                      onClick={() => deleteSubject(subject.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* LECTURER FORM */}

        <div className="subject-form">
          <h2>Add Lecturer</h2>

          <div className="form-grid">
            <input
              name="lecturer_name"
              placeholder="Lecturer Name"
              value={lecturerForm.lecturer_name}
              onChange={handleLecturerChange}
            />

            <input
              name="max_hours_per_day"
              type="number"
              placeholder="Max Hours"
              value={lecturerForm.max_hours_per_day}
              onChange={handleLecturerChange}
            />

            <input
              name="preferred_days"
              placeholder="Preferred Days"
              value={lecturerForm.preferred_days}
              onChange={handleLecturerChange}
            />

            <input
              name="unavailable_day"
              placeholder="Unavailable Day"
              value={lecturerForm.unavailable_day}
              onChange={handleLecturerChange}
            />

            <input
              name="unavailable_slot"
              type="number"
              placeholder="Unavailable Slot"
              value={lecturerForm.unavailable_slot}
              onChange={handleLecturerChange}
            />
          </div>

          <button className="add-btn" onClick={addLecturer}>
            Add Lecturer
          </button>
        </div>

        {/* LECTURER TABLE */}

        <div className="subject-table-container">
          <h2>Lecturer List</h2>

          <table className="subject-table">
            <thead>
              <tr>
                <th>Name</th>

                <th>Max Hours</th>

                <th>Preferred Days</th>

                <th>Unavailable</th>

                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              {lecturers.map((lecturer) => (
                <tr key={lecturer.id}>
                  <td>{lecturer.lecturer_name}</td>

                  <td>{lecturer.max_hours_per_day}</td>

                  <td>{lecturer.preferred_days}</td>

                  <td>
                    {lecturer.unavailable_day} Slot {lecturer.unavailable_slot}
                  </td>

                  <td>
                    <button
                      className="delete-btn"
                      onClick={() => deleteLecturer(lecturer.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* TIMETABLE */}

        <div className="timetable-section">
          <table className="timetable">
            <thead>
              <tr>
                <th>Time</th>

                {DAYS.map((day) => (
                  <th key={day}>{day}</th>
                ))}
              </tr>
            </thead>

            <tbody>
              {SLOTS.map((slotObj) => (
                <>
                  <tr key={slotObj.slot}>
                    <td className="time-cell">{slotObj.label}</td>

                    {DAYS.map((day) => {
                      const data = getSlotData(
                        day,

                        slotObj.slot,
                      );

                      return (
                        <td key={day}>
                          {data && (
                            <div
                              className={`subject-card ${
                                data.subject_name.includes("Programming")
                                  ? "blue-card"
                                  : data.subject_name.includes("Database")
                                    ? "green-card"
                                    : data.subject_name.includes("Mathematics")
                                      ? "purple-card"
                                      : data.subject_name.includes(
                                            "Architecture",
                                          )
                                        ? "orange-card"
                                        : "default-card"
                              }`}
                            >
                              <strong>{data.subject_name}</strong>

                              <p>{data.lecturer_name}</p>

                              <p>{data.hall_name}</p>

                              <small>{data.student_group}</small>
                            </div>
                          )}
                        </td>
                      );
                    })}
                  </tr>

                  {slotObj.slot === 5 && (
                    <tr>
                      <td className="lunch-cell">Lunch</td>

                      <td colSpan="5" className="lunch-break">
                        🍔 Lunch Break
                      </td>
                    </tr>
                  )}
                </>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default App;
