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

class LoginTestCSV:
    def __init__(self, csv_file="test_data.csv"):
        self.csv_file = csv_file
        self.results = []
        self.driver = None
        self.original_data = None  # Lưu dữ liệu CSV gốc
        
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
            # Đọc CSV với pandas để xử lý tốt hơn các trường trống
            df = pd.read_csv(self.csv_file, encoding='utf-8')
            self.original_data = df  # Lưu DataFrame gốc
            
            for index, row in df.iterrows():
                test_data.append({
                    'stt': str(row['STT']),
                    'test_case': str(row['Test_Case']),
                    'username': str(row['Username']) if pd.notna(row['Username']) else '',
                    'password': str(row['Password']) if pd.notna(row['Password']) else '',
                    'expected': str(row['Expected']),
                    'description': str(row['Description']) if pd.notna(row['Description']) else ''
                })
            
            print(f"✅ Đã đọc {len(test_data)} test cases từ {self.csv_file}")
            return test_data
            
        except FileNotFoundError:
            print(f"❌ Không tìm thấy file {self.csv_file}")
            return []
        except Exception as e:
            print(f"❌ Lỗi đọc file CSV: {str(e)}")
            return []
    
    def test_login(self, test_data):
        """Test đăng nhập với dữ liệu từ CSV"""
        start_time = time.time()
        
        try:
            # Mở trang login
            login_url = "file:///" + os.path.abspath("web_ban_sach/front-end/UI-EcommerceApp/login.html").replace("\\", "/")
            self.driver.get(login_url)
            
            print(f"\n🔍 Test #{test_data['stt']}: {test_data['test_case']}")
            print(f"   📝 Mô tả: {test_data['description']}")
            print(f"   👤 Username: '{test_data['username']}'")
            print(f"   🔐 Password: '{test_data['password']}'")
            print(f"   🎯 Kết quả mong đợi: {test_data['expected']}")
            
            # Tìm và điền username
            username_field = self.driver.find_element(By.ID, "user")
            username_field.clear()
            username_field.send_keys(test_data['username'])
            
            # Tìm và điền password
            password_field = self.driver.find_element(By.ID, "pass")
            password_field.clear()
            password_field.send_keys(test_data['password'])
            
            # Click nút login
            login_button = self.driver.find_element(By.ID, "login")
            login_button.click()
            
            # Chờ 2 giây để xem kết quả
            time.sleep(2)
            
            execution_time = round(time.time() - start_time, 2)
            
            # Lưu kết quả
            actual_result = 'PASS'  # Giả định PASS nếu không có lỗi
            result = {
                'STT': test_data['stt'],
                'Test Case': test_data['test_case'],
                'Username': test_data['username'],
                'Password': test_data['password'],
                'Expected': test_data['expected'],
                'Actual': actual_result,
                'Status': 'PASS' if test_data['expected'] == actual_result else 'FAIL',
                'Thời gian (s)': execution_time,
                'Mô tả': test_data['description'],
                'Ghi chú': f'{str(e)}'
            }
            
            self.results.append(result)
            print(f"   ✅ Kết quả: THÀNH CÔNG")
            
        except Exception as e:
            execution_time = round(time.time() - start_time, 2)
            actual_result = 'FAIL'
            result = {
                'STT': test_data['stt'],
                'Test Case': test_data['test_case'],
                'Username': test_data['username'],
                'Password': test_data['password'],
                'Expected': test_data['expected'],
                'Actual': actual_result,
                'Status': 'PASS' if test_data['expected'] == actual_result else 'FAIL',
                'Thời gian (s)': execution_time,
                'Mô tả': test_data['description'],
                'Ghi chú': f'{str(e)}'
            }
            self.results.append(result)
            print(f"   ❌ Kết quả: THẤT BẠI - {str(e)}")
    
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
        filename = f'test_results/login_test.xlsx'
        
        # Export Excel
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Sheet kết quả chi tiết
            df.to_excel(writer, sheet_name='Kết quả test', index=False)
            
            # Tự động điều chỉnh độ rộng cột
            worksheet = writer.sheets['Kết quả test']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 40)
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
                    'Tỷ lệ thành công (%)'
                ],
                'Giá trị': [total, passed, failed, expected_pass, expected_fail, pass_rate]
            })
            summary.to_excel(writer, sheet_name='Tóm tắt', index=False)
            
            # Sheet test data gốc
            if self.original_data is not None:
                self.original_data.to_excel(writer, sheet_name='Test Data Gốc', index=False)
            else:
                # Fallback: tạo sheet trống nếu không có dữ liệu gốc
                pd.DataFrame().to_excel(writer, sheet_name='Test Data Gốc', index=False)
        
        print(f"\n📊 Đã xuất kết quả ra file: {filename}")
        return filename
    
    def run_tests(self):
        """Chạy tất cả test cases từ CSV"""
        print("=" * 60)
        print("🧪 BẮT ĐẦU TEST ĐĂNG NHẬP TỪ FILE CSV")
        print("=" * 60)
        
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
            self.test_login(test_data)
            time.sleep(1)  # Nghỉ 1 giây giữa các test
        
        # Đóng browser
        self.driver.quit()
        
        # Hiển thị tóm tắt kết quả
        print("\n" + "=" * 60)
        print("📋 TÓM TẮT KẾT QUẢ TEST")
        print("=" * 60)
        
        total = len(self.results)
        passed = len([r for r in self.results if r['Status'] == 'PASS'])
        failed = total - passed
        
        print(f"📊 Tổng số test: {total}")
        print(f"✅ Thành công: {passed}")
        print(f"❌ Thất bại: {failed}")
        print(f"📈 Tỷ lệ thành công: {round((passed/total)*100, 1)}%")
        
        print("\n📋 Chi tiết:")
        for result in self.results:
            status_icon = "✅" if result['Status'] == 'PASS' else "❌"
            print(f"{status_icon} #{result['STT']} {result['Test Case']}: {result['Status']}")
        
        # Export Excel
        excel_file = self.export_to_excel()
        
        print(f"\n🎉 Hoàn thành! File Excel: {excel_file}")
        print(f"📁 File CSV gốc: {self.csv_file}")

if __name__ == "__main__":
    # Chạy test từ CSV
    test = LoginTestCSV("login_test.csv")
    test.run_tests() 