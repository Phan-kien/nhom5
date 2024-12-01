import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime


# Hàm kết nối cơ sở dữ liệu
def tao_ket_noi():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456789',
        database='hotel_booking_system'
    )

def dang_ky_khach_hang(username, email, phone, password):
    conn = tao_ket_noi()
    if conn is None:
        messagebox.showerror("Lỗi", "Không thể kết nối cơ sở dữ liệu.")
        return

    cursor = conn.cursor()
    query = """
        INSERT INTO Customer (username, email, phone, password)
        VALUES (%s, %s, %s, %s)
    """
    try:
        # Mã hóa mật khẩu
        cursor.execute(query, (username, email, phone, password))
        conn.commit()
        messagebox.showinfo("Thông báo", "Khách hàng đã đăng ký thành công!")
    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e):
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc email đã tồn tại.")
        else:
            messagebox.showerror("Lỗi", f"Lỗi khi đăng ký: {e}")
    except mysql.connector.Error as e:
        messagebox.showerror("Lỗi", f"Lỗi cơ sở dữ liệu: {e}")
    finally:
        cursor.close()
        conn.close()



# Hàm đăng nhập khách hàng
def dang_nhap_khach_hang(username, password):
    conn = tao_ket_noi()
    cursor = conn.cursor()
    query = "SELECT customer_id, username FROM Customer WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    customer = cursor.fetchone()

    cursor.close()
    conn.close()

    if customer:
        messagebox.showinfo("Thông báo", f"Chào mừng {customer[1]}!")
        return customer[0]
    else:
        messagebox.showerror("Lỗi", "Thông tin đăng nhập không hợp lệ.")
        return None

def xu_ly_dang_nhap():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
        return

    # Kiểm tra đăng nhập
    customer_id = dang_nhap_khach_hang(username, password)
    if customer_id:
        messagebox.showinfo("Thông báo", f"Xin chào {username}, bạn đã đăng nhập thành công!")
        hien_thi_menu(customer_id)
    else:
        messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không chính xác.")



def xu_ly_dang_ky():
    username = entry_username.get()
    email = entry_email.get()
    phone = entry_phone.get()
    password = entry_password.get()

    print(f"Debug: username={username}, email={email}, phone={phone}, password={password}")

    if not username or not email or not phone or not password:
        messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
        return

    dang_ky_khach_hang(username, email, phone, password)


def hien_thi_dang_ky():
    # Ẩn giao diện đăng nhập
    for widget in root.winfo_children():
        widget.grid_forget()

    # Hiển thị giao diện đăng ký
    label_username.grid(row=0, column=0, padx=10, pady=10)
    entry_username.grid(row=0, column=1, padx=10, pady=10)

    label_email.grid(row=1, column=0, padx=10, pady=10)
    entry_email.grid(row=1, column=1, padx=10, pady=10)

    label_phone.grid(row=2, column=0, padx=10, pady=10)
    entry_phone.grid(row=2, column=1, padx=10, pady=10)

    label_password.grid(row=3, column=0, padx=10, pady=10)
    entry_password.grid(row=3, column=1, padx=10, pady=10)

    btn_register.config(command=xu_ly_dang_ky)
    btn_register.grid(row=4, column=0, columnspan=2, pady=10)

    btn_back_to_login.grid(row=5, column=0, columnspan=2, pady=10)



# Hàm hiển thị giao diện đăng nhập
def hien_thi_dang_nhap():
    # Xóa các widget của menu trước khi hiển thị lại giao diện đăng nhập
    for widget in root.winfo_children():
        widget.grid_forget()

    # Hiển thị lại giao diện đăng nhập
    label_username = tk.Label(root, text="Tên đăng nhập:")
    label_username.grid(row=0, column=0, padx=10, pady=10)

    global entry_username
    entry_username = tk.Entry(root)
    entry_username.grid(row=0, column=1, padx=10, pady=10)

    label_password = tk.Label(root, text="Mật khẩu:")
    label_password.grid(row=1, column=0, padx=10, pady=10)

    global entry_password
    entry_password = tk.Entry(root, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10)

    btn_login = tk.Button(root, text="Đăng nhập", command=xu_ly_dang_nhap)
    btn_login.grid(row=2, column=0, columnspan=2, pady=20)


