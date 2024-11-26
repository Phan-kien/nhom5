INSERT INTO Hotel (username, location, rating, phone, email, amenities)
VALUES
('Grand Hotel', 'Hanoi, Vietnam', 4.5, '0901234567', 'grandhotel@gmail.com', 'Free Wi-Fi, Pool, Spa'),
('Luxury Resort', 'Da Nang, Vietnam', 5.0, '0912345678', 'luxuryresort@yahoo.com', 'Beachfront, Fitness Center, Restaurant'),
('City Inn', 'Ho Chi Minh City, Vietnam', 3.8, '0923456789', 'cityinn@hotmail.com', 'Free Parking, Restaurant, Bar');

INSERT INTO Room (hotel_id, room_type, price_per_night, capacity, status, description)
VALUES
(1, 'Deluxe', 100.00, 2, 'available', 'A luxurious room with a king-sized bed and great city view.'),
(1, 'Standard', 60.00, 2, 'available', 'A cozy room for two with a comfortable bed and basic amenities.'),
(2, 'Ocean View', 150.00, 2, 'available', 'A beautiful room with an ocean view and a private balcony.'),
(2, 'Suite', 250.00, 4, 'maintenance', 'A spacious suite with two bedrooms and a living area.'),
(3, 'Single', 40.00, 1, 'available', 'A small room for a single guest with basic amenities.'),
(3, 'Double', 80.00, 2, 'available', 'A room with a double bed and modern facilities.'),
(1, 'Premium Suite', 300.00, 4, 'available', 'A top-tier suite with premium facilities and breathtaking views.'),
(1, 'Economy', 50.00, 2, 'available', 'An affordable room with basic amenities for budget travelers.'),
(2, 'Family Room', 120.00, 4, 'available', 'A spacious room for families with two queen-sized beds.'),
(2, 'Executive', 200.00, 3, 'available', 'A luxurious room tailored for business travelers.'),
(3, 'Studio', 90.00, 2, 'available', 'A modern studio room with a kitchenette and a comfortable bed.'),
(3, 'Penthouse', 500.00, 6, 'maintenance', 'An exclusive penthouse with a private terrace and premium services.'),
(2, 'Twin', 70.00, 2, 'available', 'A room with two single beds, ideal for friends or colleagues.'),
(2, 'Honeymoon Suite', 180.00, 2, 'available', 'A romantic suite perfect for couples with special decor.'),
(3, 'Bungalow', 220.00, 4, 'available', 'A private bungalow with a garden view and all modern amenities.'),
(3, 'Loft', 110.00, 3, 'available', 'A trendy loft-style room with unique interior design.');


INSERT INTO Customer (username, email, phone, password)
VALUES
('john_doe', 'johndoe@gmail.com', '0987654321', 'password123'),
('alice_smith', 'alice_smith@yahoo.com', '0912345678', 'mypassword456'),
('bob_jones', 'bob_jones@hotmail.com', '0909876543', 'securepassword789');


INSERT INTO Booking (customer_id, room_id, check_in_date, check_out_date, total_price, status, payment_status)
VALUES
(1, 1, '2024-12-01', '2024-12-05', 400.00, 'confirmed', 'paid'),
(2, 3, '2024-12-10', '2024-12-15', 750.00, 'pending', 'pending'),
(3, 5, '2024-12-15', '2024-12-20', 200.00, 'cancelled', 'pending');  -- Chỉnh sửa payment_status thành 'pending'



INSERT INTO Payment (booking_id, payment_method, payment_amount, status)
VALUES
(1, 'thẻ tín dụng', 400.00, 'paid'),
(2, 'Momo', 750.00, 'pending'),
(3, 'chuyển khoản ngân hàng', 200.00, 'cancelled');

INSERT INTO Employee (username, email, phone, position, salary, hotel_id, hire_date, status)
VALUES
('jane_doe', 'jane_doe@grandhotel.com', '0901122334', 'Manager', 1500.00, 1, '2024-01-01', 'active'),
('michael_smith', 'michael_smith@luxuryresort.com', '0912233445', 'Receptionist', 1200.00, 2, '2023-11-15', 'active'),
('susan_jones', 'susan_jones@cityinn.com', '0923344556', 'Housekeeper', 1000.00, 3, '2024-06-10', 'inactive');

INSERT INTO Review (booking_id, customer_id, rating, comment)
VALUES
(1, 1, 5, 'Great stay! The room was clean and the staff were very helpful.'),
(2, 2, 4, 'The view was amazing, but the room was a bit smaller than expected.'),
(3, 3, 3, 'The hotel was fine, but the service could have been better.');

