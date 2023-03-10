#!/usr/bin/python3
<<<<<<< HEAD
"""Defines unittests for models/place.py.

Unittest classes:
    TestPlace_instantiation
    TestPlace_save
    TestPlace_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Place class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Place, type(Place()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_is_public_class_attribute(self):
        pl = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(pl))
        self.assertNotIn("city_id", pl.__dict__)

    def test_user_id_is_public_class_attribute(self):
        pl = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(pl))
        self.assertNotIn("user_id", pl.__dict__)

    def test_name_is_public_class_attribute(self):
        pl = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(pl))
        self.assertNotIn("name", pl.__dict__)

    def test_description_is_public_class_attribute(self):
        pl = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(pl))
        self.assertNotIn("desctiption", pl.__dict__)

    def test_number_rooms_is_public_class_attribute(self):
        pl = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(pl))
        self.assertNotIn("number_rooms", pl.__dict__)

    def test_number_bathrooms_is_public_class_attribute(self):
        pl = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(pl))
        self.assertNotIn("number_bathrooms", pl.__dict__)

    def test_max_guest_is_public_class_attribute(self):
        pl = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(pl))
        self.assertNotIn("max_guest", pl.__dict__)

    def test_price_by_night_is_public_class_attribute(self):
        pl = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(pl))
        self.assertNotIn("price_by_night", pl.__dict__)

    def test_latitude_is_public_class_attribute(self):
        pl = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(pl))
        self.assertNotIn("latitude", pl.__dict__)

    def test_longitude_is_public_class_attribute(self):
        pl = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(pl))
        self.assertNotIn("longitude", pl.__dict__)

    def test_amenity_ids_is_public_class_attribute(self):
        pl = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(pl))
        self.assertNotIn("amenity_ids", pl.__dict__)

    def test_two_places_unique_ids(self):
        pl1 = Place()
        pl2 = Place()
        self.assertNotEqual(pl1.id, pl2.id)

    def test_two_places_different_created_at(self):
        pl1 = Place()
        sleep(0.05)
        pl2 = Place()
        self.assertLess(pl1.created_at, pl2.created_at)

    def test_two_places_different_updated_at(self):
        pl1 = Place()
        sleep(0.05)
        pl2 = Place()
        self.assertLess(pl1.updated_at, pl2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        pl = Place()
        pl.id = "123456"
        pl.created_at = pl.updated_at = dt
        plstr = pl.__str__()
        self.assertIn("[Place] (123456)", plstr)
        self.assertIn("'id': '123456'", plstr)
        self.assertIn("'created_at': " + dt_repr, plstr)
        self.assertIn("'updated_at': " + dt_repr, plstr)

    def test_args_unused(self):
        pl = Place(None)
        self.assertNotIn(None, pl.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        pl = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(pl.id, "345")
        self.assertEqual(pl.created_at, dt)
        self.assertEqual(pl.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_save(unittest.TestCase):
    """Unittests for testing save method of the Place class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        pl = Place()
        sleep(0.05)
        first_updated_at = pl.updated_at
        pl.save()
        self.assertLess(first_updated_at, pl.updated_at)

    def test_two_saves(self):
        pl = Place()
        sleep(0.05)
        first_updated_at = pl.updated_at
        pl.save()
        second_updated_at = pl.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        pl.save()
        self.assertLess(second_updated_at, pl.updated_at)

    def test_save_with_arg(self):
        pl = Place()
        with self.assertRaises(TypeError):
            pl.save(None)

    def test_save_updates_file(self):
        pl = Place()
        pl.save()
        plid = "Place." + pl.id
        with open("file.json", "r") as f:
            self.assertIn(plid, f.read())


