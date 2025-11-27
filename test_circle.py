import math
from circle import Circle
import pytest
import unittest
class CircleTests(unittest.TestCase):
    def setUp(self):
        self.obj=Circle(2)
    def test_is_instance(self):
        self.assertIsInstance(self.obj,Circle)
    def test_getRadius(self):
        obj=Circle(2)
        self.assertEqual(obj.getRadius(), 2)
        obj.setRadius(3)
        self.assertEqual(obj.getRadius(),3)
    def test_allows_negative_radius(self):
        obj=Circle(-2)
        self.assertEqual(obj.getRadius(),-2)
        obj=Circle(-5)
        self.assertEqual(obj.getRadius(),-5)
    def test_setRadius(self):
        obj=Circle(0)
        obj.setRadius(2)
        self.assertEqual(obj.getRadius(),2)
        obj.setRadius(-2)
        self.assertEqual(obj.getRadius(),2)
        self.assertTrue(obj.setRadius(4))
        self.assertFalse(obj.setRadius(-3))
    def test_getArea(self):
        obj=Circle(2)
        self.assertEqual(obj.getArea(),0)
        obj.setRadius(3)
        self.assertEqual(obj.getArea(),(math.pi*3*3))
    def test_getCircumference(self):
        obj=Circle(4)
        self.assertEqual(obj.getCircumference(),(2.*math.pi*4))
        obj=Circle(5)
        self.assertEqual(obj.getCircumference(),(2.*math.pi*5))
    def test_allows_bad_init(self):
        obj=Circle(None)
        self.assertEqual(obj.getRadius(),None)
        obj1=Circle("hello")
        self.assertIsInstance(obj1.getRadius(),str)
    def test_raises_on_bad_radius_calculations(self):
        obj=Circle(None)
        with self.assertRaises(TypeError):
            obj.getArea()
        with self.assertRaises(TypeError):
            obj.getCircumference()
        obj1=Circle("hello")
        with self.assertRaises(TypeError):
            obj.getArea()
        with self.assertRaises(TypeError):
            obj.getCircumference()
    def test_raises_on_bad_radius(self):
        obj=Circle(2)
        with self.assertRaises(TypeError):
            obj.setRadius(None)
        with self.assertRaises(TypeError):
            obj.setRadius("hello")

