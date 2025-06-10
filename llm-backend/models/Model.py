from abc import ABC

class Model(ABC):

    def to_json(self, excluded_attributes=[]) -> dict:
        json = dict()

        for attribute in self.__dict__:
            if not attribute in excluded_attributes:
                json[attribute] = self.__getattribute__(attribute)

        return json

    @classmethod
    def from_db(cls, db_res):
        """Builds objects from database"""
        attributes = cls.__dict__["__static_attributes__"]
        class_params = dict()

        for attribute_index, attribute in enumerate(attributes):
            class_params[attribute] = db_res[attribute_index]
        built_obj = cls(**class_params)

        return built_obj