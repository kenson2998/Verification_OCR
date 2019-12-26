圖片處理
===

## 需要指定你的Tesseract-OCR位置 我是和img_pros.py放在當前目錄下

如果是mac 
直接安裝 brew install tesseract

安装pytesseract
pip install pytesseract

---
title: 'image process'
disqus: hackmd
---


###### tags: `pytesseract` `Opencv`

d01.png~d07.png的驗證碼範例圖

d01~d04的圖形使用預設threshould=80 
![](https://i.imgur.com/0pfQQsr.png)

![](https://i.imgur.com/z4aYaQX.png)

d04~d07的圖形需要更換 threshould=180
此類型圖片有橫線、噪音干擾 可以順利除去
但歪斜的部分OCR辨識不出來
![](https://i.imgur.com/N3Zem9s.png)

![](https://i.imgur.com/LDnA0tV.png)



