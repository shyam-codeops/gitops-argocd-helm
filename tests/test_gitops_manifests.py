"""
Unit tests validating GitOps ArgoCD & Rollouts manifests using standard library.
"""

import os
import re
import unittest


class TestGitOpsManifests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    def read_manifest(self, rel_path: str) -> str:
        full_path = os.path.join(self.repo_root, rel_path)
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()

    def test_root_app_spec(self):
        content = self.read_manifest("bootstrap/root-app.yaml")
        self.assertIn("kind: Application", content)
        self.assertIn("project: enterprise-platform", content)
        self.assertIn("prune: true", content)
        self.assertIn("selfHeal: true", content)

    def test_applicationset_multi_env(self):
        content = self.read_manifest("bootstrap/applicationset-environments.yaml")
        self.assertIn("kind: ApplicationSet", content)
        self.assertIn("env: dev", content)
        self.assertIn("env: stage", content)
        self.assertIn("env: prod", content)
        # Verify manual sync gate for prod
        self.assertTrue(re.search(r"env:\s*prod\s*\n\s*namespace:\s*prod-apps\s*\n\s*autoSync:\s*false", content))

    def test_appproject_governance(self):
        content = self.read_manifest("bootstrap/argocd-project.yaml")
        self.assertIn("kind: AppProject", content)
        self.assertIn("prod-apps", content)
        self.assertIn("syncWindows:", content)

    def test_canary_progressive_delivery(self):
        content = self.read_manifest("progressive-delivery/canary-rollout.yaml")
        self.assertIn("kind: AnalysisTemplate", content)
        self.assertIn("kind: Rollout", content)
        self.assertIn("setWeight: 10", content)
        self.assertIn("successCondition: result[0] >= 0.99", content)


if __name__ == "__main__":
    unittest.main()
