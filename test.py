from canvasapi import Canvas
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import os
import pytz


# Create course object
class Course:
    def __init__(self, course_name):
        self.course_name = course_name


# Create assignment object
class Assignment:
    def __init__(self, name, due_at_date, course_name):
        self.name = name
        self.due_at_date = due_at_date
        self.course_name = course_name


def main():
    # Load environment variables
    API_URL = os.getenv("API_URL")
    API_TOKEN = os.getenv("API_TOKEN")

    # Initialize a new Canvas object
    canvas = Canvas(API_URL, API_TOKEN)
    courses = canvas.get_courses()

    # Determine the current semester (SP23, FA23, etc.)
    current_date = datetime.now(timezone.utc)
    if current_date.month < 7:
        course_term = "SP" + str(current_date.year)[2:]
    else:
        course_term = "FA" + str(current_date.year)[2:]

    course_list = []
    assignment_list = []

    # Search through courses
    for course in courses:
        if not hasattr(course, "name"):  # If course has no enrollment term, continue
            continue
        if course_term not in course.name:  # If course is not in the current semester, continue
            continue

        # Add course to course_list
        course_list.append(Course(course.name[:course.name.index(":")]))
        assignments = course.get_assignments()

        # Search through assignments, add to assignment_list
        for assignment in assignments:
            # If assignment has no due date, continue
            if not hasattr(assignment, "due_at") or assignment.due_at is None:
                continue
            # If assignment is not within the next week, continue
            if assignment.due_at_date < current_date or assignment.due_at_date > current_date \
                    + timedelta(days=7):
                continue
            # Add assignment to assignment_list
            assignment_list.append(Assignment(assignment.name, assignment.due_at_date,
                                              course.name[:course.name.index(":")]))

    # Sort assignments by due date
    assignment_list.sort(key=lambda x: x.due_at_date)

    # Print assignments
    print("ASSIGNMENTS " + current_date.astimezone().strftime("%m/%d/%Y %H:%M:%S")
          + "\n---------------------------------")
    for assignment in assignment_list:
        print("- [ ] " + assignment.due_at_date.astimezone().strftime("%m/%d/%Y %H:%M:%S")
              + "\t" + assignment.course_name
              + " : " + assignment.name)


if __name__ == "__main__":
    main()
