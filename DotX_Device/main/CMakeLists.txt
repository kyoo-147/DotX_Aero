idf_component_register(
    SRCS "app_main.c"
    INCLUDE_DIRS "."
    REQUIRES esp-tls mqtt esp_wifi nvs_flash esp_netif protocol_examples_common freertos lwip driver esp_event
    EMBED_TXTFILES "certs/digicert_global_root_g2.pem"
)

target_compile_options(${COMPONENT_LIB} PRIVATE "-Wno-format")
