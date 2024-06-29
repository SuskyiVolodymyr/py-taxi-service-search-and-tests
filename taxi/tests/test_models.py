from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test_name",
            country="country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_manufacturers_ordering(self):
        Manufacturer.objects.bulk_create([
            Manufacturer(name="BB_test", country="country"),
            Manufacturer(name="AA_test", country="country")
        ])
        self.assertEqual(
            list(Manufacturer.objects.all()),
            list(Manufacturer.objects.order_by("name"))
        )

    def test_driver_str(self):
        username = "Test_name"
        password = "Test_1234"
        license_number = "ABC12345"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test_name",
            country="country"
        )
        car = Car.objects.create(model="Test", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)
