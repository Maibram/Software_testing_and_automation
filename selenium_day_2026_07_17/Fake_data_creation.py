from faker import Faker
from openpyxl import Workbook

fake_data = Faker()
wb = Workbook()
ws = wb.active
ws.title = "FakeUsers"

ws.append(["Name", "Email", "Phone", "Address", "Company"])

for _ in range(10):
    ws.append([
        fake_data.name(),
        fake_data.email(),
        fake_data.phone_number(),
        fake_data.address(),
        fake_data.company(),
    ])

wb.save("fake_user_data.xlsx")
print("Fake user data saved to fake_user_data.xlsx")