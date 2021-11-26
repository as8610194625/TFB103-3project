# TFB103-3project

>爬蟲程式
```
At : crewdatas_functions
```
>資料
```
At : kingstone_datas/json & book_comment
```
>Line Bot Server 及 功能 程式
```
At: Project-linebot
```
>Dockerfile & docker-compose.yml
```
docker-compose up
```
## 本地測試操作步驟

1.打開SecretFile.txt
把需要的資料貼到對應的位置
對照:
|channelAccessToken|channelSecret|
|:---|:---|:---|:---
|LINE Message API Token|LINE channel Secret

2.cd到localtest_docker下執行:
```
docker-compose up
``` 
3.使用另一個終端機cd到localtest_docker下，執行:
```
curl $(docker port chatbot_ngrok 4040)/api/tunnels
```
把「https:....」貼到LINE BOT DEVELOPER 的Webhook ，再加上/callback

4.可以常使用LINE BOT了

## Elasticsearch-kibana_yml

錯誤解決：max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]

> 然後可以執行以下命令，設置 vm.max_map_count ，但是重啟後又恢復為預設值。

sudo sysctl -w vm.max_map_count=262144
```
sudo sysctl -p
```
or 永久改變
```
sudo vim /etc/sysctl.conf
vm.max_map_count=262144
sudo sysctl -p
```
