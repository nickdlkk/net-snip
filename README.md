# 使用PyWebIO打造的网络剪辑板
使用SQLite保存的英文单词作为密钥。数据库使用PostgreSQL，方便部署到云服务

包含密码访问，自动保存，支持MarkDown格式。

## 安装

```bash
pip install -r requirements.txt
```
## Test

```bash
python network_snip.py
```

## 运行

```bash
python index.py
```

## 使用

打开浏览器访问`http://localhost:8080`

## Docker

### Build
```shell
docker build -t nickdlk/net-snip:latest .
```
### Run
```shell
docker run -d -p 8080:8080 nickdlk/net-snip:latest
```

### Docker Compose
```shell
docker-compose up -d
```

### 设置容器自动更新

```shell
docker run -d \
    --name watchtower \
    -v /var/run/docker.sock:/var/run/docker.sock \
    containrrr/watchtower \
    net_snip
```

## TODO
1. [x] 支持MarkDown格式
2. [x] 支持密码访问
3. [x] 支持自动保存
4. [ ] 支持查看历史记录
5. [x] 支持上传文件,下载文件,文件限制大小
6. [ ] 系统初始化/重置,清空数据库数据
7. [ ] 安全加固,密码加密保存,文本/文件加密保存,同ip限制创建和访问
8. [ ] 增加分享超时时间
9. [ ] 增加查看次数
10. [x] Vercel部署
11. [x] Dockerfile,Docker Compose
12. [ ] 定时清理
13. [ ] 分享连接,二维码分享,支持分享只读链接,对key进行加密分享
14. [ ] 优化页面布局
15. [ ] 支持删除文件,下载次数统计
16. [x] 支持输入key和生成key
17. [ ] 生成短链
18. [x] 多端编写同步更新
19. [x] GitHub Action 自动打包Docker

# 部署
## Vercel
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fnickdlkk%2Fnet_snip&env=STREAM_MODE&project-name=net_snip&repository-name=net_snip)