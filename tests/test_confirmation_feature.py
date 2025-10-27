import pytest
from click.testing import CliRunner
from src.main import cli

class TestConfirmationFeature:
    def setup_method(self):
        self.runner = CliRunner()
    
    def test_inv_6_delete_confirmation_accept(self, monkeypatch):
        """Test INV-6: Confirmation when user accepts deletion"""
        # Simulate user input 'y' for confirmation
        monkeypatch.setattr('click.confirm', lambda prompt: True)
        
        result = self.runner.invoke(cli, ['delete-product', '--sku', 'TEST123'])
        
        # Should proceed with deletion flow
        assert "PRODUCT TO DELETE" in result.output
        assert "Are you sure" in result.output

    def test_inv_6_delete_confirmation_reject(self, monkeypatch):
        """Test INV-6: Confirmation when user rejects deletion"""
        # Simulate user input 'n' for confirmation
        monkeypatch.setattr('click.confirm', lambda prompt: False)
        
        result = self.runner.invoke(cli, ['delete-product', '--sku', 'TEST123'])
        
        # Should show cancellation message
        assert "Deletion cancelled" in result.output