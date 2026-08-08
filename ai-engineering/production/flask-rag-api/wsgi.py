import os
from flask_rag_api import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