def hien_thi_menu(customer_id):
    # Xóa giao diện đăng nhập
    for widget in root.winfo_children():
        widget.grid_forget()

    # Hiển thị các lựa chọn sau khi đăng nhập
    label_welcome = tk.Label(root, text="Chào mừng bạn đến với hệ thống đặt phòng!", font=("Arial", 16))
    label_welcome.grid(row=0, column=0, columnspan=2, pady=20)

    # Lựa chọn phòng
    btn_choose_room = tk.Button(root, text="Chọn phòng", command=lambda: hien_thi_chon_loai_phong(customer_id))
    btn_choose_room.grid(row=1, column=0, padx=10, pady=10)

    # Hủy đặt phòng
    btn_cancel_booking = tk.Button(root, text="Hủy đặt phòng", command=lambda: hien_thi_huy_dat_phong(customer_id))
    btn_cancel_booking.grid(row=2, column=0, padx=10, pady=10)

    # Hiển thị danh sách đặt phòng
    btn_view_bookings = tk.Button(root, text="Xem danh sách đặt phòng", command=lambda: hien_thi_danh_sach_dat_phong(customer_id))
    btn_view_bookings.grid(row=3, column=0, padx=10, pady=10)

    # Đăng xuất
    btn_logout = tk.Button(root, text="Đăng xuất", command=hien_thi_dang_nhap)
    btn_logout.grid(row=4, column=0, columnspan=2, pady=20)

# Hàm hiển thị danh sách đặt phòng trong giao diện chính
def hien_thi_danh_sach_dat_phong(customer_id):
    # Xóa giao diện hiện tại
    for widget in root.winfo_children():
        widget.grid_forget()

    # Lấy danh sách đặt phòng từ cơ sở dữ liệu
    bookings = xem_danh_sach_dat_phong(customer_id)

    # Kiểm tra nếu không có đặt phòng nào
    if not bookings:
        messagebox.showinfo("Thông báo", "Hiện tại bạn chưa có đặt phòng nào.")
        hien_thi_menu(customer_id)  # Quay lại menu nếu không có đặt phòng
        return

    # Tạo tiêu đề
    headers = ["Mã đặt phòng", "Mã phòng", "Loại phòng", "Ngày nhận phòng", "Ngày trả phòng", "Tổng giá (VND)", "Trạng thái"]
    for col, header in enumerate(headers):
        label = tk.Label(root, text=header, font=("Arial", 10, "bold"))
        label.grid(row=0, column=col, padx=10, pady=5)

    # Hiển thị dữ liệu đặt phòng
    for row, booking in enumerate(bookings, start=1):
        for col, data in enumerate(booking):
            label = tk.Label(root, text=data, font=("Arial", 10))
            label.grid(row=row, column=col, padx=10, pady=5)

    # Nút quay lại menu chính
    btn_back = tk.Button(root, text="Quay lại", command=lambda: hien_thi_menu(customer_id))
    btn_back.grid(row=len(bookings) + 1, column=0, columnspan=len(headers), pady=10)



def hien_thi_huy_dat_phong(customer_id):
    # Xóa giao diện hiện tại
    for widget in root.winfo_children():
        widget.grid_forget()

    # Hiển thị form nhập mã đặt phòng
    label_booking_id = tk.Label(root, text="Nhập mã đặt phòng để hủy:")
    label_booking_id.grid(row=0, column=0, padx=10, pady=10)

    entry_booking_id = tk.Entry(root)
    entry_booking_id.grid(row=0, column=1, padx=10, pady=10)

    def validate_and_cancel():
        try:
            booking_id = int(entry_booking_id.get())
            # Hủy đặt phòng
            huy_dat_phong(booking_id, customer_id)
            # Hiển thị lại danh sách đặt phòng sau khi hủy
            xem_danh_sach_dat_phong(customer_id)
        except ValueError:
            messagebox.showerror("Lỗi", "Mã đặt phòng không hợp lệ. Vui lòng nhập lại.")

    btn_cancel = tk.Button(root, text="Hủy đặt phòng", command=validate_and_cancel)
    btn_cancel.grid(row=1, column=0, columnspan=2, pady=10)

    btn_back = tk.Button(root, text="Quay lại", command=lambda: hien_thi_menu(customer_id))
    btn_back.grid(row=2, column=0, columnspan=2, pady=10)


