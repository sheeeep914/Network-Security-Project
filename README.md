# 開發流程

1. 各自clone下來，開新的branch寫。

    #### 主要分支 (已經存在的)
    * **master** -> 穩定版 (只有確定要把這個功能加上去才把 **develop** merge到 **origin/master** 上)
    * **develop** -> 測試版 (用來另外再分支出 **feature** )

    #### 次要分支 (自己開發時新建的)
    * **myfeature** -> 新功能 （由 **develop** 直接分支，開發新功能。最後merge回 **develop branch**）

2. 兩個人開發時，記得先`git checkout -b myfeature`，切換到自己的分支(**feature**)，每次寫code...
    1. **PULL** -> `git pull`，更新本機code 
    2. **Coding** -> 修改完一個新功能，就記得`git add` `git commit`
    3. **Push** -> 切換到**develop branch** (`git checkout develop`) 利用 –no-ff 合併分支 (`git merge --no-ff myfeature`) 再來刪除 **myfeature** 分支(`git branch -d myfeature`) 最後資料上傳 (`git push origin develop`)


---
# 進度
- **4/10**
    - 用feature inverse回去看pca的重要feature有哪些?\
    *(實驗後發現 pca和我們理解的不一樣 不能選重要feature)*
- **4/17**  
    - 把time feature拿掉看看
    - 



---
### *補充：Clone fork 差別*

- **Clone** : 把專案在遠端儲存庫上的所有內容複製到**本地**，建立起**本機儲存庫**及工作目錄

- **Fork** : 把別人專案的遠端儲存庫內容複製一份到自己的**遠端儲存庫**

- **使用方法** : 如果在開發者在GitHub上看到有興趣的專案，可以執行Fork指令，把別人專案的遠端儲存庫複製到自己的遠端儲存庫，再執行Clone指令，把自己遠端儲存庫的整個專案的所有內容（包括各版本）複製到本機端儲存庫。

---
### *參考資料*

- [git branch](https://blog.wu-boy.com/2011/03/git-%E7%89%88%E6%9C%AC%E6%8E%A7%E5%88%B6-branch-model-%E5%88%86%E6%94%AF%E6%A8%A1%E7%B5%84%E5%9F%BA%E6%9C%AC%E4%BB%8B%E7%B4%B9/)

