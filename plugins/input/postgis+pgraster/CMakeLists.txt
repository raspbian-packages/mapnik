mapnik_find_package(PostgreSQL REQUIRED)

add_plugin_target(input-postgis+pgraster "postgis+pgraster")
target_sources(input-postgis+pgraster ${_plugin_visibility}
    ../postgis/postgis_datasource.cpp
    ../postgis/postgis_featureset.cpp
    ../pgraster/pgraster_datasource.cpp
    ../pgraster/pgraster_featureset.cpp
    ../pgraster/pgraster_wkb_reader.cpp
)
target_link_libraries(input-postgis+pgraster ${_plugin_visibility}
    mapnik::mapnik
    PostgreSQL::PostgreSQL
)
