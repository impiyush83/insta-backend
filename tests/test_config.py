from insta_backend.app import create_app
from insta_backend.config import ProdConfig


def test_production_config():
    """Production config."""
    app = create_app(ProdConfig)
    assert not app.config.get('DEBUG')

