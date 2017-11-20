#### Dev server
    source ./probleme/bin/activate
    ESI_CONFIG=~/esi.conf SECRET_KEY=test ./run.py    
    

#### esi.conf
    ESI_CLIENT_ID='c1l2i3e4n5t6_7i8d'
    ESI_SECRET='1s2e3c4r5e6t7'
    ESI_CALLBACK_URL='http://localhost:5000/probleme_callback'
    

#### MIGRATIONS
    ./manage.py script_sql mysql <script description>
    ./manage.py db_version
    ./manage.py upgrade
    ./manage.py test
    ./manage.py downgrade <version>


#### SDE Import
    ESI_CONFIG=~/esi.conf python3 ./sde.py ~/Downloads/sde-20171024-TRANQUILITY.zip
        
        
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

    SELECT t.id, t.name,             
           ta.value, 
           ta2.value as rig_size,           
           taH.value as rig_H,
           taL.value as rig_L,
           taZ.value as rig_Z
      FROM eve_types t,
           eve_groups g,
           eve_type_attributes ta,
           eve_attributes a,
           eve_type_attributes ta2,
           eve_attributes a2,
           eve_type_attributes taH,
           eve_attributes aH,           
           eve_type_attributes taL,
           eve_attributes aL,           
           eve_type_attributes taZ,
           eve_attributes aZ
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
        and taH.type_id=t.id
        and aH.id=taH.attribute_id
        and aH.id in (2355)        
        and taL.type_id=t.id
        and aL.id=taL.attribute_id
        and aL.id in (2356)        
        and taZ.type_id=t.id
        and aZ.id=taZ.attribute_id
        and aZ.id in (2357)
      order by t.name  
            
processing skills

    SELECT t.id, t.name, ta.value, a.id, a.name
      FROM evecalc_dev.eve_types t,
           eve_type_attributes ta,
           eve_attributes a
      where t.market_group_id=1323
        and ta.type_id=t.id
        and a.id=ta.attribute_id
        and a.id in (379)
      order by t.name      
         
skill to ores
         
     SELECT t.id, 
            t.name, 
            ore.type_id, 
            tor.name,
            g.*
       FROM eve_types t,       
            eve_market_groups g,
            eve_type_attributes ore,
            eve_attributes ao,
            eve_types tor
       where t.id in (12180,12181) #processing skill id
         and ore.value = t.id
         and ao.id=ore.attribute_id
         and ore.attribute_id in (790)
         and tor.id=ore.type_id
         and g.id = tor.market_group_id
       order by t.name, tor.name