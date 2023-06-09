------------------------------Câu 1----------------------------

---------------------------Cách AFTER INSERT-------------------
CREATE TRIGGER tg_SV_Them 
ON SINH_VIEN 
AFTER INSERT
AS 
BEGIN 
    IF EXISTS (SELECT * FROM inserted i 
               LEFT JOIN KHOA k ON i.Ma_khoa = k.Ma_khoa   //trả về tất cả các bản ghi từ bảng bên trái (SINHVIEN) và các bản ghi phù hợp từ bảng bên phải (KHOA).
               WHERE k.Ma_khoa IS NULL)
    BEGIN
        RAISERROR ('Ma khoa khong ton tai!', 16, 1);
        ROLLBACK TRANSACTION;
    END
    IF EXISTS (SELECT * FROM inserted i 
               WHERE DATEDIFF(YEAR, i.Ngay_sinh, GETDATE()) < 18)
    BEGIN
        RAISERROR ('Sinh vien chua du 18 tuoi!', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;
---------------------------Cách INSTEAD OF-------------------
CREATE TRIGGER tg_SV_Them2 
ON SINH_VIEN 
INSTEAD OF INSERT
AS 
BEGIN 
    IF EXISTS (SELECT * FROM inserted i 
               LEFT JOIN KHOA k ON i.Ma_khoa = k.Ma_khoa   //trả về tất cả các bản ghi từ bảng bên trái (SINHVIEN) và các bản ghi phù hợp từ bảng bên phải (KHOA).
               WHERE k.Ma_khoa IS NULL)
    BEGIN
        RAISERROR ('Ma khoa khong ton tai!', 16, 1);
        ROLLBACK TRANSACTION;
    END
    IF EXISTS (SELECT * FROM inserted i 
               WHERE DATEDIFF(YEAR, i.Ngay_sinh, GETDATE()) < 18)
    BEGIN
        RAISERROR ('Sinh vien chua du 18 tuoi!', 16, 1);
        ROLLBACK TRANSACTION;
    END
    ELSE 
    BEGIN
        INSERT INTO SINH_VIEN (Ma_sinh_vien,Ho_sinh_vien, Ngay_sinh, Gioi_tinh, Ma_khoa) 
        SELECT Ma_sinh_vien, Ho_sinh_vien, Ngay_sinh, Gioi_tinh, Ma_khoa 
        FROM inserted;
    END
END;

------------------------------Câu 2----------------------------
---------------------------Cách AFTER INSERT-------------------
CREATE TRIGGER tg_KQ_Sua
ON KET_QUA
AFTER UPDATE
AS
BEGIN
    IF EXISTS (SELECT * FROM inserted i
               JOIN deleted d ON i.Ma_sinh_vien = d.Ma_sinh_vien AND i.Ma_mon = d.Ma_mon
               WHERE i.Diem < 0 OR i.Diem > 10)
    BEGIN
        RAISERROR('Diem phai thuoc [0,10]!', 16, 1);
        ROLLBACK TRANSACTION;
    END
    IF EXISTS (SELECT * FROM inserted i
               JOIN deleted d ON i.Ma_sinh_vien = d.Ma_sinh_vien AND i.Ma_mon = d.Ma_mon
               WHERE i.Ma_sinh_vien != d.Ma_sinh_vien OR i.Ma_mon != d.Ma_mon)
    BEGIN
        RAISERROR('Khong cho phep sua ma SV hoac ma MH!', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;
---------------------------Cách INSTEAD OF-------------------
CREATE TRIGGER tg_KQ_Sua2
ON KET_QUA
INSTEAD OF UPDATE
AS
BEGIN
    IF EXISTS (SELECT * FROM inserted i
               JOIN deleted d ON i.MaSV = d.MaSV AND i.MaMH = d.MaMH
               WHERE i.Diem < 0 OR i.Diem > 10)
    BEGIN
        RAISERROR('Diem phai thuoc [0,10]!', 16, 1);
        ROLLBACK TRANSACTION;
    END
    IF EXISTS (SELECT * FROM inserted i
               JOIN deleted d ON i.MaSV = d.MaSV AND i.MaMH = d.MaMH
               WHERE i.MaSV != d.MaSV OR i.MaMH != d.MaMH)
    BEGIN
        RAISERROR('Khong cho phep sua ma SV hoac ma MH!', 16, 1);
        ROLLBACK TRANSACTION;
    END
    ELSE
    BEGIN
        UPDATE KET_QUA
        SET Diem = i.Diem
        FROM inserted i
        WHERE KET_QUA.MaSV = i.MaSV AND KET_QUA.MaMH = i.MaMH;
    END
END;


------------------------------Câu 3----------------------------
CREATE TRIGGER tg_SV_Xoa
ON SINH_VIEN
AFTER DELETE
AS
BEGIN
    DECLARE @sv_id INT;
    DECLARE @mon_duoi_5 INT;
    
    SELECT @sv_id = deleted.Ma_sinh_vien FROM deleted;
    
    SELECT @mon_duoi_5 = COUNT(*) FROM KET_QUA
    WHERE Ma_sinh_vien = @sv_id AND diem < 5;
    
    IF (@mon_duoi_5 > 4)
    BEGIN
        RAISERROR ('Khong the xoa sinh vien nay vi co qua nhieu mon diem duoi 5', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END
END;


-----------------
CREATE TRIGGER tg_SV_Xoa3
ON SINH_VIEN
INSTEAD OF DELETE
AS
BEGIN
    DECLARE @sv_id INT;
    DECLARE @mon_duoi_5 INT;
    
    SELECT @sv_id = Ma_sinh_vien FROM deleted;
    
    SELECT @mon_duoi_5 = COUNT(*) FROM KET_QUA
    WHERE Ma_sinh_vien = @sv_id AND diem < 5;
    
    IF (@mon_duoi_5 > 4)
    BEGIN
        RAISERROR ('Khong the xoa sinh vien nay vi co qua nhieu mon diem duoi 5', 16, 1);
        RETURN;
    END
    
    DELETE FROM SINH_VIEN
    WHERE Ma_sinh_vien = @sv_id;
END;


------------------------------Câu 4----------------------------
-- Tạo view vw_SINH_VIEN
CREATE VIEW vw_SINH_VIEN AS
SELECT SV.Ma_sinh_vien, SV.Ho_sinh_vien, SV.Ten_sinh_vien, SV.gioi_tinh, SV.ma_khoa
FROM SINH_VIEN SV
INNER JOIN KHOA K ON SV.ma_khoa = K.ma_khoa;
