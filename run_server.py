import argparse

import uvicorn
from dotenv import load_dotenv
from app.main import app


def main():
    uvicorn.run(app, reload=True, host="127.0.0.1", port=8000, lifespan="auto")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", required=False, default="dev")
    args = parser.parse_args()

    load_dotenv(dotenv_path=f"_env/{args.env}.env", override=True)

    main()
