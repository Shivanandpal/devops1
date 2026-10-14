from flask import Flask, jsonify

app = Flask(__name__)

# Sample data for practical examination purposes.
STUDENTS = {
    "101": {"name": "Aarav Shah", "python": 78, "mathematics": 82, "devops": 91},
    "102": {"name": "Diya Patil", "python": 67, "mathematics": 73, "devops": 69},
    "103": {"name": "Kabir Joshi", "python": 28, "mathematics": 45, "devops": 32},
}

PASS_MARK = 35


def calculate_result(student):
    """Return total, percentage, and pass/fail status for a student's marks."""
    marks = [student["python"], student["mathematics"], student["devops"]]
    total = sum(marks)
    percentage = round(total / len(marks), 2)
    status = "PASS" if all(mark >= PASS_MARK for mark in marks) else "FAIL"

    return {
        "total": total,
        "percentage": percentage,
        "status": status,
    }


@app.get("/")
def home():
    return jsonify({
        "application": "Student Result Management System",
        "message": "Use /results/<roll_number> to view a student's result.",
        "sample_roll_numbers": list(STUDENTS.keys()),
    })


@app.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.get("/results/<roll_number>")
def get_result(roll_number):
    student = STUDENTS.get(roll_number)
    if student is None:
        return jsonify({"error": "Student roll number not found"}), 404

    result = calculate_result(student)
    response = {
        "roll_number": roll_number,
        "name": student["name"],
        "marks": {
            "python": student["python"],
            "mathematics": student["mathematics"],
            "devops": student["devops"],
        },
        **result,
    }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
