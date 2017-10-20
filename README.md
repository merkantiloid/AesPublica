#### MIGRATIONS
    ./manage.py script_sql mysql <script description>
    ./manage.py db_version
    ./manage.py upgrade
    ./manage.py test
    ./manage.py downgrade <version>

#### SDE Import
    python3 ./sde.py ~/Downloads/sde-20170818-TRANQUILITY.zip
        
#### TIPS

citadels

    SELECT t.*
      FROM eve_types t,
           eve_groups g
      where g.category_id=65 
        and g.published=1
        and t.group_id = g.id 
    	and t.published=1;   