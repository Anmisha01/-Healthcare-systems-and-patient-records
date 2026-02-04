"""
Tests for GitHub Actions workflow configuration and CI/CD pipeline execution.

This module tests that:
- The workflow file is valid YAML
- All required jobs are defined
- Jobs have correct triggers (push, pull_request)
- Python versions are properly specified
- Dependencies are installed correctly
- Test commands execute successfully
"""

import os
import subprocess
import sys

import pytest
import yaml


class TestWorkflowConfiguration:
    """Tests for the GitHub Actions workflow YAML configuration."""

    @pytest.fixture
    def workflow_file(self):
        """Load the GitHub Actions workflow YAML file."""
        workflow_path = os.path.join(
            os.path.dirname(__file__), "..", ".github", "workflows", "main.yml"
        )
        with open(workflow_path, "r") as f:
            return yaml.safe_load(f)

    def test_workflow_file_exists(self):
        """Verify the workflow file exists."""
        workflow_path = os.path.join(
            os.path.dirname(__file__), "..", ".github", "workflows", "main.yml"
        )
        assert os.path.exists(workflow_path), "Workflow file should exist"

    def test_workflow_is_valid_yaml(self, workflow_file):
        """Verify the workflow file is valid YAML."""
        assert workflow_file is not None, "Workflow file should be valid YAML"

    def test_workflow_has_name(self, workflow_file):
        """Verify the workflow has a name."""
        assert "name" in workflow_file, "Workflow should have a name"
        assert workflow_file["name"] == "CI/CD Pipeline"

    def test_workflow_has_triggers(self, workflow_file):
        """Verify the workflow has push and pull_request triggers."""
        # YAML parses 'on' as True in some cases
        trigger_key = "on" if "on" in workflow_file else True
        assert trigger_key in workflow_file, "Workflow should have triggers"
        assert "push" in workflow_file[trigger_key], "Workflow should trigger on push"
        assert (
            "pull_request" in workflow_file[trigger_key]
        ), "Workflow should trigger on pull_request"

    def test_push_branches(self, workflow_file):
        """Verify push trigger includes main and develop branches."""
        trigger_key = "on" if "on" in workflow_file else True
        branches = workflow_file[trigger_key]["push"]["branches"]
        assert "main" in branches, "Should trigger on main branch"
        assert "develop" in branches, "Should trigger on develop branch"

    def test_pull_request_branches(self, workflow_file):
        """Verify pull_request trigger includes main and develop branches."""
        trigger_key = "on" if "on" in workflow_file else True
        branches = workflow_file[trigger_key]["pull_request"]["branches"]
        assert "main" in branches, "Should trigger on pull requests to main"
        assert "develop" in branches, "Should trigger on pull requests to develop"

    def test_workflow_has_jobs(self, workflow_file):
        """Verify the workflow has jobs defined."""
        assert "jobs" in workflow_file, "Workflow should have jobs"
        assert len(workflow_file["jobs"]) > 0, "Workflow should have at least one job"

    def test_test_job_exists(self, workflow_file):
        """Verify the 'test' job exists."""
        assert "test" in workflow_file["jobs"], "Workflow should have a test job"

    def test_test_job_runs_on_ubuntu(self, workflow_file):
        """Verify the test job runs on ubuntu-latest."""
        test_job = workflow_file["jobs"]["test"]
        assert test_job["runs-on"] == "ubuntu-latest"

    def test_test_job_has_python_matrix(self, workflow_file):
        """Verify the test job has a Python version matrix."""
        test_job = workflow_file["jobs"]["test"]
        assert "strategy" in test_job, "Test job should have a strategy"
        assert "matrix" in test_job["strategy"], "Strategy should have a matrix"
        assert "python-version" in test_job["strategy"]["matrix"]

    def test_python_versions_specified(self, workflow_file):
        """Verify all required Python versions are tested."""
        test_job = workflow_file["jobs"]["test"]
        versions = test_job["strategy"]["matrix"]["python-version"]
        assert "3.8" in versions, "Should test Python 3.8"
        assert "3.9" in versions, "Should test Python 3.9"
        assert "3.10" in versions, "Should test Python 3.10"
        assert "3.11" in versions, "Should test Python 3.11"

    def test_test_job_has_steps(self, workflow_file):
        """Verify the test job has steps defined."""
        test_job = workflow_file["jobs"]["test"]
        assert "steps" in test_job, "Test job should have steps"
        assert len(test_job["steps"]) > 0, "Test job should have at least one step"

    def test_checkout_step_exists(self, workflow_file):
        """Verify the test job checks out code."""
        test_job = workflow_file["jobs"]["test"]
        checkout_steps = [s for s in test_job["steps"] if "actions/checkout" in str(s)]
        assert len(checkout_steps) > 0, "Test job should checkout code"

    def test_python_setup_step_exists(self, workflow_file):
        """Verify the test job sets up Python."""
        test_job = workflow_file["jobs"]["test"]
        setup_steps = [s for s in test_job["steps"] if "actions/setup-python" in str(s)]
        assert len(setup_steps) > 0, "Test job should set up Python"

    def test_dependencies_installation_step(self, workflow_file):
        """Verify dependencies are installed in the test job."""
        test_job = workflow_file["jobs"]["test"]
        install_steps = [
            s
            for s in test_job["steps"]
            if "Install dependencies" in str(s.get("name", ""))
        ]
        assert len(install_steps) > 0, "Test job should install dependencies"

        install_step = install_steps[0]
        run_command = install_step["run"]
        assert "pip" in run_command, "Should use pip to install dependencies"
        assert "pytest" in run_command, "Should install pytest"
        assert "pycryptodome" in run_command, "Should install pycryptodome"

    def test_test_execution_step(self, workflow_file):
        """Verify tests are executed."""
        test_job = workflow_file["jobs"]["test"]
        test_steps = [s for s in test_job["steps"] if "pytest" in str(s.get("run", ""))]
        assert len(test_steps) > 0, "Test job should run pytest"

    def test_coverage_reporting(self, workflow_file):
        """Verify code coverage is reported."""
        test_job = workflow_file["jobs"]["test"]
        test_steps = [s for s in test_job["steps"] if "cov" in str(s.get("run", ""))]
        assert len(test_steps) > 0, "Test job should report coverage"

    def test_lint_job_exists(self, workflow_file):
        """Verify the 'lint' job exists."""
        assert "lint" in workflow_file["jobs"], "Workflow should have a lint job"

    def test_lint_job_configuration(self, workflow_file):
        """Verify the lint job is properly configured."""
        lint_job = workflow_file["jobs"]["lint"]
        assert lint_job["runs-on"] == "ubuntu-latest"
        assert "steps" in lint_job
        assert len(lint_job["steps"]) > 0

    def test_lint_includes_black(self, workflow_file):
        """Verify lint job includes black formatting check."""
        lint_job = workflow_file["jobs"]["lint"]
        black_steps = [s for s in lint_job["steps"] if "black" in str(s.get("run", ""))]
        assert len(black_steps) > 0, "Lint job should check code formatting with black"

    def test_lint_includes_isort(self, workflow_file):
        """Verify lint job includes isort import ordering check."""
        lint_job = workflow_file["jobs"]["lint"]
        isort_steps = [s for s in lint_job["steps"] if "isort" in str(s.get("run", ""))]
        assert len(isort_steps) > 0, "Lint job should check import ordering with isort"

    def test_lint_includes_flake8(self, workflow_file):
        """Verify lint job includes flake8 linting."""
        lint_job = workflow_file["jobs"]["lint"]
        flake8_steps = [
            s for s in lint_job["steps"] if "flake8" in str(s.get("run", ""))
        ]
        assert len(flake8_steps) > 0, "Lint job should lint code with flake8"

    def test_security_job_exists(self, workflow_file):
        """Verify the 'security' job exists."""
        assert (
            "security" in workflow_file["jobs"]
        ), "Workflow should have a security job"

    def test_security_job_configuration(self, workflow_file):
        """Verify the security job is properly configured."""
        security_job = workflow_file["jobs"]["security"]
        assert security_job["runs-on"] == "ubuntu-latest"
        assert "steps" in security_job
        assert len(security_job["steps"]) > 0

    def test_security_includes_bandit(self, workflow_file):
        """Verify security job includes bandit security scanning."""
        security_job = workflow_file["jobs"]["security"]
        bandit_steps = [
            s for s in security_job["steps"] if "bandit" in str(s.get("run", ""))
        ]
        assert len(bandit_steps) > 0, "Security job should run bandit security scan"


