import os
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for, session, flash, Response 
import hashlib 
import datetime 
import csv 
import io

app = Flask(__name__)
app.secret_key = '12345678'

def get_db_connection():
    # Kết nối tới MariaDB Local vừa cài
    connection = mysql.connector.connect(
        host='localhost',
        user='app_user',       # User bạn mới tạo
        password='123456',     # Pass bạn mới tạo
        database='my_app'      # Database bạn mới tạo
    )
    return connection

def execute_query(query, params=None, fetch_results=True):
    connection = get_db_connection()
    if connection is None:
        return None

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True) 
        cursor.execute(query, params or ())
    
        if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP')):
            connection.commit()
            return cursor.rowcount
        
        if fetch_results:
            return cursor.fetchall()
        else:
            return True
            
    except Error as e:
        print(f"Lỗi khi thực thi truy vấn: {e}")
        connection.rollback() 
        return None
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        query = "SELECT id, username, password FROM admin WHERE username = %s"
        admin_user = execute_query(query, (username,))

        if admin_user:
            if admin_user[0]['password'] == password: 
                session['logged_in'] = True
                session['username'] = username
                flash('Đăng nhập thành công!', 'success') 
                return redirect(url_for('dashboard')) 
            else:
                error = 'Sai tên đăng nhập hoặc mật khẩu.'
        else:
            error = 'Sai tên đăng nhập hoặc mật khẩu.'
        return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/dashboard') 
def dashboard():
    if not session.get('logged_in'):
        flash('Bạn cần đăng nhập để truy cập trang này.', 'danger')
        return redirect(url_for('login'))
    total_employees = execute_query("SELECT COUNT(*) AS count FROM NhanVien")[0]['count']
    total_departments = execute_query("SELECT COUNT(*) AS count FROM CuaHang")[0]['count'] 
    total_salaries = execute_query("SELECT COUNT(*) AS count FROM Luong")[0]['count']
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    employees_paid_this_month_query = """
    SELECT COUNT(DISTINCT MaNhanVien) AS count
    FROM Luong 
    WHERE Thang = %s AND Nam = %s
    """
    employees_paid_this_month_result = execute_query(employees_paid_this_month_query, (current_month, current_year))
    employees_paid_this_month = employees_paid_this_month_result[0]['count'] if employees_paid_this_month_result else 0
    recent_employees_query = """
    SELECT 
        nv.MaNhanVien, nv.HoTen, nv.Email, ch.TenCuaHang, cv.TenChucVu, nv.NgayVaoLam
    FROM NhanVien nv
    LEFT JOIN CuaHang ch ON nv.MaCuaHang = ch.MaCuaHang 
    LEFT JOIN ChucVu cv ON nv.MaChucVu = cv.MaChucVu
    ORDER BY nv.MaNhanVien ASC
    LIMIT 10
    """
    recent_employees = execute_query(recent_employees_query)
    return render_template(
        'dashboard.html', 
        total_employees=total_employees,
        total_departments=total_departments, 
        total_salaries=total_salaries,
        employees_paid_this_month=employees_paid_this_month,
        recent_employees=recent_employees
    )

@app.route('/logout') 
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Bạn đã đăng xuất.', 'info')
    return redirect(url_for('login'))

def get_all_cua_hang_for_dropdown():
    """Lấy tất cả các cửa hàng để điền vào dropdown."""
    query = "SELECT MaCuaHang, TenCuaHang FROM CuaHang ORDER BY TenCuaHang"
    return execute_query(query)

def get_all_chuc_vu_for_dropdown():
    """Lấy tất cả các chức vụ để điền vào dropdown."""
    query = "SELECT MaChucVu, TenChucVu FROM ChucVu ORDER BY TenChucVu"
    return execute_query(query)

