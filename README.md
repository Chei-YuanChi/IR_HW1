# IR_HW1

## 環境設置
* ### Django 2.2.5
* ### python 3.6
* ### Need to install:
    * #### ntlk:
        ```pip install -U ntlk```
    * #### punkt:
    1.     Create file folder(nltk_data/tokenizers) in your environment:
               (like this: user/anaconda/envs/.../nltk_data/tokenizers) 
    2.     Unzip the file to "tokenizers" folder
## 使用方式

* ### github 檔案下載與執行
```
(terminal)
git clone https://github.com/Chei-YuanChi/IR_HW1.git
cd IR_HW1
python manage.py runserver
(google)
localhost:8000
```
* ### 操作
### Home : Go to the main page.
### Upload/GET STARTED : Go to upload page.
### Search : Go to search page.
![](https://i.imgur.com/UG4zoYo.jpg)
### UPLOAD : Upload the file you choose.
![](https://i.imgur.com/CmdDEYd.jpg)
### CHOOSE FILE : Choose the file you already uploaded.
### SEARCH : Input the words you want to search and return it to server.
### CLEAR : Clear display file.
### statistics : Number of characters, words, phrases, result of searching in this file.
### DELETE : Delete the displayed file
![](https://i.imgur.com/YEtmMTG.jpg)
