from flask_restful import Resource, reqparse
from models.class_ import ClassModel


class Class(Resource):
    def get(self, name):
        class_ = ClassModel.find_by_name(name)
        if class_:
            return class_.json()
        return {"message": "This class doesn't exist"}

    def post(self, name):
        if ClassModel.find_by_name(name):
            return {"message": "class with that name already exists"}

        class_ = ClassModel(name)

        class_.save_to_db()

        return class_.json()

    def delete(self, name):
        class_ = ClassModel.find_by_name(name)
        if class_:
            class_.delete_from_db()
            return {"message": "Class deleted"}
        return {"message": f"Class '{name}' doesn't exist"}



class Classes(Resource):
    def get(self):
        return {"Classes": [class_.json() for class_ in ClassModel.find_all()]}