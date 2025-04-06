def main() -> None:
    import uvicorn
    uvicorn.run(app="inferadmin.main:app")

if __name__ == "__main__":
    main()