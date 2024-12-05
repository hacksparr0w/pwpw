import uvicorn


def main():
    uvicorn.run(
        "pwpwd.application:application",
        host="0.0.0.0",
        port=9393
    )


if __name__ == "__main__":
    main()
