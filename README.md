# Django blog project

![django blog screenshot](./screenshot.png)

## 相关资源

[在线预览](https://www.zmrenwu.com/)

[用户使用手册](https://django-blog-project.readthedocs.io/zh/latest/)

## 特性一览

- 简约优雅的 UI，移动端优先的响应式设计。
- Webpack 前端资源打包。
- 基于 Vue 的多级评论系统。
- 文章、评论内容支持 Markdown 与代码高亮。
- 支持 GitHub、新浪微博社交账户登录。
- 中文全文搜索，关键词高亮。
- 完善的通知系统，评论、回复博客内通知，同时邮件提醒。
- 独有的教程系统，方便地管理系列文章。
- Docker 部署，无痛上线。

## 部署上线

1. 安装 Docker 和 Docker Compose。

2. 克隆代码到线上服务器

   ```shell
   $ git clone https://github.com/zmrenwu/django-blog-project
   ```

3. 创建项目所需的环境变量文件，在项目**根目录**创建名为 .envs 的文件夹，并在 .envs 下创建 .production 文件，写入如下内容

   ```
   SECRET_KEY=your-own-secret-key
   DJANGO_SETTINGS_MODULE=config.settings.production
   DJANGO_SENDGRID_API_KEY=your-own-sendgrid-api-key
   # 设置允许访问的 HOSTS，逗号分隔
   DJANGO_ALLOWED_HOSTS=your-domain.com,www.yourdomain.com
   # 设置管理员邮箱，用于接收邮件通知提醒
   DJANGO_ADMINS=zmrenwu <zmrenwu@163.com>
   SERVER_EMAIL=noreply@djangoblogproject.com
   ```

   `SECRET_KEY`：项目密钥，推荐使用 [Django Secret Key Generator](https://www.miniwebtool.com/django-secret-key-generator/) 自动生成。

   `DJANGO_SENDGRID_API_KEY`：[SendGrid](https://sendgrid.com/) 邮件发送密钥，配置后才能发送邮件提醒。

4. 复制 compose/production/nginx/conf.d/blogproject.conf-tmpl 到同级目录（即 conf.d 下），重命名为 blogproject.conf，将 blogproject.conf 中的 xxx.com 替换为你自己的域名。

5. 进入项目根目录，启动 Docker 容器

   ```shell
   $ docker-compose -f production.yml up --build -d
   ```

6. 开启 HTTPS

   ```shell
   $ docker exec -it blogproject_nginx certbot --nginx -n --agree-tos --redirect --email your-email@example.com -d your-domain.com,www.your-domain.com
   ```

   解释下关键参数的含义：

   `--redirect`：自动将所有 HTTP 请求重定向为 HTTPS 请求。

   `--email`：你的 email，用于接收 letsencrypt 的消息提醒。

   `-d`：后跟需要配置 HTTPS 证书的域名列表，以逗号分隔。

7. 创建后台管理员账户

   ```shell
   $ docker exec -it blogproject python manage.py createsuperuser
   ```

8. Over~~

## 本地运行

1. 安装 Docker 和 Docker Compose。

2. 克隆代码到本地

   ```shell
   $ git clone https://github.com/zmrenwu/django-blog-project
   ```

3. 进入项目根目录，启动 Docker 容器

   ```shell
   $ docker-compose -f local.yml up --build
   ```

4. 进入 frontend 目录，启动静态文件服务器

   ```shell
   $ npm install
   $ npm run dev
   ```

5. Over~~

## 新功能开发路线图

详见：[django-blog-project 版本规划与新功能开发路线图](https://www.zmrenwu.com/post/89/)

## 版本迭代历史

详见：[django-blog-project 版本迭代历史记录](https://www.zmrenwu.com/post/90/)