@app.route('/nhan_vien/add', methods=['GET', 'POST']) 
def add_nhan_vien():
    if not session.get('logged_in'):
        flash('Bạn cần đăng nhập để truy cập trang này.', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        ma_nhan_vien = request.form['ma_nhan_vien']
        ho_ten = request.form['ho_ten']
        gioi_tinh = request.form['gioi_tinh']
        ngay_sinh = request.form['ngay_sinh']
        sdt = request.form['sdt']
        email = request.form['email']
        dia_chi = request.form['dia_chi']
        ngay_vao_lam = request.form['ngay_vao_lam']
        ma_cua_hang = request.form['ma_cua_hang']
        ma_chuc_vu = request.form['ma_chuc_vu']
        check_exist_query = "SELECT COUNT(*) AS count FROM NhanVien WHERE MaNhanVien = %s OR Email = %s"
        exist_count = execute_query(check_exist_query, (ma_nhan_vien, email))[0]['count']
        if exist_count > 0:
            flash('Mã Nhân viên hoặc Email đã tồn tại. Vui lòng kiểm tra lại.', 'danger')
            cua_hangs = get_all_cua_hang_for_dropdown()
            chuc_vus = get_all_chuc_vu_for_dropdown()
            return render_template('add_nhan_vien.html', cua_hangs=cua_hangs, chuc_vus=chuc_vus,form_data=request.form) 
        insert_query = """
        INSERT INTO NhanVien (MaNhanVien, HoTen, GioiTinh, NgaySinh, SoDienThoai, Email, DiaChi, NgayVaoLam, MaCuaHang, MaChucVu)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (ma_nhan_vien, ho_ten, gioi_tinh, ngay_sinh, sdt, email, dia_chi, ngay_vao_lam, ma_cua_hang, ma_chuc_vu)
        result = execute_query(insert_query, params, fetch_results=False) 
        if result is not None:
            flash('Thêm nhân viên mới thành công!', 'success')
            return redirect(url_for('nhan_vien')) 
        else:
            flash('Có lỗi xảy ra khi thêm nhân viên.', 'danger')
    cua_hangs = get_all_cua_hang_for_dropdown()
    chuc_vus = get_all_chuc_vu_for_dropdown()
    return render_template('add_nhan_vien.html', cua_hangs=cua_hangs, chuc_vus=chuc_vus)

@app.route('/nhan_vien')
def nhan_vien():
    if not session.get('logged_in'):
        flash('Bạn cần đăng nhập để truy cập trang này.', 'danger')
        return redirect(url_for('login'))
    query = """
    SELECT 
        nv.MaNhanVien, nv.HoTen, nv.GioiTinh, nv.NgaySinh, nv.SoDienThoai, nv.Email, nv.DiaChi, nv.NgayVaoLam,
        ch.TenCuaHang, cv.TenChucVu
    FROM NhanVien nv
    LEFT JOIN CuaHang ch ON nv.MaCuaHang = ch.MaCuaHang
    LEFT JOIN ChucVu cv ON nv.MaChucVu = cv.MaChucVu
    ORDER BY nv.MaNhanVien ASC
    """ 
    employees = execute_query(query)
    headers = ['Mã NV', 'Họ Tên', 'Giới Tính', 'Ngày Sinh', 'SĐT', 'Email', 'Địa Chỉ', 'Ngày Vào Làm', 'Cửa Hàng', 'Chức Vụ']
    return render_template('module_template.html', title='Quản lý Nhân viên', data=employees, headers=headers)


@app.route('/nhan_vien/edit/<string:ma_nv>', methods=['GET', 'POST'])
def edit_nhan_vien(ma_nv):
    if not session.get('logged_in'):
        flash('Bạn cần đăng nhập để truy cập trang này.', 'danger')
        return redirect(url_for('login'))

    employee = execute_query("SELECT * FROM NhanVien WHERE MaNhanVien = %s", (ma_nv,))
    if not employee:
        flash('Không tìm thấy nhân viên.', 'danger')
        return redirect(url_for('nhan_vien'))
    employee = employee[0] 

    cua_hangs = get_all_cua_hang_for_dropdown()
    chuc_vus = get_all_chuc_vu_for_dropdown()

    if request.method == 'POST':
        ho_ten = request.form['ho_ten']
        gioi_tinh = request.form['gioi_tinh']
        ngay_sinh = request.form['ngay_sinh']
        sdt = request.form['sdt']
        email = request.form['email']
        dia_chi = request.form['dia_chi']
        ngay_vao_lam = request.form['ngay_vao_lam']
        ma_cua_hang = request.form['ma_cua_hang']
        ma_chuc_vu = request.form['ma_chuc_vu']

        check_email_query = "SELECT COUNT(*) AS count FROM NhanVien WHERE Email = %s AND MaNhanVien != %s"
        email_exist_count = execute_query(check_email_query, (email, ma_nv))[0]['count']
        if email_exist_count > 0:
            flash('Email đã tồn tại cho nhân viên khác. Vui lòng chọn Email khác.', 'danger')
            return render_template('edit_nhan_vien.html', employee=employee, cua_hangs=cua_hangs, chuc_vus=chuc_vus, form_data=request.form)

        update_query = """
        UPDATE NhanVien SET 
            HoTen = %s, GioiTinh = %s, NgaySinh = %s, SoDienThoai = %s, Email = %s, 
            DiaChi = %s, NgayVaoLam = %s, MaCuaHang = %s, MaChucVu = %s
        WHERE MaNhanVien = %s
        """
        params = (ho_ten, gioi_tinh, ngay_sinh, sdt, email, dia_chi, ngay_vao_lam, ma_cua_hang, ma_chuc_vu, ma_nv)
        
        result = execute_query(update_query, params, fetch_results=False)

        if result is not None:
            flash('Cập nhật thông tin nhân viên thành công!', 'success')
            return redirect(url_for('nhan_vien'))
        else:
            flash('Có lỗi xảy ra khi cập nhật nhân viên.', 'danger')
    
    return render_template('edit_nhan_vien.html', employee=employee, cua_hangs=cua_hangs, chuc_vus=chuc_vus)

@app.route('/nhan_vien/delete/<string:ma_nv>', methods=['GET'])
def delete_nhan_vien(ma_nv):
    if not session.get('logged_in'):
        flash('Bạn cần đăng nhập để truy cập trang này.', 'danger')
        return redirect(url_for('login'))

    delete_query = "DELETE FROM NhanVien WHERE MaNhanVien = %s"
    result = execute_query(delete_query, (ma_nv,), fetch_results=False)

    if result is not None:
        flash(f'Đã xóa nhân viên {ma_nv} thành công!', 'success')
    else:
        flash(f'Có lỗi xảy ra khi xóa nhân viên {ma_nv}.', 'danger')
    
    return redirect(url_for('nhan_vien'))

@app.route('/nhan_vien/export_csv') 
def export_nhan_vien_csv():
    """
    Exports employee data to a CSV file.
    Configured for better compatibility with Excel (UTF-8 with BOM, semicolon delimiter).
    """
    if not session.get('logged_in'):
        flash('Bạn cần đăng nhập để truy cập trang này.', 'danger')
        return redirect(url_for('login'))
    query = """
    SELECT 
        nv.MaNhanVien, nv.HoTen, nv.GioiTinh, nv.NgaySinh, nv.SoDienThoai, nv.Email, nv.DiaChi, nv.NgayVaoLam,
        ch.TenCuaHang, cv.TenChucVu
    FROM NhanVien nv
    LEFT JOIN CuaHang ch ON nv.MaCuaHang = ch.MaCuaHang
    LEFT JOIN ChucVu cv ON nv.MaChucVu = cv.MaChucVu
    ORDER BY nv.MaNhanVien
    """
    employees = execute_query(query)
    if not employees:
        flash('Không có dữ liệu nhân viên để xuất CSV.', 'info')
        return redirect(url_for('nhan_vien'))
    si = io.StringIO()
    si.write('\ufeff')
    cw = csv.writer(si, delimiter=';') 
    headers = ['Mã NV', 'Họ Tên', 'Giới Tính', 'Ngày Sinh', 'SĐT', 'Email', 'Địa Chỉ', 'Ngày Vào Làm', 'Cửa Hàng', 'Chức Vụ']
    cw.writerow(headers)
    for employee in employees:
        row = [
            employee['MaNhanVien'],
            employee['HoTen'],
            employee['GioiTinh'],
            str(employee['NgaySinh']) if employee['NgaySinh'] else '', 
            employee['SoDienThoai'],
            employee['Email'],
            employee['DiaChi'],
            str(employee['NgayVaoLam']) if employee['NgayVaoLam'] else '', 
            employee['TenCuaHang'],
            employee['TenChucVu']
        ]
        cw.writerow(row)
    output = si.getvalue()
    response = Response(output, mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=nhan_vien.csv"
    response.headers["Content-Type"] = "text/csv; charset=utf-8" 
    return response


@app.route('/cua_hang') 
def cua_hang():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    query = "SELECT MaCuaHang, TenCuaHang, DiaChi, SoDienThoai FROM CuaHang ORDER BY MaCuaHang"
    data = execute_query(query)
    headers = ['Mã Cửa Hàng', 'Tên Cửa Hàng', 'Địa Chỉ', 'Số Điện Thoại']
    return render_template('module_template.html', title='Quản lý Cửa hàng', data=data, headers=headers)

@app.route('/chuc_vu') 
def chuc_vu():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    query = "SELECT MaChucVu, TenChucVu, HeSoLuong FROM ChucVu ORDER BY MaChucVu"
    data = execute_query(query)
    headers = ['Mã Chức Vụ', 'Tên Chức Vụ', 'Hệ Số Lương']
    return render_template('module_template.html', title='Quản lý Chức vụ', data=data, headers=headers)

@app.route('/luong') 
def luong():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    query = """
   SELECT l.MaLuong, nv.MaNhanVien, nv.HoTen, l.Thang, l.Nam, l.LuongCoBan, l.PhuCap, l.SoNgayCong, l.GhiChu
    FROM Luong l
    JOIN NhanVien nv ON l.MaNhanVien = nv.MaNhanVien
    WHERE l.Thang = 4 AND l.Nam = 2025
    ORDER BY l.MaLuong ASC, nv.MaNhanVien ASC
    """ 
    data = execute_query(query)
    headers = ['Mã Lương', 'Mã NV', 'Nhân Viên', 'Tháng', 'Năm', 'Lương Cơ Bản', 'Phụ Cấp', 'Số Ngày Công', 'Ghi Chú']
    return render_template('module_template.html', title='Quản lý Lương', data=data, headers=headers)

@app.route('/cham_cong') 
def cham_cong():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    query = """
    SELECT cc.MaChamCong, nv.MaNhanVien, nv.HoTen, cc.Ngay, cl.TenCa, cc.TrangThai
    FROM ChamCong cc
    JOIN NhanVien nv ON cc.MaNhanVien = nv.MaNhanVien
    JOIN CaLam cl ON cc.MaCa = cl.MaCa
    ORDER BY cc.MaChamCong ASC, nv.MaNhanVien ASC, cc.Ngay DESC
    """ 
    data = execute_query(query)
    headers = ['Mã Chấm Công', 'Mã NV','Nhân Viên', 'Ngày', 'Ca Làm', 'Trạng Thái']
    return render_template('module_template.html', title='Quản lý Chấm công', data=data, headers=headers)

@app.route('/ca_lam') 
def ca_lam():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    query = "SELECT MaCa, TenCa, GioBatDau, GioKetThuc FROM CaLam ORDER BY MaCa"
    data = execute_query(query)
    headers = ['Mã Ca', 'Tên Ca', 'Giờ Bắt Đầu', 'Giờ Kết Thúc']
    return render_template('module_template.html', title='Quản lý Ca làm', data=data, headers=headers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
