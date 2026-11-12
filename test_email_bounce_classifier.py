import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import classify, classify_rows

def row(mid, code, reason):
    return {"message_id": mid, "smtp_code": code, "reason": reason}

class TestBounceClassifier(unittest.TestCase):
    def test_5xx_is_hard(self):
        self.assertEqual(classify("550", "mailbox unavailable"), ("HARD BOUNCE", "REMOVE"))
    def test_4xx_is_soft(self):
        self.assertEqual(classify("421", "service unavailable"), ("SOFT BOUNCE", "RETRY"))
    def test_mailbox_full_is_soft_even_on_5xx(self):
        self.assertEqual(classify("552", "mailbox full"), ("SOFT BOUNCE", "RETRY"))
    def test_user_unknown_is_hard_even_on_4xx(self):
        self.assertEqual(classify("450", "user unknown"), ("HARD BOUNCE", "REMOVE"))
    def test_no_such_user_is_hard(self):
        self.assertEqual(classify("550", "no such user here"), ("HARD BOUNCE", "REMOVE"))
    def test_2xx_is_unknown(self):
        self.assertEqual(classify("250", "ok"), ("UNKNOWN", "INVESTIGATE"))
    def test_empty_reason_5xx_is_hard(self):
        self.assertEqual(classify("550", ""), ("HARD BOUNCE", "REMOVE"))
    def test_hard_first(self):
        r = classify_rows([row("M-2", "421", "try again later"),
                           row("M-1", "550", "user unknown")])
        self.assertEqual(r[0][0], "M-1")
    def test_empty_input(self):
        self.assertEqual(classify_rows([]), [])
