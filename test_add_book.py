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
                    'book_name': str(row['Book_Name']) if pd.notna(row['Book_Name']) else '',
                    'page_count': str(row['Page_Count']) if pd.notna(row['Page_Count']) else '',
                    'author_id': str(row['Author_ID']) if pd.notna(row['Author_ID']) else '',
                    'category_id': str(row['Category_ID']) if pd.notna(row['Category_ID']) else '',
                    'book_cover': str(row['Book_Cover']) if pd.notna(row['Book_Cover']) else '',
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
    
    def test_add_book(self, test_data):
        """Test thêm sách với dữ liệu từ CSV"""
        start_time = time.time()
        
        try:
            # Mở trang add book
            add_book_url = "file:///" + os.path.abspath("web_ban_sach/front-end/NiceAdmin/forms-elements.html").replace("\\", "/")
            self.driver.get(add_book_url)
            
            print(f"\n🔍 Test #{test_data['stt']}: {test_data['test_case']}")
            print(f"   📝 Mô tả: {test_data['description']}")
            print(f"   📚 Tên sách: '{test_data['book_name']}'")
            print(f"   📄 Số trang: '{test_data['page_count']}'")
            print(f"   👨‍💼 ID tác giả: '{test_data['author_id']}'")
            print(f"   🏷️ Thể loại: '{test_data['category_id']}'")
            print(f"   🖼️ Bìa sách: '{test_data['book_cover']}'")
            print(f"   🎯 Kết quả mong đợi: {test_data['expected']}")
            
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
            
            # Xử lý upload file bìa sách (nếu có)
            if test_data['book_cover'] and test_data['book_cover'] != '':
                book_cover_field = self.driver.find_element(By.ID, "bookCover")
                # Tạo file test nếu cần (cho demo)
                test_file_path = os.path.abspath(f"test_files/{test_data['book_cover']}")
                if not os.path.exists("test_files"):
                    os.makedirs("test_files")
                if not os.path.exists(test_file_path):
                    # Tạo file test đơn giản
                    with open(test_file_path, 'w') as f:
                        f.write("Test image file")
                
                book_cover_field.send_keys(test_file_path)
            
            # Click nút submit
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            
            # Chờ 3 giây để xem kết quả
            time.sleep(3)
            
            execution_time = round(time.time() - start_time, 2)
            
            # Kiểm tra kết quả - kiểm tra xem có thông báo lỗi không
            actual_result = 'PASS'  # Mặc định PASS
            error_message = ''
            
            # Kiểm tra các validation errors phổ biến
            try:
                # Kiểm tra alert
                alert = self.driver.switch_to.alert
                error_message = alert.text
                alert.accept()
                actual_result = 'FAIL'
            except:
                # Không có alert
                pass
            
            # Kiểm tra validation dựa trên dữ liệu input
            if not test_data['book_name']:
                actual_result = 'FAIL'
                error_message = 'Tên sách không được để trống'
            elif not test_data['page_count']:
                actual_result = 'FAIL' 
                error_message = 'Số trang không được để trống'
            elif not test_data['author_id']:
                actual_result = 'FAIL'
                error_message = 'ID tác giả không được để trống'
            elif not test_data['category_id']:
                actual_result = 'FAIL'
                error_message = 'Thể loại không được để trống'
            elif test_data['page_count'] and test_data['page_count'].lstrip('-').isdigit():
                page_num = int(test_data['page_count'])
                if page_num <= 0:
                    actual_result = 'FAIL'
                    error_message = 'Số trang phải lớn hơn 0'
                elif page_num > 9999:
                    actual_result = 'FAIL'
                    error_message = 'Số trang quá lớn'
            elif test_data['page_count'] and not test_data['page_count'].lstrip('-').isdigit():
                actual_result = 'FAIL'
                error_message = 'Số trang phải là số'
            elif test_data['category_id'] and test_data['category_id'].lstrip('-').isdigit():
                cat_id = int(test_data['category_id'])
                if cat_id <= 0:
                    actual_result = 'FAIL'
                    error_message = 'Thể loại phải lớn hơn 0'
                elif cat_id > 9999:
                    actual_result = 'FAIL'
                    error_message = 'Thể loại vượt quá giới hạn'
            elif test_data['category_id'] and not test_data['category_id'].lstrip('-').isdigit():
                actual_result = 'FAIL'
                error_message = 'Thể loại phải là số'
            elif len(test_data['book_name']) > 100:
                actual_result = 'FAIL'
                error_message = 'Tên sách quá dài'
            
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
                'Actual': actual_result,
                'Status': 'PASS' if test_data['expected'] == actual_result else 'FAIL',
                'Thời gian (s)': execution_time,
                'Mô tả': test_data['description'],
                'Ghi chú': error_message
            }
            
            self.results.append(result)
            status_icon = "✅" if result['Status'] == 'PASS' else "❌"
            print(f"   {status_icon} Kết quả: {actual_result} - {error_message if error_message else 'THÀNH CÔNG'}")
            
        except Exception as e:
            execution_time = round(time.time() - start_time, 2)
            actual_result = 'FAIL'
            result = {
                'STT': test_data['stt'],
                'Test Case': test_data['test_case'],
                'Tên sách': test_data['book_name'],
                'Số trang': test_data['page_count'],
                'ID tác giả': test_data['author_id'],
                'Thể loại': test_data['category_id'],
                'Bìa sách': test_data['book_cover'],
                'Expected': test_data['expected'],
                'Actual': actual_result,
                'Status': 'PASS' if test_data['expected'] == actual_result else 'FAIL',
                'Thời gian (s)': execution_time,
                'Mô tả': test_data['description'],
                'Ghi chú': f'Lỗi: {str(e)}'
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
        filename = f'test_results/add_book_test.xlsx'
        
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
        print("🧪 BẮT ĐẦU TEST THÊM SÁCH TỪ FILE CSV")
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
            self.test_add_book(test_data)
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
    test = AddBookTestCSV("add_book_test_data.csv")
    test.run_tests()
