Cau 1
CREATE PROCEDURE sp_GetCandidatesBySchool
    @MaTruong INT
AS
BEGIN
    SELECT HOTEN
    FROM THISINH ts
    INNER JOIN TRUONG t ON ts.MATRUONG = t.MATRUONG
    WHERE t.MATRUONG = @MaTruong
END

--------------------------
Cau 2
CREATE FUNCTION fn_CountFailedCandidatesBySchool
    (@MaTruong INT)
RETURNS INT
AS
BEGIN
    DECLARE @Count INT
    SELECT @Count = COUNT(*)
    FROM (
        SELECT DISTINCT SOBD
        FROM KETQUA kq
        INNER JOIN THISINH ts ON kq.SOBD = ts.SOBD
        INNER JOIN TRUONG t ON ts.MATRUONG = t.MATRUONG
        WHERE t.MATRUONG = @MaTruong
        GROUP BY SOBD
        HAVING MIN(DIEM) < 1
    ) AS FailedCandidates
    RETURN @Count
END

--------------------------
Cau 3
CREATE TRIGGER trg_Thisinh
ON THISINH
AFTER INSERT, UPDATE
AS
BEGIN
  IF EXISTS (SELECT * FROM inserted WHERE DATEDIFF(year, NGAYSINH, GETDATE()) < 18 OR NAMDUTHI != YEAR(GETDATE()))
  BEGIN
    RAISERROR ('Thí sinh phải từ 18 tuổi trở lên và năm dự thi không được khác năm hiện tại!', 16, 1)
    ROLLBACK TRANSACTION
  END
END