def xem_danh_sach_dat_phong(customer_id):
    conn = tao_ket_noi()
    cursor = conn.cursor()

    # Lấy danh sách đặt phòng của khách hàng
    query = """
            SELECT Booking.booking_id, Room.room_id, Room.room_type, Booking.check_in_date, Booking.check_out_date, 
                   Booking.total_price, Booking.status
            FROM Booking
            JOIN Room ON Booking.room_id = Room.room_id
            WHERE Booking.customer_id = %s AND Booking.status != 'cancelled'
        """
    cursor.execute(query, (customer_id,))
    bookings = cursor.fetchall()

    cursor.close()
    conn.close()

    return bookings




# Hàm hiển thị danh sách phòng theo loại phòng đã chọn
def hien_thi_phong_theo_loai(customer_id, room_type):
    for widget in root.winfo_children():
        widget.grid_forget()

    # Lấy danh sách phòng theo loại
    rooms = xem_phong_theo_loai(room_type)

    if not rooms:
        messagebox.showinfo("Thông báo", f"Hiện tại không có phòng {room_type} nào trống.")
        return

    # Hiển thị danh sách phòng
    label_room_list = tk.Label(root, text=f"Danh sách phòng loại {room_type}:")
    label_room_list.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    listbox_rooms = tk.Listbox(root, width=80, height=10)
    for room in rooms:
        listbox_rooms.insert(
            tk.END,
            f"Khách sạn: {room[0]} - Mã phòng: {room[1]} - Giá: {room[3]:.2f} VND - Sức chứa: {room[4]}"
        )
    listbox_rooms.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # Nút chọn phòng
    btn_select_room = tk.Button(
        root,
        text="Chọn phòng",
        command=lambda: xu_ly_chon_phong(customer_id, listbox_rooms)
    )
    btn_select_room.grid(row=2, column=0, columnspan=2, pady=10)

    # Nút quay lại
    btn_back = tk.Button(root, text="Quay lại", command=lambda: hien_thi_chon_loai_phong(customer_id))
    btn_back.grid(row=3, column=0, columnspan=2, pady=10)


def xu_ly_chon_phong(customer_id, listbox_rooms):
    selected = listbox_rooms.curselection()
    if not selected:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một phòng!")
        return

    # Lấy thông tin mã phòng từ danh sách
    selected_room = listbox_rooms.get(selected)
    room_id = int(selected_room.split(" - ")[1].split(":")[1].strip())

    # Chuyển sang giao diện đặt phòng
    hien_thi_form_dat_phong(customer_id, room_id)


def hien_thi_chon_loai_phong(customer_id):
    for widget in root.winfo_children():
        widget.grid_forget()

    # Hiển thị lựa chọn loại phòng
    label_room_type = tk.Label(root, text="Chọn loại phòng:", font=("Arial", 14))
    label_room_type.grid(row=0, column=0, padx=10, pady=10)

    # Các loại phòng (ví dụ)
    global room_type_var
    room_type_var = tk.StringVar(value="single")  # Loại phòng mặc định là "single"

    room_types = ["single", "double", "Premium Suite"]
    for i, room_type in enumerate(room_types):
        radio_button = tk.Radiobutton(root, text=room_type.capitalize(), variable=room_type_var, value=room_type)
        radio_button.grid(row=i + 1, column=0, padx=10, pady=10, sticky="w")

    # Nút xem phòng theo loại đã chọn
    btn_view_rooms = tk.Button(
        root,
        text="Xem phòng",
        command=lambda: hien_thi_phong_theo_loai(customer_id, room_type_var.get())
    )
    btn_view_rooms.grid(row=len(room_types) + 1, column=0, padx=10, pady=20)

    # Tạo Listbox để hiển thị danh sách phòng
    global listbox_rooms
    listbox_rooms = tk.Listbox(root, width=80, height=10)
    listbox_rooms.grid(row=len(room_types) + 2, column=0, columnspan=2, padx=10, pady=10)

    # Nút quay lại menu chính
    btn_back_to_menu = tk.Button(root, text="Quay lại menu", command=lambda: hien_thi_menu(customer_id))
    btn_back_to_menu.grid(row=len(room_types) + 3, column=0, columnspan=2, pady=10)




