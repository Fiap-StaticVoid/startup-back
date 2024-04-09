from uvicorn import run

if __name__ == "__main__":
    run(
        "servidor.config:app",
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=True,
    )
