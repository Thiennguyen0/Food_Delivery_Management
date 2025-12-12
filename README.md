Dự án nhóm tụi con gồm: Nguyễn Ngọc Ái Minh 11Ti10, Phạm Hoàng Nhật Huy 11Ti11, Nguyễn Hữu Thiện 11Ti10, Hà Tuấn Kiệt 11Ti10

Bảng tóm tắt dự án:
Trong bối cảnh các quán ăn, cửa hàng kinh doanh thực phẩm chưa được tối ưu tốt về hệ thống quản trị nhân lực, giá thành, nhập-xuất và vận chuyển, dẫn đến sự hao tổn trong kinh phí, sai sót trong việc kiểm kê các đơn hàng,... xảy ra bởi dữ liệu và lượng lớn thông tin không có tính nhất quán, chưa được đồng bộ hoặc phải dùng nhiều cơ sở dữ liệu khác nhau cho các thao tác riêng biệt gồm: nhập liệu, quản lý nguyên-vật liệu, thời gian, vận chuyển, đơn hàng,... Đề tài này tập trung xây dựng hệ thống quản lý thực phẩm, vận chuyển đồ ăn (food delivery dashboard) với quy mô phục vụ cho các cơ sở tư nhân kinh doanh thực phẩm, dựa trên cơ sở dữ liệu nhằm tối ưu hóa quy trình vận hành của các quán ăn hay nhà hàng. Hệ thống có khả năng tích hợp các chức năng như quản lý kho nguyên liệu, quản lý khâu chế biến và thời gian cho các món ăn, xử lý đơn hàng, theo dõi thao tác giao hàng, giúp kết nối chặt chẽ giữa các khâu chế biến, giao nhận và quản trị. Dữ liệu được lưu trữ và xử lý trong cơ sở dữ liệu quan hệ, đảm bảo tính toàn vẹn, nhất quán và khả năng cập nhật theo thời gian thực. Thông qua giao diện, người quản lý có thể dễ dàng theo dõi tình trạng nguyên liệu, các món đang được chuẩn bị, doanh thu, đơn hàng đã, đang hoặc sẽ giao. Hệ thống góp phần nâng cao hiệu quả quản lý, giảm thiểu sai sót thủ công và có thể được mở rộng ra thêm giao diện dành cho người dùng và tích hợp các sự kiện, mã giảm giá. (https://docs.google.com/document/d/1hJZVvj8bn0-FttisvloVSNhsf7DUWIIfwkU18FU2HBE/edit?usp=sharing)

Do sự linh hoạt và hiệu cũng như dễ dùng và phạm vi sử dụng rộng rại của ngôn ngữ python nên bọn em đã chọn nó làm ngôn ngữ chính cho dự án này.

Dự án sử dụng SQLite (để làm việc với cơ sở dữ liêu), thư viện CustomTkinter để lập trình giao diện, các thư viện phụ như datetime, json để làm việc với thời gian và đóng và mở gói cấu trúc json.

Tổng số file trong dự án này là 6 files bao gồm (create_db.py dùng để tạo lập cơ sở dữ liệu ban đầu, food_db.db là cơ sở dữ liệu - có thể trực quan hóa bằng phần mềm DB Browser, backend.py dùng để handle query và kết nối với cơ sở dữ liệu, fixed_ui.py là phần giao diện đã được sửa lại nhiều lần để phù hợp nhất với các tính năng và có tính thẩm mỹ, 1 file đc xuất chương trình ra .exe để tiện cho việc sử dụng, và file README.md)

Các tính năng chính:
- Quản lý kho nguyên liệu  
- Quản lý món ăn và thời gian chế biến  
- Quản lý đơn hàng (đã/đang/sắp giao)  
- Thống kê doanh thu  
- Giao diện trực quan với CustomTkinter  
