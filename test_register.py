import time
import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import os

class RegisterTestCSV:
    def __init__(self, csv_file="register_test_data.csv"):
        self.csv_file = csv_file
        self.results = []
        self.driver = None
        
    def setup_driver(self):
        """Thiết lập Chrome driver"""
        chrome_options = Options()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
    
    def load_test_data(self):
        """Đọc dữ liệu test từ file CSV"""
        test_data = []
        
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    test_data.append({
                        'stt': row['STT'],
                        'test_case': row['Test_Case'],
                        'name': row['Name'] if row['Name'] else '',
                        'address': row['Address'] if row['Address'] else '',
                        'phone': row['Phone'] if row['Phone'] else '',
                        'username': row['Username'] if row['Username'] else '',
                        'password': row['Password'] if row['Password'] else '',
                        'confirm_password': row['Confirm_Password'] if row['Confirm_Password'] else '',
                        'expected': row['Expected'],
                        'description': row['Description']
                    })
            
            print(f"✅ Đã đọc {len(test_data)} test cases từ {self.csv_file}")
            return test_data
            
        except FileNotFoundError:
            print(f"❌ Không tìm thấy file {self.csv_file}")
            return []
        except Exception as e:
            print(f"❌ Lỗi đọc file CSV: {str(e)}")
            return []
    
    def test_register(self, test_data):
        """Test đăng ký với dữ liệu từ CSV"""
        start_time = time.time()
        
        try:
            # Mở trang đăng ký
            register_url = "file:///" + os.path.abspath("web_ban_sach/front-end/UI-EcommerceApp/register.html").replace("\\", "/")
            self.driver.get(register_url)
            
            print(f"\n🔍 Test #{test_data['stt']}: {test_data['test_case']}")
            print(f"   📝 Mô tả: {test_data['description']}")
            print(f"   👤 Tên: '{test_data['name']}'")
            print(f"   🏠 Địa chỉ: '{test_data['address']}'")
            print(f"   📞 SĐT: '{test_data['phone']}'")
            print(f"   🔑 Username: '{test_data['username']}'")
            print(f"   🔐 Password: '{test_data['password']}'")
            print(f"   ✅ Confirm: '{test_data['confirm_password']}'")
            print(f"   🎯 Kết quả mong đợi: {test_data['expected']}")
            
            # Tìm và điền tên
            name_field = self.driver.find_element(By.XPATH, "//input[@placeholder='name']")
            name_field.clear()
            name_field.send_keys(test_data['name'])
            
            # Tìm và điền địa chỉ
            address_field = self.driver.find_element(By.XPATH, "//input[@placeholder='address']")
            address_field.clear()
            address_field.send_keys(test_data['address'])
            
            # Tìm và điền số điện thoại
            phone_field = self.driver.find_element(By.XPATH, "//input[@placeholder='phone_numbers']")
            phone_field.clear()
            phone_field.send_keys(test_data['phone'])
            
            # Tìm và điền username
            username_field = self.driver.find_element(By.XPATH, "//input[@placeholder='account_user']")
            username_field.clear()
            username_field.send_keys(test_data['username'])
            
            # Tìm và điền password
            password_field = self.driver.find_element(By.XPATH, "//input[@placeholder='password_user']")
            password_field.clear()
            password_field.send_keys(test_data['password'])
            
            # Tìm và điền confirm password
            confirm_password_field = self.driver.find_element(By.XPATH, "//input[@placeholder='confirm_password']")
            confirm_password_field.clear()
            confirm_password_field.send_keys(test_data['confirm_password'])
            
            # Click nút register
            register_button = self.driver.find_element(By.XPATH, "//button[text()='Register']")
            register_button.click()
            
            # Chờ 3 giây để xem kết quả
            time.sleep(3)
            
            execution_time = round(time.time() - start_time, 2)
            
            # Kiểm tra validation
            validation_result = self.check_validation(test_data)
            
            # Lưu kết quả
            result = {
                'STT': test_data['stt'],
                'Test Case': test_data['test_case'],
                'Tên': test_data['name'],
                'Địa chỉ': test_data['address'],
                'SĐT': test_data['phone'],
                'Username': test_data['username'],
                'Password': test_data['password'],
                'Confirm Password': test_data['confirm_password'],
                'Expected': test_data['expected'],
                'Actual': validation_result['status'],
                'Status': 'PASS' if validation_result['status'] == test_data['expected'] else 'FAIL',
                'Thời gian (s)': execution_time,
                'Mô tả': test_data['description'],
                'Ghi chú': validation_result['message']
            }
            
            self.results.append(result)
            status_icon = "✅" if result['Status'] == 'PASS' else "❌"
            print(f"   {status_icon} Kết quả: {result['Status']} - {validation_result['message']}")
            
        except Exception as e:
            execution_time = round(time.time() - start_time, 2)
            result = {
                'STT': test_data['stt'],
                'Test Case': test_data['test_case'],
                'Tên': test_data['name'],
                'Địa chỉ': test_data['address'],
                'SĐT': test_data['phone'],
                'Username': test_data['username'],
                'Password': test_data['password'],
                'Confirm Password': test_data['confirm_password'],
                'Expected': test_data['expected'],
                'Actual': 'ERROR',
                'Status': 'FAIL',
                'Thời gian (s)': execution_time,
                'Mô tả': test_data['description'],
                'Ghi chú': f'{str(e)}'
            }
            self.results.append(result)
            print(f"   ❌ Kết quả: THẤT BẠI - {str(e)}")
    
    def check_validation(self, test_data):
        """Kiểm tra validation logic"""
        # Kiểm tra các trường bắt buộc
        if not test_data['name']:
            return {'status': 'FAIL', 'message': 'Tên không được để trống'}
        
        if not test_data['address']:
            return {'status': 'FAIL', 'message': 'Địa chỉ không được để trống'}
        
        if not test_data['phone']:
            return {'status': 'FAIL', 'message': 'Số điện thoại không được để trống'}
        
        if not test_data['username']:
            return {'status': 'FAIL', 'message': 'Username không được để trống'}
        
        if not test_data['password']:
            return {'status': 'FAIL', 'message': 'Password không được để trống'}
        
        if not test_data['confirm_password']:
            return {'status': 'FAIL', 'message': 'Confirm password không được để trống'}
        
        # Kiểm tra password khớp
        if test_data['password'] != test_data['confirm_password']:
            return {'status': 'FAIL', 'message': 'Password và confirm password không khớp'}
        
        # Kiểm tra độ dài password
        if len(test_data['password']) < 6:
            return {'status': 'FAIL', 'message': 'Password phải có ít nhất 6 ký tự'}
        
        # Kiểm tra số điện thoại
        phone = test_data['phone']
        if phone:
            if not phone.isdigit():
                return {'status': 'FAIL', 'message': 'Số điện thoại chỉ được chứa số'}
            
            if len(phone) < 10 or len(phone) > 11:
                return {'status': 'FAIL', 'message': 'Số điện thoại phải có 10-11 số'}
            
            if not phone.startswith('0'):
                return {'status': 'FAIL', 'message': 'Số điện thoại phải bắt đầu bằng số 0'}
        
        # Kiểm tra username
        username = test_data['username']
        if len(username) > 50:
            return {'status': 'FAIL', 'message': 'Username quá dài'}
        
        # Kiểm tra ký tự đặc biệt trong username (trừ email)
        if '@' not in username and any(char in username for char in '@#$%^&*()'):
            return {'status': 'FAIL', 'message': 'Username chứa ký tự đặc biệt không hợp lệ'}
        
        # Kiểm tra khoảng trắng trong password
        if ' ' in test_data['password']:
            return {'status': 'FAIL', 'message': 'Password không được chứa khoảng trắng'}
        
        # Kiểm tra tên có số
        if any(char.isdigit() for char in test_data['name']):
            return {'status': 'FAIL', 'message': 'Tên không được chứa số'}
        
        return {'status': 'PASS', 'message': 'Đăng ký hợp lệ'}
    
    def export_to_excel(self):
        """Export kết quả ra Excel"""
        if not self.results:
            print("Không có kết quả để export!")
            return
        
        # Tạo DataFrame
        df = pd.DataFrame(self.results)
        
        # Tạo thư mục kết quả
        os.makedirs('test_results', exist_ok=True)
        
        # Tên file với timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'test_results/register_test.xlsx'
        
        # Export Excel
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Sheet kết quả chi tiết
            df.to_excel(writer, sheet_name='Kết quả test đăng ký', index=False)
            
            # Tự động điều chỉnh độ rộng cột
            worksheet = writer.sheets['Kết quả test đăng ký']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 35)
                worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Sheet tóm tắt
            total = len(self.results)
            passed = len([r for r in self.results if r['Status'] == 'PASS'])
            failed = total - passed
            expected_pass = len([r for r in self.results if r['Expected'] == 'PASS'])
            expected_fail = len([r for r in self.results if r['Expected'] == 'FAIL'])
            pass_rate = round((passed/total)*100, 1) if total > 0 else 0
            
            summary = pd.DataFrame({
                'Thông số': [
                    'Tổng số test', 
                    'Thực tế PASS', 
                    'Thực tế FAIL',
                    'Mong đợi PASS',
                    'Mong đợi FAIL',
                    'Tỷ lệ đúng (%)',
                    'Avg execution time (s)'
                ],
                'Giá trị': [
                    total, 
                    passed, 
                    failed, 
                    expected_pass, 
                    expected_fail, 
                    pass_rate,
                    round(sum([r['Thời gian (s)'] for r in self.results]) / total, 2) if total > 0 else 0
                ]
            })
            summary.to_excel(writer, sheet_name='Tóm tắt', index=False)
            
            # Sheet test data gốc
            df_original = pd.read_csv(self.csv_file)
            df_original.to_excel(writer, sheet_name='Test Data Gốc', index=False)
        
        print(f"\n📊 Đã xuất kết quả ra file: {filename}")
        return filename
    
    def run_tests(self):
        """Chạy tất cả test cases từ CSV"""
        print("=" * 70)
        print("🧪 BẮT ĐẦU TEST ĐĂNG KÝ TỪ FILE CSV")
        print("=" * 70)
        
        # Đọc dữ liệu test từ CSV
        test_data_list = self.load_test_data()
        
        if not test_data_list:
            print("❌ Không có dữ liệu test để chạy!")
            return
        
        # Thiết lập driver
        self.setup_driver()
        
        print(f"🚀 Sẽ chạy {len(test_data_list)} test cases...")
        
        # Chạy từng test
        for test_data in test_data_list:
            self.test_register(test_data)
            time.sleep(1)  # Nghỉ 1 giây giữa các test
        
        # Đóng browser
        self.driver.quit()
        
        # Hiển thị tóm tắt kết quả
        print("\n" + "=" * 70)
        print("📋 TÓM TẮT KẾT QUẢ TEST ĐĂNG KÝ")
        print("=" * 70)
        
        total = len(self.results)
        passed = len([r for r in self.results if r['Status'] == 'PASS'])
        failed = total - passed
        expected_pass = len([r for r in self.results if r['Expected'] == 'PASS'])
        
        print(f"📊 Tổng số test: {total}")
        print(f"✅ Test đúng: {passed}")
        print(f"❌ Test sai: {failed}")
        print(f"🎯 Test cases mong đợi PASS: {expected_pass}")
        print(f"📈 Tỷ lệ test đúng: {round((passed/total)*100, 1)}%")
        
        print("\n📋 Chi tiết kết quả:")
        for result in self.results:
            status_icon = "✅" if result['Status'] == 'PASS' else "❌"
            print(f"{status_icon} #{result['STT']} {result['Test Case']}: {result['Status']} - {result['Ghi chú']}")
        
        # Export Excel
        excel_file = self.export_to_excel()
        
        print(f"\n🎉 Hoàn thành! File Excel: {excel_file}")
        print(f"📁 File CSV gốc: {self.csv_file}")

if __name__ == "__main__":
    # Chạy test từ CSV
    test = RegisterTestCSV("register_test_data.csv")
    test.run_tests() 