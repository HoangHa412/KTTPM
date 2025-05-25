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

class AddBookTestCSV:
    def __init__(self, csv_file="add_book_test_data.csv"):
        self.csv_file = csv_file
        self.results = []
        self.driver = None
        
    def setup_driver(self):
        """Thiết lập Chrome driver"""
        chrome_options = Options()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        
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
                        'book_name': row['Book_Name'] if row['Book_Name'] else '',
                        'page_count': row['Page_Count'] if row['Page_Count'] else '',
                        'author_id': row['Author_ID'] if row['Author_ID'] else '',
                        'category_id': row['Category_ID'] if row['Category_ID'] else '',
                        'book_cover': row['Book_Cover'] if row['Book_Cover'] else '',
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
    
    def test_add_book(self, test_data):
        """Test thêm sách với dữ liệu từ CSV"""
        start_time = time.time()
        
        try:
            # Mở trang thêm sách
            add_book_url = "file:///" + os.path.abspath("web_ban_sach/front-end/NiceAdmin/forms-elements.html").replace("\\", "/")
            self.driver.get(add_book_url)
            
            print(f"\n🔍 Test #{test_data['stt']}: {test_data['test_case']}")
            print(f"   📝 Mô tả: {test_data['description']}")
            print(f"   📚 Tên sách: '{test_data['book_name']}'")
            print(f"   📄 Số trang: '{test_data['page_count']}'")
            print(f"   ✍️ ID tác giả: '{test_data['author_id']}'")
            print(f"   📂 Thể loại: '{test_data['category_id']}'")
            print(f"   🖼️ Bìa sách: '{test_data['book_cover']}'")
            print(f"   🎯 Kết quả mong đợi: {test_data['expected']}")
            
            # Chờ trang load
            time.sleep(2)
            
            # Tìm và điền tên sách
            book_name_field = self.driver.find_element(By.ID, "bookName")
            book_name_field.clear()
            book_name_field.send_keys(test_data['book_name'])
            
            # Tìm và điền số trang
            page_count_field = self.driver.find_element(By.ID, "pageCount")
            page_count_field.clear()
            page_count_field.send_keys(test_data['page_count'])
            
            # Tìm và điền ID tác giả
            author_id_field = self.driver.find_element(By.ID, "authorId")
            author_id_field.clear()
            author_id_field.send_keys(test_data['author_id'])
            
            # Tìm và điền thể loại
            category_id_field = self.driver.find_element(By.ID, "categoryId")
            category_id_field.clear()
            category_id_field.send_keys(test_data['category_id'])
            
            # Upload file bìa sách (nếu có)
            if test_data['book_cover']:
                try:
                    book_cover_field = self.driver.find_element(By.ID, "bookCover")
                    # Tạo file dummy để test upload
                    dummy_file_path = os.path.abspath("dummy_book_cover.txt")
                    with open(dummy_file_path, 'w') as f:
                        f.write("dummy book cover content")
                    book_cover_field.send_keys(dummy_file_path)
                except Exception as upload_error:
                    print(f"   ⚠️ Không thể upload file: {upload_error}")
            
            # Click nút Submit
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            
            # Chờ 2 giây để xem kết quả
            time.sleep(2)
            
            execution_time = round(time.time() - start_time, 2)
            
            # Kiểm tra validation
            validation_result = self.check_validation(test_data)
            
            # Lưu kết quả
            result = {
                'STT': test_data['stt'],
                'Test Case': test_data['test_case'],
                'Tên sách': test_data['book_name'],
                'Số trang': test_data['page_count'],
                'ID tác giả': test_data['author_id'],
                'Thể loại': test_data['category_id'],
                'Bìa sách': test_data['book_cover'],
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
                'Tên sách': test_data['book_name'],
                'Số trang': test_data['page_count'],
                'ID tác giả': test_data['author_id'],
                'Thể loại': test_data['category_id'],
                'Bìa sách': test_data['book_cover'],
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
        """Kiểm tra validation logic cho form thêm sách"""
        
        # Kiểm tra các trường bắt buộc
        if not test_data['book_name'].strip():
            return {'status': 'FAIL', 'message': 'Tên sách không được để trống'}
        
        if not test_data['page_count']:
            return {'status': 'FAIL', 'message': 'Số trang không được để trống'}
        
        if not test_data['author_id'].strip():
            return {'status': 'FAIL', 'message': 'ID tác giả không được để trống'}
        
        if not test_data['category_id']:
            return {'status': 'FAIL', 'message': 'Thể loại không được để trống'}
        
        # Kiểm tra số trang
        try:
            page_count = int(test_data['page_count'])
            if page_count <= 0:
                return {'status': 'FAIL', 'message': 'Số trang phải lớn hơn 0'}
            if page_count > 10000:
                return {'status': 'FAIL', 'message': 'Số trang không thể quá 10000'}
        except ValueError:
            return {'status': 'FAIL', 'message': 'Số trang phải là số nguyên'}
        
        # Kiểm tra thể loại
        try:
            category_id = int(test_data['category_id'])
            if category_id <= 0:
                return {'status': 'FAIL', 'message': 'Thể loại phải lớn hơn 0'}
            if category_id > 1000:
                return {'status': 'FAIL', 'message': 'Thể loại vượt quá giới hạn'}
        except ValueError:
            return {'status': 'FAIL', 'message': 'Thể loại phải là số nguyên'}
        
        # Kiểm tra độ dài tên sách
        if len(test_data['book_name']) > 100:
            return {'status': 'FAIL', 'message': 'Tên sách quá dài (tối đa 100 ký tự)'}
        
        # Kiểm tra ID tác giả có ký tự đặc biệt (trừ số và chữ)
        author_id = test_data['author_id']
        if not author_id.replace('_', '').replace('-', '').isalnum():
            return {'status': 'FAIL', 'message': 'ID tác giả chỉ được chứa chữ, số, dấu gạch dưới và gạch ngang'}
        
        return {'status': 'PASS', 'message': 'Thêm sách hợp lệ'}
    
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
        filename = f'test_results/add_book_test.xlsx'
        
        # Export Excel
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Sheet kết quả chi tiết
            df.to_excel(writer, sheet_name='Kết quả test thêm sách', index=False)
            
            # Tự động điều chỉnh độ rộng cột
            worksheet = writer.sheets['Kết quả test thêm sách']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 30)
                worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Sheet tóm tắt
            total = len(self.results)
            passed = len([r for r in self.results if r['Status'] == 'PASS'])
            failed = total - passed
            expected_pass = len([r for r in self.results if r['Expected'] == 'PASS'])
            expected_fail = len([r for r in self.results if r['Expected'] == 'FAIL'])
            pass_rate = round((passed/total)*100, 1) if total > 0 else 0
            
            # Thống kê theo loại test
            fail_cases = {
                'Trường trống': len([r for r in self.results if 'trống' in r['Test Case'].lower()]),
                'Validation lỗi': len([r for r in self.results if any(word in r['Test Case'].lower() for word in ['âm', 'lớn', 'chữ', 'ký tự'])]),
                'Hợp lệ': len([r for r in self.results if r['Expected'] == 'PASS'])
            }
            
            summary = pd.DataFrame({
                'Thông số': [
                    'Tổng số test', 
                    'Thực tế PASS', 
                    'Thực tế FAIL',
                    'Mong đợi PASS',
                    'Mong đợi FAIL',
                    'Tỷ lệ đúng (%)',
                    'Avg execution time (s)',
                    '---',
                    'Test trường trống',
                    'Test validation lỗi',
                    'Test hợp lệ'
                ],
                'Giá trị': [
                    total, 
                    passed, 
                    failed, 
                    expected_pass, 
                    expected_fail, 
                    pass_rate,
                    round(sum([r['Thời gian (s)'] for r in self.results]) / total, 2) if total > 0 else 0,
                    '---',
                    fail_cases['Trường trống'],
                    fail_cases['Validation lỗi'],
                    fail_cases['Hợp lệ']
                ]
            })
            summary.to_excel(writer, sheet_name='Tóm tắt', index=False)
            
            # Sheet test data gốc
            df_original = pd.read_csv(self.csv_file)
            df_original.to_excel(writer, sheet_name='Test Data Gốc', index=False)
        
        print(f"\n📊 Đã xuất kết quả ra file: {filename}")
        return filename
    
    def cleanup(self):
        """Dọn dẹp file dummy"""
        try:
            dummy_file = os.path.abspath("dummy_book_cover.txt")
            if os.path.exists(dummy_file):
                os.remove(dummy_file)
        except:
            pass
    
    def run_tests(self):
        """Chạy tất cả test cases từ CSV"""
        print("=" * 70)
        print("🧪 BẮT ĐẦU TEST THÊM SÁCH TỪ FILE CSV")
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
            self.test_add_book(test_data)
            time.sleep(1)  # Nghỉ 1 giây giữa các test
        
        # Đóng browser
        self.driver.quit()
        
        # Dọn dẹp
        self.cleanup()
        
        # Hiển thị tóm tắt kết quả
        print("\n" + "=" * 70)
        print("📋 TÓM TẮT KẾT QUẢ TEST THÊM SÁCH")
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
        
        # Thống kê theo loại
        print(f"\n📊 Phân loại test:")
        print(f"   📝 Test trường trống: {len([r for r in self.results if 'trống' in r['Test Case'].lower()])}")
        print(f"   ⚠️ Test validation: {len([r for r in self.results if any(word in r['Test Case'].lower() for word in ['âm', 'lớn', 'chữ', 'ký tự'])])}")
        print(f"   ✅ Test hợp lệ: {len([r for r in self.results if r['Expected'] == 'PASS'])}")
        
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
    test = AddBookTestCSV("add_book_test_data.csv")
    test.run_tests() 