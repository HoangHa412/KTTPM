import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import openpyxl
from datetime import datetime
import time  # Add time module import

class TestOrderManagement(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        
        # Load test data from Excel
        self.wb = openpyxl.load_workbook('testcase.xlsx')
        self.sheet = self.wb['CapNhatTrangThaiDonHang']
        
    def test_update_order_status(self):
        # Test 8 different cases from Excel rows 2-9
        for row in range(2, 10):  # Test cases from row 2 to 9
            try:
                # Get test data from Excel for current row
                username = self.sheet[f'C{row}'].value or ' '  # Username from column C
                password = self.sheet[f'D{row}'].value or ' '  # Password from column D
                role_value = self.sheet[f'E{row}'].value or ' '  # Role from column B
                order_id = self.sheet[f'F{row}'].value or ' '  # Order ID from column E
                order_status = self.sheet[f'G{row}'].value or ' '  # Order status from column F
                
                # Login
                self.driver.get("https://localhost:44329/Login")
                username_elem = self.driver.find_element(By.ID, "txtUsername")
                password_elem = self.driver.find_element(By.ID, "txtPassword")
                username_elem.send_keys(username)
                password_elem.send_keys(password)
                
                # Select role based on Excel value
                role_dropdown = Select(self.driver.find_element(By.ID, "ddlRole"))
                if role_value == "admin":
                    role_dropdown.select_by_value("1")  # Admin has value "1"
                else:
                    role_dropdown.select_by_value("2")  # Khách hàng has value "2"
                
                time.sleep(2)
                self.driver.find_element(By.ID, "btnLogin").click()
                
                # Check for login error message
                try:
                    error_message = self.wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
                    )
                    time.sleep(1)
                    if "error" in error_message.get_attribute("class"):
                        # Update Excel with login failure
                        self.sheet[f'J{row}'] = f"Login failed: {error_message.text}"
                        self.sheet[f'I{row}'] = "FAIL"
                        self.wb.save('testcase.xlsx')  # Save to original file
                        continue  # Skip to next test case
                except:
                    # No error message found, login successful
                    pass
                
                # Navigate to order management
                self.driver.get("https://localhost:44329/Admin/quanlydonhang")
                
                try:
                    # Find the row with the order ID
                    target_row = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, f"//tr[td[text()='{order_id}']]"))
                    )
                except:
                    # Order ID not found, skip this test case
                    self.sheet[f'J{row}'] = "Không tìm thấy đơn hàng"
                    self.sheet[f'I{row}'] = "FAIL"
                    self.wb.save('testcase.xlsx')
                    continue

                # Find and click the update button in that row
                update_btn = target_row.find_element(By.XPATH, ".//input[@value='Cập nhật']")
                # Scroll to the button
                self.driver.execute_script("arguments[0].scrollIntoView(true);", update_btn)
                time.sleep(2)
                # Click the button
                update_btn.click()
                
                # Wait for dropdown to appear and select status
                status_dropdown_elem = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//select[contains(@id, 'ddlTrangThai')]"))
                )
                status_dropdown = Select(status_dropdown_elem)
                
                # Check if the status exists in dropdown
                available_statuses = [option.text for option in status_dropdown.options]
                if order_status not in available_statuses:
                    self.sheet[f'J{row}'] = "Trạng thái không hợp lệ"
                    self.sheet[f'I{row}'] = "FAIL"
                    self.wb.save('testcase.xlsx')
                    continue

                status_dropdown.select_by_visible_text(order_status)
                
                # Get the selected status before clicking save
                selected_status = status_dropdown.first_selected_option.text
                
                # Click save button
                save_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and (@value='Cập nhật' or @value='Update')]"))
                )
                time.sleep(2)
                save_btn.click()
                
                # Verify result
                success_message = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "message")))
                result = "Cập nhật thành công" in success_message.text
                
                # Update Excel with test result
                self.sheet[f'I{row}'] = result  # Test Status
                if result == "PASS":
                    self.sheet[f'J{row}'] = "Cập nhật thành công"
                else:
                    self.sheet[f'J{row}'] = "Cập nhật thất bại"
                
            except Exception as e:
                self.sheet[f'J{row}'] = f"Error: {str(e)}"
                self.sheet[f'I{row}'] = "FAIL"
                
            # Save results after each test case
            self.wb.save('testcase.xlsx')  # Save to original file
            
    def test_view_order_details(self):
        # Similar implementation for viewing order details
        pass
        
    def test_filter_orders(self):
        # Similar implementation for filtering orders
        pass
        
    def tearDown(self):
        # Final save of Excel file with test results
        self.wb.save('testcase.xlsx')  # Save to original file
        self.driver.quit()

if __name__ == '__main__':
    unittest.main() 