# Hàm xem phòng theo loại phòng đã chọn
def xem_phong_theo_loai(room_type):
    conn = tao_ket_noi()
    cursor = conn.cursor()
    query = """
        SELECT Hotel.username AS ten_khach_san, Room.room_id, Room.room_type, Room.price_per_night, Room.capacity
        FROM Room
        JOIN Hotel ON Room.hotel_id = Hotel.hotel_id
        WHERE Room.status = 'available' AND Room.room_type = %s
    """
    cursor.execute(query, (room_type,))
    rooms = cursor.fetchall()

    cursor.close()
    conn.close()

    return rooms


def huy_dat_phong(booking_id, logged_in_customer_id):
    conn = tao_ket_noi()
    cursor = conn.cursor()

    try:
        # Kiểm tra trạng thái của booking và quyền hủy
        query = "SELECT status, room_id, customer_id FROM Booking WHERE booking_id = %s"
        cursor.execute(query, (booking_id,))
        booking = cursor.fetchone()

        if not booking:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin đặt phòng.")
            return

        if booking[0] != 'confirmed':
            messagebox.showerror("Lỗi", "Chỉ có thể hủy các đặt phòng đã được xác nhận.")
            return

        if booking[2] != logged_in_customer_id:
            messagebox.showerror("Lỗi", "Bạn không có quyền hủy đặt phòng này.")
            return

        # Cập nhật trạng thái đặt phòng thành 'cancelled'
        update_booking_query = "UPDATE Booking SET status = 'cancelled' WHERE booking_id = %s"
        cursor.execute(update_booking_query, (booking_id,))

        # Cập nhật trạng thái phòng thành 'available'
        update_room_query = "UPDATE Room SET status = 'available' WHERE room_id = %s"
        cursor.execute(update_room_query, (booking[1],))

        # Commit thay đổi
        conn.commit()

        messagebox.showinfo("Thành công", f"Đặt phòng {booking_id} đã được hủy thành công!")

    except Exception as e:
        conn.rollback()  # Rollback nếu có lỗi
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi hủy đặt phòng: {e}")

    finally:
        cursor.close()
        conn.close()




# Hàm kiểm tra và hủy đặt phòng
def validate_and_cancel(booking_id, customer_id):
    # Kiểm tra hợp lệ các thông tin đặt phòng (có thể là kiểm tra ID đặt phòng, thông tin khách hàng)
    print(f"Đang kiểm tra hợp lệ đặt phòng với booking ID: {booking_id} và khách hàng ID: {customer_id}")

    # Nếu thông tin hợp lệ, gọi hàm hủy đặt phòng
    if booking_id and customer_id:  # Điều kiện có thể thay đổi tùy theo yêu cầu
        huy_dat_phong(booking_id, customer_id)
    else:
        print("Thông tin đặt phòng không hợp lệ.")



def hien_thi_form_dat_phong(customer_id, room_id):
    for widget in root.winfo_children():
        widget.grid_forget()

    # Hiển thị form nhập ngày
    label_room_id = tk.Label(root, text=f"Đặt phòng: {room_id}")
    label_room_id.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    label_check_in = tk.Label(root, text="Ngày nhận phòng (YYYY-MM-DD):")
    label_check_in.grid(row=1, column=0, padx=10, pady=10)

    entry_check_in = tk.Entry(root)
    entry_check_in.grid(row=1, column=1, padx=10, pady=10)

    label_check_out = tk.Label(root, text="Ngày trả phòng (YYYY-MM-DD):")
    label_check_out.grid(row=2, column=0, padx=10, pady=10)

    entry_check_out = tk.Entry(root)
    entry_check_out.grid(row=2, column=1, padx=10, pady=10)

    from datetime import datetime  # Đảm bảo import đúng module

    def validate_and_book():
        check_in_data = entry_check_in.get()
        check_out_data = entry_check_out.get()

        try:
            check_in_date = datetime.strptime(check_in_data, "%Y-%m-%d")
            check_out_date = datetime.strptime(check_out_data, "%Y-%m-%d")

            if check_in_date >= check_out_date:
                messagebox.showwarning("Lỗi", "Ngày trả phòng phải sau ngày nhận phòng!")
                return

            # Now this line should work correctly as both total_price and booking_id are returned
            total_price, booking_id = dat_phong(customer_id, room_id, check_in_date, check_out_date)

            if total_price is not None:
                messagebox.showinfo("Thành công", f"Đặt phòng thành công với tổng giá: {total_price:.2f} VND")
                hien_thi_phuong_thuc_thanh_toan(customer_id, booking_id, total_price)  # Passing both values
            else:
                messagebox.showerror("Lỗi", "Không thể đặt phòng.")
        except ValueError:
            messagebox.showerror("Lỗi", "Định dạng ngày không hợp lệ! Vui lòng nhập theo YYYY-MM-DD.")

    btn_book = tk.Button(
        root,
        text="Đặt phòng",
        command=validate_and_book
    )
    btn_book.grid(row=3, column=0, columnspan=2, pady=10)

    btn_back = tk.Button(root, text="Quay lại", command=lambda: hien_thi_menu(customer_id))
    btn_back.grid(row=4, column=0, columnspan=2, pady=10)



