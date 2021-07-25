TYPE=VIEW
query=select `stock`.`stock`.`Sid` AS `Sid`,`stock`.`stock`.`Sname` AS `Sname`,`stock`.`kline`.`Kdate` AS `Kdate`,`stock`.`kline`.`Kclose` AS `Kclose`,`stock`.`kline`.`Khigh` AS `Khigh`,`stock`.`kline`.`Klow` AS `Klow`,`stock`.`kline`.`Kopen` AS `Kopen`,`stock`.`kline`.`Kpre` AS `Kpre`,`stock`.`kline`.`Kvol` AS `Kvol`,`stock`.`kline`.`Kamount` AS `Kamount` from `stock`.`kline` join `stock`.`stock` where (`stock`.`kline`.`K_Sid` = `stock`.`stock`.`Sid`)
md5=6a300887faf0fc944cd2a6da932c19c1
updatable=1
algorithm=0
definer_user=root
definer_host=localhost
suid=2
with_check_option=0
timestamp=2021-06-19 05:21:22
create-version=1
source=select Sid,Sname,Kdate,Kclose,Khigh,Klow,Kopen,Kpre,Kvol,Kamount\n \nfrom kline,stock\n \nwhere kline.K_Sid=stock.Sid
client_cs_name=utf8
connection_cl_name=utf8_general_ci
view_body_utf8=select `stock`.`stock`.`Sid` AS `Sid`,`stock`.`stock`.`Sname` AS `Sname`,`stock`.`kline`.`Kdate` AS `Kdate`,`stock`.`kline`.`Kclose` AS `Kclose`,`stock`.`kline`.`Khigh` AS `Khigh`,`stock`.`kline`.`Klow` AS `Klow`,`stock`.`kline`.`Kopen` AS `Kopen`,`stock`.`kline`.`Kpre` AS `Kpre`,`stock`.`kline`.`Kvol` AS `Kvol`,`stock`.`kline`.`Kamount` AS `Kamount` from `stock`.`kline` join `stock`.`stock` where (`stock`.`kline`.`K_Sid` = `stock`.`stock`.`Sid`)
