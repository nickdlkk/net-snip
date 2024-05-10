# 使用PyWebIO打造的网络剪辑板
数据库使用SQLite

包含密码访问，自动保存，支持MarkDown格式。

## 安装

```bash
pip install -r requirements.txt
```

## 运行

```bash
python main.py
```

## 使用

打开浏览器访问`http://localhost:8080`

## TODO
1. [x] 支持MarkDown格式
2. [x] 支持密码访问
3. [x] 支持自动保存
4. [ ] 支持查看历史记录
5. [ ] 支持上传文件
6. [ ] 系统初始化/重置,清空数据库数据
7. [ ] 安全加固
8. [ ] 增加分享超时时间
9. [ ] 增加查看次数
10. [ ] Vercel部署

# 部署
## Vercel
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Faurora-develop%2Faurora&env=STREAM_MODE&project-name=aurora&repository-name=aurora)