# Hàm cập nhật trạng thái phòng
def cap_nhat_trang_thai_phong(room_id, new_status):
    conn = tao_ket_noi()
    cursor = conn.cursor()
    query = "UPDATE Room SET status = %s WHERE room_id = %s"
    cursor.execute(query, (new_status, room_id))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Thông báo", f"Trạng thái phòng {room_id} đã được cập nhật thành {new_status}.")


def kiem_tra_phong_co_san(room_id):
    conn = tao_ket_noi()
    cursor = conn.cursor()
    query = "SELECT status FROM Room WHERE room_id = %s"
    cursor.execute(query, (room_id,))
    room_status = cursor.fetchone()

    cursor.close()
    conn.close()

    if room_status and room_status[0] == 'available':
        return True
    else:
        return False

def dat_phong(customer_id, room_id, check_in_date, check_out_date):
    conn = tao_ket_noi()  # Kết nối đến cơ sở dữ liệu
    cursor = conn.cursor()

    try:
        # Kiểm tra phòng có sẵn
        if not kiem_tra_phong_co_san(room_id):
            messagebox.showerror("Lỗi", f"Phòng {room_id} không có sẵn!")
            return None, None  # Nếu phòng không sẵn sàng, trả về None

        # Lấy giá mỗi đêm và tính tổng giá
        query = "SELECT price_per_night FROM Room WHERE room_id = %s"
        cursor.execute(query, (room_id,))
        result = cursor.fetchone()

        if not result:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin phòng.")
            return None, None  # Trả về None nếu không tìm thấy thông tin phòng

        price_per_night = result[0]

        # Tính số đêm
        num_nights = (check_out_date - check_in_date).days

        if num_nights <= 0:
            messagebox.showwarning("Lỗi", "Ngày trả phòng phải sau ngày nhận phòng!")
            return None, None  # Trả về None nếu ngày không hợp lệ

        # Tính tổng giá
        total_price = price_per_night * num_nights

        # Thêm đặt phòng vào cơ sở dữ liệu
        booking_query = """
            INSERT INTO Booking (customer_id, room_id, check_in_date, check_out_date, total_price, status)
            VALUES (%s, %s, %s, %s, %s, 'confirmed')
        """
        cursor.execute(booking_query, (customer_id, room_id, check_in_date, check_out_date, total_price))

        # Lấy ID của đặt phòng vừa thêm
        booking_id = cursor.lastrowid

        # Cập nhật trạng thái phòng thành 'booked'
        room_update_query = "UPDATE Room SET status = 'booked' WHERE room_id = %s"
        cursor.execute(room_update_query, (room_id,))

        # Commit thay đổi
        conn.commit()

        messagebox.showinfo("Thành công", f"Phòng {room_id} đã được đặt với tổng giá: {total_price:.2f} VND")

        return total_price, booking_id  # Trả về tổng giá và mã đặt phòng

    except Exception as e:
        conn.rollback()  # Hoàn tác nếu có lỗi
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi đặt phòng: {e}")
        return None, None

    finally:
        # Đảm bảo đóng kết nối
        cursor.close()
        conn.close()


