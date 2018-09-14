import pytest


@pytest.fixture
def get_price(client):
    def _fn(**kwargs):
        response = client.get('/api/get-price', kwargs)
        return response.json()
    return _fn


def test_empty_request(get_price):
    data = get_price()
    assert 'date' in data
    assert 'productCode' in data
    err_msg = "This field is required."
    assert data['date'] == [err_msg]
    assert data['productCode'] == [err_msg]


@pytest.mark.django_db
def test_normal_small_price(get_price):
    data = get_price(date='2018-06-01', productCode='sm_widget')
    assert data['price'] == 9900


@pytest.mark.django_db
def test_normal_big_price(get_price):
    data = get_price(date='2018-06-01', productCode='big_widget')
    assert data['price'] == 100000


@pytest.mark.django_db
def test_black_friday_small_price(get_price):
    data = get_price(date='2018-11-23', productCode='sm_widget')
    assert data['price'] == 0


@pytest.mark.django_db
def test_black_friday_big_price(get_price):
    data = get_price(date='2018-11-23', productCode='big_widget')
    assert data['price'] == 80000


@pytest.mark.django_db
def test_2019_small_price(get_price):
    data = get_price(date='2019-01-01', productCode='sm_widget')
    assert data['price'] == 12500


@pytest.mark.django_db
def test_2019_big_price(get_price):
    data = get_price(date='2019-01-01', productCode='big_widget')
    assert data['price'] == 120000


@pytest.mark.django_db
def test_10off_gift_card_small(get_price):
    data = get_price(date='2018-06-01',
                     productCode='sm_widget', giftCardCode='10OFF')
    assert data['price'] == 8900


@pytest.mark.django_db
def test_50off_gift_card_small(get_price):
    data = get_price(date='2018-06-01',
                     productCode='sm_widget', giftCardCode='50OFF')
    assert data['price'] == 4900


@pytest.mark.django_db
def test_250off_gift_card_small(get_price):
    data = get_price(date='2018-06-01',
                     productCode='sm_widget', giftCardCode='250OFF')
    # Ensure we get zero, not a negative number
    assert data['price'] == 0


@pytest.mark.django_db
def test_10off_gift_card_big(get_price):
    data = get_price(date='2018-06-01',
                     productCode='big_widget', giftCardCode='10OFF')
    assert data['price'] == 99000


@pytest.mark.django_db
def test_50off_gift_card_big(get_price):
    data = get_price(date='2018-06-01',
                     productCode='big_widget', giftCardCode='50OFF')
    assert data['price'] == 95000


@pytest.mark.django_db
def test_250off_gift_card_big(get_price):
    data = get_price(date='2018-06-01',
                     productCode='big_widget', giftCardCode='250OFF')
    assert data['price'] == 75000
