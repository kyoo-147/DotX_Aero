/* MQTT over Websockets Example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/
#include <stdio.h>
#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "esp_wifi.h"
#include "esp_system.h"
#include "nvs_flash.h"
#include "esp_event.h"
#include "esp_netif.h"
#include "protocol_examples_common.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "freertos/queue.h"

#include "lwip/sockets.h"
#include "lwip/dns.h"
#include "lwip/netdb.h"

#include "esp_log.h"
#include "mqtt_client.h"
#include "driver/gpio.h"

static const char *TAG = "MQTTWS_EXAMPLE";

#define LED_PIN1 22
#define LED_PIN2 23

#define LED_PIN3 18
#define LED_PIN4 19

static void log_error_if_nonzero(const char *message, int error_code)
{
    if (error_code != 0) {
        ESP_LOGE(TAG, "Last error %s: 0x%x", message, error_code);
    }
}

/*
 * @brief Event handler registered to receive MQTT events
 *
 *  This function is called by the MQTT client event loop.
 *
 * @param handler_args user data registered to the event.
 * @param base Event base for the handler(always MQTT Base in this example).
 * @param event_id The id for the received event.
 * @param event_data The data for the event, esp_mqtt_event_handle_t.
 */
static void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data)
{
    ESP_LOGD(TAG, "Event dispatched from event loop base=%s, event_id=%d", base, event_id);
    esp_mqtt_event_handle_t event = event_data;
    esp_mqtt_client_handle_t client = event->client;
    int msg_id;
    char topic[128]; // Kích thước tối đa hợp lý cho topic
    char data[128];  // Kích thước tối đa hợp lý cho data
    switch ((esp_mqtt_event_id_t)event_id) {
    case MQTT_EVENT_CONNECTED:
        ESP_LOGI(TAG, "MQTT_EVENT_CONNECTED");

        // msg_id = esp_mqtt_client_publish(client, "/topic/qos1", "data_test1", 0, 1, 0);
        // ESP_LOGI(TAG, "sent publish successful, msg_id=%d", msg_id);

        msg_id = esp_mqtt_client_subscribe(client, "/topic/qos0", 0);
        ESP_LOGI(TAG, "sent subscribe successful, msg_id=%d", msg_id);

        msg_id = esp_mqtt_client_subscribe(client, "/topic/qos1", 0);
        ESP_LOGI(TAG, "sent subscribe successful, msg_id=%d", msg_id);

        msg_id = esp_mqtt_client_subscribe(client, "/topic/qos2", 0);
        ESP_LOGI(TAG, "sent subscribe successful, msg_id=%d", msg_id);

        msg_id = esp_mqtt_client_subscribe(client, "/topic/qos3", 0);
        ESP_LOGI(TAG, "sent subscribe successful, msg_id=%d", msg_id);

        // msg_id = esp_mqtt_client_unsubscribe(client, "/topic/qos1");
        // ESP_LOGI(TAG, "sent unsubscribe successful, msg_id=%d", msg_id);
        break;
    case MQTT_EVENT_DISCONNECTED:
        ESP_LOGI(TAG, "MQTT_EVENT_DISCONNECTED");
        break;

    case MQTT_EVENT_SUBSCRIBED:
        ESP_LOGI(TAG, "MQTT_EVENT_SUBSCRIBED, msg_id=%d", event->msg_id);
        msg_id = esp_mqtt_client_publish(client, "/topic/qos0", "light1_already", 0, 0, 0);
        ESP_LOGI(TAG, "sent publish successful, msg_id=%d", msg_id);

        msg_id = esp_mqtt_client_publish(client, "/topic/qos1", "light2_already", 0, 1, 0);
        ESP_LOGI(TAG, "sent publish successful, msg_id=%d", msg_id);

        ESP_LOGI(TAG, "MQTT_EVENT_SUBSCRIBED, msg_id=%d", event->msg_id);
        msg_id = esp_mqtt_client_publish(client, "/topic/qos2", "light3_already", 0, 0, 0);
        ESP_LOGI(TAG, "sent publish successful, msg_id=%d", msg_id);

        msg_id = esp_mqtt_client_publish(client, "/topic/qos3", "light4_already", 0, 1, 0);
        ESP_LOGI(TAG, "sent publish successful, msg_id=%d", msg_id);
        break;
    case MQTT_EVENT_UNSUBSCRIBED:
        ESP_LOGI(TAG, "MQTT_EVENT_UNSUBSCRIBED, msg_id=%d", event->msg_id);
        break;
    case MQTT_EVENT_PUBLISHED:
        ESP_LOGI(TAG, "MQTT_EVENT_PUBLISHED, msg_id=%d", event->msg_id);
        break;
    case MQTT_EVENT_DATA:
        ESP_LOGI(TAG, "MQTT_EVENT_DATA");
        printf("TOPIC=%.*s\r\n", event->topic_len, event->topic);
        printf("DATA=%.*s\r\n", event->data_len, event->data);
        // Copy dữ liệu và đảm bảo kết thúc chuỗi
        strncpy(topic, event->topic, event->topic_len);
        topic[event->topic_len] = '\0';
        strncpy(data, event->data, event->data_len);
        data[event->data_len] = '\0';
        snprintf(topic, sizeof(topic), "%.*s", event->topic_len, event->topic);
        snprintf(data, sizeof(data), "%.*s", event->data_len, event->data);
        ESP_LOGI(TAG, "Received message on topic %s: %s", topic, data);

        if (strcmp(topic, "/topic/qos0") == 0) {
            if (strcmp(data, "ON") == 0) {
                ESP_LOGI(TAG, "Turn ON relay - Light 1");
                //control_led1(1);
                gpio_set_level(LED_PIN1, 1);
                msg_id = esp_mqtt_client_publish(client, "/topic/qos0", "light1_turn_on", 0, 0, 0);
                ESP_LOGI(TAG, "sent publish successful, msg_id=%d", msg_id);
            } else if (strcmp(data, "OFF") == 0) {
                ESP_LOGI(TAG, "Turn OFF relay - Light 1");
                gpio_set_level(LED_PIN1, 0);
                msg_id = esp_mqtt_client_publish(client, "/topic/qos0", "light1_turn_off", 0, 0, 0);
                ESP_LOGI(TAG, "sent publish successful, msg_id=%d", msg_id);
            }
        }

        if (strcmp(topic, "/topic/qos1") == 0) {
            if (strcmp(data, "ON") == 0) {
                ESP_LOGI(TAG, "Turn ON relay - Light 2");
                msg_id = esp_mqtt_client_publish(client, "/topic/qos1", "light2_turn_on", 0, 1, 0);
                ESP_LOGI(TAG, "sent publish successful, msg_id=%d", msg_id);
                //control_led2(1);
                gpio_set_level(LED_PIN2, 1);
            } else if (strcmp(data, "OFF") == 0) {
                ESP_LOGI(TAG, "Turn OFF relay - Light 2");
                gpio_set_level(LED_PIN2, 0);
                msg_id = esp_mqtt_client_publish(client, "/topic/qos1", "light2_turn_off", 0, 1, 0);
                ESP_LOGI(TAG, "sent publish successful, msg_id=%d", msg_id);
            }
        }

        if (strcmp(topic, "/topic/qos2") == 0) {
            if (strcmp(data, "ON") == 0) {
                ESP_LOGI(TAG, "Turn ON relay - Light 3");
                msg_id = esp_mqtt_client_publish(client, "/topic/qos2", "light3_turn_on", 0, 1, 0);
                ESP_LOGI(TAG, "sent publish successful, msg_id=%d", msg_id);
                //control_led2(1);
                gpio_set_level(LED_PIN3, 1);
            } else if (strcmp(data, "OFF") == 0) {
                ESP_LOGI(TAG, "Turn OFF relay - Light 3");
                gpio_set_level(LED_PIN3, 0);
                msg_id = esp_mqtt_client_publish(client, "/topic/qos2", "light3_turn_off", 0, 1, 0);
                ESP_LOGI(TAG, "sent publish successful, msg_id=%d", msg_id);
            }
        }

        if (strcmp(topic, "/topic/qos3") == 0) {
            if (strcmp(data, "ON") == 0) {
                ESP_LOGI(TAG, "Turn ON relay - Light 4");
                msg_id = esp_mqtt_client_publish(client, "/topic/qos3", "light4_turn_on", 0, 1, 0);
                ESP_LOGI(TAG, "sent publish successful, msg_id=%d", msg_id);
                //control_led2(1);
                gpio_set_level(LED_PIN4, 1);
            } else if (strcmp(data, "OFF") == 0) {
                ESP_LOGI(TAG, "Turn OFF relay - Light 4");
                gpio_set_level(LED_PIN4, 0);
                msg_id = esp_mqtt_client_publish(client, "/topic/qos3", "light4_turn_off", 0, 1, 0);
                ESP_LOGI(TAG, "sent publish successful, msg_id=%d", msg_id);
            }
        }

        break;
    case MQTT_EVENT_ERROR:
        ESP_LOGE(TAG, "MQTT_EVENT_ERROR");
        if (event->error_handle->error_type == MQTT_ERROR_TYPE_TCP_TRANSPORT) {
            log_error_if_nonzero("reported from esp-tls", event->error_handle->esp_tls_last_esp_err);
            log_error_if_nonzero("reported from tls stack", event->error_handle->esp_tls_stack_err);
            log_error_if_nonzero("captured as transport's socket errno",  event->error_handle->esp_transport_sock_errno);
            ESP_LOGE(TAG, "Last errno string (%s)", strerror(event->error_handle->esp_transport_sock_errno));
        }
        if (event->error_handle->error_type == MQTT_ERROR_TYPE_CONNECTION_REFUSED) {
            ESP_LOGE(TAG, "Connection refused by broker");
        }
        break;
    default:
        ESP_LOGI(TAG, "Other event id:%d", event->event_id);
        break;
    }
}

