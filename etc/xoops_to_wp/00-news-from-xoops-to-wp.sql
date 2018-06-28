DROP FUNCTION IF EXISTS `slugify`;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost`
FUNCTION `slugify`(dirty_string varchar(200))
RETURNS varchar(200) CHARSET latin1
DETERMINISTIC
BEGIN
    DECLARE x, y , z Int;
    Declare temp_string, allowed_chars, new_string VarChar(200);
    Declare is_allowed Bool;
    Declare c, check_char VarChar(1);

    set allowed_chars = "abcdefghijklmnopqrstuvwxyz0123456789-";
    set temp_string = LOWER(dirty_string);

    Select temp_string Regexp('&') Into x;
    If x = 1 Then
        Set temp_string = replace(temp_string, '&', ' and ');
    End If;

    Select temp_string Regexp('[^a-z0-9]+') into x;
    If x = 1 then
        set z = 1;
        While z <= Char_length(temp_string) Do
            Set c = Substring(temp_string, z, 1);
            Set is_allowed = False;
            Set y = 1;
            Inner_Check: While y <= Char_length(allowed_chars) Do
                If (strCmp(ascii(Substring(allowed_chars,y,1)), Ascii(c)) = 0) Then
                    Set is_allowed = True;
                    Leave Inner_Check;
                End If;
                Set y = y + 1;
            End While;
            If is_allowed = False Then
                Set temp_string = Replace(temp_string, c, '-');
            End If;

            set z = z + 1;
        End While;
    End If;

    Select temp_string Regexp("^-|-$|'") into x;
    If x = 1 Then
        Set temp_string = Replace(temp_string, "'", '');
        Set z = Char_length(temp_string);
        Set y = Char_length(temp_string);
        Dash_check: While z > 1 Do
            If Strcmp(SubString(temp_string, -1, 1), '-') = 0 Then
                Set temp_string = Substring(temp_string,1, y-1);
                Set y = y - 1;
            Else
                Leave Dash_check;
            End If;
            Set z = z - 1;
        End While;
    End If;

    Repeat
        Select temp_string Regexp("--") into x;
        If x = 1 Then
            Set temp_string = Replace(temp_string, "--", "-");
        End If;
    Until x <> 1 End Repeat;

    If LOCATE('-', temp_string) = 1 Then
        Set temp_string = SUBSTRING(temp_string, 2);
    End If;

    Return temp_string;
END;;
DELIMITER ;



#Importar os posts do xoops:

INSERT INTO `website_port`.`wp_posts` SELECT (storyid+20000) AS ID, 
(uid+4) AS post_author, 
FROM_UNIXTIME( created ) AS post_date, 
FROM_UNIXTIME( created ) AS post_date_gmt, bodytext AS post_content, title AS post_title, CONCAT(SUBSTRING(hometext, 1, 400), '...') AS post_excerpt, 'publish' AS post_status, 
'open' AS comment_status, 'open' AS ping_status, '' AS post_password, title AS post_name, '' AS to_ping, '' AS pinged, FROM_UNIXTIME( created ) AS post_modified, 
FROM_UNIXTIME( created ) AS post_modified_gmt, '' AS post_content_filtered, '' AS post_parent, '' AS guid, '' AS menu_order, 'post' AS post_type, 
'' AS post_mime_type,  0 AS comment_count FROM `website_xoops`.`xoopswebsite_stories`;

#update wp_posts set post_name = slugify( lower(post_title) );

insert into `website_port`.`wp_terms` select (topic_id+200) as term_id, topic_title, slugify( lower(topic_title) ) as slug, 0 as term_group from `website_xoops`.`xoopswebsite_topics`;
insert into `website_port`.`wp_term_taxonomy`select NULL as term_taxonomy_id, term_id, 'category' as taxonomy, '' as description, 0 as parent, 0 as count from `website_port`.`wp_terms` where term_id > 200;
INSERT INTO `website_port`.`wp_term_relationships` SELECT (storyid+20000) AS object_id, (topicid+200) AS term_taxonomy_id, 0 as term_order FROM `website_xoops`.`xoopswebsite_stories`;



#Corrige as atribuições a usuários:

UPDATE `website_port`.`wp_posts` po 
LEFT JOIN `website_xoops`.`xoopswebsite_stories` st ON (st.storyid+2) = po.id 
SET post_author = uid+4;

update `website_port`.`wp_posts` set post_author = 1 where post_author = 0;
update `website_port`.`wp_posts` set post_author = 1 where post_author = 10795;

