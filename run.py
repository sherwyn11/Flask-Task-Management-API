from app import create_app

app = create_app('config.deployment')

if __name__ == '__main__':
    app.run()