// Embedded certificate (từ CMakeLists.txt EMBED_TXTFILES)
extern const uint8_t digicert_global_root_g2_pem_start[] asm("_binary_digicert_global_root_g2_pem_start");
extern const uint8_t digicert_global_root_g2_pem_end[]   asm("_binary_digicert_global_root_g2_pem_end");

static void mqtt_app_start(void)
{
    const esp_mqtt_client_config_t mqtt_cfg = {
        .broker.address.uri = CONFIG_BROKER_URI,
        .broker.verification.certificate = (const char *)digicert_global_root_g2_pem_start,
    };

    ESP_LOGI(TAG, "Connecting to MQTT broker: %s", CONFIG_BROKER_URI);
    ESP_LOGI(TAG, "Using embedded DigiCert Global Root G2 certificate for SSL verification");
    esp_mqtt_client_handle_t client = esp_mqtt_client_init(&mqtt_cfg);
    /* The last argument may be used to pass data to the event handler, in this example mqtt_event_handler */
    esp_mqtt_client_register_event(client, ESP_EVENT_ANY_ID, mqtt_event_handler, NULL);
    esp_mqtt_client_start(client);
}

// Hàm bật đèn 1
void control_led1(int state) {
    gpio_set_level(LED_PIN1, state); // Bật/tắt LED1
    // vTaskDelay(duration_ms / portTICK_PERIOD_MS);
}

