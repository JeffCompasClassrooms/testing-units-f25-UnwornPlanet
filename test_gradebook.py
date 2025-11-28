from gradebook import GradeBook
from typing import Dict, Optional
import pytest
import unittest
class GradeBookTests(unittest.TestCase):
    def setUp(self):
        self.obj=GradeBook(70)

    def test_is_instance(self):
        obj=GradeBook(80)
        self.assertIsInstance(obj,GradeBook)

    def test_init_good_input(self):
        obj=GradeBook(70)
        self.assertIsInstance(obj,GradeBook)
        self.assertEqual(obj._passing_score, 70)
        obj1=GradeBook(100)
        self.assertEqual(obj1._passing_score,100)

    def test_init_bad_input(self):
         with self.assertRaises(TypeError):
            obj=GradeBook("hello")
         with self.assertRaises(ValueError):
            obj=GradeBook(-5)
         with self.assertRaises(ValueError):
            obj=GradeBook(150)
         with self.assertRaises(TypeError):
            obj=GradeBook(None)

    def test_passing_score(self):
        obj=GradeBook(70)
        self.assertEqual(obj.passing_score,70)
        self.assertEqual(obj._passing_score,70)
        obj=GradeBook(100)
        self.assertEqual(obj.passing_score,100)
        self.assertEqual(obj._passing_score,100)

    def test_is_locked(self):
        obj=GradeBook(70)
        self.assertFalse(obj.is_locked)
        obj._locked=True
        self.assertTrue(obj.is_locked)
        obj._locked=False
        self.assertFalse(obj.is_locked)

    def test_lock(self):
        obj=GradeBook(70)
        self.assertFalse(obj._locked)
        obj.lock()
        self.assertTrue(obj._locked)
        obj.lock()
        self.assertTrue(obj._locked)

    def test_unlock(self):
        obj=GradeBook(80)
        obj._locked=True
        obj.unlock()
        self.assertFalse(obj._locked)

    def test_add_student_normal(self):
        obj=GradeBook(90)
        obj.add_student("seth cole")
        self.assertIn("seth cole", obj._students)
        obj.add_student("grant twyford")
        self.assertIn("grant twyford", obj._students)

    def test_add_student_duplicate(self):
        obj=GradeBook(90)
        obj.add_student("seth cole")
        with self.assertRaises(ValueError):
            obj.add_student("seth cole")
        obj.add_student("grant twyford")
        with self.assertRaises(ValueError):
            obj.add_student("grant twyford")

    def test_add_student_bad_input(self):
        obj=GradeBook(70)
        with self.assertRaises(ValueError):
            obj.add_student(None)
        with self.assertRaises(ValueError):
            obj.add_student(2)
        with self.assertRaises(ValueError):
            obj.add_student(5.00)
        with self.assertRaises(ValueError):
            obj.add_student("")

    def test_add_student_locked(self):
        obj=GradeBook(80)
        obj.lock()
        with self.assertRaises(RuntimeError):
            obj.add_student("seth cole")
        self.assertNotIn("seth cole", obj._students)
        obj.unlock()
        obj.add_student("seth cole")
        self.assertIn("seth cole", obj._students)

    def test_remove_student_normal(self):
        obj=GradeBook(90)
        obj.add_student("seth cole")
        obj.add_student("grant")
        obj.add_student("jane")
        obj.remove_student("seth cole")
        self.assertNotIn("seth cole", obj._students)
        obj.remove_student("grant")
        self.assertNotIn("grant",obj._students)
        self.assertIn("jane",obj._students)

    def test_remove_student_non_existent_student(self):
        obj=GradeBook(90)
        obj.add_student("jane")
        with self.assertRaises(KeyError):
            obj.remove_student("seth")
        with self.assertRaises(KeyError):
            obj.remove_student(None)
        with self.assertRaises(KeyError):
            obj.remove_student(5)

    def test_remove_while_locked(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        obj.add_student("seth")
        obj.remove_student("jane")
        self.assertNotIn("jane",obj._students)
        obj.lock()
        with self.assertRaises(RuntimeError):
            obj.remove_student("seth")

    def test_set_score(self):
        obj=GradeBook(100)
        obj.add_student("jane")
        obj.set_score("jane", "assignment1", 90)
        self.assertEqual(obj.get_score("jane", "assignment1", 70),90)
        obj.add_student("seth")
        obj.set_score("seth", "assignment1", 70)
        self.assertEqual(obj.get_score("seth", "assignment1", 60),70)

    def test_set_score_bad_assignment_name(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        with self.assertRaises(ValueError):
            obj.set_score("jane","",50)
        with self.assertRaises(ValueError):
            obj.set_score("jane","   ",50)
        with self.assertRaises(ValueError):
            obj.set_score("jane",None,50)
        with self.assertRaises(ValueError):
            obj.set_score("jane",5,50)

    def test_set_score_bad_score_value(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        with self.assertRaises(TypeError):
            obj.set_score("jane","assignment1","hello")
        with self.assertRaises(ValueError):
            obj.set_score("jane","assignment1",-10)
        with self.assertRaises(ValueError):
            obj.set_score("jane","assignment1",150)
        with self.assertRaises(TypeError):
            obj.set_score("jane","assignment1",None)

    def test_set_score_missing_student(self):
        obj=GradeBook(80)
        with self.assertRaises(KeyError):
            obj.set_score("jane","assignment1",90)

    def test_set_score_locked(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        obj.lock()
        with self.assertRaises(RuntimeError):
            obj.set_score("jane","assignment1",90)

    def test_get_score_default_none(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        self.assertIsNone(obj.get_score("jane","assignment1"))
        self.assertIsNone(obj.get_score("jane","assignment2",None))

    def test_get_score_default(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        self.assertEqual(obj.get_score("jane","assignment1",0),0)

    def test_get_score_missing_student_raises(self):
        obj=GradeBook(80)
        with self.assertRaises(KeyError):
            obj.get_score("jane","assignment1",0)

    def test_clear_score_existing_assignment(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        obj.set_score("jane","assignment1",90)
        removed=obj.clear_score("jane","assignment1")
        self.assertTrue(removed)
        self.assertIsNone(obj.get_score("jane","assignment1"))

    def test_clear_score_missing_assignment(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        obj.set_score("jane","assignment1",90)
        removed=obj.clear_score("jane","assignment2")
        self.assertFalse(removed)
        self.assertEqual(obj.get_score("jane","assignment1",0),90)

    def test_clear_score_missing_student(self):
        obj=GradeBook(80)
        with self.assertRaises(KeyError):
            obj.clear_score("jane","assignment1")

    def test_clear_score_locked(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        obj.set_score("jane","assignment1",90)
        obj.lock()
        with self.assertRaises(RuntimeError):
            obj.clear_score("jane","assignment1")

    def test_student_average_no_scores(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        self.assertIsNone(obj.student_average("jane"))

    def test_student_average_multiple_scores(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        obj.set_score("jane","a1",80)
        obj.set_score("jane","a2",100)
        obj.set_score("jane","a3",90)
        self.assertEqual(obj.student_average("jane"),90)

    def test_student_average_missing_student(self):
        obj=GradeBook(80)
        with self.assertRaises(KeyError):
            obj.student_average("jane")

    def test_class_average_no_students(self):
        obj=GradeBook(80)
        self.assertIsNone(obj.class_average())

    def test_class_average_no_scores_for_anyone(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        obj.add_student("seth")
        self.assertIsNone(obj.class_average())

    def test_class_average_mixed_students(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        obj.add_student("seth")
        obj.add_student("grant")
        obj.set_score("jane","a1",80)
        obj.set_score("jane","a2",100)  
        obj.set_score("seth","a1",70)
        obj.set_score("seth","a2",90)    
        self.assertEqual(obj.class_average(),85)

    def test_letter_grade_A(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        obj.set_score("jane","a1",90)
        self.assertEqual(obj.letter_grade("jane"),"A")

    def test_letter_grade_B(self):
        obj=GradeBook(80)
        obj.add_student("seth")
        obj.set_score("seth","a1",80)
        self.assertEqual(obj.letter_grade("seth"),"B")

    def test_letter_grade_C(self):
        obj=GradeBook(80)
        obj.add_student("grant")
        obj.set_score("grant","a1",70)
        self.assertEqual(obj.letter_grade("grant"),"C")

    def test_letter_grade_D_and_F(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        obj.set_score("jane","a1",60)
        self.assertEqual(obj.letter_grade("jane"),"D")
        obj.add_student("seth")
        obj.set_score("seth","a1",50)
        self.assertEqual(obj.letter_grade("seth"),"F")

    def test_letter_grade_no_scores(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        self.assertIsNone(obj.letter_grade("jane"))

    def test_has_passing_grade_true_false(self):
        obj=GradeBook(70)
        obj.add_student("jane")
        obj.add_student("seth")
        obj.set_score("jane","a1",80)
        obj.set_score("seth","a1",60)
        obj.set_score("seth","a2",50)   
        self.assertTrue(obj.has_passing_grade("jane"))
        self.assertFalse(obj.has_passing_grade("seth"))

    def test_has_passing_grade_no_scores(self):
        obj=GradeBook(70)
        obj.add_student("jane")
        self.assertIsNone(obj.has_passing_grade("jane"))

    def test_drop_lowest_score_no_scores(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        self.assertFalse(obj.drop_lowest_score("jane"))

    def test_drop_lowest_score_one_score(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        obj.set_score("jane","a1",90)
        self.assertFalse(obj.drop_lowest_score("jane"))
        self.assertEqual(obj.get_score("jane","a1",0),90)

    def test_drop_lowest_score_multiple_scores(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        obj.set_score("jane","a1",90)
        obj.set_score("jane","a2",70)
        obj.set_score("jane","a3",85)
        result=obj.drop_lowest_score("jane")
        self.assertTrue(result)
        self.assertIsNone(obj.get_score("jane","a2"))
        self.assertEqual(len(obj._students["jane"]),2)

    def test_drop_lowest_score_locked(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        obj.set_score("jane","a1",90)
        obj.set_score("jane","a2",70)
        obj.lock()
        with self.assertRaises(RuntimeError):
            obj.drop_lowest_score("jane")

    def test_curve_student_positive_and_clamp(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        obj.set_score("jane","a1",95)
        obj.set_score("jane","a2",50)
        obj.curve_student("jane",10)
        self.assertEqual(obj.get_score("jane","a1",0),100)
        self.assertEqual(obj.get_score("jane","a2",0),60)

    def test_curve_student_negative_and_clamp(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        obj.set_score("jane","a1",5)
        obj.set_score("jane","a2",40)
        obj.curve_student("jane",-10)
        self.assertEqual(obj.get_score("jane","a1",0),0)
        self.assertEqual(obj.get_score("jane","a2",0),30)

    def test_curve_student_bad_points(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        obj.set_score("jane","a1",90)
        with self.assertRaises(TypeError):
            obj.curve_student("jane","hello")
        with self.assertRaises(TypeError):
            obj.curve_student("jane",None)

    def test_curve_student_missing_student(self):
        obj=GradeBook(80)
        with self.assertRaises(KeyError):
            obj.curve_student("jane",10)

    def test_curve_student_locked(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        obj.set_score("jane","a1",90)
        obj.lock()
        with self.assertRaises(RuntimeError):
            obj.curve_student("jane",5)

    def test_top_student_no_students(self):
        obj=GradeBook(80)
        self.assertIsNone(obj.top_student())

    def test_top_student_no_scores(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        obj.add_student("seth")
        self.assertIsNone(obj.top_student())

    def test_top_student_normal(self):
        obj=GradeBook(80)
        obj.add_student("jane")
        obj.add_student("seth")
        obj.set_score("jane","a1",80)   
        obj.set_score("seth","a1",90)
        self.assertEqual(obj.top_student(),"seth")


