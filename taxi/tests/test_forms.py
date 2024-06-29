import pytest
from django.test import Client
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


@pytest.fixture
def authorize_user():
    user = Driver.objects.create_user(
        username="Test_name",
        password="Test_1234",
        license_number="ABC12345"
    )
    client = Client()
    client.force_login(user)
    return client


@pytest.mark.django_db
def test_correct_searching_manufacturer(authorize_user):
    Manufacturer.objects.bulk_create([
        Manufacturer(name="BB_test", country="country"),
        Manufacturer(name="AA_test", country="country")
    ])
    url = reverse("taxi:manufacturer-list") + "?name=AA"
    res = authorize_user.get(url)
    assert "AA_test" in res.content.decode()
    assert "BB_test" not in res.content.decode()


@pytest.mark.django_db
def test_correct_searching_car(authorize_user):
    manufacturer = Manufacturer.objects.create(name="test", country="country")
    Car.objects.bulk_create([
        Car(model="BB_test", manufacturer=manufacturer),
        Car(model="AA_test", manufacturer=manufacturer)
    ])
    url = reverse("taxi:car-list") + "?model=AA"
    res = authorize_user.get(url)
    assert "AA_test" in res.content.decode()
    assert "BB_test" not in res.content.decode()


@pytest.mark.django_db
def test_correct_searching_driver(authorize_user):
    Driver.objects.create_user(
        username="AA_test",
        password="Test_1234",
        license_number="AAA11111"
    )
    Driver.objects.create_user(
        username="BB_test",
        password="Test_1234",
        license_number="AAA11112"
    )

    url = reverse("taxi:driver-list") + "?username=AA"
    res = authorize_user.get(url)
    assert "AA_test" in res.content.decode()
    assert "BB_test" not in res.content.decode()


@pytest.mark.django_db
def test_pagination_manufacturer(authorize_user):
    Manufacturer.objects.bulk_create(
        [
            Manufacturer(name=f"Test{i}", country="country") for i in range(15)
        ]
    )
    url = reverse("taxi:manufacturer-list") + "?page=2"
    res = authorize_user.get(url)
    assert "next" in res.content.decode()
    assert "prev" in res.content.decode()


@pytest.mark.django_db
def test_pagination_car(authorize_user):
    manufacturer = Manufacturer.objects.create(name="Test", country="country")
    Car.objects.bulk_create(
        [
            Car(model=f"Test{i}", manufacturer=manufacturer) for i in range(15)
        ]
    )
    url = reverse("taxi:car-list") + "?page=2"
    res = authorize_user.get(url)
    assert "next" in res.content.decode()
    assert "prev" in res.content.decode()


@pytest.mark.django_db
def test_pagination_driver(authorize_user):
    Driver.objects.bulk_create(
        [
            Driver(
                username=f"Test{i}",
                password="Test_1234",
                license_number=f"AAA{i}") for i in range(10000, 10015)
        ]
    )
    url = reverse("taxi:driver-list") + "?page=2"
    res = authorize_user.get(url)
    assert "next" in res.content.decode()
    assert "prev" in res.content.decode()
