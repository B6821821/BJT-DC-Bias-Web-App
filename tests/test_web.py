"""Flask HTTP route tests — test client, ไม่ต้องเปิดเซิร์ฟเวอร์จริง."""

import unittest

from app import app


class TestWebRoutes(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index_shows_form(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        self.assertIn("VCC", body)
        self.assertIn("R1", body)

    def test_calculate_shows_results(self):
        response = self.client.post("/calculate", data=dict(
            vcc="12", r1="100", r2="22", rc="2.2", re="1",
            beta="100", vbe="0.70",
        ))
        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        self.assertIn("1.9422", body)   # VB
        self.assertIn("Forward Active", body)

    def test_invalid_input_shows_error_and_keeps_values(self):
        response = self.client.post("/calculate", data=dict(
            vcc="12", r1="100", r2="22", rc="2.2", re="0",
            beta="100", vbe="0.70",
        ))
        self.assertEqual(response.status_code, 400)
        body = response.get_data(as_text=True)
        self.assertIn("RE", body)
        self.assertIn('value="12"', body)   # ค่าที่กรอกยังคงอยู่

    def test_non_numeric_shows_error(self):
        response = self.client.post("/calculate", data=dict(
            vcc="abc", r1="100", r2="22", rc="2.2", re="1",
            beta="100", vbe="0.70",
        ))
        self.assertEqual(response.status_code, 400)
        body = response.get_data(as_text=True)
        self.assertIn("ตัวเลข", body)


if __name__ == "__main__":
    unittest.main()
