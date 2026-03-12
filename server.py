from app import create_app

app = create_app()


if __name__ == "__main__":
    # Keep debug + port behavior consistent with the original script
    app.run(debug=True, port=8000)