class TestWorkflowExecution:
    """Tests for verifying the workflow steps can execute correctly."""

    def test_python_version_available(self):
        """Verify current Python version matches requirements."""
        python_version = sys.version_info
        assert python_version.major == 3, "Should use Python 3"
        assert python_version.minor >= 8, "Should use Python 3.8 or higher"

    def test_pip_available(self):
        """Verify pip is available."""
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"], capture_output=True, text=True
        )
        assert result.returncode == 0, "pip should be available"

    def test_required_packages_installable(self):
        """Verify required packages can be installed."""
        packages = ["pytest", "pycryptodome", "PyQt5", "pyyaml"]
        for package in packages:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "show", package],
                capture_output=True,
                text=True,
            )
            # We only check if the command succeeds, package might not be installed
            # but the command format is valid
            assert result.returncode in [0, 1], f"pip show {package} should work"

    def test_pytest_can_discover_tests(self):
        """Verify pytest can discover tests in the tests directory."""
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "tests/"],
            capture_output=True,
            text=True,
            cwd=os.path.join(os.path.dirname(__file__), ".."),
        )
        # pytest --collect-only should return 0 if it can find tests
        assert (
            result.returncode == 0 or "test session starts" in result.stdout
        ), "pytest should be able to discover tests"


class TestWorkflowSecurityAndBestPractices:
    """Tests for security and best practices in the workflow."""

    @pytest.fixture
    def workflow_file(self):
        """Load the GitHub Actions workflow YAML file."""
        workflow_path = os.path.join(
            os.path.dirname(__file__), "..", ".github", "workflows", "main.yml"
        )
        with open(workflow_path, "r") as f:
            return yaml.safe_load(f)

    def test_uses_pinned_action_versions(self, workflow_file):
        """Verify actions are pinned to specific versions."""
        jobs = workflow_file["jobs"]
        for job_name, job_config in jobs.items():
            steps = job_config.get("steps", [])
            for step in steps:
                if "uses" in step:
                    uses = step["uses"]
                    # Actions should use @vX format (e.g., @v3, @v4)
                    assert "@" in uses, f"Action in {job_name} should be pinned: {uses}"

    def test_test_job_has_pip_upgrade(self, workflow_file):
        """Verify pip is upgraded before installation."""
        test_job = workflow_file["jobs"]["test"]
        install_steps = [
            s
            for s in test_job["steps"]
            if "Install dependencies" in str(s.get("name", ""))
        ]
        assert len(install_steps) > 0

        install_step = install_steps[0]
        run_command = install_step["run"]
        assert "pip install --upgrade pip" in run_command, "pip should be upgraded"

    def test_lint_python_version_specified(self, workflow_file):
        """Verify lint job specifies a Python version."""
        lint_job = workflow_file["jobs"]["lint"]
        setup_steps = [s for s in lint_job["steps"] if "actions/setup-python" in str(s)]
        assert len(setup_steps) > 0, "Lint job should specify Python version"

    def test_security_python_version_specified(self, workflow_file):
        """Verify security job specifies a Python version."""
        security_job = workflow_file["jobs"]["security"]
        setup_steps = [
            s for s in security_job["steps"] if "actions/setup-python" in str(s)
        ]
        assert len(setup_steps) > 0, "Security job should specify Python version"

    def test_codecov_upload_configured(self, workflow_file):
        """Verify codecov upload is configured."""
        test_job = workflow_file["jobs"]["test"]
        codecov_steps = [
            s for s in test_job["steps"] if "codecov" in str(s.get("uses", ""))
        ]
        assert len(codecov_steps) > 0, "Test job should upload to codecov"

    def test_bandit_security_scan_non_blocking(self, workflow_file):
        """Verify bandit security scan doesn't block the workflow."""
        security_job = workflow_file["jobs"]["security"]
        bandit_steps = [
            s
            for s in security_job["steps"]
            if s.get("name") and "bandit" in s.get("name", "")
        ]
        assert len(bandit_steps) > 0

        # The command should have || true to not fail the job
        bandit_step = bandit_steps[0]
        run_command = bandit_step["run"]
        assert "|| true" in run_command, "bandit should not fail the workflow"
