Cau 1.1
create proc sp_KiemTra
	@macd varchar(MAX),
	@maxe varchar(MAX)
as
begin
	if not exists (select x.MAXE from XE x where x.MAXE=@maxe)
		begin
			print('Ma xe khong ton tai')
		end
	else if not exists (select cd.MACD from CHUYENDI cd where cd.MACD=@macd)
		begin
			print('Ma chuyen di khong ton tai')
		end
	else if exists (select cdx.MAXE from XE x join CD_XE cdx on x.MAXE=cdx.MAXE join CHUYENDI cd on cd.MACD=cdx.MACD where cdx.MACD=@macd and cd.NGAYDI=GETDATE())
		begin
			print('Xe nay da co chuyen di')
		end
	else
		begin
			insert into CD_XE values(@macd,@maxe)
			print('chay duoc')
		end
end
go
--------------------------
Cau 1.2
create trigger tg_Xe
on XE
after update
as
begin
    IF update(BANGSO)
    begin
        declare @OldBangSo varchar(50), @NewBangSo varchar(50);
        select @OldBangSo = deleted.BANGSO, @NewBangSo = inserted.BANGSO from deleted JOIN inserted ON deleted.MAXE = inserted.MAXE;

        IF @OldBangSo <> @NewBangSo AND NOT EXISTS (select * from XE where BANGSO = @NewBangSo)
        begin
            update XE set BANGSO = @NewBangSo where MAXE IN (select MAXE from inserted);
        end
        else
        begin
            raiserror('Sai thông tin bảng số xe', 16, 1);
            rollback transaction;
            return;
        end
    end
end