class TestPlace_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        pl = Place()
        self.assertIn("id", pl.to_dict())
        self.assertIn("created_at", pl.to_dict())
        self.assertIn("updated_at", pl.to_dict())
        self.assertIn("__class__", pl.to_dict())

    def test_to_dict_contains_added_attributes(self):
        pl = Place()
        pl.middle_name = "Holberton"
        pl.my_number = 98
        self.assertEqual("Holberton", pl.middle_name)
        self.assertIn("my_number", pl.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        pl = Place()
        pl_dict = pl.to_dict()
        self.assertEqual(str, type(pl_dict["id"]))
        self.assertEqual(str, type(pl_dict["created_at"]))
        self.assertEqual(str, type(pl_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        pl = Place()
        pl.id = "123456"
        pl.created_at = pl.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(pl.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        pl = Place()
        self.assertNotEqual(pl.to_dict(), pl.__dict__)

    def test_to_dict_with_arg(self):
        pl = Place()
        with self.assertRaises(TypeError):
            pl.to_dict(None)


if __name__ == "__main__":
    unittest.main()
=======
"""
Test for the Place class
"""


from datetime import datetime
import inspect
from models import place
from models.base_model import BaseModel
import pep8
import unittest
Place = place.Place

c = "created_at"
u = "updated_at"


class TestStateDocStyle(unittest.TestCase):
    """test for documentation and pep8 style"""
    def setUp(cls):
        """set up for methods"""
        cls.place_func = inspect.getmembers(Place, inspect.isfunction)

    def test_pep8(self):
        """test pep8 in Place class"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/place.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors and warnings.")

    def test_pep8_test(self):
        """test pep8 for test to Place class"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_place.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors and warnings.")

    def test_module_doc(self):
        """test for the doc in module"""
        self.assertIsNot(place.__doc__, None,
                         "place.py without a docstring")
        self.assertTrue(len(place.__doc__) >= 1,
                        "place.py without a docstring")

    def test_class_doc(self):
        """test for class documentation"""
        self.assertIsNot(Place.__doc__, None,
                         "Place class without docstring")
        self.assertTrue(len(Place.__doc__) >= 1,
                        "Place class without docstring")

    def test_func_doc(self):
        """test for doc in methods"""
        for func in self.place_func:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} docstring needed in method".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} docstring needed in method".format(func[0]))


class TestPlaceClass(unittest.TestCase):
    """test for class"""
    def test_is_subclass(self):
        """test for a subclass of BaseModel"""
        place = Place()
        self.assertIsInstance(place, BaseModel)
        self.assertTrue(hasattr(place, "id"))
        self.assertTrue(hasattr(place, "created_at"))
        self.assertTrue(hasattr(place, "updated_at"))

    def test_city_id(self):
        """thest for for attribute city_id for Place class"""
        place = Place()
        self.assertTrue(hasattr(place, "city_id"))
        self.assertEqual(place.city_id, "")

    def test_user_id(self):
        """test for the user_id attr"""
        place = Place()
        self.assertTrue(hasattr(place, "user_id"))
        self.assertEqual(place.user_id, "")

    def test_name(self):
        """test for the name attribute in the Place class"""
        place = Place()
        self.assertTrue(hasattr(place, "name"))
        self.assertEqual(place.name, "")

    def test_description(self):
        """test for description in Place class"""
        place = Place()
        self.assertTrue(hasattr(place, "description"))
        self.assertEqual(place.description, "")

    def test_number_rooms(self):
        """test for number of rooms in Place class"""
        place = Place()
        self.assertTrue(hasattr(place, "number_rooms"))
        self.assertEqual(type(place.number_rooms), int)
        self.assertEqual(place.number_rooms, 0)

    def test_number_bathrooms_attr(self):
        """Test Place has attr number_bathrooms, and it's an int == 0"""
        place = Place()
        self.assertTrue(hasattr(place, "number_bathrooms"))
        self.assertEqual(type(place.number_bathrooms), int)
        self.assertEqual(place.number_bathrooms, 0)

    def test_to_dict_values(self):
        """test the values in dict"""
        time = "%Y-%m-%dT%H:%M:%S.%f"
        place = Place()
        new_dict = place.to_dict()
        self.assertEqual(new_dict["__class__"], "Place")
        self.assertEqual(type(new_dict[c]), str)
        self.assertEqual(type(new_dict[u]), str)
        self.assertEqual(new_dict[c], place.created_at.strftime(time))
        self.assertEqual(new_dict[u], place.updated_at.strftime(time))

    def test_max_guest_attr(self):
        """Test Place has attr max_guest, and it's an int == 0"""
        place = Place()
        self.assertTrue(hasattr(place, "max_guest"))
        self.assertEqual(type(place.max_guest), int)
        self.assertEqual(place.max_guest, 0)

    def test_price_by_night(self):
        """Test Place has attr price_by_night, and it's an int == 0"""
        place = Place()
        self.assertTrue(hasattr(place, "price_by_night"))
        self.assertEqual(type(place.price_by_night), int)
        self.assertEqual(place.price_by_night, 0)

    def test_latitude_attr(self):
        """Test Place has attr latitude, and it's a float == 0.0"""
        place = Place()
        self.assertTrue(hasattr(place, "latitude"))
        self.assertEqual(type(place.latitude), float)
        self.assertEqual(place.latitude, 0.0)

    def test_longitude(self):
        """Test Place has attr longitude, and it's a float == 0.0"""
        place = Place()
        self.assertTrue(hasattr(place, "longitude"))
        self.assertEqual(type(place.longitude), float)
        self.assertEqual(place.longitude, 0.0)

    def test_str(self):
        """test for output str method"""
        place = Place()
        string = "[Place] ({}) {}".format(place.id, place.__dict__)
        self.assertEqual(string, str(place))
>>>>>>> Giddy
