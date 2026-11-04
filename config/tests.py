import os
from pathlib import Path
import subprocess
import sys

from django.test import SimpleTestCase


class SecretKeyConfigurationTests(SimpleTestCase):
    def load_settings(self, key):
        env = os.environ.copy()
        env.pop("DJANGO_SECRET_KEY", None)
        if key is not None:
            env["DJANGO_SECRET_KEY"] = key
        # Ignore the developer's local .env when checking missing configuration.
        return subprocess.run(
            [sys.executable, "-c",
             "from unittest.mock import patch; "
             "import runpy; "
             "patch('dotenv.load_dotenv').start(); "
             "settings = runpy.run_path('config/settings.py'); "
             "assert settings['SECRET_KEY'] == 'test-private-key'"],
            cwd=Path(__file__).resolve().parent.parent,
            env=env, capture_output=True, text=True,
        )

    def test_missing_or_blank_secret_stops_startup(self):
        for key in (None, "", "   "):
            with self.subTest(key=key):
                result = self.load_settings(key)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Set DJANGO_SECRET_KEY", result.stderr)

    def test_secret_can_be_supplied_by_environment(self):
        result = self.load_settings("test-private-key")
        self.assertEqual(result.returncode, 0, result.stderr)
