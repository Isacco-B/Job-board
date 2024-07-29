from flask_restx import Resource, Namespace
# from flask_restx.errors import abort
# from ..models.user_model import Course, Student
# from ..schemas.user_schema import (
#     course_model,
#     student_model,
#     course_input_model,
#     student_input_model,
# )
# from ..utils.extensions import db

ns = Namespace("api", description="Job Board API")


@ns.route("/courses")
class CourseListApi(Resource):

    @ns.marshal_list_with(course_model)
    def get(self):
        return Course.query.all()

    @ns.expect(course_input_model)
    @ns.marshal_with(course_model)
    def post(self):
        course = Course(name=ns.payload["name"])  # type: ignore
        db.session.add(course)
        db.session.commit()
        return course, 201


@ns.route("/courses/<int:course_id>")
class CourseApi(Resource):

    @ns.marshal_with(course_model)
    def get(self, course_id):
        return Course.query.get_or_404(course_id)


@ns.route("/students")
class StudentListApi(Resource):

    @ns.marshal_list_with(student_model)
    def get(self):
        return Student.query.all()

    @ns.expect(student_input_model)
    @ns.marshal_with(student_model)
    def post(self):
        student = Student(name=ns.payload["name"], course_id=ns.payload["course_id"])  # type: ignore
        db.session.add(student)
        db.session.commit()
        return student, 201


@ns.route("/students/<int:student_id>")
class StudentApi(Resource):

    @ns.marshal_with(student_model)
    def get(self, student_id):
        return Student.query.get_or_404(student_id)

    @ns.expect(student_input_model)
    @ns.marshal_with(student_model)
    def put(self, student_id):
        student = Student.query.get_or_404(student_id)
        student.name = ns.payload["name"]
        student.course_id = ns.payload["course_id"]
        db.session.commit()
        return student, 201

    @ns.marshal_with(student_model)
    def delete(self, student_id):
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return student, 204
