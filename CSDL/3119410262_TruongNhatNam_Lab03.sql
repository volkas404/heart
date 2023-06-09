----Câu 1----
CREATE FUNCTION fn_TinhHocBong(@Ma_sinh_vien VARCHAR(10))
RETURNS INT
AS
BEGIN
    DECLARE @SoMonHocDatDiem8 INT
    DECLARE @HocBong INT
    SELECT @SoMonHocDatDiem8 = COUNT(*) FROM KET_QUA WHERE Ma_sinh_vien = @Ma_sinh_vien AND Diem >= 8
    IF @SoMonHocDatDiem8 >= 4
        SET @HocBong = 400000
    ELSE IF @SoMonHocDatDiem8 = 3
        SET @HocBong = 300000
    ELSE IF @SoMonHocDatDiem8 = 2
        SET @HocBong = 200000
    ELSE
        SET @HocBong = 0
    RETURN @HocBong
END



----Câu 2----
CREATE FUNCTION fn_DSXepHang(@k INT)
RETURNS @DanhSachXepHang TABLE (
    MaSV NVARCHAR(255) PRIMARY KEY,
    HoTen NVARCHAR(50),
    DiemTB FLOAT
)
AS
BEGIN

    INSERT INTO @DanhSachXepHang (MaSV, HoTen, DiemTB)
    SELECT TOP(@k) sv.Ma_sinh_vien, sv.Ten_sinh_vien, SUM(kq.Diem) / COUNT(*) AS DiemTB
    FROM SINH_VIEN sv
    INNER JOIN KET_QUA kq ON sv.Ma_sinh_vien = kq.Ma_sinh_vien
    GROUP BY sv.Ma_sinh_vien, sv.Ten_sinh_vien
    ORDER BY DiemTB DESC
    RETURN 

END


----Câu 3----
ALTER FUNCTION fn_DSKhongDat(@nguong FLOAT)
RETURNS @DanhSachKhongDat TABLE (
    MaSV NVARCHAR(255),
    TenSV NVARCHAR(100),
    DiemTrungBinh FLOAT
)
AS
BEGIN
    INSERT INTO @DanhSachKhongDat
    SELECT sv.Ma_sinh_vien, sv.Ten_sinh_vien, SUM(kq.Diem) / COUNT(*) AS DiemTrungBinh
    FROM KET_QUA kq, SINH_VIEN sv
	WHERE sv.Ma_sinh_vien=kq.Ma_sinh_vien
    GROUP BY sv.Ma_sinh_vien, sv.Ten_sinh_vien
    HAVING SUM(kq.Diem) / COUNT(*) < @nguong
    
    RETURN
END



----Câu 4----
CREATE FUNCTION fn_XepLoai()
RETURNS TABLE
AS
RETURN
    SELECT 
        dsxh.MaSV, 
        dsxh.HoTen, 
        dsxh.DiemTB,
        CASE 
            WHEN dsxh.DiemTB >= 9 THEN N'Xuất sắc'
            WHEN dsxh.DiemTB >= 8 THEN N'Giỏi'
            WHEN dsxh.DiemTB >= 7 THEN N'Khá'
            WHEN dsxh.DiemTB >= 6.5 THEN N'Trung bình - Khá'
            WHEN dsxh.DiemTB >= 5 THEN N'Trung bình'
            ELSE N'Yếu/Kém'
        END AS XepLoai
    FROM fn_DSXepHang(1000000) AS dsxh -- lấy tất cả sinh viên trong danh sách xếp hạng
