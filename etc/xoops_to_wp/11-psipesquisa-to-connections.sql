#alter table user_seminar add us_id Int NOT NULL AUTO_INCREMENT;
TRUNCATE TABLE`website_port2`.`wp_connections`;
TRUNCATE TABLE `website_port2`.`wp_connections_link`;

TRUNCATE TABLE `website_port2`.`wp_connections_terms`;
TRUNCATE TABLE `website_port2`.`wp_connections_term_taxonomy`;
TRUNCATE TABLE `website_port2`.`wp_connections_term_relationships`;


#copia todas as categorias do mylinks para o connections
insert into `website_port2`.`wp_connections_terms` 
select (cid+1) as term_id, 
title as name, 
slugify( lower(CONCAT(title, '-',cid+1)) ) as slug, 
0 as term_group 
from `website_xoops`.`xoopswebsite_mylinks_cat`;

#importa as categorias que nao possuem pais
insert into `website_port2`.`wp_connections_term_taxonomy`
select ca.cid+1 as term_taxonomy_id, 
ca.cid+1 as term_id, 
'category' as taxonomy, 
'' as description, 
0 as parent, 
0 as count 
from `website_xoops`.`xoopswebsite_mylinks_cat` ca
where ca.pid= 0;

#importa as categorias que possuem pais
insert into `website_port2`.`wp_connections_term_taxonomy`
select ca.cid+1 as term_taxonomy_id, 
ca.cid+1 as term_id, 
'category' as taxonomy, 
'' as description, 
ca.pid+1 as parent, 
0 as count 
from `website_xoops`.`xoopswebsite_mylinks_cat` ca
where ca.pid <> 0;

#cria as conexoes no connections: uma para cada link do mylinks
INSERT INTO `website_port2`.`wp_connections`
SELECT li.lid as id,
NULL as ts,
NULL as date_added,
'individual' as entry_type,
'public' as visibility,
slugify( lower(li.title) ) as slug,
'' as family_name,
'' as honorific_prefix,
li.title as first_name,
'' as middle_name, 
'' as last_name, 
'' as honorific_suffix, 
'' as title, 
'' as organization, 
'' as department, 
'' as contact_first_name, 
'' as contact_last_name, 
'' as addresses, 
'' as phone_numbers, 
'' as email, 
'' as im, 
'' as social,
'' as links,
'' as dates,
'' as birthday,
'' as anniversary,
te.description as bio,
'' as notes,
'' as options,
1 as added_by,
1 as edited_by,
1 as owner,
0 as user,
'approved' as status
FROM `website_xoops`.`xoopswebsite_mylinks_links` li
JOIN `website_xoops`.`xoopswebsite_mylinks_text` te ON li.lid = te.lid;

#importa os links para o connections
INSERT INTO `website_port2`.`wp_connections_link`
SELECT
NULL as id,
lid as entry_id,
0 as `order`,
0 as preferred,
'website' as type,
title,
url,
'_blank' as target,
0 as follow,
0 as image,
0 as logo, 
'public' as visibility
FROM `website_xoops`.`xoopswebsite_mylinks_links`;

#cria as relacoes entre as categorias e as conexoes
INSERT INTO `website_port2`.`wp_connections_term_relationships` 
SELECT li.lid AS object_id, 
li.cid+1 AS term_taxonomy_id, 
0 as term_order 
FROM `website_xoops`.`xoopswebsite_mylinks_links` li;



#falta serializar os dados da tabela links para ser usado na tabela de connections.



+------------+---------------------+------+-----+---------+----------------+
| Field      | Type                | Null | Key | Default | Extra          |
+------------+---------------------+------+-----+---------+----------------+
| id         | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment | 
| entry_id   | bigint(20) unsigned | NO   | PRI | 0       |                | 
| order      | tinyint(3) unsigned | NO   |     | 0       |                | 
| preferred  | tinyint(3) unsigned | NO   |     | 0       |                | 
| type       | tinytext            | NO   |     | NULL    |                | 
| title      | tinytext            | NO   |     | NULL    |                | 
| url        | tinytext            | NO   |     | NULL    |                | 
| target     | tinytext            | NO   |     | NULL    |                | 
| follow     | tinyint(3) unsigned | NO   |     | 0       |                | 
| image      | tinyint(3) unsigned | NO   |     | 0       |                | 
| logo       | tinyint(3) unsigned | NO   |     | 0       |                | 
| visibility | tinytext            | NO   |     | NULL    |                | 
+------------+---------------------+------+-----+---------+----------------+




#importa os links para o connections
INSERT INTO `website_port2`.`wp_connections_link`
SELECT
NULL as id,
lid as entry_id,
0 as `order`,
0 as preferred,
'website' as type,
title,
url,
'_blank' as target,
0 as follow,
0 as image,
0 as logo, 
'public' as visibility
FROM `website_xoops`.`xoopswebsite_mylinks_links`;


#nao funciona
#UPDATE `website_port2`.`wp_connections` co
#JOIN `website_port2`.`wp_connections_link` li ON li.entry_id = co.id
#SET co.links = CONCAT('a:1:{i:', co.id, ';a:10:{s:4:"type";s:7:"website";s:10:"visibility";s:6:"public";s:5:"title";s:', LENGTH(li.title), ':"', li.title,'";s:3:"url";s:', LENGTH(li.url), ':"', li.url, '";s:6:"target";s:4:"same";s:6:"follow";i:0;s:5:"order";i:0;s:9:"preferred";b:1;s:5:"image";b:0;s:4:"logo";b:0;}}')
#AND  co.options = 'a:2:{s:5:"entry";a:1:{s:4:"type";s:10:"individual";}s:5:"group";a:1:{s:6:"family";a:0:{}}}';






