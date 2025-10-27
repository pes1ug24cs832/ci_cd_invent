import pytest
from click.testing import CliRunner
from src.main import cli


class TestConfirmationFeature:
    def setup_method(self):
        self.runner = CliRunner()

    def test_inv_6_delete_confirmation_accept(self, monkeypatch):
        """Test INV-6: Confirmation when user accepts deletion"""
        # First add a product to delete
        with self.runner.isolated_filesystem():
            # Add a product first
            result = self.runner.invoke(
                cli,
                [
                    "add-product",
                    "--name",
                    "Test Product",
                    "--sku",
                    "TEST123",
                    "--price",
                    "10.0",
                    "--quantity",
                    "5",
                    "--category",
                    "Test",
                    "--description",
                    "Test product",
                ],
            )

            # Now test deletion with confirmation
            monkeypatch.setattr("click.confirm", lambda prompt: True)
            result = self.runner.invoke(cli, ["delete-product", "--sku", "TEST123"])

            # Should proceed with deletion flow
            assert (
                "PRODUCT TO DELETE" in result.output
                or "deleted successfully" in result.output
            )

    def test_inv_6_delete_confirmation_reject(self, monkeypatch):
        """Test INV-6: Confirmation when user rejects deletion"""
        with self.runner.isolated_filesystem():
            # Add a product first
            result = self.runner.invoke(
                cli,
                [
                    "add-product",
                    "--name",
                    "Test Product",
                    "--sku",
                    "TEST123",
                    "--price",
                    "10.0",
                    "--quantity",
                    "5",
                    "--category",
                    "Test",
                    "--description",
                    "Test product",
                ],
            )

            # Test deletion rejection
            monkeypatch.setattr("click.confirm", lambda prompt: False)
            result = self.runner.invoke(cli, ["delete-product", "--sku", "TEST123"])

            # Should show cancellation message
            assert "cancelled" in result.output.lower()
