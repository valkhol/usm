

import uvicorn

from app.app import create_app


def main():

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8110)


if __name__ == '__main__':
    main()
