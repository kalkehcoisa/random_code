#DESCRIBE xoopswebsite_xoopsfaq_categories;
#DESCRIBE xoopswebsite_xoopsfaq_contents;


INSERT INTO `website_port`.`wp_terms` (term_id, name, slug, term_group) VALUES (801, 'FAQ', 'faq', 0);
INSERT INTO `website_port`.`wp_term_taxonomy` (term_taxonomy_id, term_id, taxonomy, description, parent, count) VALUES (701, 801, 'category', '', 0, 0);

INSERT INTO `website_port`.`wp_terms`
SELECT (cat.category_id+801) as term_id, 
cat.category_title as name,
slugify( lower(cat.category_title) ) as slug,
0 as term_group
FROM `website_xoops`.`xoopswebsite_xoopsfaq_categories` cat;



INSERT INTO `website_port`.`wp_term_taxonomy`
SELECT (cat.category_id+701) as term_taxonomy_id, 
(cat.category_id+801) as term_id,
'category' as taxonomy,
'' as description, 
801 as parent, 
0 as count 
FROM `website_xoops`.`xoopswebsite_xoopsfaq_categories` cat;

INSERT INTO `website_port`.`wp_term_relationships` 
SELECT (con.contents_id+53000) AS object_id, (con.category_id+701) AS term_taxonomy_id, 0 as term_order 
FROM `website_xoops`.`xoopswebsite_xoopsfaq_contents` con;

INSERT INTO `website_port`.`wp_term_relationships` 
SELECT (con.contents_id+53000) AS object_id, (701) AS term_taxonomy_id, 0 as term_order 
FROM `website_xoops`.`xoopswebsite_xoopsfaq_contents` con;


INSERT INTO `website_port`.`wp_postmeta`
SELECT
NULL as meta_id,
(con.contents_id+53000) as post_id,
NULL as meta_key,
NULL as meta_value
FROM `website_xoops`.`xoopswebsite_xoopsfaq_contents` con;



INSERT INTO `website_port`.`wp_posts`
select (con.contents_id+53000) as id,
1 as post_author,
FROM_UNIXTIME(con.contents_time) as post_date,
FROM_UNIXTIME(con.contents_time) as post_date_gmt,
con.contents_contents as post_content,
con.contents_title as post_title,
'' as post_excerpt,
'publish' as post_status,
'closed' as comment_status,
'open' as ping_status,
'' as post_password,
contents_title as post_name,
NULL as to_ping,
NULL as pinged,
FROM_UNIXTIME(con.contents_time) as post_modified,
FROM_UNIXTIME(con.contents_time) as post_modified_gmt,
NULL as post_content_filtered,
0 as post_parent,
'' as guid,
0 as menu_order,
'post' as post_type,
'' as post_mime_type,
0 as comment_count
FROM `website_xoops`.`xoopswebsite_xoopsfaq_contents` con
LEFT JOIN `website_xoops`.`xoopswebsite_xoopsfaq_categories` cat ON con.category_id = cat.category_id;




UPDATE `website_port`.`wp_term_taxonomy` tt1
SET count =
(SELECT count(p.ID) FROM  `website_port`.`wp_term_relationships` tr
LEFT JOIN `website_port`.`wp_posts` p
   ON (p.ID = tr.object_id AND p.post_type = 'post' AND p.post_status = 'publish')
WHERE tr.term_taxonomy_id = tt1.term_taxonomy_id);
#WHERE tt1.taxonomy = 'category'