
if __name__ == "__main__":
    from src.fastapiApp import TheApp
    import uvicorn
    uvicorn.run(TheApp().app, host="0.0.0.0", port=8000)