def xu_ly_dat_phong(customer_id, room_id, check_in_data, check_out_data):
    # Kiểm tra các trường nhập có đầy đủ không
    if not customer_id or not room_id or not check_in_data or not check_out_data:
        messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
        return

    # Chuyển đổi chuỗi ngày tháng thành đối tượng datetime
    try:
        check_in_date = datetime.strptime(check_in_data, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out_data, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Lỗi", "Định dạng ngày không hợp lệ! Vui lòng nhập theo định dạng YYYY-MM-DD.")
        return

    # Kiểm tra ngày trả phòng có sau ngày nhận phòng không
    if check_in_date >= check_out_date:
        messagebox.showwarning("Lỗi", "Ngày trả phòng phải sau ngày nhận phòng!")
        return

    # Kiểm tra xem có thể đặt phòng không (gọi hàm đặt phòng)
    total_price, booking_id = dat_phong(customer_id, room_id, check_in_date, check_out_date)
    if total_price is not None:
        messagebox.showinfo("Thành công", f"Đặt phòng thành công với tổng giá: {total_price:.2f} VND")
        hien_thi_phuong_thuc_thanh_toan(customer_id, booking_id, total_price)  # Now passing booking_id here
    else:
        messagebox.showerror("Lỗi", "Không thể đặt phòng.")


def kiem_tra_phong_co_san(room_id):
    conn = tao_ket_noi()
    cursor = conn.cursor()
    try:
        query = "SELECT status FROM Room WHERE room_id = %s"
        cursor.execute(query, (room_id,))
        result = cursor.fetchone()

        if result and result[0] == 'available':
            return True
        else:
            return False
    except Exception as e:
        print(f"Lỗi khi kiểm tra phòng: {e}")
        return False
    finally:
        cursor.close()
        conn.close()



def xu_ly_chon_phong(customer_id, listbox_rooms):
    selected = listbox_rooms.curselection()
    if not selected:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một phòng!")
        return

    # Lấy thông tin mã phòng từ danh sách
    selected_room = listbox_rooms.get(selected)
    room_id = int(selected_room.split(" - ")[1].split(":")[1].strip())

    # Chuyển sang giao diện đặt phòng
    hien_thi_form_dat_phong(customer_id, room_id)

# Hàm thanh toán
def thanh_toan(booking_id, payment_method, payment_amount, total_price):
    total_price = float(total_price)

    # Kiểm tra số tiền thanh toán
    if payment_amount < total_price:
        messagebox.showwarning("Thanh toán không đủ", f"Bạn còn thiếu: {total_price - payment_amount:.2f} VND")
        return
    elif payment_amount > total_price:
        messagebox.showinfo("Thanh toán thừa", f"Bạn đã trả dư, tiền thừa là: {payment_amount - total_price:.2f} VND")

    # Ghi thông tin thanh toán vào cơ sở dữ liệu
    conn = tao_ket_noi()
    cursor = conn.cursor()
    query = """
        INSERT INTO Payment (booking_id, payment_method, payment_amount, status)
        VALUES (%s, %s, %s, 'paid')
    """
    cursor.execute(query, (booking_id, payment_method, payment_amount))
    conn.commit()

    # Cập nhật trạng thái thanh toán của booking
    update_booking_query = "UPDATE Booking SET payment_status = 'paid' WHERE booking_id = %s"
    cursor.execute(update_booking_query, (booking_id,))
    conn.commit()

    cursor.close()
    conn.close()
    messagebox.showinfo("Thanh toán thành công", "Thanh toán thành công!")

def hien_thi_phuong_thuc_thanh_toan(customer_id, booking_id, total_price):
    # Xóa giao diện hiện tại
    for widget in root.winfo_children():
        widget.grid_forget()

    # Hiển thị thông tin thanh toán
    label_payment = tk.Label(root, text=f"Tổng tiền: {total_price:.2f} VND", font=("Arial", 14))
    label_payment.grid(row=0, column=0, columnspan=2, pady=10)

    label_choose_method = tk.Label(root, text="Chọn phương thức thanh toán:", font=("Arial", 12))
    label_choose_method.grid(row=1, column=0, columnspan=2, pady=10)

    # Dropdown chọn phương thức thanh toán
    payment_method_var = tk.StringVar(value="Tiền mặt")
    payment_methods = ["Tiền mặt", "Thẻ tín dụng", "Chuyển khoản ngân hàng"]
    dropdown_payment = tk.OptionMenu(root, payment_method_var, *payment_methods)
    dropdown_payment.grid(row=2, column=0, columnspan=2, pady=10)

    # Nhập số tiền thanh toán
    label_payment_amount = tk.Label(root, text="Số tiền thanh toán:")
    label_payment_amount.grid(row=3, column=0, pady=5)
    entry_payment_amount = tk.Entry(root)
    entry_payment_amount.grid(row=3, column=1, pady=5)

    # Nút xác nhận thanh toán
    btn_confirm_payment = tk.Button(
        root,
        text="Xác nhận thanh toán",
        command=lambda: xu_ly_thanh_toan(
            customer_id, 
            booking_id, 
            payment_method_var.get(), 
            entry_payment_amount.get(), 
            total_price
        )
    )
    btn_confirm_payment.grid(row=4, column=0, columnspan=2, pady=20)

    # Nút quay lại menu chính
    btn_back = tk.Button(root, text="Quay lại menu chính", command=lambda: hien_thi_menu(customer_id))
    btn_back.grid(row=5, column=0, columnspan=2, pady=10)

def xu_ly_thanh_toan(customer_id, booking_id, payment_method, payment_amount, total_price):
    try:
        payment_amount = float(payment_amount)
        total_price = float(total_price)
    except ValueError:
        messagebox.showwarning("Lỗi", "Số tiền thanh toán không hợp lệ!")
        return

    if payment_amount < total_price:
        messagebox.showwarning("Lỗi", f"Bạn còn thiếu: {total_price - payment_amount:.2f} VND")
        return
    elif payment_amount > total_price:
        messagebox.showinfo("Thông báo", f"Bạn đã trả dư {payment_amount - total_price:.2f} VND. Tiền thừa sẽ được hoàn lại.")

    # Ghi thông tin thanh toán vào cơ sở dữ liệu
    conn = tao_ket_noi()
    cursor = conn.cursor()
    query = """
        INSERT INTO Payment (booking_id, payment_method, payment_amount, status)
        VALUES (%s, %s, %s, 'paid')
    """
    cursor.execute(query, (booking_id, payment_method, payment_amount))
    conn.commit()

    # Cập nhật trạng thái thanh toán của đặt phòng
    update_booking_query = "UPDATE Booking SET payment_status = 'paid' WHERE booking_id = %s"
    cursor.execute(update_booking_query, (booking_id,))
    conn.commit()

    cursor.close()
    conn.close()

    messagebox.showinfo("Thành công", "Thanh toán thành công!")
    hien_thi_menu(customer_id)  # Sử dụng customer_id đã truyền





# Khởi tạo cửa sổ
root = tk.Tk()
root.title("Hệ thống đặt phòng khách sạn")

# Khởi tạo các widget (các entry và button)
entry_username = tk.Entry(root)
entry_password = tk.Entry(root, show="*")
entry_email = tk.Entry(root)
entry_phone = tk.Entry(root)

# Đặt tên cho các label để hướng dẫn người dùng
label_username = tk.Label(root, text="Tên đăng nhập:")
label_password = tk.Label(root, text="Mật khẩu:")
label_email = tk.Label(root, text="Email:")
label_phone = tk.Label(root, text="Số điện thoại:")

# Đặt các button cho đăng ký và đăng nhập
btn_login = tk.Button(root, text="Đăng nhập", command=xu_ly_dang_nhap)
btn_register = tk.Button(root, text="Đăng ký", command=hien_thi_dang_ky)

# Nút quay lại đăng nhập khi ở chế độ đăng ký
btn_back_to_login = tk.Button(root, text="Quay lại đăng nhập", command=hien_thi_dang_nhap)


# Bố trí các widget trong cửa sổ cho phần đăng nhập
label_username.grid(row=0, column=0, padx=10, pady=10)
entry_username.grid(row=0, column=1, padx=10, pady=10)

label_password.grid(row=1, column=0, padx=10, pady=10)
entry_password.grid(row=1, column=1, padx=10, pady=10)

btn_login.grid(row=2, column=0, columnspan=2, pady=20)
btn_register.grid(row=3, column=0, columnspan=2, pady=10)

# Hiển thị cửa sổ
root.mainloop()
