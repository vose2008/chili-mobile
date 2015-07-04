import web

urls = (
    '/', 'index'
)

app = web.application( urls, globals() )

class index:
    def GET(slef):
        return "hello world!"

if __name__ == "__main__": app.run()
