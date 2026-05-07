''' 
  Deduplication of repeated values 
'''
with x as 
(select row_number() over (partition by id) as duplicate,* from real_estate)
delete from real_estate
where id in (select id from x where duplicate>1)

'''
Cleaning of data by removing incomplete data
'''
delete from real_estate
where carpet_area is null or "SBA" is null

'''
Joining table with pincode as location as a text cannot be used for map visualisation and using that query to create a new table
'''
create table real_estate_final as
select r.*,p."Pincode" from real_estate as r
left join pincode as p on r.location=p."Pincode"
