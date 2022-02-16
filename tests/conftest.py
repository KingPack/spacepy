import pytest

# from spacepy.main import create_app




# @pytest.fixture(scope='module')
# def app():
#     """ Create and configure a new app instance for each test case. """

#     return create_app()


@pytest.fixture()
def salgadinho():
    return 'coxinha'