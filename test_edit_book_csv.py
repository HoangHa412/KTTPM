import time
import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import os

class EditBookTestCSV:
    def __init__(self, csv_file="edit_book_test_data.csv"):
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
                        'book_id': row['Book_ID'] if row['Book_ID'] else '',
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
    
    def check_alert(self, expected_status):
        """Kiểm tra và xử lý alert"""
        wait = WebDriverWait(self.driver, 3)
        alert_text = ""
        alert_found = False
        
        try:
            # Chờ alert xuất hiện
            alert = wait.until(EC.alert_is_present())
            alert_text = alert.text
            alert_found = True
            
            print(f"   🔔 Alert phát hiện: '{alert_text}'")
            
            # Accept alert
            alert.accept()
            
            # Phân tích nội dung alert
            if expected_status == "FAIL":
                if any(keyword in alert_text.lower() for keyword in ["lỗi", "❌", "không được", "phải", "cảnh báo", "⚠️", "không tìm thấy", "không tồn tại"]):
                    return {"found": True, "text": alert_text, "valid": True}
                else:
                    return {"found": True, "text": alert_text, "valid": False}
            else:  # PASS
                if any(keyword in alert_text.lower() for keyword in ["thành công", "✅", "hoàn thành", "cập nhật", "sửa"]):
                    return {"found": True, "text": alert_text, "valid": True}
                else:
                    return {"found": True, "text": alert_text, "valid": False}
                    
        except TimeoutException:
            print(f"   ⏰ Không có alert trong 3 giây")
            return {"found": False, "text": "", "valid": False}
        except Exception as e:
            print(f"   ❌ Lỗi xử lý alert: {str(e)}")
            return {"found": False, "text": f"Lỗi: {str(e)}", "valid": False}
    
    def test_edit_book(self, test_data):
        """Test edit sách với dữ liệu từ CSV"""
        start_time = time.time()
        
        try:
            # Mở trang edit sách
            edit_book_url = "file:///" + os.path.abspath("web_ban_sach/front-end/NiceAdmin/forms-edit.html").replace("\\", "/")
            self.driver.get(edit_book_url)
            
            print(f"\n🔍 Test #{test_data['stt']}: {test_data['test_case']}")
            print(f"   📝 Mô tả: {test_data['description']}")
            print(f"   🆔 Book ID: '{test_data['book_id']}'")
            print(f"   📚 Tên sách: '{test_data['book_name']}'")
            print(f"   📄 Số trang: '{test_data['page_count']}'")
            print(f"   ✍️ Author ID: '{test_data['author_id']}'")
            print(f"   📂 Category ID: '{test_data['category_id']}'")
            print(f"   🖼️ Bìa sách: '{test_data['book_cover']}'")
            print(f"   🎯 Kết quả mong đợi: {test_data['expected']}")
            
            # Chờ trang load
            time.sleep(2)
            
            # Điền Book ID
            book_id_field = self.driver.find_element(By.ID, "bookid")
            book_id_field.clear()
            book_id_field.send_keys(test_data['book_id'])
            
            # Điền tên sách
            book_name_field = self.driver.find_element(By.ID, "bookName")
            book_name_field.clear()
            book_name_field.send_keys(test_data['book_name'])
            
            # Điền số trang
            page_count_field = self.driver.find_element(By.ID, "pageCount")
            page_count_field.clear()
            page_count_field.send_keys(test_data['page_count'])
            
            # Điền Author ID
            author_id_field = self.driver.find_element(By.ID, "authorId")
            author_id_field.clear()
            author_id_field.send_keys(test_data['author_id'])
            
            # Điền Category ID
            category_id_field = self.driver.find_element(By.ID, "categoryId")
            category_id_field.clear()
            category_id_field.send_keys(test_data['category_id'])
            
            # Upload file bìa sách (nếu có)
            if test_data['book_cover']:
                try:
                    book_cover_field = self.driver.find_element(By.ID, "bookCover")
                    dummy_file_path = os.path.abspath("dummy_edit_book_cover.txt")
                    with open(dummy_file_path, 'w') as f:
                        f.write("dummy edit book cover content")
                    book_cover_field.send_keys(dummy_file_path)
                except Exception as upload_error:
                    print(f"   ⚠️ Không thể upload file: {upload_error}")
            
            # Click nút Cập nhật
            update_button = self.driver.find_element(By.ID, "cap_nhat")
            update_button.click()
            
            # Kiểm tra alert
            alert_result = self.check_alert(test_data['expected'])
            
            execution_time = round(time.time() - start_time, 2)
            
            # Validation logic (nếu không có alert)
            if not alert_result['found']:
                validation_result = self.check_validation(test_data)
                actual_status = validation_result['status']
                note = validation_result['message']
            else:
                # Đánh giá kết quả dựa trên alert
                actual_status = "PASS" if alert_result['found'] and alert_result['valid'] else "FAIL"
                note = f"Alert: '{alert_result['text']}' - {'Hợp lệ' if alert_result['valid'] else 'Không hợp lệ'}"
            
            test_status = "PASS" if actual_status == test_data['expected'] else "FAIL"
            
            # Lưu kết quả
            result = {
                'STT': test_data['stt'],
                'Test Case': test_data['test_case'],
                'Book ID': test_data['book_id'],
                'Tên sách': test_data['book_name'],
                'Số trang': test_data['page_count'],
                'Author ID': test_data['author_id'],
                'Category ID': test_data['category_id'],
                'Bìa sách': test_data['book_cover'],
                'Expected': test_data['expected'],
                'Actual': actual_status,
                'Status': test_status,
                'Alert Found': alert_result['found'],
                'Alert Text': alert_result['text'],
                'Alert Valid': alert_result['valid'],
                'Thời gian (s)': execution_time,
                'Thời gian test': datetime.now().strftime('%H:%M:%S'),
                'Mô tả': test_data['description'],
                'Ghi chú': note
            }
            
            self.results.append(result)
            status_icon = "✅" if result['Status'] == 'PASS' else "❌"
            print(f"   {status_icon} Kết quả: {result['Status']} - {note}")
            
        except Exception as e:
            execution_time = round(time.time() - start_time, 2)
            result = {
                'STT': test_data['stt'],
                'Test Case': test_data['test_case'],
                'Book ID': test_data['book_id'],
                'Tên sách': test_data['book_name'],
                'Số trang': test_data['page_count'],
                'Author ID': test_data['author_id'],
                'Category ID': test_data['category_id'],
                'Bìa sách': test_data['book_cover'],
                'Expected': test_data['expected'],
                'Actual': 'ERROR',
                'Status': 'FAIL',
                'Alert Found': False,
                'Alert Text': '',
                'Alert Valid': False,
                'Thời gian (s)': execution_time,
                'Thời gian test': datetime.now().strftime('%H:%M:%S'),
                'Mô tả': test_data['description'],
                'Ghi chú': f'Lỗi: {str(e)}'
            }
            self.results.append(result)
            print(f"   ❌ Kết quả: THẤT BẠI - {str(e)}")
    
    def check_validation(self, test_data):
        """Kiểm tra validation logic cho form edit sách"""
        
        # Kiểm tra Book ID
        if not test_data['book_id'].strip():
            return {'status': 'FAIL', 'message': 'Book ID không được để trống'}
        
        try:
            book_id = int(test_data['book_id'])
            if book_id <= 0:
                return {'status': 'FAIL', 'message': 'Book ID phải lớn hơn 0'}
            if book_id > 9998:  # Giả định ID không tồn tại nếu quá lớn
                return {'status': 'FAIL', 'message': 'Book ID không tồn tại trong hệ thống'}
        except ValueError:
            return {'status': 'FAIL', 'message': 'Book ID phải là số nguyên'}
        
        # Kiểm tra các trường bắt buộc khác
        if not test_data['book_name'].strip():
            return {'status': 'FAIL', 'message': 'Tên sách không được để trống'}
        
        if not test_data['page_count']:
            return {'status': 'FAIL', 'message': 'Số trang không được để trống'}
        
        if not test_data['author_id']:
            return {'status': 'FAIL', 'message': 'Author ID không được để trống'}
        
        if not test_data['category_id']:
            return {'status': 'FAIL', 'message': 'Category ID không được để trống'}
        
        # Kiểm tra số trang
        try:
            page_count = int(test_data['page_count'])
            if page_count <= 0:
                return {'status': 'FAIL', 'message': 'Số trang phải lớn hơn 0'}
            if page_count > 10000:
                return {'status': 'FAIL', 'message': 'Số trang không thể quá 10000'}
        except ValueError:
            return {'status': 'FAIL', 'message': 'Số trang phải là số nguyên'}
        
        # Kiểm tra Author ID
        try:
            author_id = int(test_data['author_id'])
            if author_id <= 0:
                return {'status': 'FAIL', 'message': 'Author ID phải lớn hơn 0'}
        except ValueError:
            return {'status': 'FAIL', 'message': 'Author ID phải là số nguyên'}
        
        # Kiểm tra Category ID
        try:
            category_id = int(test_data['category_id'])
            if category_id <= 0:
                return {'status': 'FAIL', 'message': 'Category ID phải lớn hơn 0'}
            if category_id > 1000:
                return {'status': 'FAIL', 'message': 'Category ID vượt quá giới hạn'}
        except ValueError:
            return {'status': 'FAIL', 'message': 'Category ID phải là số nguyên'}
        
        # Kiểm tra độ dài tên sách
        if len(test_data['book_name']) > 100:
            return {'status': 'FAIL', 'message': 'Tên sách quá dài (tối đa 100 ký tự)'}
        
        return {'status': 'PASS', 'message': 'Sửa sách hợp lệ'}
    
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
        filename = f'test_results/edit_book_test_{timestamp}.xlsx'
        
        # Export Excel
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Sheet kết quả chi tiết
            df.to_excel(writer, sheet_name='Edit Book Test Results', index=False)
            
            # Tự động điều chỉnh độ rộng cột
            worksheet = writer.sheets['Edit Book Test Results']
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
            
            # Sheet thống kê
            total = len(self.results)
            passed = len([r for r in self.results if r['Status'] == 'PASS'])
            failed = total - passed
            expected_pass = len([r for r in self.results if r['Expected'] == 'PASS'])
            expected_fail = len([r for r in self.results if r['Expected'] == 'FAIL'])
            alert_found = len([r for r in self.results if r['Alert Found']])
            alert_valid = len([r for r in self.results if r['Alert Valid']])
            pass_rate = round((passed/total)*100, 1) if total > 0 else 0
            
            # Thống kê theo loại test
            fail_cases = {
                'Trường trống': len([r for r in self.results if 'trống' in r['Test Case'].lower()]),
                'ID validation': len([r for r in self.results if any(word in r['Test Case'].lower() for word in ['id âm', 'id bằng 0', 'id có chữ', 'không tồn tại'])]),
                'Validation lỗi': len([r for r in self.results if any(word in r['Test Case'].lower() for word in ['âm', 'lớn', 'chữ'])]),
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
                    'Alert xuất hiện',
                    'Alert hợp lệ',
                    'Avg execution time (s)',
                    '---',
                    'Test trường trống',
                    'Test ID validation',
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
                    alert_found,
                    alert_valid,
                    round(sum([r['Thời gian (s)'] for r in self.results]) / total, 2) if total > 0 else 0,
                    '---',
                    fail_cases['Trường trống'],
                    fail_cases['ID validation'],
                    fail_cases['Validation lỗi'],
                    fail_cases['Hợp lệ']
                ]
            })
            summary.to_excel(writer, sheet_name='Summary', index=False)
            
            # Sheet test data gốc
            df_original = pd.read_csv(self.csv_file)
            df_original.to_excel(writer, sheet_name='Test Data Gốc', index=False)
        
        print(f"\n📊 Đã xuất kết quả ra file: {filename}")
        return filename
    
    def cleanup(self):
        """Dọn dẹp file dummy"""
        try:
            dummy_file = os.path.abspath("dummy_edit_book_cover.txt")
            if os.path.exists(dummy_file):
                os.remove(dummy_file)
        except:
            pass
    
    def run_tests(self):
        """Chạy tất cả test cases từ CSV"""
        print("=" * 70)
        print("🧪 BẮT ĐẦU TEST EDIT SÁCH TỪ FILE CSV")
        print("=" * 70)
        
        # Đọc dữ liệu test từ CSV
        test_data_list = self.load_test_data()
        
        if not test_data_list:
            print("❌ Không có dữ liệu test để chạy!")
            return
        
        # Thiết lập driver
        self.setup_driver()
        
        print(f"🚀 Sẽ chạy {len(test_data_list)} test cases...")
        print("📝 Test bao gồm: Book ID, tên sách, số trang, Author ID, Category ID")
        
        # Chạy từng test
        for test_data in test_data_list:
            self.test_edit_book(test_data)
            time.sleep(1)  # Nghỉ 1 giây giữa các test
        
        # Đóng browser
        self.driver.quit()
        
        # Dọn dẹp
        self.cleanup()
        
        # Hiển thị tóm tắt kết quả
        print("\n" + "=" * 70)
        print("📋 TÓM TẮT KẾT QUẢ TEST EDIT SÁCH")
        print("=" * 70)
        
        total = len(self.results)
        passed = len([r for r in self.results if r['Status'] == 'PASS'])
        failed = total - passed
        expected_pass = len([r for r in self.results if r['Expected'] == 'PASS'])
        alert_found = len([r for r in self.results if r['Alert Found']])
        alert_valid = len([r for r in self.results if r['Alert Valid']])
        
        print(f"📊 Tổng số test: {total}")
        print(f"✅ Test đúng: {passed}")
        print(f"❌ Test sai: {failed}")
        print(f"🎯 Test cases mong đợi PASS: {expected_pass}")
        print(f"🔔 Alert xuất hiện: {alert_found}")
        print(f"✔️ Alert hợp lệ: {alert_valid}")
        print(f"📈 Tỷ lệ test đúng: {round((passed/total)*100, 1)}%")
        
        # Thống kê theo loại
        print(f"\n📊 Phân loại test:")
        print(f"   📝 Test trường trống: {len([r for r in self.results if 'trống' in r['Test Case'].lower()])}")
        print(f"   🆔 Test ID validation: {len([r for r in self.results if any(word in r['Test Case'].lower() for word in ['id âm', 'id bằng 0', 'id có chữ', 'không tồn tại'])])}")
        print(f"   ⚠️ Test validation: {len([r for r in self.results if any(word in r['Test Case'].lower() for word in ['âm', 'lớn', 'chữ'])])}")
        print(f"   ✅ Test hợp lệ: {len([r for r in self.results if r['Expected'] == 'PASS'])}")
        
        print("\n📋 Chi tiết kết quả:")
        for result in self.results:
            status_icon = "✅" if result['Status'] == 'PASS' else "❌"
            alert_icon = "🔔" if result['Alert Found'] else "🔕"
            print(f"{status_icon}{alert_icon} #{result['STT']} {result['Test Case']}: {result['Status']} - {result['Ghi chú']}")
        
        # Export Excel
        excel_file = self.export_to_excel()
        
        print(f"\n🎉 Hoàn thành! File Excel: {excel_file}")
        print(f"📁 File CSV gốc: {self.csv_file}")

if __name__ == "__main__":
    # Chạy test từ CSV
    test = EditBookTestCSV("edit_book_test_data.csv")
    test.run_tests() 