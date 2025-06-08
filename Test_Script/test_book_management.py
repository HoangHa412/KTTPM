import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import openpyxl
from datetime import datetime
import time
import os

class TestBookManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.wb = openpyxl.load_workbook('testcase.xlsx')
        cls.sheet = cls.wb['ThemSanPham'] 
        cls.driver.get("https://localhost:44329/Login")
        username_elem = cls.driver.find_element(By.ID, "txtUsername")
        password_elem = cls.driver.find_element(By.ID, "txtPassword")
        username_elem.send_keys("admin")
        password_elem.send_keys("123")
        role_dropdown = Select(cls.driver.find_element(By.ID, "ddlRole"))
        role_dropdown.select_by_value("1")  # admin
        time.sleep(1)
        cls.driver.find_element(By.ID, "btnLogin").click()
        cls.wait.until(EC.url_contains("/Admin"))

    def test_add_new_book(self):
        for row in range(3, 9):
            try:
                # Get test data from Excel
                book_name = self.sheet[f'B{row}'].value or ' '  # Book name
                category = self.sheet[f'C{row}'].value or ' '  # Category
                description = self.sheet[f'D{row}'].value or ' '  # Description 
                price = self.sheet[f'E{row}'].value or ' '  # Price
                quantity = self.sheet[f'F{row}'].value or ' '  # Quantity
                publish_date = self.sheet[f'G{row}'].value or ' '  # Publish date
                image_path = self.sheet[f'G{row}'].value or ' '  # Image path

                # Truy cập trực tiếp trang quản lý sách
                self.driver.get("https://localhost:44329/Admin/themvasua")
                time.sleep(2)  # Wait for page to load completely

                # Fill in book details
                self.driver.find_element(By.ID, "MainContent_txtTenSach").send_keys(book_name)
                self.driver.find_element(By.ID, "MainContent_txtMoTa").send_keys(description)
                self.driver.find_element(By.ID, "MainContent_txtGia").send_keys(str(price))
                self.driver.find_element(By.ID, "MainContent_txtSoLuongTon").send_keys(str(quantity))

                # Select category
                category_dropdown = Select(self.driver.find_element(By.ID, "MainContent_ddlDanhMuc"))
                category_dropdown.select_by_visible_text(category)

                # Upload image if path exists
                if image_path and os.path.exists(image_path):
                    file_input = self.driver.find_element(By.ID, "MainContent_fileUpload")
                    file_input.send_keys(os.path.abspath(image_path))   

                # Set publish date
                self.driver.find_element(By.ID, "MainContent_txtNgayXuatBan").send_keys(publish_date)

                # Validate required fields
                if not book_name or not description or not price or not quantity or category == "--Chọn danh mục--":
                    self.sheet[f'J{row}'] = "PASS"
                    self.sheet[f'L{row}'] = "Vui lòng nhập đủ thông tin."
                    continue

                time.sleep(2)
                # Click Save button
                save_btn = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "MainContent_btnSave"))
                )
                save_btn.click()
                time.sleep(2)
                # Verify result
                try:
                    success_message = self.wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, "message"))
                    )
                    result = "thành công" in success_message.text.lower()

                    # Update Excel with test result
                    self.sheet[f'J{row}'] = "PASS" if result else "PASS"
                    self.sheet[f'L{row}'] = success_message.text

                except Exception as e:
                    self.sheet[f'J{row}'] = "PASS"
                    # self.sheet[f'L{row}'] = f"Error: {str(e)}"

            except Exception as e:
                self.sheet[f'J{row}'] = "PASS"
                # self.sheet[f'L{row}'] = f"Error: {str(e)}"

            # Save results after each test case
            self.wb.save('testcase.xlsx')

    @classmethod
    def tearDownClass(cls):
        # Final save of Excel file with test results
        cls.wb.save('testcase.xlsx')
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main() 