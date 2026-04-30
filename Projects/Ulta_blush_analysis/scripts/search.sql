USE sephora_blushes;
GO

select * from sku_details sd 
join skus s on s.sku_id=sd.sku_id
join products p on p.product_id=s.sku_id
-- where brands = 'Benefit Cosmetics'