// Hàm bật đèn 2
void control_led2(int state) {
    gpio_set_level(LED_PIN2, state); // Bật/tắt LED2
    // vTaskDelay(duration_ms / portTICK_PERIOD_MS);
}
// Hàm bật đèn 2
void control_led3(int state) {
    gpio_set_level(LED_PIN3, state); // Bật/tắt LED2
    // vTaskDelay(duration_ms / portTICK_PERIOD_MS);
}
// Hàm bật đèn 2
void control_led4(int state) {
    gpio_set_level(LED_PIN4, state); // Bật/tắt LED2
    // vTaskDelay(duration_ms / portTICK_PERIOD_MS);
}

void app_main(void)
{
    esp_rom_gpio_pad_select_gpio(LED_PIN1);
    esp_rom_gpio_pad_select_gpio(LED_PIN2);
    esp_rom_gpio_pad_select_gpio(LED_PIN3);
    esp_rom_gpio_pad_select_gpio(LED_PIN4);
    gpio_set_direction(LED_PIN1, GPIO_MODE_OUTPUT);
    gpio_set_direction(LED_PIN2, GPIO_MODE_OUTPUT);
    gpio_set_direction(LED_PIN3, GPIO_MODE_OUTPUT);
    gpio_set_direction(LED_PIN4, GPIO_MODE_OUTPUT);
    
    ESP_LOGI(TAG, "[APP] Startup..");
    ESP_LOGI(TAG, "[APP] Free memory: %d bytes", esp_get_free_heap_size());
    ESP_LOGI(TAG, "[APP] IDF version: %s", esp_get_idf_version());

    esp_log_level_set("*", ESP_LOG_INFO);
    esp_log_level_set("MQTT_CLIENT", ESP_LOG_VERBOSE);
    esp_log_level_set("MQTT_EXAMPLE", ESP_LOG_VERBOSE);
    esp_log_level_set("TRANSPORT_BASE", ESP_LOG_VERBOSE);
    esp_log_level_set("TRANSPORT_WS", ESP_LOG_VERBOSE);
    esp_log_level_set("TRANSPORT", ESP_LOG_VERBOSE);
    esp_log_level_set("OUTBOX", ESP_LOG_VERBOSE);

    ESP_ERROR_CHECK(nvs_flash_init());
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());

    /* This helper function configures Wi-Fi or Ethernet, as selected in menuconfig.
     * Read "Establishing Wi-Fi or Ethernet Connection" section in
     * examples/protocols/README.md for more information about this function.
     */
    ESP_ERROR_CHECK(example_connect());

    mqtt_app_start();
}
