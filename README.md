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

    SELECT t.id, t.name, ta.value, a.id, a.name
      FROM eve_types t,
           eve_groups g,
		   eve_type_attributes ta,
           eve_attributes a
      where g.category_id=65 
        and g.published=1
        and t.group_id = g.id 
    	and t.published=1
        
		and ta.type_id=t.id
        and a.id=ta.attribute_id
        and a.id in (1547)  
    	
citadel bonuses    
    	
    SELECT t.id,t.name, a.id, a.code, a.name, ta.value
      FROM eve_types t,
           eve_groups g,
           eve_type_attributes ta,
           eve_attributes a
      where g.category_id=65 
        and g.published=1
        and t.group_id = g.id 
        and t.published=1
        and ta.type_id = t.id
        and a.id=ta.attribute_id
        #and a.published=1
        and a.id in (2600,2601,2602)
        
ref. implants

    SELECT t.id, t.name, ta.value
      FROM eve_types t,
           eve_groups g,
           eve_type_attributes ta,
           eve_attributes a
      where ta.type_id=t.id
        and t.published=1
        and a.id=ta.attribute_id
        and a.id=379
        and g.id=t.group_id
        and g.category_id=20
      order by t.name       
      
citadel rigs

    SELECT t.id, t.name, ta.value, ta2.value as rig_size
      FROM eve_types t,
           eve_groups g,
           eve_type_attributes ta,
           eve_attributes a,
           eve_type_attributes ta2,
           eve_attributes a2       
      where t.published=1
        and g.id=t.group_id
        and g.category_id = 66
        and t.market_group_id in (2341,2342,2343)
        and ta.type_id=t.id
        and a.id=ta.attribute_id
        and a.id in (717)
        and ta2.type_id=t.id
        and a2.id=ta2.attribute_id
        and a2.id in (1547)
      order by t.name  
         