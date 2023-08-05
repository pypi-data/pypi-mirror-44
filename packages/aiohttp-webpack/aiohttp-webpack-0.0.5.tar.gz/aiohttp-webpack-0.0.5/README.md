Utility for load static in AioHttp web framework from Webpack with help of webpack-bundle-tracker JS plugin.

Also this can be used with VueJS.

Usage:

settings.py:
```python
    STATIC_URL = '/static/'
    STATIC_PATH = './static/'
    WEBPACK_MANIFEST_PATH = './frontend/webpack_manifest.json'
```

main.py:
```python
    from aiohttp import web
    import aiohttp_jinja2
    import jinja2
    from aiohttp_webpack import WebpackManifest
    from settings import *


    @aiohttp_jinja2.template('index.html')
    async def index(request):
        context = {
            'webpack': webpack_manifest.get_links(),
        }

        return context


    if __name__ == '__main__':
        loop = asyncio.get_event_loop()

        app = web.Application()
        aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./templates'))

        webpack_manifest = WebpackManifest(WEBPACK_MANIFEST_PATH, STATIC_URL, STATIC_PATH)

        app.add_routes([
            web.get('/', index),
            web.get('/static/{path:.*}', webpack_manifest.handle_static),
        ])

        web.run_app(app)
```

index.html:
```html
    <html>
      <head>
        <meta charset="utf-8">
        <link rel="stylesheet" href="/static/index.css"> {# here you can use non webpack static too #}
        {{ webpack.css | safe }}
      </head>
      <body>
        <div id="app"></div> {# if you use VueJS #}
        {{ webpack.js | safe }}
      </body>
    </html>
```